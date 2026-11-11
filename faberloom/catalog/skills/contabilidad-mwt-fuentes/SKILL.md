---
name: "contabilidad-mwt-fuentes"
description: "Contabilidad de Muito Work Limitada: dónde vive cada dato (canon, D-101/D-150, bancos, correo, Drive, repo), cómo interpretarlo, qué no inventar y cómo resolver pendientes. Cargar al tocar cifras, cierres, pendientes, expedientes de crédito o entregables a terceros."
---

# Contabilidad de Muito Work Limitada — mapa de fuentes, reglas operativas y resolución

Entidad: Muito Work Limitada, 3-102-751710. "MWT" es Muito Work Trade ONE, la sociedad panameña (no consolida); no se usa como abreviatura de Muito Work Limitada. En documentos antiguos del canon, "MWT" se refiere a la costarricense. Moneda funcional USD. TC: saldos al cierre con el de compra BCCR a la fecha de corte; compras del exterior con el de **venta** BCCR del día de cada cargo (serie 318). Nunca estimado ni promediado. Todo output con montos declara el libro (interno / fiscal).

Espejo de `SKILL_CONTABILIDAD_MWT` §11–§13 (v1.3) y de `PLB_DOCUMENTACION_CONTABLE_MWT` (v1.7, lecciones L1–L41). Reparto: dato → canon (git); dónde buscar, cómo leer y cómo resolver → este skill.

## 1. Orden de búsqueda (antes de pedir nada al CEO)

1. `canon/IDX_CONTABILIDAD` en el proyecto Claude — router. Su última §Corrida manda sobre lo anterior.
2. El `ENT_`/`POL_`/`DELTA_` del tema. Si dos docs se contradicen, gana el más reciente y se declara.
3. `project_search` con el número de factura, DUA, FE, casilla o monto exacto. El canon suele tener ya el dato.
4. Evidencia propia: buzones, estados y expedientes del repo (§2).
5. Solo entonces pedir un insumo — **uno a la vez**, nombrándolo (archivo, no categoría).

## 2. Dónde vive cada dato

| Dato | Fuente correcta | Trampa |
|---|---|---|
| Balance histórico (31-12) para terceros | **D-101** del período: casillas 20–26 traen efectivo+CxC, inventarios, activo fijo, total activo, pasivo, capital neto. ER en casillas 27–47 | No reconstruirlo desde ATV/FE: el evaluador ya tiene la declaración y cualquier cifra distinta descuadra contra ella |
| Ventas mensuales | D-150 (IVA) casilla "ventas 13 %" = base sin IVA. Serie en `ENT_D150_2026` | El formulario de IVA 2025-2026 es **D-150**, no D-104 (D-104 solo períodos ≤ 2024). No tiene casilla de importaciones |
| FE recibidas que entran a la D-150 | Reporte "Compras recepción" de **Factura Profesional** | El buzón `506@` no es la declaración: FE sin aceptar en FP no dan crédito (sep-2026: 3 FE, IVA ₡30,001.78) |
| Ingresos del exterior (comisiones Marluvas, Best Doctors) | FE de exportación de servicio emitida por Muito Work Limitada + crédito bancario | Crédito del exterior sin FE = ingreso sin comprobante. Best Doctors es comisión, no reembolso |
| Saldos bancarios | Estados Promerica (1110 USD, 1111 USD bóveda, 1112 CRC) y Payoneer `Transactions_MM-YYYY.csv` (1115, titular Muito Work Limitada). Leer **"Saldo Parcial Actual"** | Nunca "Total Débitos". Cambios de moneda entre cuentas propias no son ingreso |
| CxC Sondel | Facturas vivas en `ENT_COBROS_FACTURA_128_SONDEL` + reporte Ventas FP / TicoFactura; cobros por avisos Davivienda y créditos 1110/1112 | El sello "PENDIENTE" de una FE es estado de emisión, no prueba de impago. Una FE anulada se refactura con otro número: anotar el vínculo |
| CxP proveedor exterior | Factura comercial Marluvas/Tecmater + SWIFT Promerica ("Aplicación de transferencia Hacia el Exterior exitosa", `solucion@promerica.fi.cr`, buzón `alvaro@`), leyendo el campo **:70:** | Plazo pactado (90 d desde B/L) ≠ plazo usado (~15 d). "Pagado" se afirma solo con SWIFT, banco o estado de cuenta del proveedor |
| Importaciones | Factura comercial + B/L o AWB + DUA en firme (Consulta de Impuestos TICA) + liquidación y FE de la agencia | Cuadrar DUA contra factura (bultos, kg, CIF): el DUA 610706 sumó el seguro dos veces |
| Inventario | Factura + flete/seguro + tributos no IVA del DUA en firme. IVA de importación = crédito fiscal, nunca costo | Un lote no puede estar en inventario y en CxC a la vez: verificar si ya se facturó |
| Comisiones Marluvas | Hoja de comisiones del CEO (PTAX del día 1 del mes siguiente) + créditos Payoneer al 99 % | No pasan por ATV; en 2024-2025 no están en la base D-101 |
| Soporte de cada movimiento | Matriz de 17 tipos en `PLB_DOCUMENTACION_CONTABLE_MWT` §2 | Clasificar antes de tener el papel produce retrabajo |
| Datos registrales | Certificación RNP (capital, notario, domicilios, gerentes, plazo) | No se maquillan. En CR hay notarios, no notarías |
| Logo y firma | Google Drive: `Logo-Muito-Work-horizontal (nuevo).png`, `Firma Trasnparente.png` (buscar por título con el MCP de Drive) | La ruta OneDrive solo sirve con el bridge a la PC |
| Correo `alvaro@`/`506@` | MCP Hostinger vía la PC: `messages_search` (remitente, asunto), `messages_text`, `messages_attachment`; los resultados grandes llegan como JSON con body base64 | **Sí lee mensajes y adjuntos** (corrige la versión anterior). Gmail MCP solo ve `sjoalfaro@` y no baja adjuntos. Ninguno se usa para enviar ni reenviar |
| Recibos de proveedores del exterior (IA, SaaS, hosting) | `sjoalfaro@gmail.com` (MCP Gmail) mientras no se cambien los perfiles de facturación a Muito Work Limitada con `alvaro@` | Payoneer cobra 1 % sobre el precio: la base es el recibo, no lo cobrado |
| Reservas de viaje | Cuenta Expedia: "Trips → Past" dice qué se compró ahí; "Pricing and rewards" da lo **Pagado** | "AVIANCA.COM" en el estado = compra directa, no Expedia. Cargos extra de aerolínea (equipaje, asiento) no dejan recibo en el correo |
| TC BCCR histórico | Herramienta `sicop_bccr_tc` (fecha → compra 317 y venta 318); tabla en `01_ESTADOS_BANCARIOS/tipo_cambio/` | No usar el TC que propone Factura Profesional para cargos de otras fechas |
| Compras del exterior registradas | Factura Profesional → Compra → Del exterior (LCE y LV) | `Compra → Por proveedor` es FEC para proveedores **locales** excluidos, no para el exterior |
| Canon versionado | `C:\repos\contabilidad-mwt` (git, remoto `sjoalfaro/contabilidad-mwt`) — **no existe en esta PC**: el repo no está clonado aquí. `C:\MWT` = cadena determinista, no encontrada desde la reinstalación del 07-09 | El conector GitHub de Cowork no ve el repo privado (404) |

## 3. Interpretación

- Quien factura al cliente define el tratamiento: Muito Work Limitada factura = venta con COGS; Marluvas factura = comisión. Cuando el fabricante factura fuera de CR, Muito Work Limitada no exporta bienes; la comisión que Muito Work Limitada cobra sí lleva su FE de exportación de servicio.
- Un desembolso = una deducción. Flete dentro del CIF del DUA o ya capitalizado no se carga otra vez: su pago posterior es `PAGO_CXP`.
- Sin comprobante a nombre de 3102751710 → 3300, nunca gasto. Tiquete sin receptor = sin crédito ni gasto.
- Una FE con fecha de hoy puede cubrir meses atrás (Paseo emitió 4 rentas en lote): leer el detalle.
- Casillas D-101 2024 mal llenadas por el contador anterior (ingresos en "servicios profesionales", costo sin compras/inventario): error de formulario, no de cifra. Presentar con etiqueta contable, monto intacto.
- Pasivo redondo declarado (₡20,000,000 en 2025): no inferir su composición. `[PENDIENTE — NO INVENTAR]`.
- Dato ausente = `[PENDIENTE — NO INVENTAR]`. Nunca rellenar con lo plausible.

## 4. Cierre mensual (Ruta B mientras no exista la cadena)

1. Tie-out por cuenta al céntimo: saldo anterior + créditos − débitos = Saldo Parcial Actual. Un desvío detiene el cierre.
2. Traslados internos por número de documento, no por monto.
3. Ingresos contra FE emitida o aviso de cobro; egresos contra la matriz del PLB.
4. DUAs: IVA → crédito; DAI + 6946 + timbres + PROCOMER → costo 1300.
5. CxC / CxP / inventario al cierre solo con documento o declaración del CEO.
6. Fiscal: cotejar contra el acuse de la D-150 presentada; lo que faltó va a una hoja de rectificación. Nunca se edita lo presentado.
7. Salida: `ENT_CIERRE_AAAA_MM` (conclusiones primero) + `DELTA_` (decía / dice / fuente) + §Corrida en el IDX + commit/push + subida al proyecto + `indexa`.

## 4bis. Compras del exterior y gastos de viaje

- **Servicios del exterior:** sin FEC. **LCE** (Liquidación de compras al exterior) por proveedor y por mes, fechada dentro del mes, firmada por el apoderado: cada cargo con referencia bancaria (texto del estado, SWIFT ref. + `:70:`, ID Payoneer), base = recibo, IVA 13 % autorrepercutido, TC BCCR venta del día, resumen mensual para la **D-150**. Script `04_GESTION_INTERNA/fec_2026/liquidaciones_proveedor.py`.
- **Solo lo efectivamente pagado.** Compensaciones (ej. cuota de una computadora) se definen aparte (D34).
- **Viajes:** **LV** por viaje al terminarlo. Motivo lo da el CEO; el agente verifica fechas de ferias y origen de la compra. Parentesco con la persona visitada se declara. Viaje familiar, aerolínea sin recibo, compras y recreación → 3300. Copa va con su FE. Script `04_GESTION_INTERNA/viajes_2026/liquidaciones_viaje.py`.
- **Registro en FP (Compra → Del exterior):** proveedor "Otro/Extranjero (Sin identificación)" con país y dirección (pedir teléfono y correo al CEO); N° = número LCE/LV; actividad 511001; rubro Servicios; Gravado 13 % (servicios) o Exento (viajes); no marcar "Aplica al cobro de IVA en tarjetas". Uno de prueba sin guardar, se muestra, luego el lote; al final, listado = índice.
- **Fechas reales.** Un rezago se documenta con la fecha de elaboración y una nota de regularización; nunca se antedata.
- **Texto fiscal:** el IVA 2025-2026 es **D-150**. Releer las lecciones del PLB antes de fijar texto en un documento que se firma.

## 5. Resolución de pendientes

Ciclo, en orden y sin saltar pasos:

| Paso | Qué |
|---|---|
| 1 · Canon | IDX → ENT/DELTA → `project_search` por número o monto |
| 2 · Evidencia propia | buzones, estados, expedientes; el soporte se guarda en `cierre_AAAA_MM\soportes\` |
| 3 · Una pregunta al CEO | **una**, cerrada, con monto, fecha y las opciones que cambian el asiento |
| 4 · Papel faltante | redactar el correo al emisor (localizador, número, monto, cédula 3-102-751710, `506@`) y **entregarlo sin enviar** |
| 5 · Registrar | `ajustes_ceo_<mmdd>.py` que modifica `clasificado_*.csv` por (cuenta, fecha, monto) con `assert` de unicidad y reconstruye la hoja de trabajo |
| 6 · Canon | si contradice un documento: corrección explícita en el `DELTA_` |

Cierre del pendiente: papel + categoría + libro, o decisión del CEO con fecha y razón (va a 3300).

Por tipo: crédito del exterior sin FE → emitir FE de exportación · cargo sin identificar → ¿empresa o personal?, 3300 a los 7 días sin respuesta · FE en buzón no aceptada → aceptarla en FP · tiquete → pedir FE · pago al exterior → factura + SWIFT `:70:` · FE "pagada" sin banco → estado del proveedor, se corrige el canon · varias FE con un pago → ¿qué meses cubren? · declaración con error → acuse y rectificación.

Al recibir una respuesta del CEO: procesarla entera y hacer **la siguiente** pregunta, no la lista de todo lo que falta. Cada corrección del CEO se escribe al canon en la misma sesión con la regla que deja.

## 6. Entregables a terceros (Del Risco, aseguradoras, bancos)

- Llenar el machote del tercero en su formato; no sustituirlo por uno propio.
- Un solo TC para todas las columnas, declarado una vez. Cada período en su moneda de origen (₡ para lo declarado, US$ para lo gerencial) y la otra como equivalente; color por moneda y leyenda.
- Tabla "base de cada columna" antes de las cifras: fuente, moneda, conversión.
- Ninguna línea gerencial puede ser menor que la misma línea del estado fiscal que el tercero ya tiene.
- Nada "por remitir" en lo que se envía: si falta, pedir el documento antes.
- Logo en carta y anexos propios; firma solo donde el fondo la deja ver. Aptos en `.docx`; el CEO genera el PDF desde Word.
- Todo lo enviado va a `03_ENTREGABLES\<AAAA-MM>_<Tercero>\` con sus scripts, y a un `DELTA_` con cifras, correcciones del CEO y pendientes.

## 7. Infraestructura y hábitos

- Archivos a la PC con `device_commit_files` (stagedPath en `/mnt/user-data/outputs/`). Si se reescribe el mismo archivo dos veces seguidas, verificar la versión en disco antes de commitear.
- Git en la carpeta conectada necesita permiso de borrado (archivos `.lock`): pedirlo una vez por sesión.
- `git config user.name/email` local antes del primer commit. `git add` por archivo; una ruta inexistente aborta el comando entero, así que los nuevos van en un `add` aparte. Nunca `git add -A`. Mensaje ASCII.
- El `push` no sale desde la VM del puente (sin credenciales): hacerlo con Desktop Commander en PowerShell de Windows: `git -C C:\repos\contabilidad-mwt push origin main`. Desde el contenedor de la nube (`/home/claude/contabilidad-mwt`) el push sí sale; después, `git pull` en la PC con Desktop Commander y `project_write` con `local_path`. En esta PC `C:\repos\contabilidad-mwt` no existe: clonar el repo antes de cualquier `git`.
- Factura Profesional por navegador: `javascript_tool` corta a los 45 s; los lotes corren en segundo plano con un log y no se toca la pestaña mientras tanto.
- Antes de escribir el IDX: comparar versión en disco contra proyección; si la proyección va adelante, bajar sus documentos al repo en el mismo commit.
- `indexa` = 0 huérfanos contra la lista real de la proyección **y** del disco; headers con id/version/status/stamp/visibility/domain/refs.
- Cuando el bridge a la PC cae no se recupera en sesión: pasar a zip + bloque PowerShell, no reintentar. Zip con nombre único por versión y SHA256 verificado en la PC; el mismo nombre en Descargas = versión vieja silenciosa.
- PowerShell 5.1 rompe con guion largo o tildes en `.ps1`: bloques en ASCII; sin `$` en línea por el puente (usar `.ps1`).
- Nunca enviar ni reenviar correos: redactar y entregar al CEO.

## 8. Límite

No construir asientos, notas ni estados que sostengan una base imponible incompleta, ni documentación que un contador firmaría sin ver lo que la contradice. El criterio fiscal (deducibilidad, exportación exenta o gravada, IVA de servicios importados, retenciones) es de Alexander Solano; mientras no haya contador firmante, el CEO firma como apoderado los criterios de `POL_CRITERIOS_EXTERIOR_2026`, cada uno con su fundamento y lo que lo contradice. El resto — reconstrucción, deducciones, cuadres, expediente de crédito — sin restricción.