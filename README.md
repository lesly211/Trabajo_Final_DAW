# Sistema Académico Integral 🎓

Plataforma modular de gestión académica construida con **React + Vite** (frontend) y **Flask** (backend).

## 📁 Estructura del Proyecto

```
sistema-academico/
├── frontend/                # React + Vite
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── .env                 # NO EN GIT
│
├── backend/                 # Flask + Python
│   ├── app.py              # Aplicación principal
│   ├── config.py           # Configuración
│   ├── requirements.txt     # Dependencias
│   ├── .env.example
│   └── .env                # NO EN GIT
│
├── database/               # Scripts SQL (PENDIENTE BD)
│   ├── README.md
│   └── schema.sql         # [PRÓXIMO]
│
├── docs/                   # Documentación visual
│   └── README.md
│
├── README.md              # Este archivo
└── .gitignore
```

## 🚀 Inicio Rápido

### 1. Clonar y Preparar

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

### 2. Backend

```bash
cd backend
python app.py
```

Servidor en: `http://localhost:5000`

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Aplicación en: `http://localhost:5173`

## 📋 Funcionalidades

- 📝 **Matrícula** - Gestión de inscripciones
- 📚 **Cursos** - Administración de asignaturas
- 📊 **Notas** - Control de calificaciones
- 📈 **Récords** - Historial académico
- 📄 **Documentos** - Certificados y trámites
- 🔒 **Seguridad** - Usuarios y roles

## 🔌 API Endpoints

```
GET  /api/health       → Estado del servidor
GET  /api/stats        → Estadísticas del sistema
GET  /api/modules      → Módulos disponibles
```

## 🛠️ Stack

| Componente | Tecnología |
|-----------|-----------|
| Frontend | React 19.2.7 + Vite 8.1.1 |
| Backend | Flask 3.0.3 + Flask-CORS |
| Lenguajes | Python, JavaScript |
| BD | [PENDIENTE] |

## 📝 Variables de Entorno

### Backend (`backend/.env`)
```env
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key
CORS_ORIGINS=http://localhost:5173
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:5000
```

Ver archivos `.env.example` para referencia completa.

## 📖 Documentación

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guía de desarrollo y endpoints
- **[database/README.md](database/README.md)** - Info sobre BD (pendiente)
- **[docs/README.md](docs/README.md)** - Capturas y documentación visual

## ⚠️ Importante

- **No subir `.env` a Git** ✅ Ya está en `.gitignore`
- Usar `.env.example` como plantilla
- En producción, cambiar `SECRET_KEY`

## 🤝 Desarrollo

Cada módulo se desarrolla de forma independiente:

**Backend**: Agregar rutas en `backend/app.py` o crear módulos en `backend/modules/`

**Frontend**: Componentes en `frontend/src/components/`

Ver **[DEVELOPMENT.md](DEVELOPMENT.md)** para detalles.

## ⏳ Pendiente

- [ ] Seleccionar y configurar base de datos
- [ ] Autenticación de usuarios
- [ ] Panel de administración
- [ ] Tests unitarios
- [ ] Deployment

## 📄 Licencia

Trabajo Final DAW - UNCP 2026
