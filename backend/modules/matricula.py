"""
MÓDULO 1: MATRÍCULA
Responsable: Olayne

Cubre:
- Solicitudes de matrícula con validación automática de requisitos
- Registro de pagos
- Generación de la ficha oficial de matrícula
"""
from datetime import datetime
from flask import Blueprint, jsonify, request

from data import (
    ESTUDIANTES, SOLICITUDES, PAGOS, CURSOS, REQUISITOS_LABELS,
    MAX_CREDITOS, COSTO_POR_CREDITO, PERIODO_ACTUAL,
    next_id, get_estudiante, get_curso, get_solicitud, get_docente,
)

matricula_bp = Blueprint("matricula", __name__, url_prefix="/api/matricula")


# ─────────────────────────────────────────────
# Helpers de validación
# ─────────────────────────────────────────────
def _hay_cruce(h1, h2):
    """Detecta si dos bloques horarios se solapan."""
    if h1["dia"] != h2["dia"]:
        return False
    return h1["hora_inicio"] < h2["hora_fin"] and h2["hora_inicio"] < h1["hora_fin"]


def _validar_requisitos(estudiante, cursos_sel):
    """Ejecuta todas las validaciones y devuelve el detalle."""
    checks = []

    # 1. Requisitos administrativos del estudiante
    for key, cumple in estudiante["requisitos"].items():
        checks.append({
            "codigo": key,
            "descripcion": REQUISITOS_LABELS[key],
            "cumple": bool(cumple),
        })

    # 2. Límite de créditos
    creditos = sum(c["creditos"] for c in cursos_sel)
    checks.append({
        "codigo": "limite_creditos",
        "descripcion": f"Carga académica dentro del límite ({creditos}/{MAX_CREDITOS} créditos)",
        "cumple": 0 < creditos <= MAX_CREDITOS,
    })

    # 3. Sin cruce de horarios entre los cursos elegidos
    cruces = []
    for i in range(len(cursos_sel)):
        for j in range(i + 1, len(cursos_sel)):
            for h1 in cursos_sel[i]["horarios"]:
                for h2 in cursos_sel[j]["horarios"]:
                    if _hay_cruce(h1, h2):
                        cruces.append(f"{cursos_sel[i]['codigo']} ↔ {cursos_sel[j]['codigo']} ({h1['dia']})")
    checks.append({
        "codigo": "sin_cruce_horarios",
        "descripcion": "Sin cruce de horarios entre los cursos seleccionados"
                       + (f" — Cruces: {', '.join(cruces)}" if cruces else ""),
        "cumple": len(cruces) == 0,
    })

    apto = all(c["cumple"] for c in checks)
    return {"checks": checks, "apto": apto, "creditos_total": creditos}


def _serializar_solicitud(s):
    est = get_estudiante(s["estudiante_id"])
    cursos = []
    for cid in s["cursos_ids"]:
        c = get_curso(cid)
        if c:
            doc = get_docente(c["docente_id"]) if c["docente_id"] else None
            cursos.append({
                "id": c["id"], "codigo": c["codigo"], "nombre": c["nombre"],
                "creditos": c["creditos"],
                "docente": doc["nombre"] if doc else "Por asignar",
                "horarios": c["horarios"],
            })
    return {
        "id": s["id"],
        "numero": f"SOL-{PERIODO_ACTUAL}-{s['id']:04d}",
        "estudiante": est,
        "periodo": s["periodo"],
        "cursos": cursos,
        "creditos_total": s["creditos_total"],
        "monto_total": s["monto_total"],
        "validacion": s["validacion"],
        "estado": s["estado"],
        "pago": s["pago"],
        "ficha": s["ficha"],
        "fecha_solicitud": s["fecha_solicitud"],
    }


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────
@matricula_bp.route("/estudiantes", methods=["GET"])
def listar_estudiantes():
    """Estudiantes disponibles para iniciar una solicitud."""
    return jsonify(ESTUDIANTES), 200


@matricula_bp.route("/solicitudes", methods=["GET"])
def listar_solicitudes():
    return jsonify([_serializar_solicitud(s) for s in SOLICITUDES]), 200


@matricula_bp.route("/solicitudes", methods=["POST"])
def crear_solicitud():
    """
    Crea una solicitud de matrícula y valida los requisitos.
    Body: { "estudiante_id": int, "cursos_ids": [int] }
    """
    body = request.get_json(silent=True) or {}
    estudiante = get_estudiante(body.get("estudiante_id"))
    if not estudiante:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    cursos_ids = body.get("cursos_ids") or []
    cursos_sel = [get_curso(cid) for cid in cursos_ids]
    if not cursos_sel or any(c is None for c in cursos_sel):
        return jsonify({"error": "Debe seleccionar al menos un curso válido"}), 400

    # Evitar solicitud duplicada activa del mismo estudiante en el periodo
    dup = next((s for s in SOLICITUDES
                if s["estudiante_id"] == estudiante["id"]
                and s["periodo"] == PERIODO_ACTUAL
                and s["estado"] != "observada"), None)
    if dup:
        return jsonify({"error": "El estudiante ya tiene una solicitud activa en este periodo"}), 409

    validacion = _validar_requisitos(estudiante, cursos_sel)
    monto = round(validacion["creditos_total"] * COSTO_POR_CREDITO, 2)

    solicitud = {
        "id": next_id("solicitud"),
        "estudiante_id": estudiante["id"],
        "periodo": PERIODO_ACTUAL,
        "cursos_ids": cursos_ids,
        "creditos_total": validacion["creditos_total"],
        "monto_total": monto,
        "validacion": validacion,
        "estado": "pendiente_pago" if validacion["apto"] else "observada",
        "pago": None,
        "ficha": None,
        "fecha_solicitud": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    SOLICITUDES.append(solicitud)
    return jsonify(_serializar_solicitud(solicitud)), 201


@matricula_bp.route("/solicitudes/<int:sol_id>/pago", methods=["POST"])
def registrar_pago(sol_id):
    """
    Registra el pago de una solicitud apta y genera la ficha oficial.
    Body: { "metodo": str, "nro_operacion": str, "monto": float }
    """
    s = get_solicitud(sol_id)
    if not s:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    if s["estado"] == "observada":
        return jsonify({"error": "La solicitud está observada: no cumple los requisitos"}), 422
    if s["estado"] == "matriculado":
        return jsonify({"error": "La solicitud ya cuenta con pago registrado"}), 409

    body = request.get_json(silent=True) or {}
    metodo = body.get("metodo")
    nro_op = body.get("nro_operacion", "").strip()
    monto = float(body.get("monto", 0))

    if metodo not in ("Efectivo", "Tarjeta", "Transferencia", "Yape/Plin"):
        return jsonify({"error": "Método de pago inválido"}), 400
    if not nro_op:
        return jsonify({"error": "Debe indicar el número de operación"}), 400
    if abs(monto - s["monto_total"]) > 0.01:
        return jsonify({"error": f"El monto no coincide. Total a pagar: S/ {s['monto_total']:.2f}"}), 400

    pago = {
        "id": next_id("pago"),
        "solicitud_id": s["id"],
        "metodo": metodo,
        "nro_operacion": nro_op,
        "monto": monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    PAGOS.append(pago)
    s["pago"] = pago

    # Generación de la ficha oficial
    nro_ficha = next_id("ficha")
    s["ficha"] = {
        "numero": f"FM-{PERIODO_ACTUAL}-{nro_ficha:05d}",
        "fecha_emision": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    s["estado"] = "matriculado"
    return jsonify(_serializar_solicitud(s)), 200


@matricula_bp.route("/solicitudes/<int:sol_id>/ficha", methods=["GET"])
def obtener_ficha(sol_id):
    """Devuelve los datos completos de la ficha oficial de matrícula."""
    s = get_solicitud(sol_id)
    if not s:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    if s["estado"] != "matriculado" or not s["ficha"]:
        return jsonify({"error": "La ficha se genera al confirmar el pago"}), 422
    data = _serializar_solicitud(s)
    return jsonify(data), 200
