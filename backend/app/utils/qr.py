"""Generación de código QR en base64."""
import base64
import io
import qrcode


def generar_qr(texto: str) -> str:
    img = qrcode.make(texto)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
