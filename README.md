# Taller Reparaciones

Módulo de Odoo 18 para la gestión de **órdenes de reparación en un taller de vehículos**. Permite registrar órdenes asociadas a un cliente y a un vehículo, añadir líneas con productos/servicios, seguir el ciclo de vida de la reparación mediante estados y descontar del stock los materiales consumidos.

- **Versión:** 18.0.1.3.0
- **Autor:** Manuel Jauregui
- **Categoría:** Other
- **Tipo:** Aplicación (`application: True`)

## Dependencias

| Módulo | Motivo |
|--------|--------|
| `base` | Núcleo de Odoo |
| `contacts` | Cliente de la orden (`res.partner`) |
| `product` | Productos/servicios de las líneas (`product.product`) |
| `account_fleet` | Vehículos (`fleet.vehicle`) + contabilidad |
| `stock` | Movimientos de inventario (`stock.picking` / `stock.move`) |
| `account` | Base para la futura facturación (`account.move`) |

## Estructura del módulo

```
taller_reparaciones/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── taller_orden.py          # Modelo taller.orden (cabecera)
│   └── taller_orden_linea.py    # Modelo taller.orden.linea (líneas)
├── views/
│   └── orden_reparacion_views.xml
├── data/
│   ├── sequence_ordenes.xml     # Secuencia OR-####
│   └── taller_reparaciones_menus.xml
├── security/
│   └── ir.model.access.csv
├── README.md
└── DETALLES.md
```

## Funcionalidad implementada

### Modelos
- **`taller.orden`** — Cabecera de la orden: cliente, vehículo, fecha, notas, estado y líneas.
- **`taller.orden.linea`** — Líneas de la orden: producto, cantidad, precio unitario y subtotal calculado.

### Ciclo de vida (estados)
`Borrador → Cotización → En Reparación → Completado → Facturado` (con salida a `Cancelado`).

Cada transición se realiza mediante botones en la cabecera del formulario, visibles según el estado actual.

### Numeración automática
Cada orden recibe un código secuencial `OR-####` mediante `ir.sequence` al crearse.

### Cálculo de subtotales
El subtotal de cada línea se calcula automáticamente (`cantidad × precio unitario`). El precio unitario se rellena con el precio de venta del producto (`lst_price`) al seleccionarlo.

### Integración con inventario
Al marcar la orden como **Completado**, se genera automáticamente un albarán de salida (`stock.picking`) y se descuentan del stock los productos de tipo **consumible** (`consu`). Los servicios no generan movimiento de inventario.

### Interfaz
- Vista lista y vista formulario de órdenes.
- Menú raíz *Taller Reparaciones → Órdenes*.
- Barra de estados (statusbar) y pestañas de *Líneas de orden* y *Descripción*.

## Lo que falta por añadir / mejorar

### 🔴 Facturación (principal pendiente)
El botón **Facturar** (`action_mark_invoiced`) solo cambia el estado a `invoiced`; **no genera ninguna factura real**. Aunque el módulo ya depende de `account`, falta:
- Crear un `account.move` (factura de cliente) a partir de las líneas de la orden.
- Mapear cada `taller.orden.linea` a una `account.move.line` (producto, cantidad, precio, impuestos, cuentas).
- Un botón inteligente (*smart button*) que enlace a la factura generada y un contador de facturas.
- Gestión de impuestos (IVA) y cuentas contables.
- Control de estado de pago.

### 🟠 Totales de la orden
- No existe un campo de **total** en la cabecera (suma de subtotales de las líneas). Debería añadirse un `amount_total` calculado.

### 🟠 Validaciones y reglas de negocio
- El TODO en `action_confirm_quote` sigue pendiente: impedir confirmar una orden sin líneas/productos.
- No se puede impedir facturar/completar una orden vacía.
- El vehículo no se filtra por el cliente seleccionado (se pueden elegir vehículos de otros clientes).

### 🟡 Trazabilidad y comunicación
- Sin `mail.thread` / `mail.activity.mixin`: no hay chatter, seguidores ni historial de cambios de estado.
- El campo `state` no tiene `tracking=True`.

### 🟡 Informes
- No hay informe PDF (orden de trabajo / presupuesto imprimible).

### 🟡 Seguridad
- El acceso (`ir.model.access.csv`) se concede sin grupos (`group_id` vacío) → acceso total para cualquier usuario. Faltan grupos de seguridad (p. ej. *Usuario de Taller* / *Responsable de Taller*) y reglas de registro.

### 🟢 Detalles menores
- `date` está declarado como `Datetime` pero su valor por defecto es `fields.Date.today` (inconsistencia de tipo).
- `statusbar_visible` en la vista usa `in_process`, pero el valor real del estado es `in_progress` (no coincide).
- `quantity` es `Integer` (no admite decimales; podría convenir `Float`).
- Sin soporte multicompañía (`company_id`) en los modelos.

## Instalación

1. Copia la carpeta `taller_reparaciones` en el directorio de *addons*.
2. Actualiza la lista de aplicaciones en Odoo.
3. Instala **Taller Reparaciones**.
