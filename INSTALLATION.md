# 🚀 Guía de Instalación y Configuración

## Problema: Variables Sensibles en Git

### ¿Por qué no incluir `.env` en el repositorio?

El archivo `.env` contiene **información sensible** como:
- Claves secretas
- Credenciales de bases de datos
- Tokens de API
- URLs internas

Si `.env` está en Git, cualquier persona con acceso al repositorio podría ver esta información.

### Solución Implementada ✅

1. **`.env` está en `.gitignore`** → No se sube a GitHub
2. **`.env.example` SÍ está en el repositorio** → Muestra la estructura necesaria
3. **Scripts de setup automático** → Copian `.env.example` a `.env` automáticamente

## 📋 Instalación Paso a Paso

### Opción 1: Script Automático (Recomendado)

#### En Windows:
```bash
setup.bat
```

#### En macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

El script:
- ✅ Verifica Python y Node.js
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Copia `.env.example` a `.env`

### Opción 2: Manual

#### Backend

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

# Copiar configuración
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Editar .env si es necesario (en desarrollo, generalmente no)
# Luego ejecutar:
python app.py
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Copiar configuración
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Ejecutar desarrollo
npm run dev
```

## ⚙️ Configuración de Variables de Entorno

### Backend: `backend/.env`

```env
# En desarrollo, esto suele funcionar así:
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

**Notas importantes:**
- En **desarrollo local**, `.env` puede ser simple
- En **producción**, cambiar `SECRET_KEY` a algo seguro
- `CORS_ORIGINS` contiene dónde puede conectar el frontend

### Frontend: `frontend/.env`

```env
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
VITE_MAX_RETRY_ATTEMPTS=3
```

**Cómo funciona:**
- `VITE_API_URL`: Dónde busca el frontend el backend
- Los `VITE_` prefijos son requeridos por Vite para exponerlos

## 🔄 Flujo de Desarrollo

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate      # macOS/Linux
# o: venv\Scripts\activate    # Windows
python app.py
```

Verás:
```
╔═══════════════════════════════════════════╗
║  Sistema Académico API
║  v1.0.0 - DEVELOPMENT
║  Puerto: 5000
╚═══════════════════════════════════════════╝
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Verás:
```
VITE v8.1.1  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Abre: **http://localhost:5173/**

## ✅ Verificación de Conexión

### 1. Health Check Manual

```bash
curl http://localhost:5000/api/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "message": "Backend Flask para el Sistema Académico está activo y funcionando.",
  "environment": "development",
  "version": "1.0.0"
}
```

### 2. En el Frontend

Si ves en la página:
- ✅ "Servidor Backend Flask: Conectado online (Puerto 5000)"
- ✅ Las estadísticas se cargan
- ✅ Los módulos aparecen

Entonces **todo está funcionando correctamente** ✨

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
# Asegúrate de que el entorno virtual esté activado
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Luego instala las dependencias
pip install -r requirements.txt
```

### "Port 5000 is already in use"

**Solución:**
```bash
# Cambiar puerto en backend/.env
PORT=5001

# O matar el proceso (en terminal diferente):
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Frontend no se conecta con backend

**Verificar:**
1. Backend está ejecutándose en puerto 5000: `http://localhost:5000/api/health`
2. Frontend tiene correcta la URL: Verifica `VITE_API_URL` en `frontend/.env`
3. CORS configurado: En `backend/.env` verificar `CORS_ORIGINS`

### "npm: command not found"

**Solución:**
- Instalar Node.js desde https://nodejs.org
- Reiniciar terminal después de instalar

## 📦 Agregando Paquetes

### Backend

```bash
cd backend
source venv/bin/activate    # o: venv\Scripts\activate
pip install nombre-paquete
pip freeze > requirements.txt
```

**Importante:** Siempre actualizar `requirements.txt` después de instalar

### Frontend

```bash
cd frontend
npm install nombre-paquete
```

**Nota:** npm automáticamente actualiza `package.json`

## 🔐 Producción

### Preparación para Deploy

#### Backend

```bash
# Cambiar variables en .env (NO en código):
FLASK_ENV=production
SECRET_KEY=<generar-clave-segura>
DEBUG=False  # Asegurar en app.py

# Usar servidor WSGI:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Frontend

```bash
# Compilar
npm run build

# Esto genera carpeta dist/
# Subir dist/ a tu hosting (Vercel, Netlify, etc.)
```

## 📝 Resumen de Archivos Importantes

| Archivo | Propósito | En Git? |
|---------|----------|--------|
| `.env.example` | Plantilla de configuración | ✅ Sí |
| `.env` | Configuración local (sensible) | ❌ No |
| `.gitignore` | Define qué ignorar | ✅ Sí |
| `config.py` (backend) | Configuración centralizada | ✅ Sí |
| `config.js` (frontend) | Configuración centralizada | ✅ Sí |
| `requirements.txt` | Dependencias Python | ✅ Sí |
| `package.json` | Dependencias Node | ✅ Sí |

## 🎯 Checklist de Setup

- [ ] Repositorio clonado
- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado
- [ ] Backend: Entorno virtual creado
- [ ] Backend: `pip install -r requirements.txt` ejecutado
- [ ] Backend: `.env` creado desde `.env.example`
- [ ] Frontend: `npm install` ejecutado
- [ ] Frontend: `.env` creado desde `.env.example`
- [ ] Backend ejecutándose en puerto 5000
- [ ] Frontend ejecutándose en puerto 5173
- [ ] Página carga correctamente
- [ ] Backend y frontend conectados (ves datos en tabla)

¡Si todo está marcado, ¡estás listo! 🎉
