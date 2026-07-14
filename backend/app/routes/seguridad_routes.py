"""Módulo 6: Administración y Seguridad (usuarios + auditoría)."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.usuario import Usuario, ROLES, ROL_ADMIN, ROL_DIRECCION
from ..models.auditoria import Auditoria
from ..utils.decorators import roles_required
from ..utils.audit import registrar

seguridad_bp = Blueprint("seguridad", __name__)


# ---- Gestión de usuarios (Admin) ----
@seguridad_bp.get("/usuarios")
@roles_required(ROL_ADMIN, ROL_DIRECCION)
def listar_usuarios():
    rol = request.args.get("rol")
    q = Usuario.query
    if rol:
        q = q.filter_by(rol=rol)
    return jsonify([u.to_dict() for u in q.order_by(Usuario.apellidos)])


@seguridad_bp.post("/usuarios")
@roles_required(ROL_ADMIN)
def crear_usuario():
    data = request.get_json() or {}
    if data.get("rol") not in ROLES:
        return jsonify(error="Rol inválido"), 400
    if Usuario.query.filter_by(username=data["username"]).first():
        return jsonify(error="El usuario ya existe"), 409

    u = Usuario(
        username=data["username"], nombres=data["nombres"],
        apellidos=data["apellidos"], rol=data["rol"],
        codigo=data.get("codigo"), especialidad=data.get("especialidad"),
    )
    u.set_password(data.get("password", "123456"))
    db.session.add(u)
    db.session.commit()
    registrar(int(get_jwt_identity()), "Creación de usuario", "Seguridad", u.username)
    return jsonify(u.to_dict()), 201


@seguridad_bp.patch("/usuarios/<int:uid>")
@roles_required(ROL_ADMIN)
def actualizar_usuario(uid):
    data = request.get_json() or {}
    u = Usuario.query.get_or_404(uid)
    for campo in ("nombres", "apellidos", "rol", "especialidad", "activo"):
        if campo in data:
            setattr(u, campo, data[campo])
    if data.get("password"):
        u.set_password(data["password"])
    db.session.commit()
    registrar(int(get_jwt_identity()), "Actualización de usuario", "Seguridad", u.username)
    return jsonify(u.to_dict())


# ---- Auditoría (Dirección) ----
@seguridad_bp.get("/seguridad/auditoria")
@roles_required(ROL_DIRECCION, ROL_ADMIN)
def auditoria():
    logs = Auditoria.query.order_by(Auditoria.fecha.desc()).limit(200).all()
    return jsonify([l.to_dict() for l in logs])
