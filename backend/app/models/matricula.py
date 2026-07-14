"""Modelo de matrícula."""
from datetime import datetime
from ..extensions import db

PENDIENTE = "pendiente"
VALIDADA = "validada"
RECHAZADA = "rechazada"


class Matricula(db.Model):
    __tablename__ = "matriculas"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), default=PENDIENTE)
    pago_registrado = db.Column(db.Boolean, default=False)
    monto = db.Column(db.Float, default=0.0)
    observacion = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship("Usuario", backref="matriculas")
    detalles = db.relationship("MatriculaDetalle", backref="matricula",
                               cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "estudiante": self.estudiante.nombre_completo if self.estudiante else None,
            "periodo": self.periodo,
            "estado": self.estado,
            "pago_registrado": self.pago_registrado,
            "monto": self.monto,
            "observacion": self.observacion,
            "cursos": [d.to_dict() for d in self.detalles],
            "creado_en": self.creado_en.strftime("%Y-%m-%d %H:%M"),
        }


class MatriculaDetalle(db.Model):
    __tablename__ = "matricula_detalles"

    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey("matriculas.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)

    curso = db.relationship("Curso")

    def to_dict(self):
        return {
            "curso_id": self.curso_id,
            "codigo": self.curso.codigo if self.curso else None,
            "nombre": self.curso.nombre if self.curso else None,
            "creditos": self.curso.creditos if self.curso else None,
        }
