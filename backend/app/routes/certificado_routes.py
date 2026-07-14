"""Módulo 5: Certificados y Documentos."""
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models.certificado import Certificado, EMITIDO
from ..models.usuario import ROL_ESTUDIANTE, ROL_ADMIN, ROL_DIRECCION
from ..utils.decorators import roles_required
from ..utils.audit import registrar
from ..utils.firma import verificar_firma, payload_certificado
from ..services.certificado_service import emitir as emitir_cert, generar_pdf

certificado_bp = Blueprint("certificado", __name__)


@certificado_bp.get("")
@jwt_required()
def listar():
    claims = get_jwt()
    uid = int(get_jwt_identity())
    q = Certificado.query
    if claims["rol"] == ROL_ESTUDIANTE:
        q = q.filter_by(estudiante_id=uid)
    return jsonify([c.to_dict() for c in q.order_by(Certificado.creado_en.desc())])


@certificado_bp.post("")
@roles_required(ROL_ESTUDIANTE)
def solicitar():
    """Estudiante solicita certificado/constancia en línea."""
    data = request.get_json() or {}
    uid = int(get_jwt_identity())
    cert = Certificado(estudiante_id=uid, tipo=data.get("tipo", "Constancia de estudios"))
    db.session.add(cert)
    db.session.commit()
    registrar(uid, "Solicitud de certificado", "Certificados", cert.tipo)
    return jsonify(cert.to_dict()), 201


@certificado_bp.patch("/<int:cid>/autorizar")
@roles_required(ROL_DIRECCION)
def autorizar(cid):
    """Dirección autoriza la emisión de documentos oficiales."""
    cert = Certificado.query.get_or_404(cid)
    cert.autorizado = True
    db.session.commit()
    registrar(int(get_jwt_identity()), "Autorización de documento", "Certificados",
              f"Certificado #{cid}")
    return jsonify(cert.to_dict())


@certificado_bp.patch("/<int:cid>/emitir")
@roles_required(ROL_ADMIN)
def emitir(cid):
    """Admin emite el certificado con firma digital y/o QR (requiere
    autorización previa de Dirección). El body puede incluir
    {"metodo": "qr" | "firma_digital" | "ambos"} (por defecto "ambos")."""
    data = request.get_json(silent=True) or {}
    metodo = data.get("metodo", "ambos")
    cert = Certificado.query.get_or_404(cid)
    if not cert.autorizado:
        return jsonify(error="El documento aún no ha sido autorizado por Dirección"), 409
    emitir_cert(cert, metodo=metodo)
    registrar(int(get_jwt_identity()), "Emisión de certificado", "Certificados",
              f"{cert.codigo_verificacion} · método: {cert.metodo_emision}")
    return jsonify(cert.to_dict())


@certificado_bp.get("/<int:cid>/pdf")
@jwt_required()
def descargar_pdf(cid):
    """Descarga el documento oficial en PDF (con QR de verificación).

    El estudiante solo puede descargar sus propios certificados;
    admin y dirección pueden descargar cualquiera.
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    cert = Certificado.query.get_or_404(cid)

    if claims["rol"] == ROL_ESTUDIANTE and cert.estudiante_id != uid:
        return jsonify(error="No autorizado"), 403
    if claims["rol"] not in (ROL_ESTUDIANTE, ROL_ADMIN, ROL_DIRECCION):
        return jsonify(error="No autorizado"), 403
    if cert.estado != EMITIDO:
        return jsonify(error="El documento aún no ha sido emitido"), 409

    pdf_bytes = generar_pdf(cert)
    registrar(uid, "Descarga de documento PDF", "Certificados", cert.codigo_verificacion)
    nombre = f"{cert.tipo.replace(' ', '_')}_{cert.codigo_verificacion}.pdf"
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre}"},
    )


@certificado_bp.get("/verificar/<codigo>")
def verificar(codigo):
    """Verificación pública (sin autenticación) de un documento emitido.

    Es el endpoint al que apunta el código QR impreso en cada certificado.
    """
    cert = Certificado.query.filter_by(codigo_verificacion=codigo, estado=EMITIDO).first()
    if not cert:
        return jsonify(valido=False, mensaje="Código no encontrado o documento no emitido"), 404

    firma_integra = True
    if cert.firma_digital:
        firma_integra = verificar_firma(payload_certificado(cert), cert.firma_digital)

    return jsonify(
        valido=True,
        firma_integra=firma_integra,
        tipo=cert.tipo,
        estudiante=cert.estudiante.nombre_completo if cert.estudiante else None,
        codigo_verificacion=cert.codigo_verificacion,
        metodo_emision=cert.metodo_emision,
        emitido_en=cert.emitido_en.strftime("%Y-%m-%d %H:%M") if cert.emitido_en else None,
    )
