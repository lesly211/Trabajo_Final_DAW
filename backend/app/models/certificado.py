"""Modelo de certificados y documentos."""
from datetime import datetime
from ..extensions import db

SOLICITADO = "solicitado"
EMITIDO = "emitido"


class Certificado(db.Model):
    __tablename__ = "certificados"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo = db.Column(db.String(60), nullable=False)
    estado = db.Column(db.String(20), default=SOLICITADO)
    codigo_verificacion = db.Column(db.String(40), unique=True)
    qr_base64 = db.Column(db.Text)
    firma_digital = db.Column(db.String(64))
    metodo_emision = db.Column(db.String(20))  # "qr" | "firma_digital" | "ambos"
    autorizado = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    emitido_en = db.Column(db.DateTime)

    estudiante = db.relationship("Usuario")

    def to_dict(self):
        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "estudiante": self.estudiante.nombre_completo if self.estudiante else None,
            "tipo": self.tipo,
            "estado": self.estado,
            "codigo_verificacion": self.codigo_verificacion,
            "qr_base64": self.qr_base64,
            "firma_digital": self.firma_digital,
            "metodo_emision": self.metodo_emision,
            "autorizado": self.autorizado,
            "creado_en": self.creado_en.strftime("%Y-%m-%d %H:%M"),
            "emitido_en": self.emitido_en.strftime("%Y-%m-%d %H:%M") if self.emitido_en else None,
        }
