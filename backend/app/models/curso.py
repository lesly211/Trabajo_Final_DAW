"""Modelos de curso, sílabo y asignación docente."""
from datetime import datetime
from ..extensions import db


class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    creditos = db.Column(db.Integer, nullable=False, default=3)
    ciclo = db.Column(db.Integer, nullable=False, default=1)
    especialidad = db.Column(db.String(120))
    docente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    horario = db.Column(db.String(120))
    silabo_url = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    docente = db.relationship("Usuario", backref="cursos_asignados")

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
            "ciclo": self.ciclo,
            "especialidad": self.especialidad,
            "docente_id": self.docente_id,
            "docente": self.docente.nombre_completo if self.docente else None,
            "horario": self.horario,
            "silabo_url": self.silabo_url,
        }
