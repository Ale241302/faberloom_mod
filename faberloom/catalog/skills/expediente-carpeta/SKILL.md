---
name: "expediente-carpeta"
description: "Cómo escribir el log y el resumen de un expediente de Muito Work y colocar documentos nuevos con respaldo y hash. Estructura, nombres y versiones de la carpeta: ordenar-expediente. La llama reconstruir-expediente."
---

# Expediente: carpeta

v1.3 · 2026-11-09 · La fila del alta cita el código de OC asignado (`MAR-…` o el del cliente) y el siguiente de la serie. v1.2 · 2026-11-09 · Cada documento de la tarjeta Documentos comerciales deja fila con id, tipo, audiencia y código; `factura_propia` es la de Muito Work. v1.1 · 2026-11-08 · Estructura de subcarpetas, nombre final y versiones pasan a `ordenar-expediente`, que es su única dueña. v1.0 · 2026-11-06 · Parte del harness de expedientes. La entrada es `reconstruir-expediente`.

## Contrato de esta skill
- **Recibe:** un encargo, las filas de la ficha con `destino = carpeta`, `log` o `resumen`, y `FICHA_LOG.csv`.
- **Devuelve:** `ENTREGA_carpeta.csv` con `fila_id` y, según el paso, `valor_actual_carpeta` (lectura) o `valor_leido_antes, valor_final, resultado, mensaje` (escritura).
- **Escribe en el disco** solo con un encargo en modo `escritura` y solo las filas `aplicar` o `crear`, siempre con respaldo previo. No edita la ficha.
- **Se detiene:** si un archivo de origen ya no coincide por hash, si una ruta no existe, o si el log o el resumen cambiaron desde la lectura.

## Log y resumen
- Cada cambio se escribe con un script en `C:\Users\alvar\.claude-server-commander\` que respalda antes en `respaldos\`, agrega filas al `LOG_EXPEDIENTE_<proforma>.csv` respetando su encabezado y sus saltos de línea, y actualiza el `RESUMEN_<proforma>.md`.
- Las filas del log salen de `FICHA_LOG.csv`. Su formato y la columna `atencion` están en `expediente-reglas`.
- Un cambio C1 deja en el log su registro breve: pedido, campo, antes, después, fuente y verificación.
- Cada documento subido o generado en la tarjeta Documentos comerciales deja una fila `accion` con el id del documento, el tipo, la audiencia y el código; si se desactiva un duplicado, una fila `correccion`.
- Cuando el alta asigna una OC (código `MAR-…` de la ficha o el número del cliente), la fila `accion` cita el código asignado y cuál es el siguiente de la serie por marca.
- En un conjunto, el resumen del padre lleva la línea «cobro del conjunto = pagos del padre + pagos de la hija» y la lista de hijas; el de cada hija nombra a su padre.

## Disco

Estructura de subcarpetas, nombre final de la carpeta y versiones: `ordenar-expediente`. Un documento nuevo se coloca en la subcarpeta que esa skill indica y con sus reglas de nombre. Lo interno marcado «NAO MOSTRAR» o «venda triangular» se conserva y consta como interno. Cada movimiento queda en `REGISTRO_COLOCACION.csv`.

### Proformas conjuntas
En disco no se anidan; dónde va cada documento compartido lo dice `ordenar-expediente`. Si cambia la agrupación, se ajustan la unión en mwt.one, los nombres y los resúmenes; solo se mueven los documentos compartidos si cambia la proforma padre.

### Colocación repetible en OneDrive
1. Crear el respaldo una sola vez, antes del primer cambio.
2. Renombrar la carpeta; si OneDrive la bloquea, reintentar.
3. Revisión previa: origen existe, hash coincide, destino vacío o idéntico por hash.
4. Si la ruta supera 250 caracteres, acortar el nombre del archivo con los primeros 8 caracteres del hash y registrar el cambio. La carpeta conserva su nombre.
5. Copiar sin sobrescribir y verificar hash; omitir lo que ya esté.
6. Mover dentro del mismo expediente.
7. Eliminar vacías con `rmdir`, con 3 reintentos; si OneDrive marcó la carpeta de solo lectura, usar `os.chmod` antes. Si una falla, registrar como pendiente y seguir: no abortar.
8. Verificar contra el respaldo: cada hash del respaldo sigue presente y cada archivo del plan está.
9. Escribir `REGISTRO_COLOCACION.csv` desde el estado real comparado con el respaldo.
- **Conjunto en disco:** comparar por hash. Lo idéntico que esté en la hija se retira al respaldo; lo compartido que solo esté en la hija se mueve al padre. Registrarlo en `Otros\REGISTRO_COLOCACION_*.csv` de las dos carpetas.

## Plantilla del resumen
```
---
proforma:
cliente_final:
pais:
oc:
bl_o_awb:
sap:
modalidad:
embarque:
proforma_padre:
proformas_hijas:
factura_propia:
estado_real:
cobertura: completo | parcial | solo documentos
nombre_final_carpeta:
actualizado:
visibilidad: INTERNO
---
# Expediente <proforma>
## Referencias: tipo · número · fuente
## En 5 líneas
## Modalidad y evidencia
## Embarque y evidencia
## Avería o faltante: texto literal · fuente · plazo · seguro · aviso enviado y a quién
## Documentos compartidos: documento · carpeta donde está
## Cronología: fecha · hecho · fuente
## Tiempos: registro · fin de Producción · salida · llegada · cobro · regla aplicada · verificado o estimado
## Comunicación clave: fecha · quién · decisión o pendiente · uid
## Atención de los correos: te corresponde · relevante · solo comunicación · pedidos dirigidos al CEO
## Documentos vigentes: tipo · número · fecha · archivo
## Evolución: documento · versión · qué cambió
## Pagos y facturación: tipo de registro · pagador · beneficiario · número · fecha · monto · fuente
## Tiempo de cobro: registro → pago · salida → pago del cliente · pago identificado → comisión
## Lo que ve el cliente (reventa): capa · estado · nota
## Faltantes y conflictos
## Diferencias con mwt.one
## Cambios: fecha · qué · valor anterior · valor nuevo · evidencia
```

En la plantilla, `factura_propia` es la factura de **Muito Work**: la FE en reventa o la factura por servicios en comisión. La factura de Marluvas o del proveedor no se anota ahí; si hace falta, va en `## Documentos vigentes` como documento del proveedor.