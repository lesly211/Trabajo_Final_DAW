# Sistema Académico Integral — UNCP / FIS

Sistema académico modular para la gestión de procesos de facultades y especialidades.
Frontend en **React + Vite**, backend en **Python Flask** con **JWT** y roles diferenciados.

> Evaluación Final — Desarrollo de Aplicaciones Web (Semestre IX)
> Dr. Jaime Suasnábar Terrel — Universidad Nacional del Centro del Perú

# INTEGRANTES
BARJA ORTIZ, Erick Gerson
ESPÍRITU DIAZ, Olayne Guadalupe María Isabel
NAVARRO SERVA, Lesly Brenda

---

## Tabla de Contenidos
- [Arquitectura](#arquitectura)
- [Módulos](#módulos)
- [Roles](#roles)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura de Carpetas](#estructura-de-carpetas)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Usuarios de Prueba](#usuarios-de-prueba)
- [API REST](#api-rest)
- [Capturas](#capturas)

---

## Arquitectura

Aplicación cliente–servidor desacoplada:

```
┌─────────────────────┐         HTTP/JSON (JWT)        ┌──────────────────────┐
│   FRONTEND           │  ─────────────────────────▶   │   BACKEND            │
│   React + Vite       │                                │   Flask (REST API)   │
│   - Router por rol   │  ◀─────────────────────────   │   - Blueprints       │
│   - Context (Auth)   │                                │   - Services         │
│   - Axios interceptor│                                │   - SQLAlchemy ORM   │
└─────────────────────┘                                │   - SQLite           │
                                                        └──────────────────────┘
```

**Patrón backend:** Capas (Routes → Services → Models). Las rutas (Blueprints) solo
orquestan HTTP; la lógica de negocio vive en `services/`; la persistencia en `models/`.

**Patrón frontend:** Componentes + Context API para autenticación, rutas protegidas
por rol, y una capa `api/` que centraliza las llamadas HTTP.

---

## Módulos

| # | Módulo | Funcionalidad principal |
|---|--------|--------------------------|
| 1 | **Matrícula** | Estudiante solicita y descarga ficha; Admin valida/registra pagos y genera ficha oficial; Dirección ve estadísticas. |
| 2 | **Cursos y Docentes** | Docente ve cursos y carga sílabos; Admin asigna docentes y horarios; Dirección evalúa carga docente. |
| 3 | **Notas** | Docente registra notas parciales/finales; Estudiante consulta hoja de notas; Admin valida actas; Dirección supervisa indicadores. |
| 4 | **Record Académico** | Estudiante ve su historial; Admin genera reportes; Dirección analiza desempeño por cohorte. |
| 5 | **Certificados y Documentos** | Estudiante solicita en línea; Admin emite con código QR; Dirección autoriza. |
| 6 | **Administración y Seguridad** | Admin define roles/usuarios; Dirección ve auditoría y reportes estratégicos. |

---

## Roles

- **Estudiante** — matrícula, notas, record, certificados.
- **Docente** — cursos asignados, sílabos, registro de notas.
- **Administrador** — validaciones, emisión, gestión de usuarios.
- **Dirección** — estadísticas, indicadores, auditoría.

---

## Stack Tecnológico

**Frontend:** React 18, Vite 5, React Router 6, Axios, CSS modular.
**Backend:** Python 3.11+, Flask 3, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS, SQLite.

---

## Estructura de Carpetas

```
sistema-academico/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Application factory
│   │   ├── config.py            # Configuración por entorno
│   │   ├── extensions.py        # db, jwt, cors
│   │   ├── models/              # Modelos SQLAlchemy
│   │   ├── routes/              # Blueprints (1 por módulo)
│   │   ├── services/            # Lógica de negocio
│   │   ├── utils/               # Decoradores, helpers (roles, QR)
│   │   └── seeds/               # Datos iniciales
│   ├── requirements.txt
│   └── run.py                   # Punto de entrada
└── frontend/
    ├── src/
    │   ├── api/                 # Capa de acceso a API
    │   ├── components/          # UI reutilizable
    │   ├── context/             # AuthContext
    │   ├── layouts/             # Layout con sidebar por rol
    │   ├── pages/               # Vistas por módulo
    │   ├── routes/              # Rutas protegidas
    │   └── styles/              # CSS global
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## Instalación y Ejecución

### Backend
```bash
cd backend
python -m venv venv
pip install -r requirements.txt
python run.py        
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Credenciales Institucionales

### Estudiantes — ingresan con su **código de matrícula**

| Código (login) | Contraseña | Nombre |
|---|---|---|
| `2021100123` | `JPerez2021*` | Juan Pérez Quispe |
| `2021100124` | `LCastro2021*` | Lucía Castro Mendoza |
| `2021100125` | `PGomez2021*` | Pedro Gómez Salas |
| `2020100090` | `RFlores2020*` | Rosa Flores Núñez |

### Docentes — ingresan con **d-nombre+apellido+secuencia**

| Usuario (login) | Contraseña | Nombre |
|---|---|---|
| `d-marialopez001` | `MLopez0001*` | María López Ríos |
| `d-jaimesuasnabar002` | `JSuasnabar0002*` | Jaime Suasnábar Terrel |

### Administración — ingresan con su **código institucional**

| Usuario (login) | Contraseña | Rol |
|---|---|---|
| `a-001` | `CRamirez0001*` | Administrador |
| `dir-001` | `ATorres0001*` | Dirección |


---

## Guía rápida de pruebas por rol

Recomendado probar en este orden, ya que algunos pasos dependen del anterior
(p. ej. no se puede emitir un certificado sin que Dirección lo autorice antes).

**1) Estudiante** (`2021100123` / `JPerez2021*` — Juan Pérez Quispe)
- Entrar a **Matrícula** → ya tiene una matrícula validada del periodo 2026-I
  (no podrá solicitar otra para ese mismo periodo, es una regla de negocio).
- Descargar la ficha de matrícula en PDF.
- Ver **Mis Notas** y **Record Académico** (promedio ponderado, créditos).
- Ir a **Certificados** → solicitar uno nuevo (queda en estado "solicitado").

**2) Dirección** (`dir-001` / `ATorres0001*` — Ana Torres Vega)
- **Inicio**: ver KPIs de matrícula e indicadores académicos.
- **Certificados**: autorizar el certificado que solicitó el estudiante en el
  paso anterior.
- **Carga Docente** y **Auditoría**: revisar que aparezcan los registros de
  las acciones anteriores.

**3) Administrador** (`a-001` / `CRamirez0001*` — Carlos Ramírez Soto)
- **Certificados**: emitir el certificado ya autorizado (elegir método: QR,
  firma digital o ambos) y descargar el PDF generado.
- **Matrículas**: validar/rechazar solicitudes pendientes (por ejemplo, las
  de `2021100124` — Lucía Castro, o `2021100125` — Pedro Gómez).
- **Cursos y Docentes**: asignar un docente/horario a un curso.
- **Actas** (Notas): consolidar (validar en bloque) las notas de un curso.
- **Usuarios**: crear un usuario nuevo y desactivar uno existente.

**4) Docente** (`d-marialopez001` / `MLopez0001*`, o `d-jaimesuasnabar002` / `JSuasnabar0002*`)
- **Mis Cursos**: cargar el sílabo de un curso asignado.
- **Registro de Notas**: elegir un curso propio, seleccionar un estudiante
  (solo aparecen los matriculados y validados) y registrar parciales/final.
  Intentar registrar sin seleccionar curso/estudiante debe mostrar un aviso,
  no un error de servidor.

**5) Verificación pública (sin iniciar sesión)**
- Abrir en una pestaña nueva `http://localhost:5173/verificar/<código>` con
  el código de verificación del certificado emitido en el paso 3. Debe
  confirmar autenticidad sin pedir login.

Si en cualquier paso aparece un error, revisen la consola del backend
(terminal donde corre `python run.py`) y la consola del navegador (F12):
casi siempre el mensaje de error del backend ya indica la causa exacta
(por ejemplo, "no tiene una matrícula validada en este curso").

---

## API REST

Base: `http://localhost:5000/api`

| Método | Endpoint | Rol | Descripción |
|--------|----------|-----|-------------|
| POST | `/auth/login` | público | Inicia sesión, devuelve JWT |
| GET | `/auth/me` | autenticado | Perfil actual |
| GET/POST | `/matricula` | estudiante/admin/dirección | Listar / solicitar matrícula |
| PATCH | `/matricula/:id/validar` | admin | Valida requisitos y registra pago |
| GET | `/matricula/:id/ficha` | dueño/admin/dirección | Descarga la ficha oficial en PDF (requiere matrícula validada) |
| GET | `/matricula/estadisticas` | dirección/admin | Estadísticas |
| GET | `/cursos` | todos | Listar cursos |
| GET | `/cursos/docentes` | admin/dirección | Listar docentes activos |
| POST | `/cursos/:id/silabo` | docente | Cargar sílabo |
| PATCH | `/cursos/:id/asignar` | admin | Asignar docente/horario |
| GET | `/cursos/carga-docente` | dirección/admin | Carga docente por profesor |
| GET/POST | `/notas` | todos (filtrado por rol) | Registrar / consultar notas |
| GET | `/notas/estudiantes-curso/:curso_id` | docente | Estudiantes matriculados en el curso |
| PATCH | `/notas/:id/validar` | admin | Validar acta individual |
| GET | `/notas/consolidado` | admin/dirección | Vista agrupada por curso+periodo |
| PATCH | `/notas/consolidar` | admin | Valida en bloque todas las notas de un curso+periodo |
| GET | `/notas/indicadores` | dirección/admin | Indicadores académicos |
| GET | `/record/:estudiante_id` | dueño/admin/dirección | Historial académico |
| GET | `/record/reportes/consolidado` | admin/dirección | Reportes consolidados |
| GET/POST | `/certificados` | estudiante/admin/dirección | Solicitar / listar |
| PATCH | `/certificados/:id/autorizar` | dirección | Autoriza la emisión |
| PATCH | `/certificados/:id/emitir` | admin | Emite con QR y/o firma digital (requiere autorización previa) |
| GET | `/certificados/:id/pdf` | dueño/admin/dirección | Descarga el documento oficial en PDF |
| GET | `/certificados/verificar/:codigo` | público | Verificación sin sesión (destino del QR) |
| GET/POST | `/usuarios` | admin/dirección (lectura) | Gestión de usuarios |
| PATCH | `/usuarios/:id` | admin | Actualizar/activar usuario |
| GET | `/seguridad/auditoria` | dirección/admin | Log de auditoría |

Todas las rutas (salvo login y verificación de certificados) requieren header
`Authorization: Bearer <token>`.

### Reglas de negocio validadas en el backend

- **Matrícula**: no se permite una segunda solicitud (pendiente o validada) del
  mismo estudiante para el mismo periodo; los cursos seleccionados deben existir;
  el total de créditos no puede superar el máximo permitido por periodo
  (`MAX_CREDITOS_POR_PERIODO = 24`, configurable en `matricula_routes.py`).
- **Notas**: un docente solo puede registrar notas a estudiantes que tengan una
  matrícula **validada** que incluya ese curso en el periodo indicado.
- **Certificados**: un certificado solo puede emitirse (Admin) después de haber
  sido autorizado por Dirección; solo puede descargarse en PDF una vez emitido.

---

## Capturas

Las capturas de pantalla de las funcionalidades principales se incluyen en la
carpeta `/docs/capturas` y en la presentación final.
