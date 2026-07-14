"""
Almacén de datos en memoria compartido entre módulos.
NOTA: Cuando se implemente la BD (database/schema.sql), estos datos
se migrarán a modelos SQLAlchemy. La estructura ya refleja las tablas futuras.
"""

# ─────────────────────────────────────────────
# DOCENTES
# ─────────────────────────────────────────────
DOCENTES = [
    {"id": 1, "codigo": "DOC-001", "nombre": "María Elena Quispe Rojas",
     "especialidad": "Desarrollo de Software", "grado": "Magíster", "max_cursos": 3},
    {"id": 2, "codigo": "DOC-002", "nombre": "Jorge Luis Mendoza Paredes",
     "especialidad": "Base de Datos", "grado": "Doctor", "max_cursos": 3},
    {"id": 3, "codigo": "DOC-003", "nombre": "Rosa Angélica Torres Vila",
     "especialidad": "Redes y Comunicaciones", "grado": "Magíster", "max_cursos": 3},
    {"id": 4, "codigo": "DOC-004", "nombre": "Carlos Alberto Huamán Ríos",
     "especialidad": "Matemática Aplicada", "grado": "Doctor", "max_cursos": 3},
    {"id": 5, "codigo": "DOC-005", "nombre": "Lucía Fernanda Cárdenas Soto",
     "especialidad": "Gestión de Proyectos", "grado": "Magíster", "max_cursos": 3},
]

# ─────────────────────────────────────────────
# CURSOS
# docente_id: None = sin asignar
# horarios: [{id, dia, hora_inicio, hora_fin, aula}]
# silabo: None o {nombre_archivo, fecha_carga, tamano_kb}
# ─────────────────────────────────────────────
CURSOS = [
    {"id": 1, "codigo": "CSC-501", "nombre": "Desarrollo de Aplicaciones Web",
     "creditos": 4, "ciclo": 5, "docente_id": 1,
     "horarios": [
         {"id": 1, "dia": "Lunes", "hora_inicio": "08:00", "hora_fin": "10:00", "aula": "Lab A-301"},
         {"id": 2, "dia": "Miércoles", "hora_inicio": "08:00", "hora_fin": "10:00", "aula": "Lab A-301"},
     ],
     "silabo": {"nombre_archivo": "silabo_CSC501_2026-I.pdf", "fecha_carga": "2026-03-10", "tamano_kb": 245}},
    {"id": 2, "codigo": "CSC-502", "nombre": "Base de Datos Avanzadas",
     "creditos": 4, "ciclo": 5, "docente_id": 2,
     "horarios": [
         {"id": 3, "dia": "Martes", "hora_inicio": "10:00", "hora_fin": "12:00", "aula": "Lab B-102"},
     ],
     "silabo": None},
    {"id": 3, "codigo": "CSC-503", "nombre": "Redes de Computadoras II",
     "creditos": 3, "ciclo": 5, "docente_id": None,
     "horarios": [], "silabo": None},
    {"id": 4, "codigo": "CSC-504", "nombre": "Investigación de Operaciones",
     "creditos": 3, "ciclo": 5, "docente_id": None,
     "horarios": [], "silabo": None},
    {"id": 5, "codigo": "CSC-505", "nombre": "Gestión de Proyectos de TI",
     "creditos": 3, "ciclo": 5, "docente_id": 5,
     "horarios": [
         {"id": 4, "dia": "Viernes", "hora_inicio": "14:00", "hora_fin": "17:00", "aula": "Aula C-204"},
     ],
     "silabo": None},
    {"id": 6, "codigo": "CSC-506", "nombre": "Arquitectura de Software",
     "creditos": 4, "ciclo": 5, "docente_id": None,
     "horarios": [], "silabo": None},
]

# ─────────────────────────────────────────────
# ESTUDIANTES (con estado de requisitos para matrícula)
# ─────────────────────────────────────────────
ESTUDIANTES = [
    {"id": 1, "codigo": "2023100456", "nombre": "Ana Sofía Ramírez Gutiérrez",
     "carrera": "Ingeniería de Sistemas", "ciclo": 5,
     "requisitos": {"sin_deuda": True, "documentos_completos": True,
                    "sin_sancion": True, "record_habilitado": True}},
    {"id": 2, "codigo": "2023100789", "nombre": "Diego Armando Flores Ccama",
     "carrera": "Ingeniería de Sistemas", "ciclo": 5,
     "requisitos": {"sin_deuda": False, "documentos_completos": True,
                    "sin_sancion": True, "record_habilitado": True}},
    {"id": 3, "codigo": "2022200341", "nombre": "Valeria Nicole Castro Mamani",
     "carrera": "Ingeniería de Sistemas", "ciclo": 5,
     "requisitos": {"sin_deuda": True, "documentos_completos": False,
                    "sin_sancion": True, "record_habilitado": True}},
    {"id": 4, "codigo": "2023101123", "nombre": "Renato Gabriel Ponce Vargas",
     "carrera": "Ingeniería de Sistemas", "ciclo": 5,
     "requisitos": {"sin_deuda": True, "documentos_completos": True,
                    "sin_sancion": True, "record_habilitado": True}},
]

REQUISITOS_LABELS = {
    "sin_deuda": "No registra deudas pendientes con la institución",
    "documentos_completos": "Documentación personal completa y validada",
    "sin_sancion": "No presenta sanciones disciplinarias vigentes",
    "record_habilitado": "Récord académico habilitado para el ciclo",
}

# ─────────────────────────────────────────────
# SOLICITUDES DE MATRÍCULA Y PAGOS (inician vacíos)
# solicitud: {id, estudiante_id, periodo, cursos_ids, creditos_total,
#             validacion: {...}, estado, pago, ficha, fecha_solicitud}
# estados: observada | pendiente_pago | matriculado
# ─────────────────────────────────────────────
SOLICITUDES = []
PAGOS = []

# Contadores autoincrementales simples
COUNTERS = {"solicitud": 0, "pago": 0, "horario": 100, "ficha": 0}

MAX_CREDITOS = 22
COSTO_POR_CREDITO = 85.0  # S/ por crédito
PERIODO_ACTUAL = "2026-I"


def next_id(key):
    COUNTERS[key] += 1
    return COUNTERS[key]


def get_docente(docente_id):
    return next((d for d in DOCENTES if d["id"] == docente_id), None)


def get_curso(curso_id):
    return next((c for c in CURSOS if c["id"] == curso_id), None)


def get_estudiante(est_id):
    return next((e for e in ESTUDIANTES if e["id"] == est_id), None)


def get_solicitud(sol_id):
    return next((s for s in SOLICITUDES if s["id"] == sol_id), None)
