# Sistema Académico Integral 🎓

Este es el proyecto base para el **Sistema Académico Integral**, estructurado con un frontend en **React + Vite** y un backend en **Python Flask**. El sistema está diseñado de manera modular y escalable para gestionar los procesos académicos de facultades, especialidades, matrícula, cursos, docentes, control de notas, récords académicos, certificados y seguridad.

---

## 📁 Estructura del Proyecto

El proyecto está dividido en dos directorios principales:

```text
Trabajo_Final_DAW/
├── frontend/             # Frontend en React + Vite
│   ├── src/              # Código fuente de React (Componentes, Vistas, CSS)
│   │   ├── App.jsx       # Componente principal con el Dashboard Académico
│   │   ├── App.css       # Estilos premium del Dashboard
│   │   └── main.jsx      # Entrada de React
│   ├── package.json      # Dependencias de npm y scripts
│   └── vite.config.js    # Configuración de Vite
│
├── backend/              # Backend en Python Flask
│   ├── venv/             # Entorno virtual de Python
│   ├── app.py            # Servidor Flask principal y endpoints de la API
│   ├── requirements.txt  # Dependencias de Python (Flask, Flask-CORS, etc.)
│   └── .env              # Configuración de variables de entorno (Puerto)
│
└── README.md             # Guía de inicio rápido (Este archivo)
```

---

## 🚀 Guía de Inicio Rápido

Para levantar los servidores y empezar a programar, sigue estos pasos:

### 1. Levantar el Backend (Python Flask)

El backend corre sobre un entorno virtual de Python ya configurado.

1. Abre una terminal y colócate en la carpeta `backend`:
   ```bash
   cd backend
   ```
2. Activa el entorno virtual:
   * **En Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **En Windows (CMD):**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   * **En macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
3. Ejecuta el servidor Flask:
   ```bash
   python app.py
   ```
   *El servidor backend se iniciará en: `http://localhost:5000`*
   *Puedes verificar la API ingresando a `http://localhost:5000/api/health` en tu navegador.*

---

### 2. Levantar el Frontend (React + Vite)

El frontend está configurado para consumir los endpoints del backend.

1. Abre una nueva terminal y colócate en la carpeta `frontend`:
   ```bash
   cd frontend
   ```
2. Ejecuta el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```
   *El servidor frontend se iniciará en: `http://localhost:5173`*

---

## 📡 Endpoints de la API Base

El backend ya cuenta con CORS habilitado para permitir peticiones desde el frontend. Los siguientes endpoints están disponibles:

* **`GET /api/health`**: Retorna el estado del servidor.
* **`GET /api/stats`**: Retorna estadísticas básicas para el Dashboard (cantidad de alumnos, profesores, etc.).
* **`GET /api/modules`**: Retorna la lista de módulos iniciales del sistema.

---

## 👥 Colaboración y Desarrollo

Cada integrante del equipo puede desarrollar su módulo de la siguiente manera:
1. **Frontend:** Crear componentes específicos dentro de `frontend/src/components/` (por ejemplo, `Matricula.jsx`, `Notas.jsx`) e importarlos en `App.jsx` o configurar rutas utilizando `react-router-dom`.
2. **Backend:** Crear nuevas rutas en `backend/app.py` o estructurar controladores en archivos separados para mantener el código limpio y modular.
