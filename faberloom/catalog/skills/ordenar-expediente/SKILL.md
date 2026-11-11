---
name: "ordenar-expediente"
description: "Entra a la carpeta de un expediente (Marluvas/Tecmater/Bangni), verifica que tenga lo que debe, la ordena, une carpetas repetidas, elimina vacías y lleva el control de versiones, sin perder un archivo."
---

# Ordenar expediente

v1.4 · 2026-11-09 · El `PO` del nombre de carpeta es el código de OC asignado (número del cliente o `MAR-…` de la ficha). v1.3 · 2026-11-09 · `Factura` incluye la factura de Muito Work (FE o HTML); `SAP` reconoce los nombres del export de Backoffice; el cliente sin OC guarda su pedido como respaldo. v1.2 · 2026-11-08 · Dueña única de estructura, nombres y versiones de la carpeta; `expediente-carpeta` escribe log, resumen y coloca documentos nuevos con estas reglas. v1.1 · 2026-11-08 · Las incongruencias se reportan al harness por `COLA_HARNESS.csv`; no se corrigen al ordenar. v1.0 · 2026-11-08 · Pedido del CEO: "entrar al expediente, verificar que la carpeta tenga lo que tiene que tener, organizar todo y el control de versionamiento; hay carpetas repetidas y vacías". Parte del harness de expedientes. Es la dueña de las reglas de disco (estructura, nombre final, versiones, conjuntos en disco) y aplica los documentos exigidos de `expediente-reglas`. No escribe en mwt.one ni en el correo.

## Cuándo se usa
- El CEO pide ordenar uno o varios expedientes, o un año completo.
- Al terminar `reconstruir-expediente` sobre un expediente.
- Cuando una auditoría muestra subcarpetas no estándar, repetidas, vacías, sueltos en la raíz, duplicados o versiones sin marcar.

## Contrato
- **Recibe:** la ruta de una carpeta de expediente o una lista de rutas.
- **Devuelve:** la carpeta ordenada, `Otros\REGISTRO_ORDEN_<fecha>.csv`, una fila `accion` en el log, la sección `## Orden de carpeta <fecha>` en el resumen y la lista de faltantes.
- **Escribe** solo dentro de la carpeta del expediente y en `respaldos\ordenar\`. Siempre con respaldo completo antes del primer cambio.
- **Nunca** sobrescribe ni borra un archivo: un duplicado exacto se retira al respaldo; un nombre ocupado recibe sufijo `(<hash8>)`.
- **Se detiene** si la verificación final muestra un archivo del respaldo que no está ni en la carpeta ni en los retirados.
- **No corrige el contenido del expediente:** lo que no cuadra se reporta al harness (sección **Incongruencias**) y lo revisa `reconstruir-expediente`.

## Qué debe tener la carpeta

### Estructura
En la raíz solo `LOG_EXPEDIENTE_<proforma>.csv` y `RESUMEN_<proforma>.md`. Subcarpetas estándar, con estos nombres exactos y sin sufijos de proforma, OC ni año:

| Subcarpeta | Contenido |
|---|---|
| `Proforma` | Versiones de la proforma (pdf, xlsx, html) |
| `OC del Cliente` | PO, OC o consecutivo interno, todas sus impresiones |
| `SAP` | xls de registro y descarga: `<sap>.xlsx`, `PF <proforma>.XLSX` o `PEDIDO <sap>.XLSX` |
| `Factura` | Factura de Muito Work (FE o HTML) y factura de Marluvas o del proveedor |
| `Packing List Detallado` | Lista de empaque y romaneio |
| `Guia` | BL, AWB, HAWB, MAWB |
| `DUA` | DUE, DU-E, DUA, liquidación de DUA |
| `Pago de Impuestos` | Liquidaciones y comprobantes de impuestos |
| `Certificado de Origen`, `Seguro`, `Liquidacion` | Según su nombre |
| `Cotizaciones` | Cotizaciones de flete |
| `Correos` | Archivo `.eml` de los correos del expediente |
| `Otros` | NF, DANFE, FE de proveedor, comprobantes de pago, etiquetas, registros (`REGISTRO_*`) y lo que no encaje |

Equivalencias que se unifican en la estándar: `Packing List` → `Packing List Detallado`; `Certificados` → `Certificado de Origen`; `PO …`, `OC …`, `OC del Cliente 504802` → `OC del Cliente`; `Factura 2417-2026`, `Guia 2417-2026`, `SAP  269433` y cualquier estándar con sufijo → la estándar; `Navio` → `Guia`. Una subcarpeta se crea solo si va a tener archivos.

### Documentos exigidos
Se verifican contra la tabla **Documentos exigidos** de `expediente-reglas`, según modalidad y etapa (registro: proforma, OC, SAP; tránsito: factura, packing, guía, certificado; más los de comisión, reventa o compra). Un faltante se busca antes en `Correos` (adjuntos de los `.eml`) y, si es conjunto, en la carpeta del padre. Si no aparece: fila `problema` en el log, línea en `## Faltantes y conflictos` del resumen y pendiente para `reconstruir-expediente`. Clientes sin OC propia no exigen OC del cliente, pero desde el 09/11/2026 su pedido (Excel o correo) se guarda en `OC del Cliente` y se sube como respaldo.

## Control de versiones
- Todas las versiones se conservan. La vigente queda en la subcarpeta con nombre limpio (`Packing List 2417-2026.pdf`); las anteriores van a `<Subcarpeta>\Anteriores\` con la fecha impresa o de creación en el nombre (`Packing List 2417-2026 (2026-04-20).pdf`).
- **Vigente:** la de versión o fecha impresa más reciente; si no hay, la fecha de creación del PDF; si no, la del correo. Excepción de `expediente-reglas`: si el comprador usó una versión anterior y el pago cuadra con ella, esa es la vigente (2465-2026 frente a 2465-2026A).
- Una guía, factura o pedido **cancelado** va a `Anteriores` con `CANCELADO` en el nombre.
- Cada decisión de versión queda en el resumen, sección `## Evolución`, y en el registro de orden.
- `2478B` y similares no son versiones: son otro envío con su propio expediente.

## Carpetas repetidas, anidadas y vacías
- **Misma proforma en dos carpetas** (ejemplos de la auditoría del 08/11/2026: 1555-2019, 2159-2023, 2349-2025): la carpeta correcta es la que corresponde a la modalidad (comisión en la carpeta del cliente; reventa en `02 M Muito Work`). Se unen por hash en la correcta: lo idéntico se retira, lo distinto se mueve, y la otra se elimina vacía. Si la modalidad no está clara en el log o el SAP, se deja como pendiente en el log de las dos.
- **Expediente anidado dentro de otro** (ejemplos: `1507-2019\1621-2020 CNFL`, `1738-2020\1746-2021`, `2304-2025\2340-2025 PO 504248`): se saca a su lugar `<país>\<cliente>\<año>\` según su propia proforma y modalidad, con su log y resumen. Si ya existe la carpeta destino, se unen por hash.
- **Conjunto:** no se anidan carpetas; cada proforma conserva la suya con el mismo BL o AWB en el nombre; los documentos compartidos (guía, factura conjunta, packing, certificado) quedan una vez en la carpeta del padre en mwt.one (si no hay padre, la de menor número) y el resumen de cada miembro dice dónde están. No se usan accesos directos de Windows.
- **Vacías:** se eliminan al final, de adentro hacia afuera, con 3 reintentos y `chmod` si OneDrive las marcó de solo lectura. Una que no se pueda eliminar queda como pendiente; no detiene el resto.

## Pasos
1. **Auditar (solo lectura):** `python ord_auditar.py` recorre `01 Ventas\01 Marluvas` y escribe `ord_auditoria.csv` por expediente: sueltos en la raíz, subcarpetas no estándar o repetidas, anidadas, vacías, duplicados por hash, faltantes básicos, rutas largas, log y resumen. Sirve para elegir el lote.
2. **Plan:** `python ord_plan.py "<carpeta>"` escribe `ord_plan_<proforma>.csv` con acciones `mover`, `retirar_duplicado`, `versiones`, `revisar`, `eliminar_vacia`. Clasifica por nombre de archivo; un nombre genérico (`Untitled`, `Captura`, `Scan`) o una contradicción entre nombre y subcarpeta queda en `revisar`.
3. **Decidir lo que el script no puede:** Claude lee el texto de cada `revisar` y `versiones` con `python ord_leer.py "<carpeta>" <rel>…` (texto de la primera página y fechas del PDF) y decide destino, nombre y vigente. Un PDF sin texto (escaneado o imagen) se deja en la subcarpeta donde está y se anota. En lotes grandes, la extracción de texto la hace el obrero (DeepSeek) y Claude decide.
4. **Plan final:** `ord_final_<proforma>.csv` con columnas `accion, origen, destino, motivo` (acciones `mover`, `retirar_duplicado`, `mantener`). Un archivo genérico se renombra por lo que es (`Untitled.pdf` → `PO 504802 (2026-05-06).pdf`). Los espacios de relleno en nombres se quitan.
5. **Aplicar:** `python ord_aplicar.py "<carpeta>" ord_final_<proforma>.csv "<nota de versiones y decisiones>"`. Respaldo completo en `respaldos\ordenar\<proforma>_<fecha-hora>`, movimientos sin sobrescribir con hash verificado, duplicados al respaldo `_retirados`, vacías eliminadas, verificación de que ningún hash del respaldo se perdió, registro en `Otros\REGISTRO_ORDEN_<fecha>.csv`, fila en el log y sección en el resumen.
6. **Nombre de la carpeta del expediente (vigilancia obligatoria, pedido del CEO 08/11/2026):** toda carpeta debe llamarse `<proforma> PO <OC> <BL o AWB>` para ubicarla fácil, y las subcarpetas deben tener los nombres estándar. La `<OC>` es el código asignado: el número del cliente (`504983`) o el de la ficha por marca (`MAR-SONDEL-CR-505515-26`); va tal cual, sin acortar. `python ord_nombres2.py` calcula el nombre de cada carpeta con datos verificados: OC desde los archivos de `OC del Cliente` («Pedido 1xxxxxx» es el pedido Marluvas, no la OC), el resumen y el nombre actual; guía desde `Guia` (el número del archivo tiene que estar impreso en el documento; house antes que master), el resumen y el nombre actual. AWB de Copa en 3-4-4 (`230-6767-2581`); otras aerolíneas en 3-8 (`549-37262256`). Sin SAP, sin espacios de relleno, sin etiquetas. `python ord_renombrar.py [archivo]` renombra con salvaguardas y actualiza `logs.json`, `ch07_spec.json`, `COLA_HARNESS.csv`, el log (`LOG-ORD-<fecha>-NOMBRE`) y `nombre_final_carpeta` del resumen. **No renombra solo** si: el nombre tiene palabras que pueden llevar información (CNFL, ESPH, fake, Magnesita…), se perdería un número que no es SAP, la proforma tiene dos carpetas o la carpeta es compartida; esos casos los decide Claude caso a caso (`ord_nombres_manual.csv` con `forzar=sí`) o el CEO. Una carpeta compartida lleva las dos proformas (`2463-2026 2465-2026 PO … HBL …`). Si falta la OC o la guía, el nombre se completa cuando aparezca el documento. Lote del 08/11/2026: 118 carpetas renombradas; 0 índices rotos.
7. **Faltantes e incongruencias:** con la carpeta ordenada, comparar contra los documentos exigidos y registrar los que falten; correr `ord_congruencia.py` y reportar al harness lo confirmado (sección **Incongruencias**).
8. **Informar:** por expediente, una línea con movidos, duplicados retirados, vacías eliminadas, versiones decididas y faltantes. En lote, una tabla.

## Incongruencias: se reportan, no se corrigen
Decisión del CEO (08/11/2026): si el agente encuentra algo que no es congruente con el expediente, lo reporta para que el harness lo revise. Ordenar no decide ni arregla datos del expediente.

**Qué es incongruente:**
| Tipo | Ejemplo |
|---|---|
| `referencia_ajena` | Un documento imprime o nombra otra proforma, OC, SAP o guía que no es del expediente ni de su conjunto. 2417: «DUA 005-2026-307232 copia desde 2453» |
| `sin_referencia_propia` | Proforma, factura, packing, OC o certificado que no imprime ninguna referencia del expediente |
| `monto_o_cantidad` | Factura, packing o proforma con total o pares distintos entre sí o con el resumen |
| `cliente_o_modalidad` | Vendido a / consignado a de otro cliente, o reventa en carpeta de comisión y al revés |
| `fecha` | Documento con fecha anterior al registro o posterior al cierre |
| `carpeta` | Proforma en dos carpetas o expediente anidado cuya modalidad no está clara |
| `estado` | Documento que dice cancelado, borrador o sustituido y figura como vigente en el resumen |

Antes de reportar o resolver, **abrir el documento** y verificar lo que imprime; el nombre del archivo no prueba nada. Si el documento trae un error, **buscar en la secuencia de correos la versión corregida**: si existe, se trae, queda vigente y la errónea va a `Anteriores`; si no existe, se anota como error no corregido con los `uid` revisados (regla de `expediente-reglas`). Script de apoyo: `inv_comparar.py` (ficha de cada documento: número, cliente, PO/SAP, totales) y `bajar_adjunto.py <carpeta> <uid> <adjunto> <destino>` (solo lectura).

No es incongruencia lo que una regla ya explica: el año de proforma mal escrito por Marluvas (`PF 2417-2025`), la factura Marluvas distinta de la FE al cliente en reventa, la hija de un conjunto sin factura.

**Cómo se detecta y reporta:**
1. `python ord_congruencia.py "<carpeta>"` (solo lectura) compara las referencias impresas en cada documento con las del expediente, su resumen y su conjunto, y escribe `ord_congruencia_<proforma>.csv` con candidatos.
2. Claude revisa cada candidato con `ord_leer.py` y descarta los que explica una regla. Los confirmados van a `ord_inc_<proforma>.csv` (`archivo, tipo, detalle`), con el detalle redactado para que se entienda sin abrir el archivo y diciendo qué hay que confirmar.
3. `python ord_reportar.py "<carpeta>" ord_inc_<proforma>.csv` agrega cada uno a `C:\Users\alvar\.claude-server-commander\COLA_HARNESS.csv` (`id, fecha, proforma, carpeta, archivo, tipo, detalle, origen, estado=abierto, resuelto_el, resolucion`) y una fila `problema` en el log del expediente con el mismo id (`INC-<proforma>-<fecha>-NN`). No duplica lo ya reportado.
4. El documento incongruente **no se mueve** fuera de su subcarpeta ni se retira: queda donde está hasta que el harness decida.
5. El informe del lote lista las incongruencias reportadas.

Primera reportada: `INC-2417-2026-20261108-01`, DUA 005-2026-307232 copiado desde 2453-2026 (otra guía): confirmar si fue un DUA compartido o si no corresponde a 2417.

## Lotes
- Orden: 2026 → 2025 → 2024 → 2023 → 2022 y anteriores. Los de 2018 a 2022 no tienen log ni resumen: se crean con la plantilla de `expediente-carpeta` (cobertura `solo documentos`) antes de ordenar.
- Un expediente por vez: plan, decisiones, aplicar, verificar. Si uno falla la verificación, se detiene el lote y se informa.
- Al terminar el lote, volver a correr `ord_auditar.py` y comparar.

## Auditoría inicial (08/11/2026)
249 carpetas de expediente: 159 con carpetas vacías, 129 con subcarpetas no estándar (`Packing List` en 106, 45 de ellas junto a `Packing List Detallado`), 111 con archivos sueltos en la raíz (290 pdf, 158 xlsx), 28 con duplicados exactos, 85 sin log ni resumen (todas de 2018-2022), 8 expedientes anidados dentro de otro y 3 proformas en dos carpetas. Piloto aplicado: 2417-2026 (22 movimientos, 3 duplicados retirados, 7 subcarpetas con sufijo unificadas, 2 versiones decididas, 0 archivos perdidos).

## Lote completo del 08/11/2026
251 carpetas de Marluvas ordenadas, 0 archivos perdidos (verificado por hash en cada una; respaldos en `respaldos\ordenar\`, 1,7 GB). Antes → después: carpetas con vacías 159 → 0; subcarpetas no estándar 129 → 2 (1746-2021 y 1750-2021 dentro de 1738-2020, reportadas); con sueltos en la raíz 111 → 0; con duplicados 28 → 0; sin log ni resumen 85 → 0 (creados con cobertura `solo documentos`). Anidados con contenido sacados a su lugar: 2037-2023, 2092-2023 (unido con el de Comtek), 2130-2023 B. Cola del harness: 317 filas (216 faltantes, 68 referencias ajenas, 25 sin referencia propia, 8 de carpeta).

Scripts del lote: `ord_auditar.py`, `ord_lote.py [--solo-plan|--solo-congruencia]`, `ord_final_auto.py` (políticas automáticas), `ord_aplicar_lote.py`, `ord_resto_plan.py` (sueltos por contenido), `ord_anidados.py`, `ord_lote_reportar.py`, `ord_faltantes.py`, `ord_verif_ids.py`.

**Políticas automáticas (se aplican sin revisión por archivo):** unificar subcarpetas equivalentes; mover por nombre solo con regla fuerte e inequívoca (dos reglas fuertes distintas = ambiguo, no se mueve), también desde `Otros`; sueltos en la raíz por contenido del PDF; duplicados exactos al respaldo; vigente = fecha de creación más reciente. Quedan para decidir por contenido: nombres genéricos (imágenes de WhatsApp, `image001.png`) y expedientes anidados sin destino claro.

**Faltantes:** se reportan al harness una fila por expediente. No se exige SAP hasta 2022 (no existía el xls de Backoffice) ni OC a UMMIE, Comtek e Importaciones y Compras.

## Errores que no se repiten
- **Versiones solo en documentos del pedido** (Proforma, Factura, Packing, Guía, OC, Certificado, Cotizaciones). En `Otros`, `Pago de Impuestos`, `DUA`, `Seguro` y `Liquidacion`, `Comprobante (1)`, `(2)`… son documentos distintos: el 08/11 se movieron por error a `Anteriores` y se devolvieron.
- **`original` no es certificado de origen:** la regla `origin` mandó facturas y packings «ORIGINAL» a Certificado; tampoco `\bco\b` (nota de crédito CO-0002).
- **Un pago o una nota no se mueve por el documento que nombra** (`Payment … Invoice`, `Comprobante DUA`, `correcao de bl nota de debito`).
- **Un archivo nombrado `factura que acompaña la carga` va a Factura**, aunque empiece con «Proforma».
- **`_hbl`, `_bl` en nombres con guion bajo:** usar límites de letra, no `\b`.
- **Respaldo por carpeta, no por proforma:** dos carpetas de la misma proforma en el mismo segundo chocaban en el nombre del respaldo; se agregó un hash de la ruta.
- **Ids de la cola:** numerar después de los ya usados ese día para esa proforma; verificar con `ord_verif_ids.py` que cada id de la cola está una sola vez en el log con su texto.
- **Logs con filas de columnas irregulares:** no reescribirlos con `DictWriter`; corregir por texto.
- No decidir la vigente solo por el nombre: `(55b7bd95)` era la versión del 30/04 y la vigente; el nombre limpio era la del 20/04.
- No dar por guía un número de DUA: `005-2026-307232` es DUA, no AWB.
- No clasificar por la subcarpeta donde está: en 2417 la PO, la FE y un packing estaban dentro de `Guia`.
- No tocar `LOG_` ni `RESUMEN_` salvo para agregar la fila y la sección del orden.