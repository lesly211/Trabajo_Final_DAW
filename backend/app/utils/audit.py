"""Helper para registrar acciones de auditoría."""
from ..extensions import db
from ..models.auditoria import Auditoria


def registrar(usuario_id, accion, modulo=None, detalle=None):
    log = Auditoria(usuario_id=usuario_id, accion=accion,
                    modulo=modulo, detalle=detalle)
    db.session.add(log)
    db.session.commit()
