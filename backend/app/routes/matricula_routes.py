"""Módulo 1: Matrícula."""
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..extensions import db
from ..models.matricula import Matricula, MatriculaDetalle, PENDIENTE, VALIDADA, RECHAZADA
from ..models.curso import Curso
from ..models.usuario import ROL_ESTUDIANTE, ROL_ADMIN, ROL_DIRECCION
from ..utils.decorators import roles_required
from ..utils.audit import registrar
from ..services.matricula_service import generar_ficha_pdf

matricula_bp = Blueprint("matricula", __name__)

MAX_CREDITOS_POR_PERIODO = 24


@matricula_bp.get("")
@jwt_required()
def listar():
    """Estudiante ve sus matrículas; admin/dirección ven todas."""
    claims = get_jwt()
    uid = int(get_jwt_identity())
    if claims["rol"] == ROL_ESTUDIANTE:
        q = Matricula.query.filter_by(estudiante_id=uid)
    else:
        q = Matricula.query
    return jsonify([m.to_dict() for m in q.order_by(Matricula.creado_en.desc())])


@matricula_bp.post("")
@roles_required(ROL_ESTUDIANTE)
def solicitar():
    """Estudiante solicita matrícula con una lista de cursos."""
    data = request.get_json() or {}
    uid = int(get_jwt_identity())
    periodo = data.get("periodo", "2026-I")
    cursos_ids = list(dict.fromkeys(data.get("cursos", [])))  # sin duplicados, conserva orden

    if not cursos_ids:
        return jsonify(error="Debe seleccionar al menos un curso"), 400

    # Requisito 1: no permitir una segunda solicitud (pendiente o ya validada)
    # del mismo estudiante para el mismo periodo.
    ya_existe = Matricula.query.filter(
        Matricula.estudiante_id == uid,
        Matricula.periodo == periodo,
        Matricula.estado.in_((PENDIENTE, VALIDADA)),
    ).first()
    if ya_existe:
        return jsonify(
            error=f"Ya existe una solicitud de matrícula para el periodo {periodo}"
        ), 409

    # Requisito 2: todos los cursos seleccionados deben existir.
    cursos = Curso.query.filter(Curso.id.in_(cursos_ids)).all()
    if len(cursos) != len(cursos_ids):
        return jsonify(error="Uno o más cursos seleccionados no existen"), 400

    # Requisito 3: tope máximo de créditos por periodo.
    total_creditos = sum(c.creditos for c in cursos)
    if total_creditos > MAX_CREDITOS_POR_PERIODO:
        return jsonify(
            error=f"El total de créditos ({total_creditos}) supera el máximo "
                  f"permitido por periodo ({MAX_CREDITOS_POR_PERIODO})"
        ), 400

    mat = Matricula(estudiante_id=uid, periodo=periodo)
    db.session.add(mat)
    db.session.flush()
    for cid in cursos_ids:
        db.session.add(MatriculaDetalle(matricula_id=mat.id, curso_id=cid))
    db.session.commit()
    registrar(uid, "Solicitud de matrícula", "Matrícula", f"Periodo {periodo}")
    return jsonify(mat.to_dict()), 201


@matricula_bp.patch("/<int:mid>/validar")
@roles_required(ROL_ADMIN)
def validar(mid):
    """Admin valida requisitos y registra pago."""
    data = request.get_json() or {}
    mat = Matricula.query.get_or_404(mid)
    aprobar = data.get("aprobar", True)
    mat.estado = VALIDADA if aprobar else RECHAZADA
    mat.pago_registrado = bool(data.get("pago", aprobar))
    mat.monto = float(data.get("monto", 350.0))
    mat.observacion = data.get("observacion")
    db.session.commit()
    registrar(int(get_jwt_identity()), "Validación de matrícula", "Matrícula",
              f"Matrícula #{mid} -> {mat.estado}")
    return jsonify(mat.to_dict())


@matricula_bp.get("/<int:mid>/ficha")
@jwt_required()
def descargar_ficha(mid):
    """Descarga la ficha oficial de matrícula en PDF.

    El estudiante solo puede descargar su propia ficha; admin y dirección
    pueden descargar cualquiera. Solo se puede descargar una matrícula
    ya validada.
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    mat = Matricula.query.get_or_404(mid)

    if claims["rol"] == ROL_ESTUDIANTE and mat.estudiante_id != uid:
        return jsonify(error="No autorizado"), 403
    if mat.estado != VALIDADA:
        return jsonify(error="La matrícula aún no ha sido validada"), 409

    pdf_bytes = generar_ficha_pdf(mat)
    registrar(uid, "Descarga de ficha de matrícula", "Matrícula", f"Matrícula #{mid}")
    nombre = f"ficha_matricula_{mat.periodo}_{mid}.pdf"
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre}"},
    )


@matricula_bp.get("/estadisticas")
@roles_required(ROL_DIRECCION, ROL_ADMIN)
def estadisticas():
    """Dirección supervisa estadísticas de matrícula."""
    total = Matricula.query.count()
    por_estado = dict(
        db.session.query(Matricula.estado, func.count(Matricula.id))
        .group_by(Matricula.estado).all()
    )
    ingresos = db.session.query(func.coalesce(func.sum(Matricula.monto), 0)).filter(
        Matricula.pago_registrado.is_(True)
    ).scalar()
    return jsonify(total=total, por_estado=por_estado, ingresos=float(ingresos))
