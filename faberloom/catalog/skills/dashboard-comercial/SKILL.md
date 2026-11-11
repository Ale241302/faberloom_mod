---
name: "dashboard-comercial"
description: "Para crear, actualizar o ampliar los dashboards internos de Muito Work (diagnóstico comercial Marluvas y otros): datos, vistas, profundización, flujo de caja y verificación. No para lo que ve un cliente."
---

# Dashboard comercial

v1.1 · 2026-11-08 · Solo dashboards internos de Muito Work; lo que ve un cliente pasa a `vista-cliente`. v1.0 · 2026-11-08 · Nace de «Diagnóstico comercial Marluvas» (artifact 5a6bae90-5c74-42ac-a7ce-6bb46b37f3d1, tipo Dashboard).

El dashboard **lee** los expedientes; no los corrige. Si al armarlo aparece un dato malo, se corrige en el expediente (harness `reconstruir-expediente`) y después se regenera el dashboard. Nunca se arregla un número solo en el dashboard.

## Para qué sirve cada vista (orden de la página)

| Vista | Decisión |
|---|---|
| Indicadores | Estado general; el cursor explica cómo se calcula cada uno y lleva a su tabla |
| Por cobrar | A quién cobrar o reclamar hoy; resueltos ocultos por defecto |
| Flujo de efectivo esperado | Cuánta caja entra y sale los próximos 4 meses si todos pagan en plazo |
| Clientes | Quién crece o se enfría; clic = ficha del cliente con grupo, crédito, días reales de pago, saldo y pedidos |
| En curso | Qué pedido está fuera de plazo |
| Histórico, tiempos, modelos, calidad | Contexto; al final |

Arriba va la fecha de corte de cada fuente.

## Profundizar con sentido

- **Cursor** en indicadores: cómo se calcula y de qué fuente sale, más un enlace a la tabla que lo compone.
- **Clic** solo donde se decide algo: fila de pedido → ficha del pedido (datos, fechas, cobro, carpeta y últimas anotaciones del registro con su fuente); fila de cliente → ficha del cliente; pedido dentro del cliente → ficha del pedido y al cerrar se vuelve al cliente.
- **Todo renglón clicable lleva a una ficha con contenido.** Un documento que no es pedido (FE de Sondel, factura de comisión) tiene su propia ficha con su fuente.

## Datos y regeneración

Scripts en la PC: `C:\Users\alvar\.claude-server-commander\dash\` (copiar al contenedor para correrlos). `build2.py` arma pedidos, comisiones, por cobrar, tiempos, en curso, productos y cobertura, y al final corre `por_cobrar_curado.py` (lista depurada), `flujo.py` y `clientes_ficha.py`. La ficha por pedido sale de los registros de cada carpeta (script `fichas_log.py` en la PC) más `base_mwt.json`.

Fuentes: mwt.one (expedientes, líneas, plazos, crédito de grupo), carpetas de expedientes, facturas de comisión (`ledger.py`), Factura Profesional y bancos (`ENT_CXC_CXP_<mes>` en contabilidad). Insumos del CEO (estados de Promerica, Payoneer, facturas por pagar): se piden uno a uno.

Publicar un dataset nuevo: `upload_asset` del archivo y `update` del dataset con `url`, `name`, `updated` y `edit`.

## Flujo de efectivo: reglas

- Comisión: salida + días de crédito del cliente = pago a Marluvas; Bianca liquida a inicios del mes siguiente; Payoneer deposita a mediados, menos 1 %. Tasas: las de las liquidaciones (Sonepar 7 %, Eguisa 6,06 %, el resto 10 %).
- Reventa: vencimiento de cada FE pendiente (60 días). Compra a Marluvas a 15 días de su factura (`credit_days_mwt`): cada reventa adelanta caja unos 70 días.
- Pedidos que no salieron: salida estimada con la mediana de su etapa.
- Lo que no tiene fecha (por reclamar, aseguradora, reventas viejas) va aparte, no en los meses.
- Siempre las dos puntas: cobros y pagos. Lo que falta (gastos fijos, otros proveedores) se dice.

## Reglas de la página (tipo Dashboard)

- Cada `<script>` corre por separado: cada uno define sus propias funciones auxiliares.
- Texto fijo en el HTML; los números en dibujos (`data-draw`) que leen un dataset.
- Cambios con `db_str_replace` sobre `files/index.html`, y después `update` del campo `edit`.

## Verificación antes de entregar

1. Tres números al azar (un indicador, un mes del flujo, un pedido): bajar con clics hasta su documento o depósito. Si un paso no tiene fuente, no se entrega.
2. La suma de la ficha de cada cliente = su fila en la tabla de clientes.
3. Leer el documento de control de la página (`data/users/<id>/check`): si dice `failed`, corregir.
4. Si no se pudo ver la página funcionando, decirlo.

## Lo que no cubre

Este dashboard es interno: muestra comisiones, tasas, costos, márgenes y registros. No se comparte con clientes ni se reutiliza para ellos. Cualquier vista para un cliente se hace con la skill `vista-cliente`.