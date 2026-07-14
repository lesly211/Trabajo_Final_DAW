"""Lógica de emisión de certificados."""
import base64
import io
import uuid
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from ..config import Config
from ..extensions import db
from ..models.certificado import Certificado, EMITIDO
from ..utils.qr import generar_qr
from ..utils.firma import firmar, payload_certificado

METODOS_VALIDOS = ("qr", "firma_digital", "ambos")


def emitir(certificado: Certificado, metodo: str = "ambos") -> Certificado:
    """Emite el certificado generando código de verificación y, según el
    método elegido (QR, firma digital HMAC-SHA256, o ambos), los datos
    técnicos que certifican su autenticidad.

    El QR codifica una URL de verificación pública dentro del propio
    sistema (frontend), de modo que al escanearlo se pueda comprobar
    la autenticidad del documento sin necesidad de iniciar sesión. La
    firma digital permite validar la integridad de los datos del
    documento (estudiante, tipo, código) sin depender de una imagen.
    """
    if metodo not in METODOS_VALIDOS:
        metodo = "ambos"

    codigo = uuid.uuid4().hex[:12].upper()
    certificado.codigo_verificacion = codigo

    if metodo in ("firma_digital", "ambos"):
        certificado.firma_digital = firmar(payload_certificado(certificado))

    if metodo in ("qr", "ambos"):
        url = f"{Config.FRONTEND_URL}/verificar/{codigo}"
        certificado.qr_base64 = generar_qr(url)

    certificado.metodo_emision = metodo
    certificado.estado = EMITIDO
    certificado.emitido_en = datetime.utcnow()
    db.session.commit()
    return certificado


def generar_pdf(certificado: Certificado) -> bytes:
    """Genera el documento oficial en PDF, con firma digital (QR) embebida.

    Requiere que el certificado ya haya sido emitido (tiene código de
    verificación y QR).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    ancho, alto = A4

    # ---- Encabezado institucional ----
    c.setFillColor(colors.HexColor("#1c2f4a"))
    c.rect(0, alto - 30 * mm, ancho, 30 * mm, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ancho / 2, alto - 14 * mm,
                        "UNIVERSIDAD NACIONAL DEL CENTRO DEL PERÚ")
    c.setFont("Helvetica", 11)
    c.drawCentredString(ancho / 2, alto - 21 * mm,
                        "Facultad de Ingeniería de Sistemas")

    # ---- Título del documento ----
    c.setFillColor(colors.HexColor("#1c2f4a"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ancho / 2, alto - 50 * mm, certificado.tipo.upper())

    # ---- Cuerpo ----
    estudiante = certificado.estudiante
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    texto = (
        f"La Facultad de Ingeniería de Sistemas de la Universidad Nacional del "
        f"Centro del Perú hace constar que:"
    )
    c.drawCentredString(ancho / 2, alto - 68 * mm, texto)

    c.setFont("Helvetica-Bold", 15)
    nombre = estudiante.nombre_completo if estudiante else "—"
    c.drawCentredString(ancho / 2, alto - 80 * mm, nombre)

    c.setFont("Helvetica", 11)
    codigo_est = estudiante.codigo if estudiante else "—"
    especialidad = estudiante.especialidad if estudiante else "—"
    c.drawCentredString(ancho / 2, alto - 88 * mm,
                        f"Código: {codigo_est}  ·  Especialidad: {especialidad}")

    c.setFont("Helvetica", 12)
    c.drawCentredString(
        ancho / 2, alto - 100 * mm,
        f"cuenta con el documento «{certificado.tipo}» debidamente autorizado y emitido",
    )
    c.drawCentredString(
        ancho / 2, alto - 107 * mm,
        "por las instancias correspondientes de la institución.",
    )

    fecha = (certificado.emitido_en or datetime.utcnow()).strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(ancho / 2, alto - 120 * mm, f"Emitido el {fecha}")

    # ---- QR + código de verificación ----
    if certificado.qr_base64:
        qr_bytes = base64.b64decode(certificado.qr_base64.split(",", 1)[1])
        qr_img = ImageReader(io.BytesIO(qr_bytes))
        qr_size = 32 * mm
        qr_x = (ancho - qr_size) / 2
        qr_y = 40 * mm
        c.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size,
                   preserveAspectRatio=True, mask="auto")

    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(ancho / 2, 35 * mm,
                        f"Código de verificación: {certificado.codigo_verificacion}")

    if certificado.firma_digital:
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.grey)
        firma_corta = f"{certificado.firma_digital[:32]}…"
        c.drawCentredString(ancho / 2, 31 * mm, f"Firma digital (HMAC-SHA256): {firma_corta}")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(
        ancho / 2, 27 * mm,
        f"Verifique la autenticidad de este documento escaneando el código QR "
        f"o ingresando a: {Config.FRONTEND_URL}/verificar/{certificado.codigo_verificacion}",
    )

    # ---- Pie ----
    c.setStrokeColor(colors.HexColor("#c9a13b"))
    c.setLineWidth(1.2)
    c.line(20 * mm, 18 * mm, ancho - 20 * mm, 18 * mm)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(ancho / 2, 12 * mm,
                        "Documento generado electrónicamente por el Sistema Académico Integral — FIS UNCP")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
