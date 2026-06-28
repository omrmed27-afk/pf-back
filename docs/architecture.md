# Arquitectura del Proyecto — MVP

> API REST para restaurante oriental con delivery.
> Stack: Django 6 + Django REST Framework 3.17

---

## Principios del MVP

- Una sola aplicación Django (monolítico) — sin microservicios
- Un endpoint por recurso, CRUD completo
- Autenticación por Token (DRF built-in)
- SQLite en desarrollo, PostgreSQL en producción
- Sin lógica de negocio en las vistas — todo en los modelos o serializers

---

## Estructura de carpetas

```
pf-back/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          ← configuración común
│   │   ├── development.py   ← SQLite, DEBUG=True
│   │   └── production.py    ← PostgreSQL, DEBUG=False
│   ├── urls.py              ← URL raíz, monta /api/v1/
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                    ← todas las apps del proyecto aquí
│   ├── warehouses/
│   ├── customers/
│   ├── suppliers/
│   ├── products/
│   ├── transport/
│   ├── drivers/
│   ├── routes/
│   └── shipments/
│
├── docs/
│   ├── database-schema.md
│   └── architecture.md
│
├── manage.py
└── requirements.txt
```

---

## Patrón por módulo

Cada app sigue exactamente esta estructura interna:

```
apps/warehouses/
├── __init__.py
├── models.py        ← definición de la tabla
├── serializers.py   ← validación y transformación de datos
├── views.py         ← ViewSet (lógica de endpoints)
├── urls.py          ← rutas del módulo
└── admin.py         ← registro en el panel admin
```

### Flujo de una petición

```
Request HTTP
    └── config/urls.py
            └── apps/<modulo>/urls.py
                    └── views.py (ViewSet)
                            └── serializers.py (validar/serializar)
                                    └── models.py (base de datos)
                                            └── Response HTTP
```

---

## URLs — versionado de API

Todas las rutas van bajo el prefijo `/api/v1/`:

| Módulo | Endpoint base |
|--------|--------------|
| warehouses | `/api/v1/warehouses/` |
| customers | `/api/v1/customers/` |
| suppliers | `/api/v1/suppliers/` |
| products | `/api/v1/products/` |
| transport | `/api/v1/transport/` |
| drivers | `/api/v1/drivers/` |
| routes | `/api/v1/routes/` |
| shipments | `/api/v1/shipments/` |

Cada endpoint genera automáticamente con DRF Router:

| Método | URL | Acción |
|--------|-----|--------|
| GET | `/api/v1/warehouses/` | listar todos |
| POST | `/api/v1/warehouses/` | crear uno |
| GET | `/api/v1/warehouses/{id}/` | obtener uno |
| PUT | `/api/v1/warehouses/{id}/` | actualizar completo |
| PATCH | `/api/v1/warehouses/{id}/` | actualizar parcial |
| DELETE | `/api/v1/warehouses/{id}/` | eliminar |

---

## Autenticación

- DRF `TokenAuthentication` — el cliente envía `Authorization: Token <token>` en cada request
- Login genera el token: `POST /api/v1/auth/login/`
- Solo `drivers` tienen usuario en el sistema (`auth_user`). Clientes y suppliers no se autentican.

---

## Orden de desarrollo (dependencias del schema)

El orden importa porque algunas tablas dependen de otras:

```
Fase 1 — sin dependencias
  ├── warehouses
  ├── suppliers
  └── customers

Fase 2 — dependen de Fase 1
  ├── products       (→ suppliers)
  ├── transport      (sin deps, pero agrupa con esta fase)
  ├── drivers        (→ auth_user)
  └── routes         (→ warehouses)

Fase 3 — depende de todo
  └── shipments      (→ customers, warehouses, drivers, transport, routes, products)
```

---

## Configuración de settings (split)

`config/settings/base.py` contiene todo lo común.
`development.py` y `production.py` importan base y sobreescriben solo lo necesario:

```python
# development.py
from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

```python
# production.py
from .base import *
import os

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        ...
    }
}
```

La variable de entorno `DJANGO_SETTINGS_MODULE` determina cuál se usa.

---

## Decisiones de diseño para el MVP

| Decisión | Elección | Por qué |
|----------|----------|---------|
| Vistas | `ModelViewSet` | genera los 6 endpoints CRUD automáticamente |
| Rutas | `DefaultRouter` de DRF | registra todas las URLs con una sola línea |
| Auth | `TokenAuthentication` | simple, sin JWT, suficiente para MVP |
| Paginación | `PageNumberPagination` (10 items) | evita respuestas gigantes |
| Settings | split base/dev/prod | permite desplegar sin cambiar código |
| Apps | dentro de `apps/` | orden y separación desde el inicio |
