"""Firma digital de documentos (HMAC-SHA256).

Genera una firma que certifica la integridad y autenticidad de un
certificado emitido: cualquier alteración posterior de sus datos
(estudiante, tipo, código) invalida la firma. La clave de firma nunca
sale del servidor, por lo que la firma no puede ser falsificada desde
el cliente.
"""
import hashlib
import hmac
from flask import current_app


def _clave_firma() -> bytes:
    return current_app.config["SECRET_KEY"].encode()


def firmar(payload: str) -> str:
    """Genera la firma digital (hex, mayúsculas) de un payload textual."""
    return hmac.new(_clave_firma(), payload.encode(), hashlib.sha256).hexdigest().upper()


def verificar_firma(payload: str, firma: str) -> bool:
    """Verifica que la firma corresponda al payload, sin filtrar timing."""
    if not firma:
        return False
    return hmac.compare_digest(firmar(payload), firma)


def payload_certificado(certificado) -> str:
    """Payload canónico que se firma para un certificado dado."""
    return (
        f"{certificado.id}|{certificado.estudiante_id}|{certificado.tipo}|"
        f"{certificado.codigo_verificacion}"
    )
