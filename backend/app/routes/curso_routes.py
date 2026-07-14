"""Módulo 2: Cursos y Docentes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..extensions import db
from ..models.curso import Curso
from ..models.usuario import Usuario, ROL_DOCENTE, ROL_ADMIN, ROL_DIRECCION
from ..utils.decorators import roles_required
from ..utils.audit import registrar

curso_bp = Blueprint("curso", __name__)


@curso_bp.get("")
@jwt_required()
def listar():
    """Lista cursos. Docente solo ve los suyos si ?mios=1."""
    claims = get_jwt()
    uid = int(get_jwt_identity())
    q = Curso.query
    if claims["rol"] == ROL_DOCENTE and request.args.get("mios") == "1":
        q = q.filter_by(docente_id=uid)
    return jsonify([c.to_dict() for c in q.order_by(Curso.ciclo, Curso.nombre)])


@curso_bp.get("/docentes")
@roles_required(ROL_ADMIN, ROL_DIRECCION)
def docentes():
    docs = Usuario.query.filter_by(rol=ROL_DOCENTE, activo=True).all()
    return jsonify([d.to_dict() for d in docs])


@curso_bp.post("/<int:cid>/silabo")
@roles_required(ROL_DOCENTE)
def cargar_silabo(cid):
    """Docente carga el sílabo del curso (URL/nombre de archivo)."""
    data = request.get_json() or {}
    curso = Curso.query.get_or_404(cid)
    if curso.docente_id != int(get_jwt_identity()):
        return jsonify(error="El curso no está asignado a usted"), 403
    curso.silabo_url = data.get("silabo_url", "silabo.pdf")
    db.session.commit()
    registrar(int(get_jwt_identity()), "Carga de sílabo", "Cursos", curso.codigo)
    return jsonify(curso.to_dict())


@curso_bp.patch("/<int:cid>/asignar")
@roles_required(ROL_ADMIN)
def asignar(cid):
    """Admin asigna docente y horario."""
    data = request.get_json() or {}
    curso = Curso.query.get_or_404(cid)
    curso.docente_id = data.get("docente_id", curso.docente_id)
    curso.horario = data.get("horario", curso.horario)
    db.session.commit()
    registrar(int(get_jwt_identity()), "Asignación de docente/horario", "Cursos",
              curso.codigo)
    return jsonify(curso.to_dict())


@curso_bp.get("/carga-docente")
@roles_required(ROL_DIRECCION, ROL_ADMIN)
def carga_docente():
    """Dirección evalúa carga docente."""
    filas = (
        db.session.query(
            Usuario.id, Usuario.nombres, Usuario.apellidos,
            func.count(Curso.id).label("cursos"),
            func.coalesce(func.sum(Curso.creditos), 0).label("creditos"),
        )
        .join(Curso, Curso.docente_id == Usuario.id)
        .group_by(Usuario.id)
        .all()
    )
    return jsonify([
        {"docente": f"{f.apellidos}, {f.nombres}", "cursos": f.cursos,
         "creditos": int(f.creditos)} for f in filas
    ])
