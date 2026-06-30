# 📝 Guía de Desarrollo

Guía para desarrolladores trabajando en el Sistema Académico.

## 🚀 Setup Inicial

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Ejecutar servidor
python app.py
```

El servidor estará en `http://localhost:5000`

### 2. Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Ejecutar en desarrollo
npm run dev
```

La aplicación estará en `http://localhost:5173`

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

Respuesta:
```json
{
  "status": "healthy",
  "message": "Backend Flask para el Sistema Académico está activo y funcionando.",
  "environment": "development",
  "version": "1.0.0"
}
```

### Estadísticas
```
GET /api/stats
```

Respuesta:
```json
{
  "students_count": 1250,
  "teachers_count": 85,
  "courses_count": 42,
  "faculties_count": 4
}
```

### Módulos
```
GET /api/modules
```

Respuesta:
```json
[
  {
    "id": "matricula",
    "name": "Matrícula",
    "description": "Gestión de inscripciones y matrículas de estudiantes."
  },
  ...
]
```

## 🔧 Estructura de Configuración

### Backend: `config.py`

Configuración centralizada por ambiente:
- **DevelopmentConfig** - Modo desarrollo (debug=true)
- **ProductionConfig** - Modo producción (debug=false)
- **TestingConfig** - Modo testing

Se activa automáticamente según `FLASK_ENV` en `.env`.

### Frontend: `src/config.js`

Centraliza:
- URLs de API
- Endpoints
- Feature flags
- Timeouts y reintentos
- Utilidad de logging

## 📦 Agregar Dependencias

### Backend

```bash
cd backend
source venv/bin/activate  # Activar entorno
pip install nombre-paquete
pip freeze > requirements.txt  # IMPORTANTE: Actualizar archivo
```

### Frontend

```bash
cd frontend
npm install nombre-paquete
# Automáticamente se actualiza package.json
```

## 🔌 Agregar Nuevos Endpoints

### Backend: `backend/app.py`

```python
@app.route('/api/nuevo-endpoint', methods=['GET', 'POST'])
def nuevo_endpoint():
    """Descripción del endpoint"""
    return jsonify({
        "datos": "respuesta"
    }), 200
```

### Frontend: Consumir en `src/App.jsx`

```javascript
import { getApiUrl } from './config'

const response = await fetch(getApiUrl('/api/nuevo-endpoint'))
const data = await response.json()
```

## 🎨 Variables de Entorno

### Backend (`.env`)

```env
FLASK_ENV=development           # development|production
PORT=5000                       # Puerto del servidor
SECRET_KEY=dev-secret-key       # Cambiar en producción
CORS_ORIGINS=http://localhost:5173  # Orígenes permitidos
DATABASE_URL=sqlite:///app.db   # [PENDIENTE] Cuando se elija BD
```

### Frontend (`.env`)

```env
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
VITE_MAX_RETRY_ATTEMPTS=3
```

## 🐛 Debug

### Backend

```python
# En backend/app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Los cambios se recargan automáticamente.

### Frontend

1. Abrir DevTools: `F12` o `Ctrl+Shift+I`
2. Ver logs en consola
3. Usar React DevTools (extensión de navegador)

## 📊 Scripts Disponibles

### Backend
```bash
python app.py              # Ejecutar servidor
```

### Frontend
```bash
npm run dev       # Desarrollo
npm run build     # Compilar para producción
npm run preview   # Ver build compilado
npm run lint      # Linter
```

## ⚠️ Troubleshooting

### Backend falla al iniciar
```bash
# Verificar que las dependencias estén instaladas
pip install -r requirements.txt

# Verificar que el entorno virtual esté activo
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Frontend no se conecta
1. Verificar que backend esté corriendo en puerto 5000
2. Verificar `VITE_API_URL` en `frontend/.env`
3. Revisar consola del navegador (F12)

### Puerto en uso
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

## 📝 Convenciones de Código

### Backend (Python)
- Usar `snake_case` para variables y funciones
- Usar `PascalCase` para clases
- Máximo 100 caracteres por línea
- Documentar con docstrings

### Frontend (JavaScript)
- Usar `camelCase` para variables
- Usar `PascalCase` para componentes React
- Nombres descriptivos (no abreviar)
- Comentar lógica compleja

## 🔐 Seguridad

**NO INCLUIR EN GIT:**
- `.env` (variables sensibles)
- `venv/` (entorno virtual)
- `node_modules/` (dependencias)
- `__pycache__/` (cache de Python)

Todos están en `.gitignore` ✅

## 📚 Próximos Pasos

- [ ] Seleccionar base de datos (PostgreSQL/MySQL/SQLite)
- [ ] Implementar autenticación/autorización
- [ ] Crear modelos de base de datos
- [ ] Agregar validaciones
- [ ] Escribir tests
- [ ] Preparar para deployment

## 🤝 Flujo de Desarrollo

1. **Crear rama**: `git checkout -b feature/nueva-funcionalidad`
2. **Desarrollar**: Backend + Frontend
3. **Probar**: Que se comuniquen correctamente
4. **Commit**: `git commit -m 'Descripción clara'`
5. **Push**: `git push origin feature/nueva-funcionalidad`

## 📖 Más Información

- Ver `README.md` para estructura del proyecto
- Ver `database/README.md` para info sobre BD
- Ver `docs/README.md` para documentación visual
