"""Modelo de auditoría / log de seguridad."""
from datetime import datetime
from ..extensions import db


class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    accion = db.Column(db.String(120), nullable=False)
    modulo = db.Column(db.String(60))
    detalle = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario.nombre_completo if self.usuario else "Sistema",
            "rol": self.usuario.rol if self.usuario else None,
            "accion": self.accion,
            "modulo": self.modulo,
            "detalle": self.detalle,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        }
