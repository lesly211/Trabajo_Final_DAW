# Guía de Desarrollo

Esta guía proporciona instrucciones para configurar y ejecutar el Sistema Académico en modo desarrollo.

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- Node.js 16+
- npm 8+

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate
# Activar entorno (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Copiar variables de entorno
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Ejecutar en modo desarrollo
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## 📝 Estructura del Código

### Backend (Flask)
- `app.py` - Aplicación principal y rutas
- `requirements.txt` - Dependencias Python

### Frontend (React + Vite)
- `src/App.jsx` - Componente principal
- `src/App.css` - Estilos
- `src/main.jsx` - Punto de entrada
- `vite.config.js` - Configuración de Vite

## 🔌 API Endpoints

### Salud del Sistema
```bash
GET /api/health
```

Respuesta:
```json
{
  "status": "healthy",
  "message": "Backend Flask para el Sistema Académico está activo y funcionando."
}
```

### Estadísticas
```bash
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
```bash
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

## 🔍 Debugging

### Backend
- Activar modo debug: Establecer `FLASK_ENV=development` en `.env`
- Ver logs: Los logs se mostrarán en la consola del servidor
- Error handling: Los errores se devuelven en formato JSON

### Frontend
- Abrir Developer Tools: F12 o Ctrl+Shift+I
- React DevTools: Extensión de navegador recomendada
- Consola: Busca mensajes de error y warnings

## 📦 Agregar Nuevas Dependencias

### Backend
```bash
pip install nombre-paquete
pip freeze > requirements.txt
```

### Frontend
```bash
npm install nombre-paquete
```

## ✅ Testing

### Backend
```bash
# Si se agrega pytest
pytest
```

### Frontend
```bash
# Si se agrega vitest
npm run test
```

## 🎨 Estilos y Convenciones

- Usar ESLint para JavaScript: `npm run lint`
- Mantener consistencia en la nomenclatura
- Documentar funciones complejas
- Commits descriptivos

## 📤 Antes de Hacer Push

1. Asegúrese de que ambos servidores funcionan correctamente
2. Verifique que no hay errores en la consola
3. Actualice las dependencias: `pip freeze > requirements.txt`
4. Commit de los cambios con mensajes descriptivos
5. Push a la rama

## 🆘 Solución de Problemas

### El frontend no se conecta al backend
- Verificar que el backend está ejecutándose en `http://localhost:5000`
- Verificar la variable de entorno `VITE_API_URL` en frontend/.env
- Revisar la consola del navegador para errores de CORS

### Error de puerto en uso
- Cambiar el puerto en backend/.env: `PORT=5001`
- Backend: `python app.py`
- Frontend: `npm run dev -- --port 5174`

### Módulos no encontrados
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

## 📚 Recursos Útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/)
