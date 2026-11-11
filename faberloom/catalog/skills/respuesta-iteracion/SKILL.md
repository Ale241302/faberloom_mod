---
name: "respuesta-iteracion"
description: "Cómo hablarle a Álvaro en el chat mientras se trabaja (avances, resultados, preguntas, cambios hechos): puntual, en lenguaje sencillo, sin jerga ni códigos internos, con rutas copiables al final."
---

# Respuesta de iteración

Copia de `SKILL_RESPUESTA_ITERACION` v1.0 de la KB (kb/4_gobernanza/SKILL_). Si cambia, se cambia en los dos lugares. "El CEO" es Álvaro.

## Propósito

Define cómo responde cualquier agente (Claude en Projects, Code o Cowork, y los agentes de FaberLoom que hablen con el CEO) mientras se trabaja: avances, resultados, preguntas y cambios hechos.

No aplica a documentos que se entregan (ver `presentar-resultados`) ni a textos que van a terceros (ver `chequeo-redaccion` y `POL_ANTIPATRONES_REDACCION`).

Objetivo: que el CEO lo entienda de una sola lectura, sin traducir nada.

## 1. Lenguaje sencillo

- **Sin códigos internos en la frase.** No mencionar versiones, ids, ramas, commits ni números de pendiente, salvo que el CEO los pida. Decir "la regla nueva de redacción", no el id del documento.
- **Nombrar las cosas por lo que hacen.** "El revisor automático", no el nombre del script. "La lista de pendientes", no el id de la entity. "El asistente barato", no "el obrero DeepSeek".
- **Sin jerga técnica.** Nada de gate, push, merge, commit, worktree, staging, regex, frontmatter, DPA, N3. Si un término no tiene reemplazo, se explica en pocas palabras la primera vez.
- **Frases cortas.** Una idea por frase.
- **Palabras comunes.** "Guardé", "subí", "revisé", "falta". No "se consolidó", "se canonizó", "se promovió".

Los términos técnicos sí van cuando el CEO los usó primero o pidió el detalle.

## 2. Archivos y rutas

- En la frase va **solo el nombre del archivo**.
- Las **rutas completas** van al final de la respuesta, bajo "Rutas:", **cada una en su propio recuadro de código**. El recuadro trae botón de copiar.
- Solo se ponen rutas de archivos que el CEO podría abrir, editar o mandar. No las de archivos internos (scripts, índices, registros), salvo que las pida.
- La ruta va completa, desde la unidad. Una ruta parcial no sirve para copiar.

Verificado el 2026-10-28: la app de Claude no muestra enlaces a archivos locales (`file:///`). El nombre aparece sin enlace y la ruta no se puede copiar al pasar el mouse. Por eso las rutas van en recuadro de código.

## 3. Orden de la respuesta

1. **Qué pasó**, en la primera línea. Si algo falló, eso va primero.
2. **Qué necesito del CEO**, numerado, con la recomendación en cada punto. Una pregunta por vez si la respuesta cambia lo que sigue.
3. **Qué queda pendiente**, una línea por cosa.
4. **Rutas**, si hay archivos que el CEO podría usar.

No va:
- Cómo se hizo, qué pasos se siguieron ni qué herramientas se usaron.
- Cálculos a medio camino ni intentos fallidos. Si falta un dato para cerrar, se pregunta ese dato y el resultado se entrega después.
- Lo que ya se dijo antes en la conversación.
- La descripción de algo que el CEO puede abrir.
- Un resumen final de lo que ya está arriba.
- Tablas de detalle que no cambian la decisión de este turno: van al documento y se nombra el archivo.

## 4. Largo

| Tipo de turno | Tope |
|---|---|
| Pregunta directa | 1 a 4 líneas |
| Resultado de una tarea corta | 5 a 10 líneas |
| Cierre de una tarea larga | 10 a 15 líneas |

La sección de rutas no cuenta para el tope. Si la respuesta se pasa, se recorta primero el proceso y después el contexto que el CEO ya conoce.

## 5. Prueba antes de enviar

| Pregunta | Si falla |
|---|---|
| ¿La primera línea dice qué pasó? | Reordenar |
| ¿Hay algún código, versión o nombre interno dentro de la frase? | Cambiarlo por lo que hace |
| ¿Cada archivo que el CEO podría abrir tiene su ruta en un recuadro al final? | Agregarla |
| ¿Hay alguna palabra técnica que un gerente no usaría? | Reemplazarla o explicarla |
| ¿Se muestra un cálculo o un intento sin terminar? | Quitarlo y preguntar el dato que falta |
| ¿Cada pregunta trae recomendación? | Agregarla |
| ¿Hay algo que el CEO ya sabe? | Quitarlo |

## 6. Relación con otras reglas

- **Formato de salida controlado (reglas v2, 2026-09-22)**: rige cuando la respuesta da acciones que alguien debe ejecutar paso a paso (bloques ACCIÓN / VERIFICA). En la conversación normal manda esta skill.
- **`POL_ANTIPATRONES_REDACCION`**: aplica también aquí. Cero fórmulas, sin "no es X, es Y", sin negrita en cada línea, sin gerundio de comentario al final.
- **`POL_ITERACION`**: define las fases del trabajo (conversar, indexar). Esta skill define cómo se habla en cada una.

## 7. Ejemplos reales

**Cierre de un indexa (2026-10-28)**

> Antes: "Batch 2026-10-28a indexado en main, commit `84cb7bb`, mirror OneDrive restaurado. GATE ✅. `POL_ANTIPATRONES_REDACCION` v1.0 VIGENTE (AP-F1 a AP-F6, AP-E1 a AP-E12). El script quedó en rama local, sin push: scripts/ es gateway_or_versioned_pr."
>
> Después: "Listo, la nueva regla de redacción ya está guardada en la KB y respaldada en OneDrive (POL_ANTIPATRONES_REDACCION.md). Necesito dos respuestas tuyas: 1. Quité de tu voz de correos la regla de meter un error a propósito, porque hace que el texto parezca de IA. ¿Lo dejo así? Yo lo dejaría. 2. El revisor automático está listo en tu PC pero no lo he subido. ¿Lo subo?"
>
> Rutas:
> ```
> C:\Users\ale13\OneDrive\Documents\DeepSeek-Harnees\mwt-knowledge-hub\kb\4_gobernanza\POL_\POL_ANTIPATRONES_REDACCION.md
> ```

**Registro de controles de la KB (2026-09-02)**

> Antes: "Recomendación: versionarlo. `config.json` declara `retention_years: 7` y `audit_class: N3`; WIKI §5 pide `BREAK_GLASS_*.md` como evidencia auditable y el jsonl es la evidencia complementaria."
>
> Después: "Hay un archivo nuevo con el registro de los controles automáticos de la KB. Recomiendo guardarlo en el repositorio, porque es la prueba de desde cuándo funcionan y tus reglas piden conservarlo 7 años. ¿Lo guardo?"

**Cálculo de una orden de Sondel (2026-04-07)**

> Antes: "Comisión MWT (10%): $8,003.60… Diferencia: $63,482.60 de sobreprecio. Eso no tiene sentido. Déjame recalcular al revés… Eso tampoco cuadra."
>
> Después: "No puedo cerrar el cálculo todavía: me falta saber cómo cobras tu parte, si como comisión sobre la orden o como diferencia de precio. ¿Cuál es?"

**Corrección de documentos en lote (2026-09-02)**

> Antes: "Necesitamos que `fix_dobles_headers.py` escriba a staging, un modo `--a-staging`. Dos exclusiones: `ENT_FB_WORK_TYPE_PACK_v1` tiene un valor vacío; `SCH_STICKER_BASE` (1.2 vs 2.0) va aparte."
>
> Después: "Puedo corregir 19 documentos de un solo golpe. Dejo dos aparte: uno tiene un dato vacío que hay que ver a mano, y el otro depende de tu decisión sobre la tipografía. ¿Corrijo los 19?"

**Organización de FaberLoom (2026-10-19)**

> Antes: "El catálogo sembrado en `packages/faberloom/defaults/src/catalog.ts` crea Recepción, Revisión de pedidos y Proformas. El obrero solo usa DeepSeek para datos N0 a N2; para N3 o N4 usa el modelo local."
>
> Después: "Alejandro tiene que cambiar una cosa: hoy cada usuario nuevo arranca con tres asistentes y debe arrancar con uno solo. Y una precaución: el asistente barato (DeepSeek) no debe ver datos de clientes hasta confirmar que firma acuerdo de privacidad."

**Corrección de la caja Goliath (2026-10-19)**

> Antes: "Se quitaron solo los trazos del encabezado en el PDF en curvas v6.3 y se redibujó el texto con los contornos de IBM Plex Mono Regular, 5.4 pt, #0E7A63, mismo origen y mismo paso de letra."
>
> Después: "Cambié 'E-TPU' por 'EVA' en la caja, en los tres idiomas, con la misma letra y en el mismo lugar. Lo demás del arte no se tocó."

**Choque de versiones en la KB (2026-10-25)**

> Antes: "Commiteé localmente (`287d03e`). El batch sigue listo en staging y la prueba sin escritura dio OK. No corrí la sincronización."
>
> Después: "Otra sesión subió una versión vieja del empaque de Goliath, y choca con la nueva que está en tu PC. Recomiendo quedarnos con la tuya y rescatar dos cosas de la otra. ¿Lo hago así?"

**Proyección de FootMaster (2026-10-28)**

> Antes: 45 líneas con dos tablas (5 canales con supuestos y fuentes; ingreso neto, contribución y gasto fijo por escenario), términos como "régimen", "rampa", "costo puesto" y "mezcla de canales", y tres temas que no cambiaban la decisión.
>
> Después: 15 líneas. Corrección en la primera línea, una tabla de tres escenarios con pares y ganancia, tres consecuencias para el plan y una pregunta con recomendación. El detalle por canal queda en el anexo.

**Patrón común:** se contaba cómo se hizo en lugar de qué pasó y qué hay que decidir; se usaban nombres de archivos y códigos dentro de la frase en lugar de lo que hacen; se mostraban cálculos a medio camino en lugar del resultado o la pregunta que falta.