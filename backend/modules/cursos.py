"""
MÓDULO 2: CURSOS Y DOCENTES
Responsable: Olayne

Cubre:
- Asignación de docentes a cursos (con control de carga máxima)
- Gestión de horarios (con detección de cruces de aula y docente)
- Carga de sílabos (PDF)
"""
import os
from datetime import datetime
from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from data import CURSOS, DOCENTES, next_id, get_curso, get_docente

cursos_bp = Blueprint("cursos", __name__, url_prefix="/api/cursos")

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "silabos")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DIAS_VALIDOS = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado")


def _serializar_curso(c):
    doc = get_docente(c["docente_id"]) if c["docente_id"] else None
    return {**c, "docente": doc}


def _hay_cruce(h1, h2):
    if h1["dia"] != h2["dia"]:
        return False
    return h1["hora_inicio"] < h2["hora_fin"] and h2["hora_inicio"] < h1["hora_fin"]


# ─────────────────────────────────────────────
# Cursos y docentes
# ─────────────────────────────────────────────
@cursos_bp.route("", methods=["GET"])
def listar_cursos():
    return jsonify([_serializar_curso(c) for c in CURSOS]), 200


@cursos_bp.route("/docentes", methods=["GET"])
def listar_docentes():
    """Docentes con su carga actual de cursos."""
    result = []
    for d in DOCENTES:
        carga = sum(1 for c in CURSOS if c["docente_id"] == d["id"])
        result.append({**d, "cursos_asignados": carga})
    return jsonify(result), 200


@cursos_bp.route("/<int:curso_id>/docente", methods=["PUT"])
def asignar_docente(curso_id):
    """
    Asigna (o retira) un docente a un curso.
    Body: { "docente_id": int | null }
    """
    curso = get_curso(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404

    body = request.get_json(silent=True) or {}
    docente_id = body.get("docente_id")

    if docente_id is None:
        curso["docente_id"] = None
        return jsonify(_serializar_curso(curso)), 200

    docente = get_docente(docente_id)
    if not docente:
        return jsonify({"error": "Docente no encontrado"}), 404

    # Control de carga máxima
    carga = sum(1 for c in CURSOS if c["docente_id"] == docente_id and c["id"] != curso_id)
    if carga >= docente["max_cursos"]:
        return jsonify({"error": f"{docente['nombre']} ya alcanzó su carga máxima ({docente['max_cursos']} cursos)"}), 422

    # Control de cruce de horarios con los otros cursos del docente
    for c in CURSOS:
        if c["docente_id"] == docente_id and c["id"] != curso_id:
            for h1 in c["horarios"]:
                for h2 in curso["horarios"]:
                    if _hay_cruce(h1, h2):
                        return jsonify({"error": f"Cruce de horario con {c['codigo']} ({h1['dia']} {h1['hora_inicio']}–{h1['hora_fin']})"}), 422

    curso["docente_id"] = docente_id
    return jsonify(_serializar_curso(curso)), 200


# ─────────────────────────────────────────────
# Horarios
# ─────────────────────────────────────────────
@cursos_bp.route("/<int:curso_id>/horarios", methods=["POST"])
def agregar_horario(curso_id):
    """
    Agrega un bloque horario a un curso.
    Body: { "dia": str, "hora_inicio": "HH:MM", "hora_fin": "HH:MM", "aula": str }
    """
    curso = get_curso(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404

    body = request.get_json(silent=True) or {}
    dia = body.get("dia")
    hi, hf = body.get("hora_inicio", ""), body.get("hora_fin", "")
    aula = (body.get("aula") or "").strip()

    if dia not in DIAS_VALIDOS:
        return jsonify({"error": "Día inválido"}), 400
    if not (hi and hf and hi < hf):
        return jsonify({"error": "Rango horario inválido (la hora de inicio debe ser menor a la de fin)"}), 400
    if not aula:
        return jsonify({"error": "Debe indicar el aula"}), 400

    nuevo = {"id": next_id("horario"), "dia": dia, "hora_inicio": hi, "hora_fin": hf, "aula": aula}

    # Conflicto 1: misma aula ocupada en ese rango (cualquier curso)
    for c in CURSOS:
        for h in c["horarios"]:
            if h["aula"].lower() == aula.lower() and _hay_cruce(h, nuevo):
                return jsonify({"error": f"El aula {aula} está ocupada por {c['codigo']} ({h['dia']} {h['hora_inicio']}–{h['hora_fin']})"}), 422

    # Conflicto 2: el docente del curso tiene otro dictado en ese rango
    if curso["docente_id"]:
        for c in CURSOS:
            if c["docente_id"] == curso["docente_id"] and c["id"] != curso_id:
                for h in c["horarios"]:
                    if _hay_cruce(h, nuevo):
                        return jsonify({"error": f"El docente tiene cruce con {c['codigo']} ({h['dia']} {h['hora_inicio']}–{h['hora_fin']})"}), 422

    curso["horarios"].append(nuevo)
    return jsonify(_serializar_curso(curso)), 201


@cursos_bp.route("/<int:curso_id>/horarios/<int:horario_id>", methods=["DELETE"])
def eliminar_horario(curso_id, horario_id):
    curso = get_curso(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    antes = len(curso["horarios"])
    curso["horarios"] = [h for h in curso["horarios"] if h["id"] != horario_id]
    if len(curso["horarios"]) == antes:
        return jsonify({"error": "Horario no encontrado"}), 404
    return jsonify(_serializar_curso(curso)), 200


# ─────────────────────────────────────────────
# Sílabos
# ─────────────────────────────────────────────
@cursos_bp.route("/<int:curso_id>/silabo", methods=["POST"])
def cargar_silabo(curso_id):
    """Carga el sílabo del curso (PDF, multipart/form-data, campo 'file')."""
    curso = get_curso(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404

    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Debe adjuntar un archivo"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "El sílabo debe ser un archivo PDF"}), 400

    filename = secure_filename(f"silabo_{curso['codigo']}_{file.filename}")
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)

    curso["silabo"] = {
        "nombre_archivo": filename,
        "fecha_carga": datetime.now().strftime("%Y-%m-%d"),
        "tamano_kb": round(os.path.getsize(path) / 1024),
    }
    return jsonify(_serializar_curso(curso)), 201


@cursos_bp.route("/<int:curso_id>/silabo", methods=["GET"])
def descargar_silabo(curso_id):
    curso = get_curso(curso_id)
    if not curso or not curso["silabo"]:
        return jsonify({"error": "El curso no tiene sílabo cargado"}), 404
    fname = curso["silabo"]["nombre_archivo"]
    if not os.path.exists(os.path.join(UPLOAD_DIR, fname)):
        return jsonify({"error": "Archivo de sílabo no disponible en el servidor"}), 404
    return send_from_directory(UPLOAD_DIR, fname, as_attachment=True)


@cursos_bp.route("/<int:curso_id>/silabo", methods=["DELETE"])
def eliminar_silabo(curso_id):
    curso = get_curso(curso_id)
    if not curso:
        return jsonify({"error": "Curso no encontrado"}), 404
    curso["silabo"] = None
    return jsonify(_serializar_curso(curso)), 200
