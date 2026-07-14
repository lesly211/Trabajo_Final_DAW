"""Rutas de autenticación."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models.usuario import Usuario
from ..utils.audit import registrar

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    # El campo puede llamarse "username" o "identifier" (código/usuario)
    identifier = (data.get("identifier") or data.get("username") or "").strip()
    password = data.get("password", "")

    # Busca primero por username, luego por codigo (para estudiantes)
    user = (
        Usuario.query.filter_by(username=identifier, activo=True).first()
        or Usuario.query.filter_by(codigo=identifier, activo=True).first()
    )
    if not user or not user.check_password(password):
        return jsonify(error="Credenciales inválidas"), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"rol": user.rol, "nombre": user.nombre_completo},
    )
    registrar(user.id, "Inicio de sesión", "Seguridad")
    return jsonify(token=token, usuario=user.to_dict())


@auth_bp.get("/me")
@jwt_required()
def me():
    user = Usuario.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify(error="Usuario no encontrado"), 404
    return jsonify(user.to_dict())
