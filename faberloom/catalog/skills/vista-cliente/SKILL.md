---
name: "vista-cliente"
description: "Para diseñar lo que ve un cliente de Muito Work en el portal de mwt.one (pedidos, estado de cuenta, documentos, reposición), incluidos grupos con empresas subsidiarias."
---

# Vista del cliente

v1.0 · 2026-11-08 · Nace de la maqueta «Portal del cliente con subsidiarias» (artifact a8adfefc-da31-4917-8b2f-2a479e20d869) y su especificación (doc 33dd93ab-ed17-4a36-bdec-235036cf1258).

Lo que ve un cliente vive en el **portal de mwt.one**, no en un artifact: solo el servidor puede decidir qué empresa ve qué dato. Claude entrega especificación y maqueta; la construcción y los permisos los hace Alejandro, con visto bueno del CEO antes de enviárselos. El dashboard interno (`dashboard-comercial`) nunca se comparte ni se adapta para un cliente.

## Quién ve qué

| Usuario | Ve | No ve |
|---|---|---|
| Empresa padre | El grupo (suma) y cada empresa, con un selector Grupo / Empresa | Otros grupos |
| Subsidiaria | Solo su empresa | Pedidos, facturas, documentos y uso de crédito del padre o de otras subsidiarias |

Grupos en mwt.one (08/11/2026): Sondel → Sondel Honduras; Imporcomp → Importaciones y Compras. El crédito se maneja por grupo: el padre ve límite, uso de cada empresa y disponible; la subsidiaria ve el disponible del grupo y su propio uso.

## Bloques

1. **Resumen:** pedidos en camino, total por pagar separado por acreedor (Muito Work o Marluvas) y vencido, próximo vencimiento, crédito.
2. **Pedidos en camino:** OC del cliente, proforma, empresa, etapa, llegada estimada, pares, documentos publicados.
3. **Estado de cuenta:** cada factura con a quién se paga, emisión, vencimiento, saldo y estado. Un cliente puede tener las dos: FE de Muito Work en reventa y factura de Marluvas en pedidos directos.
4. **Para reponer:** modelos más comprados en 12 meses, curva de tallas general y por modelo, y pedido sugerido que reparte la cantidad que indique el cliente según la curva (como referencia).

Se diseña desde las preguntas del comprador: qué llega, qué debo y a quién, qué reordeno y en qué tallas.

## Lo que nunca aparece

Comisión de Muito Work y su tasa; costo de Marluvas y margen en reventa (regla del costo emulado); liquidaciones; registros y notas internas; documentos sin publicar; datos de otros clientes.

## Maqueta

Tipo Design, con datos inventados y marcados como ejemplo (empresas, pedidos, montos y modelos ficticios). Una pantalla por tipo de usuario (padre y subsidiaria). Nunca datos reales en una maqueta.

## Antes de abrir el portal a un cliente

- El rol cliente no debe tener `expediente_phase_durations_get` (cierra expedientes en destino por el tope de 120 días).
- El acceso del usuario padre debe incluir sus subsidiarias; comprobarlo con `mwt_diag_scope`.
- Ninguna respuesta de la plataforma debe exponer claves de acceso del cliente.

## Aceptación

- Usuario de prueba de la subsidiaria: no aparece nada del padre ni de otra empresa.
- Usuario de prueba del padre: el grupo = suma exacta de las vistas por empresa.
- Buscar en la maqueta o la pantalla las palabras comisión, costo, margen, tasa y el nombre de quien liquida en Marluvas: cero resultados.