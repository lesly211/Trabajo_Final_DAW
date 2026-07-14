"""Generación de la ficha de matrícula oficial en PDF."""
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def generar_ficha_pdf(matricula) -> bytes:
    """Genera la ficha de matrícula oficial (PDF) para una matrícula validada.

    Incluye datos del estudiante, periodo, cursos matriculados con sus
    créditos, y el estado del pago.
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

    # ---- Título ----
    c.setFillColor(colors.HexColor("#1c2f4a"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(ancho / 2, alto - 45 * mm, "FICHA DE MATRÍCULA")
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.grey)
    c.drawCentredString(ancho / 2, alto - 52 * mm, f"Periodo académico {matricula.periodo}")

    # ---- Datos del estudiante ----
    est = matricula.estudiante
    y = alto - 68 * mm
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y, "Estudiante:")
    c.setFont("Helvetica", 12)
    c.drawString(65 * mm, y, est.nombre_completo if est else "—")

    y -= 8 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y, "Código:")
    c.setFont("Helvetica", 12)
    c.drawString(65 * mm, y, est.codigo if est else "—")

    y -= 8 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y, "Especialidad:")
    c.setFont("Helvetica", 12)
    c.drawString(65 * mm, y, est.especialidad if est else "—")

    # ---- Tabla de cursos ----
    y -= 16 * mm
    c.setFillColor(colors.HexColor("#1c2f4a"))
    c.rect(25 * mm, y - 2 * mm, ancho - 50 * mm, 8 * mm, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(28 * mm, y, "Código")
    c.drawString(60 * mm, y, "Curso")
    c.drawRightString(ancho - 28 * mm, y, "Créditos")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    total_creditos = 0
    for detalle in matricula.detalles:
        y -= 8 * mm
        curso = detalle.curso
        c.drawString(28 * mm, y, curso.codigo if curso else "—")
        c.drawString(60 * mm, y, curso.nombre if curso else "—")
        creditos = curso.creditos if curso else 0
        total_creditos += creditos
        c.drawRightString(ancho - 28 * mm, y, str(creditos))
        c.setStrokeColor(colors.HexColor("#e0e0e0"))
        c.line(25 * mm, y - 3 * mm, ancho - 25 * mm, y - 3 * mm)

    y -= 12 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25 * mm, y, f"Total de créditos: {total_creditos}")

    # ---- Estado de pago ----
    y -= 12 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y, "Monto:")
    c.setFont("Helvetica", 12)
    c.drawString(65 * mm, y, f"S/ {matricula.monto:.2f}")

    y -= 8 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y, "Estado de pago:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#1a7f37") if matricula.pago_registrado
                   else colors.HexColor("#b42318"))
    c.drawString(65 * mm, y, "REGISTRADO" if matricula.pago_registrado else "PENDIENTE")

    # ---- Pie ----
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Oblique", 9)
    fecha = matricula.creado_en.strftime("%d/%m/%Y %H:%M")
    c.drawString(25 * mm, 25 * mm, f"Solicitada el {fecha}")

    c.setStrokeColor(colors.HexColor("#c9a13b"))
    c.setLineWidth(1.2)
    c.line(20 * mm, 18 * mm, ancho - 20 * mm, 18 * mm)
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        ancho / 2, 12 * mm,
        "Documento generado electrónicamente por el Sistema Académico Integral — FIS UNCP",
    )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
