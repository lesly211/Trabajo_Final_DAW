"""Modelo de notas / actas."""
from datetime import datetime
from ..extensions import db


class Nota(db.Model):
    __tablename__ = "notas"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    parcial1 = db.Column(db.Float)
    parcial2 = db.Column(db.Float)
    final = db.Column(db.Float)
    promedio = db.Column(db.Float)
    validada = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship("Usuario", foreign_keys=[estudiante_id])
    curso = db.relationship("Curso")

    def calcular_promedio(self):
        vals = [v for v in (self.parcial1, self.parcial2, self.final) if v is not None]
        self.promedio = round(sum(vals) / len(vals), 2) if vals else None
        return self.promedio

    def to_dict(self):
        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "estudiante": self.estudiante.nombre_completo if self.estudiante else None,
            "curso_id": self.curso_id,
            "curso": self.curso.nombre if self.curso else None,
            "codigo": self.curso.codigo if self.curso else None,
            "creditos": self.curso.creditos if self.curso else None,
            "periodo": self.periodo,
            "parcial1": self.parcial1,
            "parcial2": self.parcial2,
            "final": self.final,
            "promedio": self.promedio,
            "validada": self.validada,
            "estado": "Aprobado" if (self.promedio or 0) >= 10.5 else "Desaprobado",
        }
