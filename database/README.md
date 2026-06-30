# Database - Scripts y Esquemas

Esta carpeta contiene toda la configuración y scripts de base de datos.

## 📁 Estructura

```
database/
├── README.md           # Este archivo
├── schema.sql          # [PENDIENTE] Esquema de base de datos
├── migrations/         # [PENDIENTE] Migraciones
└── seed_data.sql       # [PENDIENTE] Datos de prueba
```

## ⏳ Estado

**PENDIENTE**: La selección de base de datos aún no se ha definido.

Opciones en consideración:
- SQLite (desarrollo rápido)
- PostgreSQL (producción escalable)
- MySQL (alternativa)

## 📋 Cuándo se completará

Una vez se decida la BD, se añadirán:
- `schema.sql` - Esquema de tablas
- `migrations/` - Control de versiones del esquema
- `seed_data.sql` - Datos iniciales de prueba

## 🔗 Conexión Backend

El backend (`backend/config.py`) ya tiene soporte para base de datos:

```python
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
```

Cambiar en `backend/.env` cuando se decida la BD.
