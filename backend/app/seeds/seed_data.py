"""Datos iniciales del sistema."""
import unicodedata
import re
from ..extensions import db
from ..models.usuario import (
    Usuario, ROL_ESTUDIANTE, ROL_DOCENTE, ROL_ADMIN, ROL_DIRECCION,
)
from ..models.curso import Curso
from ..models.nota import Nota
from ..models.matricula import Matricula, MatriculaDetalle, VALIDADA


def _normalizar(texto):
    """Quita tildes y caracteres especiales, retorna minúsculas sin espacios."""
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", sin_tildes.lower())


def _password(primer_nombre: str, apellidos: str, codigo: str) -> str:
    """
    Fórmula: 1ª letra del primer nombre (MAYÚSCULA)
             + apellido paterno (primera palabra de apellidos, normalizado)
             + primeras 4 cifras del código (sólo dígitos, relleno con 0)
             + *
    Ejemplo: Juan Pérez Quispe / 2021100123  →  JPerez2021*
             María López Ríos  / D-001       →  MLopez0001*
    """
    inicial = primer_nombre[0].upper()
    apellido_paterno = apellidos.split()[0]          # primera palabra
    apellido_norm = unicodedata.normalize("NFKD", apellido_paterno)
    apellido_norm = "".join(c for c in apellido_norm if not unicodedata.combining(c))
    # capitaliza correctamente (respeta el normalize)
    apellido_cap = apellido_norm[0].upper() + apellido_norm[1:].lower()

    digitos = re.sub(r"\D", "", codigo)              # sólo números del código
    cifras = digitos[:4].zfill(4)                    # exactamente 4 dígitos
    return f"{inicial}{apellido_cap}{cifras}*"


def seed_all():
    if Usuario.query.first():
        return  # ya sembrado

    ESP = "Ingeniería de Sistemas"

    # ------------------------------------------------------------------
    # Estudiantes
    # username  = código de matrícula (lo que ingresa en el login)
    # password  = fórmula
    # ------------------------------------------------------------------
    estudiantes_data = [
        ("Juan",   "Pérez Quispe",      "2021100123"),
        ("Lucía",  "Castro Mendoza",    "2021100124"),
        ("Pedro",  "Gómez Salas",       "2021100125"),
        ("Rosa",   "Flores Núñez",      "2020100090"),
    ]
    usuarios = {}
    for nom, ape, cod in estudiantes_data:
        pwd = _password(nom, ape, cod)
        u = Usuario(
            username=cod,                           # login = código matrícula
            nombres=nom, apellidos=ape,
            rol=ROL_ESTUDIANTE, codigo=cod, especialidad=ESP,
        )
        u.set_password(pwd)
        db.session.add(u)
        usuarios[cod] = u
        print(f"  [EST] {cod} / {pwd}")

    # ------------------------------------------------------------------
    # Docentes
    # username  = d-{nombre}{apellidoPaterno}{seq:03d}  (todo normalizado)
    # password  = fórmula
    # ------------------------------------------------------------------
    docentes_data = [
        ("María",  "López Ríos",        "D-001", "jsuasnabar_ref"),   # seq 001
        ("Jaime",  "Suasnábar Terrel",  "D-002", None),               # seq 002
    ]
    docente_keys = []
    for seq, (nom, ape, cod, _) in enumerate(docentes_data, start=1):
        primer_nombre_norm = _normalizar(nom)
        apellido_pat_norm  = _normalizar(ape.split()[0])
        username = f"d-{primer_nombre_norm}{apellido_pat_norm}{seq:03d}"
        pwd = _password(nom, ape, cod)
        u = Usuario(
            username=username,
            nombres=nom, apellidos=ape,
            rol=ROL_DOCENTE, codigo=cod, especialidad=ESP,
        )
        u.set_password(pwd)
        db.session.add(u)
        usuarios[username] = u
        docente_keys.append(username)
        print(f"  [DOC] {username} / {pwd}")

    # ------------------------------------------------------------------
    # Admin y Dirección
    # username  = a-001 / dir-001  (coincide con su código en minúsculas)
    # password  = fórmula
    # ------------------------------------------------------------------
    staff_data = [
        ("Carlos", "Ramírez Soto", ROL_ADMIN,     "A-001",   "a-001"),
        ("Ana",    "Torres Vega",  ROL_DIRECCION, "DIR-001", "dir-001"),
    ]
    for nom, ape, rol, cod, uname in staff_data:
        pwd = _password(nom, ape, cod)
        u = Usuario(
            username=uname,
            nombres=nom, apellidos=ape,
            rol=rol, codigo=cod, especialidad=ESP,
        )
        u.set_password(pwd)
        db.session.add(u)
        usuarios[uname] = u
        print(f"  [ADM] {uname} / {pwd}")

    db.session.flush()

    # ------------------------------------------------------------------
    # Cursos
    # ------------------------------------------------------------------
    doc1_key = docente_keys[0]   # d-marialopez001
    doc2_key = docente_keys[1]   # d-jaimesuasnabar002
    cursos_data = [
        ("SI-501", "Desarrollo de Aplicaciones Web", 4, 9, doc2_key, "Lun 08-11"),
        ("SI-502", "Inteligencia Artificial",        4, 9, doc1_key, "Mar 08-11"),
        ("SI-503", "Gestión de Proyectos TI",        3, 9, doc1_key, "Mie 16-18"),
        ("SI-401", "Base de Datos II",               4, 7, doc2_key, "Jue 08-11"),
        ("SI-402", "Redes de Computadoras",          3, 7, doc1_key, "Vie 14-16"),
    ]
    cursos = {}
    for cod, nom, cred, ciclo, doc_key, hor in cursos_data:
        c = Curso(
            codigo=cod, nombre=nom, creditos=cred, ciclo=ciclo,
            especialidad=ESP, docente_id=usuarios[doc_key].id, horario=hor,
        )
        db.session.add(c)
        cursos[cod] = c
    db.session.flush()

    # ------------------------------------------------------------------
    # Matrícula de ejemplo (estudiante 2021100123 - Juan Pérez)
    # ------------------------------------------------------------------
    est_juan = usuarios["2021100123"]
    mat = Matricula(
        estudiante_id=est_juan.id, periodo="2026-I",
        estado=VALIDADA, pago_registrado=True, monto=350.0,
    )
    db.session.add(mat)
    db.session.flush()
    for cod in ("SI-501", "SI-502", "SI-503"):
        db.session.add(MatriculaDetalle(matricula_id=mat.id, curso_id=cursos[cod].id))

    # ------------------------------------------------------------------
    # Notas de ejemplo (validadas)
    # ------------------------------------------------------------------
    notas_data = [
        ("2021100123", "SI-501", 15, 16, 17),
        ("2021100123", "SI-502", 13, 14, 12),
        ("2021100123", "SI-503", 18, 17, 19),
        ("2021100124", "SI-501", 11, 10,  9),
        ("2021100125", "SI-502", 16, 15, 14),
    ]
    for est_key, cod, p1, p2, fin in notas_data:
        n = Nota(
            estudiante_id=usuarios[est_key].id, curso_id=cursos[cod].id,
            periodo="2026-I", parcial1=p1, parcial2=p2, final=fin, validada=True,
        )
        n.calcular_promedio()
        db.session.add(n)

    db.session.commit()
    print(">> Seed completado: usuarios, cursos, matrícula y notas de ejemplo.")

