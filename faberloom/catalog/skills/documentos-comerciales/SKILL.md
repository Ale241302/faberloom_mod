---
name: "documentos-comerciales"
description: "Cómo completar la tarjeta Documentos comerciales de cada expediente en mwt.one: OC/PO (código por marca), proformas por audiencia, Excel de SAP y factura de Muito Work. Incluye la API, la diferencia entre oc_id y expediente_id y las fuentes en correo y carpeta."
---

# Documentos comerciales del expediente

v1.3 · 2026-11-09 · La OC sin archivo nace con el código por marca de la ficha (`MAR-SONDEL-CR-505515-26`). v1.2 · 2026-11-09 · La fila `FACTURA` es solo de Muito Work (la del fabricante va como `OTRO`) y la OC que abre el portal nace sin archivo. v1.1 · 2026-11-09 · Agrega generar proformas por audiencia, generar la factura de MWT, identificar el Excel de SAP y el OC sustituto del cliente sin orden. v1.0 · 2026-11-09 · Nace de la carga del 09/11/2026: 23 expedientes completados con OC y 2 con el Excel de SAP. Deja escrito por qué la tarjeta puede mostrar «0 archivos», cómo se sube un archivo sin duplicar el registro vacío y por qué los enlaces de SAP de Zendesk ya no sirven.

## Qué es la tarjeta

En `https://consola.mwt.one/expedientes/<id>` la pestaña **Documentos comerciales** no lee los documentos del expediente: lee los de la **OC**.

- La URL usa el **`oc_id`**, no el `expediente_id`. Para encontrarlo: `expediente.oc_id` en `/api/expedientes/`, o `ocsApi.get(<uuid o código>)`.
- El frontend llama `GET /api/documentos/?oc=<oc_id>` (`frontend/src/pages/OCDetail.jsx`).
- Un documento guardado solo con `expediente_id` (sin `oc_id`) **no aparece** en la tarjeta. Al subir, mandar siempre `oc_id`, y `expediente_id` cuando exista.
- «0 archivos» no significa que no haya filas: hay registros con `file_size_bytes = 0` y `storage_url` vacío. Esos son los que hay que rellenar.

## Qué documento va en cada fila

| `kind` | Etiqueta en pantalla | Qué es |
|---|---|---|
| `OC` | OC del Cliente | La orden de compra o el pedido del cliente (PDF; para Importaciones y Compras y Ummie suele ser un Excel «PEDIDO …»). Si el cliente no emite OC, va el correo o Excel con que pidió |
| `PROFORMA` | Proforma Cliente / MWT / Fábrica / CEO | La proforma del fabricante. La audiencia decide la etiqueta |
| `FACTURA` | Factura comercial | La factura de Muito Work (FE en reventa o factura por servicios en comisión). La del fabricante o proveedor no va aquí: va como `OTRO` o solo en la carpeta |
| `ART-04` | Confirmación SAP | El Excel que manda Backoffice con el pedido digitado |

**Cuántas proformas:** si el operador es el cliente, una (`CLIENT`). Si el operador es Muito Work Limitada, tres: `FABRICA` (la del fabricante), `MWT_INTERNAL` (la de MWT) y `CLIENT` (la que ve el cliente). No se sube la del fabricante como `CLIENT` en reventa: expone el costo.

**OC creada por el alta del portal:** el wizard abre la OC con el código por marca de la ficha del cliente (`MAR-SONDEL-CR-505515-26`, o `PO 504289` si el cliente emitió su número) y el registro nace **sin archivo**. La fila no está completa hasta que el cliente suba su PDF. Si no lo tiene, aplica **OC sustituto**.

## De dónde sale cada archivo

1. **Carpeta del expediente**, que manda:
   - `OC del Cliente/<PO>.pdf` (o `PEDIDO … .xlsx`)
   - `Proforma/PF <proforma>.pdf`
   - `SAP/<sap>.xlsx`
2. **Correo** (`alvaro@muitowork.com`, MCP `hostinger_mail`), solo para lo que falte:
   - La OC llega **adjunta** (PDF del cliente). El log del expediente trae el `uid`.
   - El Excel de SAP llega de dos formas: **adjunto** en el correo de registro de Backoffice con el nombre `PF <proforma>.XLSX` o `PEDIDO <sap>.XLSX`, o como **enlace de Zendesk en el cuerpo** («Digitado na OV <sap>»). El adjunto es el export real; se reconoce por la cabecera `Emissor da ordem` y el SAP sale de `Documento de vendas`.
3. **Prohibido inventar**: un Excel armado por nosotros no es la confirmación de SAP.

### Los enlaces de SAP están muertos
Los enlaces `https://marluvas-8550.zendesk.com/attachments/token/…` responden **HTTP 200 con «Help Center Closed»**: el tenant está cerrado. No es un enlace caducado de un archivo: no hay archivo detrás. Consecuencia: el Excel de SAP solo se recupera si ya está en `SAP/` de la carpeta. Si no está, se registra el faltante en log y resumen y se pide a Marluvas/Backoffice; no se sustituye.

### El `uid` del log no basta
El `uid` es de la carpeta IMAP donde vive el mensaje, y se repite entre carpetas. `hm_get_message(uid, folder="INBOX")` puede devolver otro mensaje con el mismo número. Antes de descargar, comprobar asunto y nombre del adjunto. Si no coincide, buscar en la carpeta del cliente (`INBOX.SONEPAR…`, `INBOX.IMPORTACIONES Y COMPRAS…`, etc.); `hm_search_messages` con `subject`/`text` falla con guiones y acentos, así que conviene recorrer carpetas.

## Cómo se sube (API, sin la UI)

1. **Token.** `POST /api/auth/login/` con `{usuario, password}`. El login tiene throttle: cachear el `access` y reutilizarlo; no loguearse por archivo.
2. **Subir el binario.** `POST /api/storage/upload-proxy/` multipart `{file, scope, filename}` → `{key}`. Scope sugerido: `documento/reconstruccion-2026-11`. (`upload-url` + PUT también sirve, pero obliga a firmar desde la PC.)
3. **Rellenar o crear:**
   - Si ya existe el registro vacío (`kind` + `oc_id`, `file_size_bytes=0`): `PATCH /api/documentos/<id>/` con `{storage_url: key, file_size_bytes, file_ext, fecha}`. La fecha es la del documento, no la de hoy.
   - Si no existe: `POST /api/documentos/` con `{storage_key: key, kind, codigo, oc_id, expediente_id, audience}`.
4. **No crear cuando hay registro vacío.** El `POST` con `storage_key` **siempre inserta**: el dedupe de OC vacía solo corre en el create multipart. Si se crea de más, se deja el duplicado en `is_active=false` (no borrar: el `destroy` elimina el objeto de MinIO, que es el que usa el registro bueno).
5. **Verificar.** `GET /api/documentos/?oc=<oc_id>`: una fila activa por documento, `file_size_bytes > 0`, `storage_url` con `documento/…`.

### Audiencias
- `CLIENT`: visible en el portal del cliente.
- `MWT_INTERNAL`: visible para MWT, no para el cliente.
- `ADMIN_ONLY`: solo admin/CEO.
- `FABRICA`: proforma del fabricante.

En reventa, la proforma del fabricante va `FABRICA` o `MWT_INTERNAL`, nunca `CLIENT`. El Excel de SAP va `ADMIN_ONLY`.

## Generar la proforma

No se sube a mano: `POST /api/expedientes/<id>/generate-proforma/` con `{codigo: "<proforma>"}`.
- Operador Muito Work Limitada: crea 3 (`CLIENT`, `MWT_INTERNAL`, `FABRICA`).
- Operador cliente: crea 1 (`CLIENT`).

Cada llamada inserta documentos nuevos. Antes de llamar, guardar los ids de las proformas activas; después, desactivarlas con `PATCH is_active=false`. Verificar que queden 1 o 3.

Efecto secundario: el expediente pasa a `proforma_codigo = "PF <n>"` y conserva el original en `proforma_codigos`. Avisar a Alejandro.

## Generar la factura comercial

La factura es la de **Muito Work**, no la de Marluvas. No hay endpoint de backend: el frontend usa `GET /api/expedientes/<id>/factura-payload/` y `buildTransferInvoiceHtml` (`frontend/src/lib/transferInvoiceHtml.js`) con audiencia `MWT`.
- Archivo: `Factura_<proforma>_MWT.html`.
- Se sube como `FACTURA`, audiencia `MWT_INTERNAL`.
- Es la factura de mercadería de MWT; la factura mensual de comisiones es otro documento y, si existe, tiene prioridad.
- Si el payload no trae `transferencia` o no trae líneas, no se genera: se registra el faltante.

## Identificar el Excel de SAP

- Nombre: `PF <proforma>.XLSX` o `PEDIDO <sap>.XLSX`.
- Cabecera de la primera hoja: `Emissor da ordem`, `Nome emissor ordem`, `Documento de vendas`, `Material`, `Qtd Ordem`.
- El número de SAP/OV es el primer valor de `Documento de vendas`.
- Un xlsx de proforma (`Proforma <pf>.xlsx`, hoja `Proforma`) **no** es el export de SAP.
- Los enlaces `marluvas-8550.zendesk.com` están muertos: responden «Help Center Closed» con HTTP 200.

## OC sustituto (cliente sin OC)

Si el cliente no emite OC (Ummie, Comtek, Impormcomp, Importaciones y Compras, EGUISA sin PO), se sube como `OC` el Excel o correo con que pidió (`PEDIDO …xlsx`, `Copy of purchase-order …xlsx`, `PEDIDO MARLUVAS …xlsx`):
- audiencia `MWT_INTERNAL`;
- en el log se dice que es respaldo del pedido, no una OC formal;
- si no hay ningún archivo, la fila queda vacía y se registra el faltante.

## Duplicados y audiencias

- Clave para comparar: `(oc_id, kind, audience)` con archivo. Si ya existe, no crear otro.
- Si se creó de más, `PATCH is_active=false`; nunca borrar.
- Audiencias: `CLIENT` (portal), `MWT_INTERNAL` (MWT), `ADMIN_ONLY` (CEO), `FABRICA` (fábrica).
- Factura de MWT: `MWT_INTERNAL`. OC sustituto y SAP: `MWT_INTERNAL`/`ADMIN_ONLY`. Proforma: según el operador.

## Cierre
Cada archivo subido deja, en la misma pasada:
- fila `accion` en `LOG_EXPEDIENTE_<proforma>.csv` con documento, código y fuente;
- `actualizado: <fecha>` en `RESUMEN_<proforma>.md`.

Y se compara carpeta con mwt.one: lo que está en uno debe estar en el otro. Lo que no se pudo subir queda escrito con el motivo (por ejemplo, «enlace Zendesk cerrado») y quién lo resuelve.

## Errores ya cometidos (no repetir)
- Confundir `oc_id` con `client_id` o con `expediente_id`: el documento queda colgado de otra entidad y no aparece en la tarjeta. Se corrige con `PATCH {oc_id}`.
- Subir un `xlsx` de proforma como SAP: no es la confirmación de Backoffice.
- Dar por bueno un `uid` sin abrir el mensaje: devuelve un correo de otro año con el mismo número.
- Subir la factura de Marluvas (o del proveedor) como `FACTURA`: la factura comercial de la tarjeta es la de Muito Work. La de Marluvas va como `OTRO` o solo en la carpeta `Factura`.
