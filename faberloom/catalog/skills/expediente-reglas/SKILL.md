---
name: "expediente-reglas"
description: "Reglas de negocio del harness de expedientes Marluvas/Tecmater/Bangni: referencias, modalidad, conjuntos, log, fechas, facturas y pagos. La entrada es reconstruir-expediente."
---

# Expediente: reglas

v1.10 · 2026-11-09 · El consecutivo de OC es de 1 a 6 dígitos, por cliente y marca, y no se reinicia con el año; la fuente es G25, no la bitácora. v1.9 · 2026-11-09 · El correlativo de OC es por cliente y marca (`MAR-UMMIE-GT-04-25`) y se edita en la ficha del cliente; el alta toma el siguiente de esa fila. v1.8 · 2026-11-09 · Alta desde el portal: la OC sin número toma el consecutivo del cliente (`oc_correlativo`) y, si no hay serie, el código de POL_CODIGO_OC (`MAR-UMMIE-GT-04-26`); el expediente nace como `EXP-…` y la REF muestra ese código cuando todavía no hay proforma ni OC. v1.7 · 2026-11-09 · La factura comercial es la de Muito Work, no la de Marluvas; proformas por audiencia (1 o 3); el cliente sin OC sube su pedido como respaldo. v1.6 · 2026-11-08 · AWB aéreo directo como documento house del conjunto; factura CIP mayor que el pedido no es diferencia. v1.5 · 2026-11-08 · Comisión buscada en cuatro fuentes en orden, con la liquidación de Bianca como verdad de monto y tasa; etiquetas erradas; factura comercial que agrupa proformas. v1.4 · 2026-11-08 · Cobro histórico comprobado con facturas de comisión y FE pagadas en la contabilidad; registrar pagos con comprobante o nota de crédito. v1.3 · 2026-11-08 · Expediente siempre actualizado; marca de conjunto en el log (`LOG-CONJUNTO-<padre>`); factura del conjunto según lo impreso; expediente único con varias proformas; factura vigente confirmada por el pago; no repreguntar lo resuelto; margen de reventa. v1.2 · 2026-11-08 · Códigos de expediente y de OC de POL_CODIGO_OC v1.4. v1.1 · 2026-11-07 · Agrega búsqueda en todas las carpetas de correo, el papel de la proforma frente a la OC, el código para pedidos sin OC, MELEXA como SONEPAR Colombia y la fecha de cierre de comisiones históricas. Parte del harness de expedientes. La entrada es `reconstruir-expediente`.

## Contrato de esta skill
- **Recibe:** un encargo (`ENCARGO.json`) y la ficha actual.
- **Devuelve:** `ENTREGA_reglas.csv` con `fila_id, proforma, unidad, campo, destino, valor_propuesto, regla, fuente, ubicacion_en_fuente, confianza, estimado`, y `FICHA_LOG.csv` con las filas propuestas para el log.
- **Escribe:** solo esos dos archivos. No escribe en mwt.one, en el disco del expediente ni en el correo, y no edita la ficha.
- **No consulta mwt.one ni el disco por su cuenta:** decide con los valores actuales que la entrada incorporó a la ficha, y si le falta uno lo pide en `mensaje`. Correo y Portal Marluvas sí los lee directamente, solo para leer.
- **Se detiene:** cuando una decisión es comercial (va como `preguntar`, con el dato que la sostiene ya comprobado) o cuando no hay fuente (`sin_evidencia`). No completa con suposiciones.

## Proceso de lectura
1. **Punto de partida:** leer el log y el resumen; luego los valores actuales de mwt.one y del disco que trae la ficha. Al correo se va por lo que falte. Que un hilo ya esté en el log no prueba que su contenido esté completo.
2. **Correo por rondas:** revisar la carpeta completa y buscar en `INBOX` e `INBOX.Sent` por proforma y por cada referencia que aparezca, hasta que una ronda no agregue referencias. Eliminar repetidos por `messageId`. **La búsqueda en `INBOX` no incluye sus subcarpetas:** buscar además en `INBOX.Sent`, en las carpetas por cliente (`INBOX.SONDEL`, `INBOX.SONEPAR`, `INBOX.IMPORCOMP GUA`, `INBOX.IMPORTACIONES Y COMPRAS`, `INBOX.MTN`, `INBOX.MUITO WORK`, `INBOX.UMMIE`, `INBOX.COMTEK`, `INBOX.PRO CUSTOMER`, `INBOX.FORAGRO`) y en `INBOX.Junk`; la lista vigente sale de `folders_list`. Buscar también por nombre o dominio del cliente y por el SAP, no solo por la proforma. Una coincidencia por subcadena no es evidencia: confirmar que el documento imprime la proforma (2111: la NF-e 211103 no era de 2111). En conjuntos o contenedores compartidos, el hecho puede estar en el log de la otra proforma: cruzarlos. El buzón `506@` es fuente de FE y de lo enviado a Sondel.
3. **Portal Marluvas:** en pedidos de Marluvas, consultar SAP, estado e historial. Que el correo no traiga algo ya no prueba que no ocurrió.
4. **Lectura completa del correo:** abrir lo que se indica en **Qué abrir además del texto**.
5. **Log:** redactar en `FICHA_LOG.csv` las filas de comunicaciones, acciones, resoluciones, hechos y problemas. Las agrega `expediente-carpeta`.
6. **Documentos:** proponer con `accion = crear` todo adjunto documental que no esté en el expediente, comparando por hash, y verificar número impreso, proforma, OC y comprador. La descarga y la colocación las hace `expediente-carpeta`. Enlaces Zendesk: un enlace es "expirado" solo con la respuesta HTTP.
7. **Versiones:** la última es la vigente, por versión o fecha impresa y, si no existen, por fecha del correo. Un borrador posterior a un definitivo se marca `revisar`. Conservar todas y registrar qué cambió.
   **Errores corregidos en la secuencia de correos (decisión del CEO, 08/11/2026):** cuando un documento trae un error (número de proforma, fecha, cantidad, cliente), se sigue el hilo y los correos posteriores hasta encontrar la versión que lo corrige; esa es la vigente y la errónea pasa a `Anteriores` con su fecha y el error en el nombre. La versión corregida se trae del correo si falta en la carpeta y se carga en mwt.one. Solo si ninguna versión posterior lo corrige se anota como «error no corregido» con los `uid` revisados. Ejemplos: 2347 (factura del 02/10 imprimía 2247; la definitiva IBCO-EXP-0518-25 imprime 2347), 2495 (borrador de CO con 2484; el emitido imprime 2495), 2355 (factura definitiva IBCO-EXP-0520-25 traída del correo; el packing imprime 2354 en todas sus versiones: error no corregido).
   **El nombre del archivo no prueba lo que es:** antes de clasificar, mover o declarar incongruente un documento, se abre y se verifica lo que imprime (número, cliente, SAP, OC, total, peso). Ejemplo: `2296-2025.pdf` era un correo de 2047-2023; `Proforma 1666-2022.xlsx` imprimía 1966-2022.
8. **Bitácora:** fecha real del hecho, hito, fuente y confianza (`A` documento impreso, `B` correo del emisor, `C` mención indirecta). La fecha de carga no es la fecha del hecho.
9. **Embarque y modalidad:** Claude decide con la evidencia.

## Portal Marluvas (Salesforce)
`https://marluvas.my.site.com/s/`. Desde octubre de 2026, Backoffice trabaja en Salesforce y parte de lo registrado no genera correo. Se consulta en el navegador integrado, solo para leer.

| Dato | Uso | Dónde |
|---|---|---|
| SAP | Confiable. Si el campo está vacío, sale de `Chave do Registro` (`PED-0000297771`) o del historial | Pedido |
| Estado y cancelación | Confiable: `Status SF`, `Situação Pedido ERP` e historial con fecha | Pedido, Histórico de pedido |
| Quién creó el pedido | `Criado por`: el usuario de Muito Work o `Integrador Marluvas` | Informações do sistema |
| Comprador y plazo | Confiable: `Emissor` y `Pagador` confirman modalidad | Pedido |
| Fecha de registro | `Data do documento`, solo si no hay xls SAP; manda el xls. Ejemplo: 2495 dice 03/08 en el portal y 31/07 en el xls | Pedido |
| Líneas y totales | **No usar** en pedidos de `Integrador Marluvas`: repite líneas. Ejemplos: 2519 trae 6.480 pares contra 1.620; 2520 trae 10.100 contra 2.525. Usar xls SAP o proforma | — |
| Líneas y totales de pedidos creados con el usuario de Muito Work | Sirven si la suma cuadra. Ejemplo: 2515, 24 líneas, 290 piezas, USD 3.617,70 | Itens do pedido |
| Número de NF | Útil cuando exista; `Data Faturamento ERP` no: copia la fecha del documento aunque no haya factura | Pedido |
| `Data Desejada de Faturamento` | Es un deseo, no el fin de Producción | Pedido |

Limitaciones: el 06/11/2026 mostraba 7 pedidos, no cubre expedientes anteriores y un SAP vigente puede no aparecer (298663 de 2522). `Meus casos` estaba vacío: los tickets de Backoffice siguen por correo. El extracto de comisiones pide otra clave, que ingresa el CEO. Fin de Producción, embarque, llegada y cobro no están.

Cada dato queda en el log con fuente `Portal Marluvas` y fecha de lectura. Si el pedido del portal difiere de la proforma, se avisa al CEO antes de que Marluvas facture. Ejemplo: 2515 cambió de producto, agregó plantillas y subió USD 277,15.

## Qué abrir además del texto
| Elemento | Regla | Ejemplo |
|---|---|---|
| Imágenes dentro del correo | Ignorar logos y firmas. Abrir las que acompañan "notar", "adjunto detalle", "movimiento de inventario", "itinerario" o "ver imagen", y transcribir su contenido | 2488: el movimiento 2026-811469 traía la avería solo en una imagen. 2410: el vuelo del 25/03 venía solo en una imagen |
| Estados de comisión | Suelen venir como imagen: transcribir cliente, factura, valor pagado, porcentaje, comisión y referencia | «Comissões Junho/26» y «Comissões Setembro» |
| Correos adjuntos (`message/rfc822`, sin nombre) | Abrirlos antes de decir que falta un documento | 2488: las FE 152010 y 152100 venían dentro |
| PDF cifrado o ilegible | No suponer el monto; registrar qué no se pudo leer | Comprobante de pago a PCS en 2488 |

## Identificar el expediente

### Referencias
La proforma no cambia: es la llave del expediente. Las demás referencias se correlacionan con ella.

**Quién ve qué (decisión del CEO, 07/11/2026):** la proforma la asigna el fabricante y será el número de la factura; es la referencia principal y la que ve el administrador. La OC o PO del cliente es un apuntador alternativo: el cliente busca y asocia su pedido con su propia numeración, que lleva a la misma proforma. **Códigos (POL_CODIGO_OC v1.4, decisión del CEO 07/11/2026):**

| Código | Formato | Ejemplo |
|---|---|---|
| Interno del expediente (lo ve el administrador) | `{PRV}-{CLIENTE}-{DES}-{proforma}` | `MAR-IMPORCOMP-GUA-2296-2025` |
| OC con número del cliente | El número del cliente | `12505` |
| OC sin número del cliente | `{PRV}-{CLIENTE}-{PAÍS}-{NN}-{AA}` | `MAR-IMPORCOMP-GT-01-25` |

`PRV`: `MAR` Marluvas, `TEC` Tecmater, `BAN` Bangni. `CLIENTE`: nombre corto en mayúsculas (SONDEL, SONEPAR, IMPORCOMP, IMPORTACIONES, SIASA, EGUISA, UMMIE, COMTEK, PROCUSTOMER, MAGNESITA, FORAGRO, MUITO para reventa o importación propia); no la primera palabra de la razón social. `DES`: aeropuerto IATA (aéreo) o país del puerto (marítimo). `PAÍS`: ISO-2 del cliente. `NN`: consecutivo de **1 a 6 dígitos por cliente y marca**, solo pedidos sin OC del cliente; vive en `clientes.cliente_marca_correlativo` (G25) y no se reutiliza. En la carga manual va en orden de proforma; la bitácora `ch09_consecutivos.json` queda solo para clientes que aún no existen en mwt.one. El consecutivo no se reinicia con el año: si el último es `04`, el siguiente es `05` aunque cambie el año. `AA`: año del código. Antes de asignar un consecutivo se busca la OC en el correo: si aparece con número, manda el del cliente. Nunca la proforma ni un marcador en lugar de la OC. Límite de mwt.one: 32 caracteres (28 al crear, mientras exista el prefijo `EXP-`).

### Alta desde el portal (`/portal/nueva-oc`, 09/11/2026)
El alta del portal —admin o cliente B2B— aplica los mismos códigos y no deja inventar `OC-AUTO-…`:
1. **El cliente sube su OC numerada** (PDF o Excel): la OC conserva el número del cliente (se ve `PO 504983`). El expediente nace `EXP-{PRV}-{CLIENTE}-{PAÍS}-{número}`.
2. **No la sube**: se consume el siguiente consecutivo de la marca para ese cliente (`clientes.cliente_marca_correlativo`, G25) y se arma `{PRV}-{CLIENTE}-{PAÍS}-{NN}-{AA}` (`MAR-UMMIE-GT-05-26`). La ficha del cliente muestra el código completo y el próximo.
3. En **/expedientes**, si todavía no hay proforma ni OC, la columna REF muestra ese código (`EXP-…` o `PO MAR-…`); nunca queda en blanco.
Si la creación trae `proforma` y `destino` (alta interna hecha por API), el código nace completo: `EXP-MAR-SONEPAR-BOG-2371-2025`. El código y la OC nunca superan 32 caracteres: si no cabe, se recorta por tramos y el número de la OC manda.

**El correlativo es por marca (corregido el 09/11/2026):** `MAR-UMMIE-GT-04-25`. `MAR` es la marca (`MAR` Marluvas, `TEC` Tecmater, `BAN` Bangni), `UMMIE` el nombre corto de la empresa, `GT` el país del cliente, `04` el consecutivo editable y `25` el año. Se edita en la ficha del cliente, una fila por marca (hoy solo Marluvas). El próximo es consecutivo + 1: si dice `04`, sigue `05`; si se cambia a `11`, sigue `12`. El consecutivo admite 1 a 6 dígitos (Sondel usa `505515`). El valor viejo `clientes.cliente.oc_correlativo` solo siembra la migración.

Semillas al 09/11/2026: Sondel 505515, Sondel Honduras 700143, Sonepar 110024463, Procustomer 800120, Imporcomp 12544, Ummie 05, Comtek 05, Importaciones 04, Siasa 01; Eguisa y Muito arrancan en 01.

**Clientes:** MELEXA es SONEPAR Colombia tras el cambio de dueño: todo lo de MELEXA se registra en SONEPAR Colombia. Importaciones y Compras (Honduras) es cliente distinto de Imporcomp (Guatemala).

| Referencia | Ejemplo | Dónde queda |
|---|---|---|
| Proforma | 2455-2026 | Nombre de carpeta, resumen y `referencias.csv` |
| OC del cliente o consecutivo interno | PO 504983 | Nombre de carpeta, resumen y `referencias.csv` |
| BL o AWB | BL SSZ1811398A | Nombre de carpeta, resumen y `referencias.csv` |
| SAP, factura Marluvas, contenedor, gestión de agencia, DUA, DU-E, FE, comisión y pago | 269486 · Alfa 2608004 · FE 133 | Resumen y `referencias.csv` |

`referencias.csv`: `id_observacion, proforma, tipo_referencia, numero, emisor, fecha, se_relaciona_con, documento_o_uid, confianza`.

Las relaciones no siempre son uno a uno: varias proformas pueden compartir factura, guía, contenedor, OC o agencia, y una proforma puede dividirse. Registrar cada coincidencia por separado; compartir una no prueba que compartan las demás. En una importación de Muito Work Limitada, buscar también el número de gestión de la agencia.

Números que parecen distintos y no lo son:
- **DUA:** el "Nro. de Envío" no es el número de DUA. Ejemplo: 2965 frente a 005-2026-307232.
- **Asunto y cuerpo:** manda el cuerpo o el documento impreso, y la diferencia se anota. Ejemplo: asunto "2455 y 2480", cuerpo "2488 USD 9.413,01".
- **Año de la proforma:** Marluvas puede escribir otro año. Ejemplo: su estado dice 2410-2025 para 2410-2026. Se anota y no cambia el monto.

### Proformas por audiencia (decisión del CEO, 09/11/2026)
En la tarjeta **Documentos comerciales** de mwt.one la proforma se repite por audiencia:
- **Operador = el cliente:** una sola proforma, audiencia `CLIENT`.
- **Operador = Muito Work Limitada:** tres, `CLIENT`, `MWT_INTERNAL` y `FABRICA`.
La de fábrica no se marca `CLIENT` en reventa: expone el costo. Un expediente está bien cuando tiene exactamente 1 o 3, según su operador; cualquier otra cuenta se corrige.

### Modalidad
La decide la evidencia, no la carpeta. Primero `Emissor da ordem` del xlsx SAP y `Vendido a` de la factura; luego el destino de la guía.

| Modalidad | Prueba | Quién factura |
|---|---|---|
| Comisión | Emissor es el cliente | Marluvas al cliente; Muito Work Limitada factura su comisión |
| Reventa FULL | Emissor 4000000145, destino Costa Rica | Muito Work Limitada al cliente |
| Triangular | Emissor 4000000145, guía a otro país | Muito Work Limitada al cliente exterior |
| Venta sucesiva | Venta antes de nacionalizar; el comprador nacionaliza | Muito Work Limitada |
| Compra | Factura del proveedor a Muito Work Limitada | Proveedor |

### Solo o conjunto
- Conjunto significa mismo documento de transporte house (HBL o HAWB) impreso.
- Mismo contenedor o master con house distinto no es conjunto. Ejemplo: 2455 y 2456.
- En aéreo con AWB directo de la aerolínea (sin HAWB), ese AWB hace de house: dos proformas con el mismo AWB impreso son conjunto. Ejemplos: 2457/2458 (AWB 230-6683-2113), 2328/2342 (AWB 230-6534-9351). Lo mismo en marítimo con un solo BL: 2304/2322.
- Compartir OC, factura o agencia no une expedientes por sí solo.
- Manda el número impreso, no el del asunto.
- Si la agrupación cambió, registrar el cambio con su fecha; no borrar el plan anterior.
- Antes de tratar varias proformas como trabajos separados, revisar `fusion_label` y el HBL. Un conjunto es un solo embarque: arribo, aduana y costos del embarque se registran una vez, con la misma fuente en cada log. PO, SAP, precios y cobro siguen separados. Ejemplo: 2493, 2498 y 2505 con HBL JMVIX00262026.

### Proforma en varios envíos
Si una proforma salió en más de un envío (ejemplo: 2478 y 2478B), cada envío tiene su expediente, su AWB o BL y sus fechas. Al responder o proponer, decir de qué envío se trata; si el pedido no lo dice, preguntarlo.

### Conjunto: padre e hija
**Principio (decisión del CEO, 06/11/2026): al fusionarse, el padre hereda de la hija el monto y el inventario desde el despacho.** La hija conserva solo lo propio de su pedido: proforma, OC, SAP, packing por pedido, registro y producción. Todo lo demás se ve y se evalúa en el padre.

| Elemento | Padre | Hija |
|---|---|---|
| Factura comercial | Una sola, la que viaja con la carga, con el **total impreso completo**. No se reparte | Sin artefacto de factura; total facturado 0 |
| Cobro | El del conjunto: **pagos del padre + pagos de la hija** | Lo que tenga registrado cuenta para el padre |
| Inventario | Una sola transferencia con las líneas de los dos; se mueve una vez | — |
| AWB o BL, packing conjunto, DU-E, certificado, NF, cartas, cotización de flete | Una sola vez, en la carpeta y en mwt.one | No se duplican, ni siquiera como borrador |
| Salida, llegada, Tránsito, En destino, estado y cierre | Los del embarque | Los mismos del padre, con la misma fuente en los dos logs. Ejemplo: 2491 se cerró con el cobro de la FE 134 de su padre 2480 |
| Proforma, OC, SAP, packing por pedido, registro, producción | Los suyos | Los suyos |
| Nombre de carpeta | `<proforma> PO <OC> <mismo AWB o BL>` | `<proforma> PO <OC> <mismo AWB o BL>` |

- **Límite de mwt.one:** un pago ya registrado no se puede mover ni editar. Si quedó en la hija, se deja ahí y el saldo se evalúa en el conjunto. Se anota una vez en el resumen del padre: «cobro del conjunto = pagos del padre + pagos de la hija». Ejemplo: 2457 con 6.251,00 y 2458 con 906,75 suman los 7.157,75 de la factura del padre. No se pregunta.
- **Saldo aparente:** mwt.one sigue mostrando saldo por proforma (el padre con pendiente, la hija con exceso). Se explica en el resumen de los dos y no se registra un cobro para cuadrarlo. Si eso afecta reportes de cobranza, se informa a Alejandro.
- **Hija con artefacto de factura:** se deja con total 0 y sin publicar. No se elimina.
- **Padre e hija son una unidad** en el encargo: se leen, deciden, aplican y verifican juntos.
- **Quién es el padre:** el que tiene la factura y el AWB o BL en mwt.one; si no está claro, el de menor número. Se escribe en el resumen de los dos (`proforma_padre`, `proformas_hijas`).
- **Antes de tocar un conjunto,** leer los dos miembros, sus eventos y sus carpetas, y corregir los dos en la misma pasada. Verificar los dos al final.
- **Marca de conjunto (decisión del CEO, 08/11/2026):** cada miembro lleva en su log una fila `hecho` con id `LOG-CONJUNTO-<padre>` (el mismo id en todos) que dice: miembros, padre, documento de transporte, cómo va la factura y cómo se evalúa el cobro. El resumen de cada miembro lleva llenos `embarque`, `proforma_padre` y `proformas_hijas`. Se detecta con `fusion_label` de `expediente_obtener` más el HBL o HAWB impreso, y se marca en la misma pasada en que se detecta. Marcados el 08/11/2026: 2457/2458, 2480/2491, 2493/2498/2505, 2472/2486, 2393/2404/2428, 2400/2405.
- **Factura del conjunto según lo impreso:** si existe una sola factura impresa para el embarque, va completa en el padre y las hijas quedan en 0 (2457: USD 7.157,75). Si cada proforma tiene su propia factura impresa, cada una conserva la suya: no se suman ni se reparten (HBL JMVIX00082026: 2393, 2404 y 2428).
- **Expediente único con varias proformas:** mwt.one puede guardar dos proformas en un solo expediente (`proforma_codigos` con las dos). Consultar cada proforma devuelve el mismo expediente y los mismos montos: no es doble registro. Se comprueba con `proforma_codigos` antes de reportarlo. Ejemplo: 2400 y 2405, USD 40.198,05.
- **No se repregunta:** antes de presentar al CEO una diferencia de factura, saldo o cobro, leer la fila `LOG-CONJUNTO` y las filas `resolucion` del log de cada miembro. Si hay resolución del CEO, se aplica sin preguntar. Un pendiente que el CEO resuelve se cierra con una fila `resolucion` que cita el id del pendiente: un pendiente abierto en el log es lo que provoca la pregunta repetida.

## Compras para inventario
Tecmater y Bangni. Muito Work Limitada compra para inventario y vende con margen. La llave es el código de la orden: `MW-{PROVEEDOR}-{ORIGEN}-{DESTINO}-{NNN}-{AAAA}`, con destino `CR` si es marítimo o `SJO` si es aéreo.

- La orden del cliente (Génesis o Estefani, de Sondel) va dentro del expediente: no se abre una venta aparte.
- La carpeta se completa con DUA y costos relacionados.
- Una factura sin comprobante es deuda, no pago.
- Tecmater no está construido en mwt.one: mientras tanto, viven en carpeta, log y resumen, y la construcción se coordina con Alejandro. No inventar cómo se reflejará.
- Marluvas no se aplica aquí: ni SAP, ni Portal Marluvas, ni fases de Marluvas sin decisión del CEO.

## Log del expediente
`LOG_EXPEDIENTE_<proforma>.csv`, en la raíz del expediente. Debe permitir entender qué pasó sin volver al buzón. Es la lectura inicial de cada trabajo local.

**El expediente siempre se mantiene actualizado (decisión del CEO, 08/11/2026):** todo cambio, hallazgo o intento fallido sobre un expediente (en mwt.one, en la carpeta o en una revisión de conflictos) se escribe en su log y en su resumen en la misma pasada, antes de informar al CEO. Vale también fuera de un encargo y para los hallazgos sobre expedientes vecinos. Un hallazgo que solo queda en la conversación no cuenta como hecho. El resumen lleva `actualizado` con la fecha del día.

Columnas: `id_observacion, proforma, fecha, tipo_registro, quien, que_paso, por_que, resultado, pendiente, fuente, carpeta, uid, messageId, destinatarios, asunto, adjuntos, confianza, atencion`.

| `tipo_registro` | Qué registra |
|---|---|
| `comunicacion` | Quién informó o pidió qué, y a quién |
| `accion` | Lo que alguien hizo: emitir, pagar, despachar, corregir, subir |
| `resolucion` | Una decisión o la solución de un problema, con quién la tomó y por qué |
| `hecho` | Lo ocurrido con fecha: arribo, levante, entrega, retención |
| `problema` | Error, retraso, reclamo, diferencia, riesgo o pendiente, y cómo terminó |
| `correccion` | Corrige otra fila; cita su identificador y explica por qué |
| `estado` | Situación del expediente al cierre de una revisión |

### A quién le corresponde
Marluvas y sus agentes copian al CEO en correos entre ellos. Cada fila de correo lleva `atencion`, decidida **leyendo el contenido**: estar en «Para» o en copia no basta.

| `atencion` | Significado | Ejemplo |
|---|---|---|
| `te_corresponde` | Le escriben al CEO, le piden o preguntan algo, espera su respuesta, un cliente le escribe, o lo envía él | Eguisa pregunta por FCA; Backoffice pide validar un SAP; Bianca pide conferir comisiones |
| `relevante` | Conversación entre ellos sin pedido al CEO, con un hecho que cambia el expediente: factura, NF, DU-E, reserva, salida, llegada, cancelación, costo o problema de carga | Maycon ordena cancelar el booking; un agente informa cambio de vuelo |
| `comunicacion` | Conversación entre ellos sin hecho nuevo: acuses, recordatorios, coordinación, encuestas, reacciones | JM Logística confirma a Maycon lo que ya constaba |
| `revisar` | No se puede decidir con lo disponible | Texto cortado o `uid` repetido entre carpetas |
| `sin_correo` | Fila sin correo: acción interna o dato de otra fuente | Cambio en mwt.one |

- `te_corresponde` no significa pendiente abierto: algunos son avisos dirigidos a él o asuntos ya resueltos.
- Solo se presenta al CEO como pendiente suyo lo que es `te_corresponde` y sigue abierto. Lo que Marluvas gestiona con sus agentes (confirmación del armador, costo de una reserva) no se le atribuye.
- Un hecho `relevante` sigue siendo evidencia de fechas y estado; se cita diciendo entre quiénes fue.
- El `uid` puede repetirse entre carpetas: agrupar por `uid` y carpeta.

- Una fila por correo y otra por cada acción, resolución, hecho o problema que ese correo muestre, con el mismo `uid`.
- Texto redactado a partir del mensaje completo, no copia ni primera frase. Sin saludos, firmas, avisos legales ni hilo citado. Ejemplo malo: «Maycon, boa tarde!». Bueno: «Flávio Barbosa señaló que el documento dice FOB y preguntó si la carga se entrega en aeropuerto o se recoge en planta, y cuál es el destino».
- Conservar cifras, números de documento y nombres que ayuden a entender.
- Destinatarios y asunto van en sus columnas, no en `que_paso`. En `destinatarios`, separar `Para:` y `CC:`.
- La clasificación se hace leyendo el mensaje, no por palabras clave.
- `por_que` y `resultado` solo si constan.
- Fuentes: correo, documentos, bitácora, pagos, evolución de documentos, cambios en mwt.one, Portal Marluvas, archivos subidos y decisiones del CEO en conversación.
- `LOG_COMUNICACION_<proforma>.csv`, donde exista, se conserva como fuente.
- Si aún faltan los correos, el log lo dice en una fila `problema`.
- **Errores propios:** un cambio equivocado en mwt.one queda en el log de cada expediente afectado, con el valor restaurado.
- **Avería o faltante:** toda observación de almacén, sello o bultos va como `problema`, con el texto literal, y se sigue **Avería y seguro**.
- **Mensaje nuevo:** un correo se asigna por lo que nombra su mensaje nuevo o sus adjuntos. Excepción: un acuse corto ("Valor recebido", "Notado") se asigna con la referencia del mensaje al que responde. Ejemplo: uid 20032 confirma el pago de 2488.

## Fechas

### Por fase en mwt.one
| Fase | Inicio | Fin |
|---|---|---|
| Registro | **Fecha de registro** | La misma |
| Producción | Fecha de registro | **Fin de Producción** |
| Preparación | Fin de Producción | **Salida** |
| Despacho | Salida | La misma: no lleva tiempo ni suma al total |
| Tránsito | Salida del aeropuerto o puerto de origen | Llegada al aeropuerto o puerto de destino |
| En destino | **Fecha de llegada** | Reventa de Muito Work: **fecha de la FE al cliente**. Comisión y demás: **fecha de pago** (la misma del cierre) |
| Cerrado | **Fecha de registro** | **Fecha de pago**: muestra el ciclo completo, del registro al cobro |

- Preparación y Despacho son **una sola etapa**: el tiempo entre el fin de Producción y el día que vuela o zarpa. No se separan con ninguna otra fecha. En un marítimo puede durar 2, 3 o 4 semanas mientras llega el barco: eso no es un error.
- Producción empieza el día del registro. No hay etapa aparte de espera.
- Cerrado responde esta pregunta del CEO: si registro un pedido hoy, en cuánto tiempo lo cobro.
- Los días de Cerrado incluyen todas las fases anteriores: no se suman con ellas. Registro y Despacho tampoco suman al total, aunque mwt.one los muestre con 1 día.
- Cerrado empieza el día de registro y termina el día de pago. El estado pasa a CERRADO ese día de pago, nunca antes ni sin evidencia.
- Mientras no haya FE (reventa) o pago (comisión), En destino queda abierta y el estado en EN_DESTINO.
- Los tramos Producción, Preparación y Tránsito deben sumar el calendario de registro a llegada, sin huecos ni días dobles.
- En destino empieza el día de llegada. En reventa termina con la FE al cliente y Cerrado sigue abierto hasta el cobro; en comisión termina el mismo día que Cerrado, con el pago de la comisión.
- El estado interno se sigue llamando CERRADO. El cambio de nombre en pantalla lo decide y aplica Alejandro.
- Una `PREPARACION_DESPACHO` suelta que no coincide con este tramo se reporta y se quita solo con aprobación del CEO.

### Fecha de registro
El CEO envía la proforma y Backoffice registra el pedido. Esa secuencia no es un error. Un pedido también puede crearse en el Portal Marluvas con el usuario de Muito Work, sin correo. Ejemplo: 2515.

| Caso | Fecha de registro | Ejemplo |
|---|---|---|
| Regla general | `Data do documento` del xls SAP de Backoffice | 2472: `Criado em` 21/05, pedido para julio, `Data do documento` 21/07 |
| `Data do documento` queda después del fin de Producción | `Criado em`, sin marca de estimado | 2498: factura 03/09, `Data do documento` 05/10, registro 05/08 |
| Sin xls SAP | `Data do documento` del Portal Marluvas; se pide el xls | 2519: 26/10 |

- `Criado em` queda anotada en el log.
- Quien digita y registra por correo es Backoffice, no Marluvas.
- Con más de un SAP, usar el pedido original de esa proforma, no uno posterior. Ejemplo: 2484 usa 282455, no 290089. Un SAP cancelado no cuenta. Ejemplo: 2522 usa 298663, no 298635.
- No confundir el xls SAP con otros xls del expediente, como descarga o inclusión de cliente.

### Fin de Producción
En históricos no se reconstruye la fecha real de fábrica: estas reglas quedan cerca de lo real.

| Caso | Fin de Producción | Estado |
|---|---|---|
| Sin factura, o factura a 5 días o menos de la salida (aéreo) o a 10 o menos (marítimo) | Salida menos 5 días (aéreo) o menos 10 días (marítimo) | Estimado |
| Factura más lejos de la salida que esos 5 o 10 días | 1 día hábil antes de la factura | Estimado |

- Si el resultado cae sábado o domingo, se usa el viernes anterior. No se descuentan feriados.
- Ejemplos: aéreo con salida viernes 11/09: viernes 04/09. Marítimo 2472, factura 20/08 y salida 10/09: 19/08.
- Una fecha cierta de fin de Producción, si existe en correo o documento, prevalece.
- Una factura con fecha anterior al registro se revisa: puede ser otro documento.

### Salida
Tránsito va del día en que la carga sale del aeropuerto o puerto de origen (Confins, Viracopos, Santos o el que sea) hasta el día en que llega al de destino, según el AWB o BL.

Fuente, en este orden:
1. Itinerario en los correos: se toma la fecha propuesta; si un correo posterior la cambia, manda el último. Abrir las imágenes: el itinerario suele venir solo en imagen.
2. Si hay duda, rastreo en el sitio del operador por AWB, BL o contenedor. Copa Cargo: `https://copa.smartkargo.com/FrmAWBTracking.aspx?AWBPrefix=230&AWBNo=<8 dígitos>` (el buscador de copacargo.com abre esa ventana). Da reserva, aceptación, salida («Departed»), llegada («Arrived») y entrega con hora. Ejemplo: 2457 y 2458, AWB 230-6683-2113, salió de Confins el 29/06 01:30 y llegó a Tocumen el 29/06 06:17.
3. Si nada lo confirma: emisión del BL o AWB, marcada como estimada.

No son salida: la entrega de la carga en el aeropuerto o al forwarder (2457: 26/06; 2480: 28/08 en Confins, voló el 31/08), la emisión del AWB o BL, el booking o una reserva que después cambió (2277-2025: «no voló el sábado, vuela hoy» → 29/04), ni la fecha de la NF. Manda el último cambio. El vuelo CM734 despega de madrugada (00:20–01:40): la salida es el día siguiente al del itinerario. Antes de dejar salida o llegada pendiente, buscar en el propio LOG «partiu», «voou», «decolou», «embarcado», «chegou», «recepcionada» y rastrear el AWB en Copa. Los días de crédito corren desde la salida: es el día 1 de tránsito.

### Llegada
Se busca en este orden:
1. Correos: confirmación o primera señal de llegada (inspección, ingreso a almacén, recibo del cliente) es verificado o fecha máxima. Itinerario es estimado.
2. Rastreo en el sitio de la naviera o aerolínea, por BL, contenedor o AWB (ver **Salida**). La llegada es «Arrived», no la entrega al consignatario.
3. Salida más el promedio de tránsito verificado por medio de transporte, marcada como estimada.

Si el ETA aún no ha pasado y no hay señal de llegada, el expediente sigue en Tránsito. Ejemplos de mejor evidencia: 2410, primera señal de llegada; 2437, recibo del cliente; 2405, disponibilidad anunciada.

### Toda fecha estimada
La fecha sustituta o calculada lleva marca `estimado` en log, resumen y tabla. Se corrige si aparece un documento o correo que la muestre.

### Cierre con el pago
| Modalidad | Fecha de pago | Evidencia |
|---|---|---|
| Comisión | Día en que entra el depósito de la comisión | Hasta agosto de 2025 llegó a Promerica 1110 por el total del comprobante del mes menos USD 15; desde septiembre de 2025 llega a Payoneer por el total × 0,99. El depósito del mes M llega a mediados de M+1. En carga histórica sin depósito identificable, la fecha de cierre es el 15 del mes de emisión de la factura de comisión que incluye la proforma (ver **Cobro de expedientes históricos**). Un pago menor al 100 % puede deberse a un descuento por reclamo: se anota y no bloquea el cierre. Verificar en el comprobante de comisiones del mes (`OneDrive\06 Comisiones\01 Facturas de Comisiones`) qué proformas incluye; los xlsx de 2025 traen el contenido del mes siguiente, usar el PDF. Esos comprobantes no son facturas del sistema: citarlos por mes («comprobante de comisiones de julio 2026»), nunca por su número |
| Reventa | Día en que el cliente termina de pagar la FE | Comprobante o movimiento bancario |

Señales de un cierre falso: nota «Carga histórica», evento Producción → Cerrado, días que siguen sumando o una fecha de cierre anterior al pago del cliente. El estado CERRADO no prueba que el cierre sea correcto.

Expediente en CERRADO sin fecha de pago: en comisión liquidada por Bianca sigue en Cerrado y la fecha se pone al depositarse. En reventa con FE sin cobrar vuelve a En destino hasta el cobro, si mwt.one lo permite; si no, queda escrito como pendiente en log y resumen.

**Cobro de expedientes históricos (decisión del CEO, 08/11/2026):** el cobro no se da por registrado: se comprueba en estas fuentes.
- **Comisión: si no está en una fuente, está en otra.** Buscar en este orden y no declarar «sin comisión» hasta revisar las cuatro:
  1. Liquidación mensual de Bianca («Comissões – Referente ao mês …», la tabla viene como imagen). Es la verdad de monto y tasa: la tasa real puede no ser 5 % (2248+2249 al 1,55 %, 2339 al 4,12 %).
  2. Respuesta del CEO con la factura de comisión adjunta (`INBOX.Sent`).
  3. `OneDrive\06 Comisiones\01 Facturas de Comisiones` (desde marzo de 2022). Incompleta: falta, por ejemplo, la de marzo 2026, que está en Sent. Abrir el PDF; los xlsx son plantillas reusadas y pueden traer otro mes.
  4. Depósitos: Promerica 1110 hasta agosto 2025, Payoneer desde septiembre 2025.
  Las facturas de comisión traen etiquetas erradas («Ummie 2331» era 2339) o sin número («Distribuidora Comtek 708,18»): identificar la proforma por valor pagado × tasa. Una factura comercial puede agrupar varias proformas (la 2190-2024 incluye la línea de la 2196): abrir la factura firmada y el comprobante o SWIFT del cliente antes de asignar una línea de comisión. Fecha de cierre: el depósito si aparece en los estados; si no, el 15 del mes de emisión de la factura de comisión, marcada `estimado`.
- **Reventa:** la FE de Muito Work Limitada al cliente figura `Pagada` en la contabilidad (`C:\repos\contabilidad-mwt\02_ATV\ATV_Ventas_*.xlsx`) y, desde noviembre de 2024, con su crédito en `01_ESTADOS_BANCARIOS`. Fecha de cierre: la del crédito; sin estado bancario del período, se anota la FE pagada y la fecha queda pendiente.
- **Sin evidencia en ninguna:** antes de anotarlo, cruzar el resumen de la carpeta con los correos de cobranza de Bianca al cliente y con los acuerdos posteriores (notas de crédito, descuentos negociados). Si aún no aparece, no se cierra: queda como cobro sin evidencia en log y resumen, con la pregunta concreta para Bianca.
Cruce vigente: `C:\Users\alvar\.claude-server-commander\cobro_cruce.csv` (`cobro_cruce.py`).

Un reclamo abierto no impide cerrar con el pago: queda escrito como pendiente en el log y el resumen, y se informa al CEO.

### Tiempo de cobro
No se mide con una sola fase. Calcular con las fechas y dejar en el resumen:

| Medida | Qué muestra |
|---|---|
| Registro → pago (Cerrado) | Cuánto tarda en cobrarse un pedido desde que se registra |
| Salida → pago del cliente | Días de crédito consumidos: corren desde el día 1 de tránsito |
| Pago identificado → comisión cobrada | Cuánto tarda Marluvas en pagar |

No afirmar que un cliente pagó dentro o fuera de plazo sin tener la fecha de salida.

### Fechas que se confunden
| Hecho | Fuente correcta | No usar |
|---|---|---|
| Arribo real | Correo de la agencia que confirma la llegada | Aviso de llegada o frases como "se mantiene para" y "estimado" como si fueran reales: traen una fecha programada; solo sirven marcadas como estimadas |
| Ingreso a almacén y descarga | Correo de la agencia o del almacén | Fecha que marca el sistema de la naviera |
| Levante | DUA impreso | Autorización de retiro |
| Salida real | Vuelo o zarpe confirmado | Fecha de emisión del BL o AWB, cuando hubo reprogramación |
| Fecha de pago | Depósito o movimiento bancario | Fecha de carga en mwt.one o fecha marcador de un pago |

### DUA de tránsito
Régimen 80 o tipo TRANSITO no nacionaliza. Se registra con número y fecha, indicando en el número que es tránsito; no se pone monto ni cierra fase. "Pago Impuestos: Pago" en ese DUA no prueba pago de nacionalización. El ingreso a almacén fiscal tampoco es nacionalización.

## Facturas, totales y pagos

### Factura comercial: la de Muito Work (decisión del CEO, 09/11/2026)
En la tarjeta **Documentos comerciales** de mwt.one, `kind = FACTURA` es la factura que emite **Muito Work Limitada**, no la de Marluvas ni la del proveedor.
- **Reventa:** la FE de Muito Work al cliente.
- **Comisión:** la factura por servicios de Muito Work a Marluvas; es mensual y puede cubrir varias proformas.
- La factura de Marluvas o del proveedor **no se sube como `FACTURA`**: va como `OTRO` si hace falta tenerla en la tarjeta, o se queda solo en la carpeta `Factura`.
- Si la factura de MWT no existe, se genera desde la consola (ver `mwt-one-operar`) o se registra el faltante; no se sustituye por la de Marluvas.

- Una factura no es un pago. En `pagos.csv` y en el resumen, cada fila lleva `tipo_registro`: `factura_emitida`, `factura_recibida` o `pago`.
- Solo es `pago` con comprobante o movimiento bancario. Una factura recibida sin comprobante se escribe "sin pago comprobado".
- `total_invoiced` suma `field-0118` de **todas** las facturas comerciales del expediente, publicadas o no. Despublicar no lo cambia. Por eso se ajusta el campo:
  - **Reventa:** la FE al cliente lleva el total con IVA y la factura Marluvas queda en 0. Mientras no exista FE, el valor se deja, se dice que es costo y no se toma como venta.
  - **Conjunto:** el padre lleva el total y la hija queda en 0. En reventa, el total del padre es el de la FE. Sin padre confirmado, no se toca.
- **Factura vigente:** la última emitida a ese comprador por esa venta, según el documento impreso. Excepción: si el comprador decidió usar una versión anterior y el pago cuadra con ella, manda esa. Ejemplo: 2465-2026 (USD 5.258,85) frente a 2465-2026A (5.275,35): Sonepar importó con la inicial y pagó 5.258,85 menos la nota de crédito de 500.
- **Nota de crédito:** reduce lo cobrado, no la factura. La factura conserva su total impreso y la nota se registra como pago `NOTA_CREDITO` contra ella. Mientras no se pueda registrar, el saldo que muestra mwt.one se explica en log y resumen como la nota de crédito, no como deuda.
- **Cartera:** corregir un total contra la factura vigente está autorizado. Registrar un cobro con comprobante, estado de comisiones o nota de crédito vigente, también; conciliar, no. Si la factura vigente no existe o dos versiones se contradicen, no se toca el total: se deja para el CEO.
- Cada ajuste consta con valor anterior, valor nuevo y efecto en saldo.
- **Moneda:** un total en reales de la NF no se escribe como total en USD. Ejemplo: 2410 tenía 60.225,68 de la NF 270175 donde correspondían USD 11.578,30.
- **Comisión:** la real es la del estado de Marluvas, sobre lo acreditado. La de mwt.one se calcula sobre lo facturado y puede diferir.
- **Total y saldo (decisión del CEO, 08/11/2026, conflicto 1):** la factura lleva siempre su total impreso (factura vigente). El saldo que muestre mwt.one se explica por su forma y se cierra con el movimiento que le corresponde; no hay una regla única de «sin total»:

| Forma | Cómo queda | Ejemplo |
|---|---|---|
| Pago completo | Pagado = total | 2429, 2452, 2463 |
| Envío conjunto | Total completo en el padre, hija en 0; cobro = pagos del padre + pagos de la hija; el saldo aparente se explica con `LOG-CONJUNTO` | 2457/2458 (906,75 en la hija); 2480/2491 |
| Nota de crédito | El total no cambia; la nota se registra como pago `NOTA_CREDITO` con su número vigente; pagado + nota = total | 2465: NC CO-0002-2026 por 500 (la CO-0001 se invalidó) |
| Descuento por reclamo aplicado en otra proforma | El total no cambia; el descuento se anota aquí y se registra en la proforma donde se aplicó | 2437: faltante 631,31 descontado en la PF 2505 |
| Marluvas acreditó menos de lo transferido | No se registra un cobro para cuadrar; se escribe la diferencia | 2410 (20,00), 2437 (104,50) |
| Cliente pagó de más | Se anota como crédito a favor del cliente, con la proforma donde se usa | 2414 |
| Reventa con margen | El total es el de la FE al cliente; la factura Marluvas va en 0; la diferencia es margen por arbitraje, no un saldo | 2480, 2455 |
| Aún no cobrado | Saldo normal mientras el pago no ocurre | 2472, 2493 |
| Factura CIP o CPT | El total impreso = mercadería + seguro + flete, mayor que el pedido; no es diferencia ni se corrige. El monto del pedido sigue siendo el de la proforma | 2296 (24.232,85 + 86,00 + 1.645,41 = 25.964,26), 2376 |
| mwt.one no deja registrar el pago o la nota (409) | El total se carga igual; el saldo se explica en log y resumen con el pago o la nota pendiente de registrar y su fuente | 2355, 2465 |

Un saldo que no encaja en ninguna forma se investiga en el correo y en los estados de comisión antes de informarlo; no se deja sin explicación.
- **Saldo pequeño con «Pago total»:** si el cliente transfirió el total y Marluvas acreditó menos, no se registra un cobro para llevarlo a cero. Se escribe la diferencia y se informa. No suponer su causa sin documento.
- **Facturas de agencias en colones:** van en plantilla 24 sin monto, porque el campo no indica moneda. El monto queda en el log y el resumen.

## Reventa

### Margen de reventa
En reventa, la diferencia entre lo que Muito Work Limitada paga a Marluvas y lo que factura al cliente es margen por arbitraje (decisión del CEO, 07/11/2026). Es lo esperado: no se presenta como conflicto. Ejemplo: 2480.

### Dos órdenes para una misma venta
La **PO 50xxxx** es Sondel a Marluvas y fija el pedido y el precio base. La **OC 20xxx** es Sondel a Muito Work Limitada, se emite después y sustituye a la PO para facturar. Que coexistan es lo esperado. Ejemplos: 2473 PO 505107 y OC 20973; 2453 PO 504990 y OC 20131; 2454 OC 20159; 2480 y 2491 OC 20330. `unit_price_client` guarda el precio de la PO, no el DDP: es correcto.

### Dos realidades en mwt.one
| Capa | Interno | Cliente | Qué controla |
|---|---|---|---|
| Precio por línea | `unit_price_mwt` | `unit_price_client` | El rol, según la guía de mwt.one |
| Documentos | `ADMIN_ONLY`, `MWT_INTERNAL`, `FABRICA` | `CLIENT` | La audiencia de cada documento |
| Artefactos | Sin publicar | Publicados | `publicado` |
| Factura del sistema | `Factura_TRF-…_MWT` | `Factura_TRF-…_CLIENTE` | La audiencia |
| Proforma | Versión interna | `proforma_generar` con audiencia `CLIENT` | La audiencia |
| Costos de transferencia | `price_view=MWT`: costo real | Sin vista cliente comprobada | No exponer; `transfer_liquidacion_preview` es interno |
| Portal | — | `portal_embarque`: cantidades, fechas, salidas, AWB, documentos `CLIENT` | Filtro del portal |

- `operated_by_mwt=true` identifica las ventas operadas por Muito Work Limitada.
- La emulada vive en la Liquidación DDP (plantilla 39). `price_view` existe en `transfer_costo_agregar`, pero sus valores no están documentados: no usarlo para la emulada sin confirmarlo con Alejandro.
- Con token admin, `unit_price_for_viewer` devuelve el precio interno. Eso no prueba lo que recibe un cliente.
- Sin usuario de prueba con rol de cliente, informar "visible por audiencia o publicación", nunca "comprobado como cliente".
- `factura_payload` y el portal pueden traer transferencias de prueba (`FIXTRF-…`, `AWB-FIXTURE`). No tomarlas como dato. Reportarlas a Alejandro; no eliminarlas.

### Documentos para el cliente
- **Documento final:** Liquidación DDP (plantilla 39), con la FE al cliente como respaldo fiscal.
- **Construcción:** corre en paralelo hasta la llegada a Costa Rica, con el precio de la orden del cliente, flete y seguro. La nacionalización va como se emitió con la factura. No se reescribe con costos reales.
- **Formato:** mantiene el formato visual de la pestaña DDP SONDEL de las proformas.
- **Redacción:** no dice "real" ni cita números de DUA, naviera o agencia.
- **Monto:** manda la FE. Si la referencia difiere por redondeo, se muestra y se aclara.
- **Corrección:** el documento corregido se sube como archivo nuevo del mismo artefacto, sin publicar, y el anterior queda en disco.
- **Nombres:** Liquidación DDP es la del cliente. Liquidación de DUA es de la agencia y es interna.

| Documento | Cliente | Condición |
|---|---|---|
| Liquidación DDP en PDF, FE al cliente | Sí | Solo con precios emulados |
| Packing, BL o AWB, certificado emitido | Sí | Sin precios ni costos |
| Factura Marluvas, NF-e o DANFE, DU-E, DUA, impuestos | No | — |
| Facturas de agencias, navieras y transporte, comprobantes | No | — |
| Proforma HTML | No | Contiene arbitraje y margen; nunca se sube ni se publica tal cual |
| Costo real, margen, conciliaciones, resumen y log | No | Interno |

Un BL con cargos de flete impresos se revisa antes de publicar. Publicar un artefacto expone también sus campos adicionales: revisarlos todos antes.

### Revisión por capas
Hacerla al terminar un expediente de reventa y al cambiar lo publicado:
1. **Documentos:** `documento_listar` por expediente. Cada uno con audiencia `CLIENT` se revisa por dentro. Si abrirlo exige un enlace firmado, pedir autorización al CEO; mientras tanto queda "sin revisar".
2. **Artefactos:** leer `data` real de cada publicado, con todos sus campos de archivo.
3. **Portal:** `portal_embarque`: cantidades contra BL y packing; ningún `FIXTRF` ni dato interno. Si la diferencia viene de una transferencia de prueba, es tema de plataforma: va a Alejandro.
4. **Coherencia:** FE, Liquidación DDP y proforma `CLIENT` cuentan el mismo precio.
5. **Resultado:** cada capa queda `correcta`, `a corregir` o `sin revisar` en la entrega; `expediente-carpeta` lo pasa al resumen y al log.

## mwt.one: qué revisar
Comparar por tipo de documento y revisar estos campos, que suelen traer errores:
- Cada fecha de fase contra la tabla de fechas.
- `total_invoiced` y `total_paid` contra factura y cobro reales.
- `shipment_date` y `eta` contra salida y arribo reales.
- Resumen de envío: un courier de documentos puede aparecer como transporte de la carga.
- Transferencias: `ref_tracking` debe coincidir con la guía.
- Más de un documento OC con códigos distintos.
- Archivos de artefactos publicados: que el archivo sea el documento correcto. Ejemplos: factura comercial que abre la NF en reales; certificado publicado en borrador cuando ya existe el emitido.
- Fecha marcador en un pago: se lee en sus notas.
- En un conjunto, que las fases, fechas y días coincidan entre sus miembros.
- Fechas de relleno: todas las fases con la misma fecha o Producción con 0 días. Ejemplos: 2466 y 2493.
- Fin de En destino a los 120 días exactos de la salida: es el cálculo de mwt.one, no una fecha real.

No eliminar fases sueltas sin aprobación del CEO.

## Documentos exigidos
Proforma, OC y SAP desde el registro. Factura Marluvas, packing, guía y certificado de origen desde el tránsito. El aviso de que el embarque salió se exige; el aviso de arribo no, porque va al cliente o dueño de la carga.

| Modalidad | Además exige | No aplica |
|---|---|---|
| Comisión | Comprobante de pago del cliente, estado de comisiones y factura de comisión al cobrarse | DUA, impuestos, FE de venta |
| Reventa FULL | DUA, impuestos, gestión de agencia, pago a Marluvas, FE, Liquidación DDP | Factura de comisión |
| Compra para inventario | Orden de compra, orden del cliente si existe, factura del proveedor, guía, DUA, costos y comprobante de pago | SAP, comisión |

Clientes sin OC propia (UMMIE, Comtek, Importaciones y Compras, y pedidos registrados por el CEO) usan el código `{PRV}-{CLIENTE}-{PAÍS}-{NN}-{AA}` de `POL_CODIGO_OC`: su OC del cliente no se exige, pero **desde el 09/11/2026 se sube como documento `OC` el Excel o correo con que pidieron** (audiencia `MWT_INTERNAL`, marcado como respaldo del pedido), para que la tarjeta no quede vacía. La carpeta lo guarda en `OC del Cliente`.