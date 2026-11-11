# Hallazgos propios — estatus real y cómo cerrarlos

Ocho observaciones de producción, auditadas contra el research de Kimi Swarm
(`ENT_PLAT_RESEARCH_SEEDANCE_*`, 2026-08-17).

**Ninguna es todavía una regla del modelo.** Todas son comportamiento observado
en una interfaz, con n=1 y en varios casos con variables confundidas.

---

## La jerarquía de evidencia, corregida

El encargo original tenía cuatro niveles y le faltaba el que más importa acá.

| Nivel | Qué es |
|---|---|
| **A** | Documentación oficial de ByteDance / Seed / BytePlus |
| **B** | Benchmark con metodología y muestra declaradas |
| **O** | **Observación propia reproducible** — archivo generado, prompt literal, configuración registrada, n declarado |
| **C** | Blogs, agencias, casos de estudio |
| **D** | Foros, Reddit, YouTube |

**El nivel O va por encima de C y por debajo de B.** Es la categoría que
faltaba: ningún blog va a publicar el comportamiento de tu cuenta, así que la
ausencia de fuente pública **no refuta** una medición propia. Pero una medición
con n=1 y variables confundidas tampoco es una regla.

Requisitos para que algo sea nivel O: archivo conservado, prompt literal,
plataforma y versión mostrada, ajustes de UI, y **n declarado**.

---

## Tabla de estatus

| # | Hallazgo | Estatus | Qué hacer hoy |
|---|---|---|---|
| **H1** | Director mode parsea por comas y reparte los fragmentos en tramos | **O, n=1** · contradicho por documentación oficial que usa prosa con comas | **Seguir la regla igual.** Es asimétrica: frases cortas no cuestan nada. Probablemente sea un preprocesador de la interfaz, no del modelo |
| **H2** | `Duration:` en el texto no controla la duración | **CONFIRMADO** para API ModelArk 2.0 y para Dreamina (nivel A) · **O, n=2** para Lumina | Tratar como regla. La duración va en el control, siempre |
| **H3** | El modelo destila un guion más largo que la duración disponible | **O, n=1** · 2.0 declara respuesta a guiones largos, sin garantía de orden | No prometerlo. Contar los intervalos contra la duración real |
| **H4** | La salida no hereda el aspect ratio de la referencia | **O, n=1** · las plataformas exponen ratio como setting | Fijar el ratio en la UI siempre. El absoluto «nunca hereda» no está probado |
| **H5** | `Prohibited content: audio` no bloquea el audio | **CONFIRMADO** en arquitectura: la API expone `generate_audio` como parámetro (nivel A) · **O, n=2** para el toggle de Lumina | Tratar como regla. Las capacidades se apagan con controles |
| **H6** | 4 s rompe la tipografía, 2 s aguanta | **NO DEMOSTRADO.** Las dos generaciones diferían en duración **y** en encuadre **y** en número de escenas. n=1 por celda | **No codificar el umbral.** La observación de que el texto se degrada es real; la atribución a la duración no está sostenida |
| **H7** | El corte duro sale limpio y no reinventa el producto | **O, n=1** · hay ejemplos oficiales multi-plano, sin prueba de identidad de producto | Usable, con gate: comparar el frame anterior y el posterior al corte |
| **H8** | Los negative prompts recién funcionan de forma estable en 2.5 | **NO DEMOSTRADO** como hecho generacional. No hay benchmark 2.0 vs 2.5 | Usar el campo si existe; no afirmar que sea nuevo ni que sea estable |

---

## Protocolos para cerrarlos

### P1 · Gramática real de la interfaz — cierra H1, H3, H7

Pares con la misma referencia, mismos settings y misma semilla si existe.
Variar **una sola cosa** por par:

- coma latina `,` contra coma ideográfica `，`
- prosa contra lista contra campos con encabezado
- tiempos que suman la duración contra tiempos que no suman
- `HARD CUT` contra `CUT TO` contra corte descrito en prosa

Registrar prompt literal, optimizador on/off, archivo de salida y metadata.
Comparar la segmentación observada frame a frame.

### P2 · Umbral de supervivencia del texto — cierra H6

Ensayo factorial. Es el pendiente de mayor impacto de todo el research.

| Variable | Niveles |
|---|---|
| Permanencia en cuadro | 2 s · 4 s · 8 s |
| Cámara | fija · órbita 15° |
| Tamaño del sujeto | 40% · 70% del alto de cuadro |
| Contraste del texto | alto · bajo |

≥10 repeticiones por celda. **Solo se varía una dimensión a la vez.** OCR y
cotejo del 100% de los frames donde el texto es visible.

Prompt base, cambiando únicamente lo que la celda pide:

```
Use @image1 as the exact product identity reference. Keep the geometry, printed
wordmark, printed vector graphics, halftone pattern, textile texture, colored
edge and engraved relief unchanged. Locked tripod camera. The product remains
front-facing and fills 70% of frame height. Keep the wordmark fully visible and
unobstructed for the entire clip. No new text, no replacement letters, no
redesign, no smoothing of the relief.
```

### P3 · Superficie real de la cuenta — cierra H2, H4, y desbloquea el presupuesto

Capturar plan, región, versión que muestra la UI, modo, resolución, toggle de
audio y **todas las opciones del selector de duración**.

Luego: mismo prompt, selector en la duración más corta, y otra vez en la más
larga. Leer la duración del archivo descargado y el débito de créditos antes y
después. Si la salida sigue al selector, H2 queda confirmado para Lumina.

Y una pregunta que decide todo: **¿la UI dice Seedance 2.5, o dice 1.5 o 2.0?**
Una cuenta que ofrece 4 s puede simplemente no estar corriendo 2.5.

### P4 · Flexión de material — no medido nunca

```
Use @image1 as the exact product identity reference. Two natural adult hands
gently flex the insole once by 20 degrees and release it. The printed graphics
must deform continuously with the textile surface, preserving line spacing,
halftone density, color boundaries, wordmark letter shapes, edge thickness and
engraved relief depth. No sliding decal, no stretching independent of the
material, no melted fingers, no extra fingers. Locked macro camera, product
fills 80% of frame height.
```

Los 20° y el 80% son parámetros experimentales, no umbrales documentados.

---

## Lo que la documentación oficial sí sostiene

| Dato | Nivel |
|---|---|
| Seedance 2.5: hasta 30 s por generación, hasta 2 extensiones | A |
| Seedance 2.0 reconoce margen de mejora en precisión de texto | A |
| Seedance 2.5 promete «control preciso de referencia» — **sin métrica publicada** | A |
| API ModelArk: `duration` entero 4-15 s, `-1` auto, default 5 s | A |
| API ModelArk: `generate_audio` booleano | A |
| API ModelArk 2.0, 5 s: 480p $0.35 · 720p $0.76 · 1080p $1.87 · 4K $3.89 | A |
| Lumina: 900 créditos/mes = 90 videos 720p/5 s | A |
| Una referencia, un sujeto; declarar rol y exclusiones | A |
| Texto que deba ser exacto es trabajo de posproducción | A |
| Los rangos de tiempo son presupuesto de ritmo, no cortes al frame | A |
| Kling 3.0: storyboard multi-plano documentado, 3-15 s | A |
| Veo 3.1: 4 / 6 / 8 s | A |

---

## Conflictos abiertos — reportados, no resueltos

- **Versión mostrada.** La página de BytePlus Lumina mostraba Seedance 1.5/2.0
  mientras Dreamina anuncia 2.5.
- **Gramática.** El único skill público de 2.5 prescribe prosa natural y prohíbe
  listas separadas por comas; H1 observó lo contrario en Director mode.
- **Créditos 2.5.** No hay tabla pública por duración, resolución ni modo.
- **Manual oficial 2.5.** Vive en un documento Lark que no fue accesible; lo que
  circula son condensaciones de terceros.
- **Región de la beta ultra-larga.** Sin lista de regiones publicada.

---

## Build vs. buy — estado

| Capacidad | Componente | Veredicto |
|---|---|---|
| Base de prompting 2.5 | `xiaoliangliang/seedance-2.5-prompt-skill` (MIT, 1 commit) | **FORKEAR** — es lo más cercano, no adoptar tal cual |
| Skills 2.0 | zhouwei713 · songguoxs · liangdabiao · dexhunter | **DESCARTAR** como base 2.5. Corpus histórico solamente |
| Ejecución automatizada | `byteplus-sa/modelark-mcp` — expone `seedance_2_5_create_task` | **PILOTO** — verificar licencia, seguridad y smoke test mínimo |
| Cliente de respaldo | SDK oficial BytePlus ModelArk | **ADOPTAR** para modelos documentados |
| Bancos de prompts | AtlasCloud · Tosea · YouMind · Toolcentral | **DESCARTAR** como reglas. Inspiración no normativa |
| Gramática de Director mode | ninguno verificado | **CONSTRUIR** — protocolo P1 |
| Gate de fidelidad | ninguno verificado | **CONSTRUIR** — protocolo P2 |
