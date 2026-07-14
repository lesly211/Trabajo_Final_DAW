"""Módulo 3: Notas."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..extensions import db
from ..models.nota import Nota
from ..models.curso import Curso
from ..models.matricula import Matricula, MatriculaDetalle, VALIDADA
from ..models.usuario import Usuario, ROL_DOCENTE, ROL_ESTUDIANTE, ROL_ADMIN, ROL_DIRECCION
from ..utils.decorators import roles_required
from ..utils.audit import registrar

nota_bp = Blueprint("nota", __name__)


@nota_bp.get("")
@jwt_required()
def listar():
    """Estudiante: sus notas. Docente: por curso (?curso_id). Admin: todas."""
    claims = get_jwt()
    uid = int(get_jwt_identity())
    q = Nota.query
    if claims["rol"] == ROL_ESTUDIANTE:
        q = q.filter_by(estudiante_id=uid)
    elif claims["rol"] == ROL_DOCENTE:
        curso_id = request.args.get("curso_id", type=int)
        if curso_id:
            q = q.filter_by(curso_id=curso_id)
        else:
            ids = [c.id for c in Curso.query.filter_by(docente_id=uid)]
            q = q.filter(Nota.curso_id.in_(ids or [0]))
    periodo = request.args.get("periodo")
    if periodo:
        q = q.filter_by(periodo=periodo)
    return jsonify([n.to_dict() for n in q.all()])


@nota_bp.post("")
@roles_required(ROL_DOCENTE)
def registrar_nota():
    """Docente registra/actualiza notas parciales y finales."""
    data = request.get_json() or {}
    uid = int(get_jwt_identity())
    curso = Curso.query.get_or_404(data["curso_id"])
    if curso.docente_id != uid:
        return jsonify(error="El curso no está asignado a usted"), 403

    estudiante = Usuario.query.get(data.get("estudiante_id"))
    if not estudiante or estudiante.rol != ROL_ESTUDIANTE:
        return jsonify(error="El estudiante indicado no existe o no tiene rol de estudiante"), 400

    periodo = data.get("periodo", "2026-I")

    # El estudiante debe tener una matrícula VALIDADA que incluya este curso
    # en el periodo indicado; de lo contrario no se le puede registrar nota.
    matriculado = (
        db.session.query(MatriculaDetalle.id)
        .join(Matricula, Matricula.id == MatriculaDetalle.matricula_id)
        .filter(
            Matricula.estudiante_id == estudiante.id,
            Matricula.periodo == periodo,
            Matricula.estado == VALIDADA,
            MatriculaDetalle.curso_id == data["curso_id"],
        )
        .first()
    )
    if not matriculado:
        return jsonify(
            error="El estudiante no tiene una matrícula validada en este curso "
                  "para el periodo indicado"
        ), 409

    nota = Nota.query.filter_by(
        estudiante_id=data["estudiante_id"], curso_id=data["curso_id"],
        periodo=periodo,
    ).first()
    if not nota:
        nota = Nota(estudiante_id=data["estudiante_id"], curso_id=data["curso_id"],
                    periodo=periodo)
        db.session.add(nota)

    for campo in ("parcial1", "parcial2", "final"):
        if campo in data and data[campo] is not None:
            setattr(nota, campo, float(data[campo]))
    nota.calcular_promedio()
    db.session.commit()
    registrar(uid, "Registro de notas", "Notas", curso.codigo)
    return jsonify(nota.to_dict()), 201


@nota_bp.patch("/<int:nid>/validar")
@roles_required(ROL_ADMIN)
def validar_acta(nid):
    """Admin valida acta y consolida."""
    nota = Nota.query.get_or_404(nid)
    nota.validada = True
    db.session.commit()
    registrar(int(get_jwt_identity()), "Validación de acta", "Notas", f"Nota #{nid}")
    return jsonify(nota.to_dict())


@nota_bp.get("/estudiantes-curso/<int:curso_id>")
@roles_required(ROL_DOCENTE)
def estudiantes_curso(curso_id):
    """Lista los estudiantes matriculados en un curso del docente autenticado.

    Permite construir un selector de estudiantes en el registro de notas
    en vez de tener que digitar el ID manualmente.
    """
    uid = int(get_jwt_identity())
    curso = Curso.query.get_or_404(curso_id)
    if curso.docente_id != uid:
        return jsonify(error="El curso no está asignado a usted"), 403

    filas = (
        db.session.query(Usuario)
        .join(Matricula, Matricula.estudiante_id == Usuario.id)
        .join(MatriculaDetalle, MatriculaDetalle.matricula_id == Matricula.id)
        .filter(MatriculaDetalle.curso_id == curso_id, Matricula.estado == VALIDADA)
        .order_by(Usuario.apellidos)
        .all()
    )
    return jsonify([u.to_dict() for u in filas])


@nota_bp.get("/consolidado")
@roles_required(ROL_ADMIN, ROL_DIRECCION)
def consolidado():
    """Vista consolidada de actas por curso/periodo para el administrador.

    Agrupa las notas registradas por curso y periodo, indicando cuántas
    están pendientes de validar y cuántas ya fueron consolidadas.
    """
    filas = (
        db.session.query(
            Nota.curso_id, Nota.periodo, Curso.codigo, Curso.nombre,
            func.count(Nota.id).label("total"),
            func.sum(func.cast(Nota.validada, db.Integer)).label("validadas"),
            func.coalesce(func.avg(Nota.promedio), 0).label("promedio"),
        )
        .join(Curso, Curso.id == Nota.curso_id)
        .group_by(Nota.curso_id, Nota.periodo)
        .order_by(Nota.periodo.desc(), Curso.codigo)
        .all()
    )
    return jsonify([
        {
            "curso_id": f.curso_id,
            "codigo": f.codigo,
            "curso": f.nombre,
            "periodo": f.periodo,
            "total": f.total,
            "validadas": int(f.validadas or 0),
            "pendientes": f.total - int(f.validadas or 0),
            "promedio": round(float(f.promedio), 2),
            "consolidada": f.total == int(f.validadas or 0),
        } for f in filas
    ])


@nota_bp.patch("/consolidar")
@roles_required(ROL_ADMIN)
def consolidar():
    """Admin consolida (valida) de una sola vez todas las notas de un
    curso + periodo, cerrando el acta completa."""
    data = request.get_json() or {}
    curso_id = data.get("curso_id")
    periodo = data.get("periodo")
    if not curso_id or not periodo:
        return jsonify(error="Debe indicar curso_id y periodo"), 400

    notas = Nota.query.filter_by(curso_id=curso_id, periodo=periodo).all()
    if not notas:
        return jsonify(error="No hay notas registradas para ese curso y periodo"), 404

    for n in notas:
        n.validada = True
    db.session.commit()
    curso = Curso.query.get(curso_id)
    registrar(int(get_jwt_identity()), "Consolidación de acta", "Notas",
              f"{curso.codigo if curso else curso_id} · {periodo} ({len(notas)} notas)")
    return jsonify(consolidadas=len(notas), curso_id=curso_id, periodo=periodo)


@nota_bp.get("/indicadores")
@roles_required(ROL_DIRECCION, ROL_ADMIN)
def indicadores():
    """Dirección supervisa indicadores académicos."""
    total = Nota.query.count()
    aprobados = Nota.query.filter(Nota.promedio >= 10.5).count()
    promedio_general = db.session.query(
        func.coalesce(func.avg(Nota.promedio), 0)
    ).scalar()
    return jsonify(
        total=total,
        aprobados=aprobados,
        desaprobados=total - aprobados,
        tasa_aprobacion=round((aprobados / total * 100), 1) if total else 0,
        promedio_general=round(float(promedio_general), 2),
    )
