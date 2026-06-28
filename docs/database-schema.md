# Esquema de Base de Datos

> Contexto: API para restaurante oriental con servicio de delivery.
> Los nombres de apps/tablas son genéricos en inglés; el dominio real es gastronómico.

## Tablas de Django (reutilizadas)

### `auth_user` ← Django built-in
Usada como base para el módulo de repartidores mediante relación OneToOne.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK |
| username | varchar | único |
| email | varchar | |
| first_name | varchar | |
| last_name | varchar | |
| password | varchar | hasheado por Django |
| is_staff | boolean | acceso al admin |
| is_active | boolean | |
| date_joined | datetime | |

---

## Tablas del proyecto

### `customers`
Persona que realiza pedidos al restaurante. No tiene acceso al sistema (no usa `auth_user`).

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| name | varchar(200) | requerido |
| email | varchar(254) | único |
| phone | varchar(20) | |
| address | text | dirección de entrega habitual |
| customer_type | varchar(10) | choices: `company` / `individual` |
| tax_id | varchar(50) | nullable — RUT/CUIT/NIF según país |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `suppliers`
Empresas que proveen ingredientes y materiales al restaurante.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| name | varchar(200) | requerido |
| email | varchar(254) | |
| phone | varchar(20) | |
| address | text | |
| contact_name | varchar(100) | persona de contacto |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `warehouses`
Locales / sucursales del restaurante. Punto de origen de los pedidos.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| name | varchar(100) | nombre del local (ej: "Sucursal Centro") |
| address | text | |
| city | varchar(100) | |
| country | varchar(100) | |
| capacity | integer | capacidad de mesas o aforo del local |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `products`
Platos e ítems del menú del restaurante.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| name | varchar(200) | nombre del plato, requerido |
| description | text | nullable |
| sku | varchar(100) | único — código interno del plato |
| unit_price | decimal(10,2) | precio del plato |
| stock | integer | unidades disponibles para el día |
| supplier_id | integer | FK → `suppliers`, nullable |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `transport`
Vehículos de delivery del restaurante.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| license_plate | varchar(20) | único |
| vehicle_type | varchar(20) | choices: `motorcycle` / `van` / `bicycle` |
| brand | varchar(100) | |
| model | varchar(100) | |
| status | varchar(20) | choices: `available` / `in_use` / `maintenance` |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `drivers`
Repartidores del restaurante. Extiende `auth_user` con OneToOne.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| user_id | integer | OneToOne → `auth_user` |
| license_number | varchar(50) | único — licencia de conducir |
| phone | varchar(20) | |
| status | varchar(20) | choices: `available` / `on_route` / `off_duty` |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `routes`
Rutas de delivery asignadas a un repartidor, con origen en un local.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| name | varchar(100) | nombre descriptivo de la ruta |
| origin_warehouse_id | integer | FK → `warehouses` (local de origen) |
| created_at | datetime | auto |
| updated_at | datetime | auto |

### `route_stops`
Paradas individuales dentro de una ruta de delivery, ordenadas.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| route_id | integer | FK → `routes` |
| stop_order | integer | orden de entrega (1, 2, 3…) |
| address | text | dirección de entrega |
| city | varchar(100) | |
| estimated_arrival | time | nullable |

---

### `shipments`
Pedido del cliente. Unidad central de negocio. Incluye los platos pedidos, el local de origen, el repartidor y el costo total.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| tracking_number | varchar(20) | único, generado automáticamente |
| customer_id | integer | FK → `customers` |
| origin_warehouse_id | integer | FK → `warehouses` (local que prepara el pedido) |
| destination_address | text | dirección de entrega del pedido |
| destination_city | varchar(100) | |
| status | varchar(20) | choices: `pending` / `in_transit` / `delivered` / `cancelled` / `returned` |
| estimated_delivery_date | datetime | fecha y hora estimada de entrega |
| actual_delivery_date | datetime | nullable — se completa al entregar |
| calculated_cost | decimal(10,2) | total del pedido: costo de platos + costo de delivery |
| driver_id | integer | FK → `drivers`, nullable — asignado al despachar |
| transport_id | integer | FK → `transport`, nullable — asignado al despachar |
| route_id | integer | FK → `routes`, nullable — asignado al despachar |
| notes | text | nullable — indicaciones especiales del cliente |
| created_at | datetime | auto |
| updated_at | datetime | auto |

### `shipment_products`
Detalle del pedido: qué platos y en qué cantidad. Tabla intermedia (M2M) entre `shipments` y `products`.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| shipment_id | integer | FK → `shipments` |
| product_id | integer | FK → `products` |
| quantity | integer | cantidad de ese plato en el pedido |
| unit_price | decimal(10,2) | precio del plato al momento del pedido |

---

### `tables`
Mesas físicas de cada local. Tienen un ciclo de vida: libre → reservada → ocupada → libre.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| warehouse_id | integer | FK → `warehouses` (local donde está la mesa) |
| number | integer | número de mesa dentro del local |
| capacity | integer | cantidad máxima de personas |
| status | varchar(20) | choices: `available` / `reserved` / `occupied` |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

### `reservations`
Reserva de mesa hecha por un cliente. Se liga a una mesa específica del local.

| Columna | Tipo | Notas |
|---------|------|-------|
| id | integer | PK, auto |
| customer_id | integer | FK → `customers` |
| table_id | integer | FK → `tables` |
| date | date | fecha de la reserva |
| time | time | hora de la reserva |
| party_size | integer | cantidad de personas |
| status | varchar(20) | choices: `pending` / `confirmed` / `cancelled` |
| notes | text | nullable — pedidos especiales del cliente |
| created_at | datetime | auto |
| updated_at | datetime | auto |

---

## Diagrama de relaciones

```
auth_user ──────────── drivers (OneToOne)
                           │
                           │ FK
                           ▼
suppliers ──── products    shipments ──── customers
                   │           │                │
              M2M via          │ FK             │ FK
         shipment_products     ├──── transport  ▼
                               ├──── routes ── route_stops
                               └──── warehouses (local origen)
                                         │
                                         │ FK
                                         ▼
                                       tables
                                         │
                                         │ FK
                                         ▼
                                    reservations ──── customers
```

## Resumen de relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| `drivers` → `auth_user` | OneToOne | repartidor es usuario del sistema |
| `products` → `suppliers` | ManyToOne | plato puede tener proveedor de ingredientes |
| `shipments` → `customers` | ManyToOne | cada pedido pertenece a un cliente |
| `shipments` → `warehouses` | ManyToOne | local que origina el pedido |
| `shipments` → `drivers` | ManyToOne | nullable, asignado al despachar |
| `shipments` → `transport` | ManyToOne | nullable, asignado al despachar |
| `shipments` → `routes` | ManyToOne | nullable, asignado al despachar |
| `shipments` ↔ `products` | ManyToMany | via `shipment_products` (detalle del pedido) |
| `routes` → `warehouses` | ManyToOne | local de origen de la ruta |
| `route_stops` → `routes` | ManyToOne | paradas pertenecen a una ruta |
| `tables` → `warehouses` | ManyToOne | mesa pertenece a un local |
| `reservations` → `customers` | ManyToOne | reserva hecha por un cliente |
| `reservations` → `tables` | ManyToOne | reserva asignada a una mesa específica |
