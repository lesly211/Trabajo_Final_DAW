# Sistema Académico - Trabajo Final DAW

Un sistema de gestión académica moderno construido con **Flask** (backend) y **React + Vite** (frontend).

## 📋 Descripción del Proyecto

Este sistema proporciona funcionalidades completas para la gestión académica de una institución educativa, incluyendo:

- 📝 **Matrícula**: Gestión de inscripciones y matrículas de estudiantes
- 📚 **Cursos y Docentes**: Administración de asignaturas, horarios y asignación docente
- 📊 **Control de Notas**: Registro y evaluación de calificaciones académicas
- 📈 **Récord Académico**: Historial académico y seguimiento de progreso estudiantil
- 📄 **Certificados y Documentos**: Emisión de constancias, certificados y trámites documentales
- 🔒 **Administración y Seguridad**: Gestión de usuarios, roles y auditoría del sistema

## 🏗️ Estructura del Proyecto

```
Trabajo_Final_DAW/
├── backend/              # API Flask
│   ├── app.py
│   ├── requirements.txt
│   └── .env
├── frontend/             # Aplicación React + Vite
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env
└── README.md
```

## 🚀 Requisitos Previos

- **Python** 3.8 o superior
- **Node.js** 16+ y **npm**
- **Git** (para control de versiones)

## 📦 Instalación y Configuración

### Backend (Flask)

1. **Navegar al directorio backend**:
   ```bash
   cd backend
   ```

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   # Crear archivo .env basado en el ejemplo
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

5. **Ejecutar el servidor**:
   ```bash
   python app.py
   ```
   El servidor estará disponible en `http://localhost:5000`

### Frontend (React + Vite)

1. **Navegar al directorio frontend**:
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**:
   ```bash
   # Crear archivo .env basado en el ejemplo
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

4. **Ejecutar en modo desarrollo**:
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:5173`

## 🔌 Endpoints de la API

### Health Check
- **GET** `/api/health` - Verifica que el backend esté activo

### Estadísticas
- **GET** `/api/stats` - Obtiene estadísticas del sistema académico

### Módulos
- **GET** `/api/modules` - Lista los módulos disponibles del sistema

## 📝 Desarrollo

### Scripts Disponibles

**Backend**:
```bash
# Ejecutar servidor en modo debug
python app.py
```

**Frontend**:
```bash
# Modo desarrollo
npm run dev

# Compilar para producción
npm run build

# Vista previa de la compilación
npm run preview

# Ejecutar linter
npm run lint
```

## 🔐 Variables de Entorno

### Backend (`.env`)
```
FLASK_ENV=development
PORT=5000
```

### Frontend (`.env`)
```
VITE_API_URL=http://localhost:5000
```

## 📚 Tecnologías Utilizadas

### Backend
- **Flask** 3.0.3 - Framework web
- **Flask-CORS** 4.0.1 - Soporte CORS
- **python-dotenv** 1.0.1 - Gestión de variables de entorno

### Frontend
- **React** 19.2.7 - Biblioteca UI
- **Vite** 8.1.1 - Herramienta de compilación
- **CSS** - Estilos nativos

## 🤝 Contribución

Para contribuir al proyecto:

1. Crear una rama para la nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
2. Commit de los cambios: `git commit -m 'Agregar nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Abrir un Pull Request

## ⚙️ Configuración de Producción

Para desplegar en producción:

1. **Backend**:
   - Establecer `FLASK_ENV=production`
   - Configurar `debug=False` en `app.run()`
   - Usar un servidor WSGI (Gunicorn, uWSGI, etc.)

2. **Frontend**:
   - Ejecutar: `npm run build`
   - Desplegar la carpeta `dist/` generada

## 📄 Licencia

Este proyecto es propiedad de UNCP - Trabajo Final DAW.

## 👨‍💻 Autor

Desarrollado como proyecto final del curso de Desarrollo de Aplicaciones Web (DAW) - UNCP
