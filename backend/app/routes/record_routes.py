"""Módulo 4: Record Académico."""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..extensions import db
from ..models.nota import Nota
from ..models.usuario import Usuario, ROL_ESTUDIANTE, ROL_ADMIN, ROL_DIRECCION
from ..utils.decorators import roles_required
from ..services.record_service import record_estudiante

record_bp = Blueprint("record", __name__)


@record_bp.get("/<int:estudiante_id>")
@jwt_required()
def record(estudiante_id):
    """Estudiante ve su propio record; admin/dirección ven cualquiera."""
    claims = get_jwt()
    uid = int(get_jwt_identity())
    if claims["rol"] == ROL_ESTUDIANTE and uid != estudiante_id:
        return jsonify(error="No autorizado"), 403
    estudiante = Usuario.query.get_or_404(estudiante_id)
    data = record_estudiante(estudiante_id)
    data["estudiante"] = estudiante.to_dict()
    return jsonify(data)


@record_bp.get("/reportes/consolidado")
@roles_required(ROL_ADMIN, ROL_DIRECCION)
def consolidado():
    """Admin genera reportes consolidados; Dirección analiza por cohorte."""
    filas = (
        db.session.query(
            Usuario.id, Usuario.nombres, Usuario.apellidos, Usuario.especialidad,
            func.count(Nota.id).label("cursos"),
            func.coalesce(func.avg(Nota.promedio), 0).label("promedio"),
        )
        .join(Nota, Nota.estudiante_id == Usuario.id)
        .filter(Usuario.rol == ROL_ESTUDIANTE)
        .group_by(Usuario.id)
        .all()
    )
    return jsonify([
        {
            "estudiante": f"{f.apellidos}, {f.nombres}",
            "especialidad": f.especialidad,
            "cursos": f.cursos,
            "promedio": round(float(f.promedio), 2),
        } for f in filas
    ])
