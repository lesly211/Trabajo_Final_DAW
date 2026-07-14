# Referencia rápida de la API

Base URL: `http://localhost:5000/api`
Autenticación: JWT Bearer en header `Authorization: Bearer <token>`.

## Auth
- `POST /auth/login` — `{username, password}` → `{token, usuario}`
- `GET /auth/me` — perfil actual

## Matrícula (Módulo 1)
- `GET /matricula` — lista (estudiante: solo suyas)
- `POST /matricula` — `{periodo, cursos:[id]}` (estudiante)
- `PATCH /matricula/:id/validar` — `{aprobar, pago, monto}` (admin)
- `GET /matricula/estadisticas` — (dirección/admin)

## Cursos (Módulo 2)
- `GET /cursos?mios=1` — lista (docente: solo asignados)
- `GET /cursos/docentes` — (admin/dirección)
- `POST /cursos/:id/silabo` — `{silabo_url}` (docente)
- `PATCH /cursos/:id/asignar` — `{docente_id, horario}` (admin)
- `GET /cursos/carga-docente` — (dirección/admin)

## Notas (Módulo 3)
- `GET /notas?curso_id=&periodo=` — lista filtrada por rol
- `POST /notas` — `{curso_id, estudiante_id, parcial1, parcial2, final}` (docente)
- `GET /notas/estudiantes-curso/:curso_id` — estudiantes matriculados y validados en el curso (docente, para el selector de registro)
- `PATCH /notas/:id/validar` — valida un acta individual (admin)
- `GET /notas/consolidado` — vista agrupada por curso+periodo con total/validadas/pendientes (admin/dirección)
- `PATCH /notas/consolidar` — `{curso_id, periodo}` valida en bloque todas las notas de un curso+periodo (admin)
- `GET /notas/indicadores` — (dirección/admin)

## Record (Módulo 4)
- `GET /record/:estudiante_id` — historial + resumen
- `GET /record/reportes/consolidado` — (admin/dirección)

## Certificados (Módulo 5)
- `GET /certificados`
- `POST /certificados` — `{tipo}` (estudiante)
- `PATCH /certificados/:id/autorizar` — (dirección)
- `PATCH /certificados/:id/emitir` — `{metodo: "qr"|"firma_digital"|"ambos"}` (admin, requiere autorización previa). Genera código de verificación y, según el método, QR y/o firma digital HMAC-SHA256.
- `GET /certificados/:id/pdf` — descarga el documento oficial en PDF con el QR embebido (estudiante dueño, admin o dirección; requiere que ya esté emitido)
- `GET /certificados/verificar/:codigo` — **pública, sin token**. Es el destino del QR impreso en el documento; confirma autenticidad e integridad de la firma sin necesidad de iniciar sesión

## Seguridad (Módulo 6)
- `GET /usuarios?rol=` — (admin/dirección)
- `POST /usuarios` — crear (admin)
- `PATCH /usuarios/:id` — actualizar/activar (admin)
- `GET /seguridad/auditoria` — log (dirección/admin)
