# CLAUDE.md

Este archivo provee instrucciones a Claude Code (claude.ai/code) para trabajar en este repositorio.

## Reglas del proyecto

- **Comunicación y documentación**: siempre en español (respuestas, comentarios, docstrings, archivos .md)
- **Código**: siempre en inglés (nombres de variables, funciones, clases, carpetas, tablas, columnas, rutas de URL, commits)
- **Entorno virtual**: activar siempre antes de ejecutar cualquier comando dentro del proyecto (`.\.venv\Scripts\Activate.ps1`)
- **Comandos**: Claude puede ejecutar todos los comandos del proyecto excepto `python manage.py runserver`, que siempre debe ejecutarse manualmente por el desarrollador

## Contexto del proyecto

API REST para restaurante oriental con delivery y reservas de mesa. Conecta clientes, proveedores, almacenes (locales), transportes y conductores en torno al envío/pedido como unidad central de negocio.

## Módulos implementados

| Módulo | App name | Estado |
|--------|----------|--------|
| Almacén/Local | `warehouses` | ✅ completo + tests |
| Proveedores | `suppliers` | ✅ completo + tests |
| Clientes | `customers` | ✅ completo + tests |
| Transporte | `transport` | ✅ completo + tests |
| Productos/Platos | `products` | ✅ completo + tests |
| Conductores | `drivers` | ✅ completo + tests |
| Autenticación | `authentication` | ✅ completo + tests |
| Rutas | `routes` | ✅ completo + tests |
| Mesas | `tables` | ✅ completo + tests |
| Reservas | `reservations` | ✅ completo + tests |
| Pedidos/Envíos | `shipments` | ✅ completo + tests |

## Arquitectura

> **IMPORTANTE**: Leer [`docs/architecture.md`](./docs/architecture.md) antes de cualquier tarea de desarrollo.

> **IMPORTANTE**: Leer [`docs/database-schema.md`](./docs/database-schema.md) antes de cualquier tarea de desarrollo.

### Patrón por módulo
Cada módulo tiene: `models.py` → `serializers.py` → `services.py` → `views.py` → `urls.py` → `admin.py`

### Autenticación
- `POST /api/v1/auth/login/` → `{token}`
- `POST /api/v1/auth/logout/`
- `POST /api/v1/auth/register/` → crea User + Driver en una sola llamada
- TokenAuthentication en todos los endpoints excepto GET de products (público)

### Tablas adicionales
`tables` y `reservations` (mesas y reservas del restaurante). `tables` tiene ciclo available→reserved→occupied→available con endpoint `/change-status/`.

## Stack

Python · Django 6.0.6 · Django REST Framework 3.17.1 · SQLite3 (desarrollo) · psycopg2-binary (PostgreSQL producción) · python-decouple · coverage 7.14.2

## Comandos

```bash
.\.venv\Scripts\Activate.ps1

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test

# Tests con cobertura
python -m coverage run --append manage.py test apps.<modulo>
python -m coverage report
python -m coverage html
```

## Cómo agregar una funcionalidad

1. Crear app en `apps/` con estructura completa (models, serializers, services, views, urls, admin)
2. Registrar en `INSTALLED_APPS` → `makemigrations` → `migrate`
3. Montar URLs en `config/urls.py`
4. Escribir tests en `apps/<modulo>/tests/` con carpeta y múltiples archivos
5. Verificar cobertura ≥ 80%
