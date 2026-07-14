"""Modelo de usuario y roles."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

ROL_ESTUDIANTE = "estudiante"
ROL_DOCENTE = "docente"
ROL_ADMIN = "admin"
ROL_DIRECCION = "direccion"
ROLES = (ROL_ESTUDIANTE, ROL_DOCENTE, ROL_ADMIN, ROL_DIRECCION)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nombres = db.Column(db.String(120), nullable=False)
    apellidos = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default=ROL_ESTUDIANTE)
    codigo = db.Column(db.String(20), unique=True)
    especialidad = db.Column(db.String(120))
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    @property
    def nombre_completo(self):
        return f"{self.apellidos}, {self.nombres}"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "nombre_completo": self.nombre_completo,
            "rol": self.rol,
            "codigo": self.codigo,
            "especialidad": self.especialidad,
            "activo": self.activo,
        }
