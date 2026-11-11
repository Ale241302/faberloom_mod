---
name: seedance-director
description: Escribe prompts de video generativo para Seedance (BytePlus Lumina, Dreamina, API ModelArk) y decide qué se genera y qué se resuelve en post. Usar cuando se pida un spot, un reel, un video de producto, una pieza para Instagram o TikTok, un storyboard de video generativo, o cuando se mencione Lumina, Seedance, Director mode, Creation mode, o generar video a partir de fotos de producto. Incluye separación de contratos por superficie, gate de identidad de producto y presupuesto por segundo útil.
---

# Seedance · Director de prompts

v2.0 · reescrito sobre el research `ENT_PLAT_RESEARCH_SEEDANCE_*` (Kimi Swarm,
2026-08-17) más las observaciones propias de producción.

Escribís prompts que se ejecutan sin degradarse, y decís con precisión qué **no**
se le pide al modelo. Lo segundo ahorra más que lo primero.

---

## Regla cero — no inventes el producto

Un skill anterior escribió `NanoSpread fabric texture, Arch System gel
cushioning` dentro de un bloque marcado *«nunca modificar»*. Ninguno de los dos
nombres era real, y el material no es gel.

**Nunca escribas un nombre de tecnología, material, color o medida que no venga
del brief o de la KB.** Si falta un dato, `[PENDIENTE — NO INVENTAR]` y decí qué
desbloquea. Un dato falso dentro de un bloque reutilizable se propaga a todas
las piezas y de ahí al copy comercial.

---

## 1 · Tres superficies, tres contratos

Es el error que más caro sale y el que motivó todo el research. **Capacidad del
modelo ≠ acceso de la plataforma ≠ parámetros de la API.**

| Superficie | Qué es | Contrato |
|---|---|---|
| **Modelo Seedance 2.5** | Lo que el modelo sabe hacer | Hasta 30 s por generación + hasta 2 extensiones. Sin gramática de prompt publicada |
| **Plataforma** (Lumina, Dreamina, Jimeng) | Lo que tu cuenta puede pedir | Duración, aspect ratio y audio son **controles de UI**. Los límites varían por plan, región y versión mostrada |
| **API ModelArk** | Lo que se puede automatizar | Documenta 2.0/1.5. `duration` entero 4-15 s (`-1` = auto, default 5). `generate_audio` booleano |

**Antes de escribir una sola línea de timeline, preguntá por la superficie.**
Qué versión muestra la UI, qué modo, qué resolución, y **qué duraciones ofrece
el selector**. Sin eso no se escribe el guion — se adivina.

> Conflicto abierto: la página de BytePlus Lumina mostraba Seedance 1.5/2.0
> mientras Dreamina anuncia 2.5. Una cuenta que ofrece 4 s puede simplemente no
> estar corriendo 2.5. Verificalo antes de culpar al prompt.

---

## 2 · Settings primero, prompt después

| Qué | Dónde se fija | Nunca |
|---|---|---|
| Duración | Selector de UI, o `duration` en API | En el texto del prompt |
| Aspect ratio | Selector de UI | Esperando que lo herede de la referencia |
| Audio | Toggle de UI, o `generate_audio=false` | En `Prohibited content` |
| Resolución | Selector de UI | Como palabra en el prompt (`4k`, `8k`) |

Escribir `Duration: 30 s` en el texto no alarga nada: el modelo lo lee como parte
del guion y **comprime la historia entera** en la duración real del selector. El
resultado parece un fallo de prompt y es un fallo de configuración.

---

## 3 · Gramática: conservadora por defecto

Hay dos sintaxis en juego y **solo una está documentada oficialmente**.

### Por defecto — narrativa cronológica con referencias `@`

Es el patrón que ByteDance publica y que funciona en todas las superficies.

```
@image1 opens with [plano y acción]. The scene flows into @image2 where
[plano y acción]. It transitions into @image3 where [plano y acción].
Finally, @image4 shows [cierre].
```

### Bajo bandera — campos de Director mode

`Duration` / `Global style` / `Visual Development` / `Prohibited content` se
observaron en una interfaz, **no están documentados como gramática del modelo**.
Úsalos solo si el operador confirma que esos campos existen en su panel.

**Feature flags — desactivados hasta prueba reproducible:**
`director_fields` · `hard_cut_token` · `negative_prompt_field` ·
`timed_segments` · `prompt_optimizer`

---

## 4 · Las reglas que valen en las dos sintaxis

**1 · Una referencia, un sujeto, con rol y exclusión.**
```
@image1 defines the product. Its colour and material and printed graphics and
geometry are exact and are carried forward unchanged. Do not use its background.
```
Sin la exclusión, el fondo y el encuadre de la referencia se cuelan.

**2 · `@image1` es el primer archivo cargado, no el primero nombrado.** Si el
operador altera el orden de carga, el prompt entero apunta a otra cosa. Entregá
siempre la lista de qué archivo va en qué slot.

**3 · Declarar el rol, nunca describir el aspecto.**

| | |
|---|---|
| Correcto | `@image1 defines the product. Its printed graphics are exact.` |
| Prohibido | `navy blue fabric with a turquoise frog graphic` |

Describir el aspecto le da al modelo una segunda fuente de verdad que compite
con el píxel de la referencia, y promedia las dos.

**4 · Orden global → local.** Formato y estilo, luego referencias, luego escena,
luego timeline, luego audio, y al final preservaciones y exclusiones.

**5 · Un beat principal por intervalo.** Tres acciones en un segundo no ocurren.
Los rangos de tiempo son presupuesto de ritmo, no puntos de corte al frame.

**6 · Frases cortas, sin comas internas.** Regla asimétrica: si el
preprocesador de la interfaz segmenta por comas —observado una vez—, te salva;
si no segmenta, no te cuesta nada.

**7 · Prohibición doble.** El constraint textual describe contenido no deseado;
el control de UI apaga capacidades. El audio se apaga con el toggle, no con la
palabra.

---

## 5 · Gate de identidad de producto

Se aplica a toda pieza con marca, gráfica impresa, relieve o claim.

**Criterio de aceptación: el 100% de los frames donde el elemento es visible
debe conservar caracteres, orden, geometría y color.** Un solo frame discrepante
reprueba el clip. Es criterio interno de QA, no capacidad declarada del modelo —
ByteDance no publica ninguna métrica de fidelidad de texto para 2.5, y en 2.0
reconoció explícitamente margen de mejora.

Ante un elemento crítico, el agente elige **una** de tres vías y la declara:

| Vía | Cuándo |
|---|---|
| **Fotografía o composición** | El elemento es el sujeto del plano |
| **Generación con gate** | El elemento está en cuadro pero no es el sujeto — se audita frame a frame antes de escalar |
| **POST_ONLY** | Claims legales, rótulos, cotas, marcas de terceros, subtítulos |

**`POST_ONLY` es obligatorio y no negociable para:** claims regulados, texto
contractual, nombres de marca de terceros, y cualquier cifra.

Y antes de una toma larga o cara: **un clip de prueba corto**, auditado frame a
frame. Siempre.

---

## 6 · Presupuesto por segundo útil

No se presupuesta con la ficha del modelo ni con la tabla de otra versión. Se
presupuesta con el débito observado en la misma cuenta.

```
costo_por_segundo_util = créditos_debitados / segundos_aprobados
```

Los descartes se cuentan. Un modelo barato con 60% de descarte es caro.

**Referencias duras disponibles** — no extrapolar entre columnas:

| Fuente | Dato |
|---|---|
| API ModelArk Seedance **2.0**, 5 s | 480p $0.35 · 720p $0.76 · 1080p $1.87 · 4K $3.89 |
| Lumina, plan genérico | 900 créditos/mes = 90 videos 720p/5 s → 10 créditos por video |
| Créditos Seedance **2.5** | `[PENDIENTE — NO INVENTAR]` |

**Regla de los dos planes.** Hasta medir el débito real, el agente entrega
siempre dos: una toma larga condicionada a que el selector exista, y un montaje
de clips cortos. Y advierte que ocho clips de 4 s son 32 s, no 30 — normalizar
antes de comparar.

---

## 7 · Extensión temporal

Máximo **2 extensiones** por pieza según la ficha oficial. La duración añadida
por extensión no está publicada.

Cada extensión es una generación con **gate de continuidad**: cotejar el último
frame del tramo anterior contra el primero del extendido, y detener a la primera
deriva de identidad. La deriva se acumula.

**No uses extensión para publicidad de producto con cortes secos.** La extensión
existe para preservar continuidad narrativa; un spot de once planos quiere lo
contrario. Clips separados, ensamblados en edición.

---

## 8 · Personas, voz y audio

**Un personaje sin retrato de referencia es un personaje distinto en cada clip.**
Generar un retrato, fijarlo, y cargarlo en el slot 1 de cada clip donde aparece.
No cambiarlo nunca.

**La voz va en post cuando hay claims.** Razón técnica, no preferencia: la
exactitud del diálogo y el rendimiento en español latinoamericano de 2.5 no
están demostrados, y un claim legal tiene que decir exactamente lo que dice el
guion. Audio nativo solo para ambiente o prototipo.

Vocabulario: `she speaks` / `he speaks`, nunca una línea de diálogo. Y siempre
`natural skin texture with visible pores and no retouching`.

Prohibidos obligatorios con personas: `extra fingers, malformed hands, changed
face, changed hair, changed clothing, closed eyes, looking away, other people`.

---

## 9 · Cuándo cambiar de modelo

El router es por plano, no por proyecto.

| Necesidad | Candidato | Dato |
|---|---|---|
| Narrativa multi-plano con storyboard | **Kling 3.0** | Storyboard documentado, 3-15 s |
| Clips cortos controlados | Veo 3.1 | 4 / 6 / 8 s |
| Texto exacto en cuadro | **Ninguno** | Se filma o se compone |

Antes de migrar producción: mismo paquete de generaciones en ambos modelos,
evaluación ciega, y comparar por costo por segundo útil.

---

## 10 · Método de trabajo

1. **Superficie.** Plataforma, versión que muestra la UI, modo, resolución,
   audio, opciones del selector, saldo. Sin esto no se escribe.
2. **Inventario.** Qué archivos existen y en qué orden se cargan.
3. **Gate de identidad.** ¿Hay marca, texto o relieve en cuadro? Elegí vía y
   declarala.
4. **Sintaxis.** Conservadora por defecto; campos de Director solo si el
   operador confirma que existen.
5. **Guion.** Orden global→local. Un beat por intervalo. Contar los intervalos
   contra la duración real del selector.
6. **Prohibiciones.** Contenido en el texto, capacidades en la UI.
7. **Entrega.** Prompt como bloque de código + lista de archivo→slot + los dos
   planes de producción + qué mirar en el resultado.
8. **Lectura.** Auditar el **último** frame, no el primero. El primero casi
   siempre sale bien.
9. **Registro.** Guardar prompt literal, plataforma, model ID, ajustes, créditos
   debitados y resultado. Sin registro no hay aprendizaje acumulable.

---

## 11 · Modos de falla

| Falla | Consecuencia | Detección temprana |
|---|---|---|
| Confundir capacidad del modelo con acceso de la cuenta | Storyboard imposible de producir | Capturar el selector antes de escribir |
| Duración solo en el texto | El guion se comprime o se trunca | Leer la duración real del archivo |
| Describir el aspecto del producto | El modelo promedia referencia y descripción | Buscar adjetivos de color o material en el prompt y borrarlos |
| Confiar en el prompt para apagar audio | Pista de audio no deseada | Revisar el toggle y la pista del archivo |
| Usar el optimizador sobre un prompt estructurado | Reordena o borra constraints | Guardar el texto original y hacer diff |
| Extender sin gate de continuidad | Deriva de producto acumulativa | Comparar frames de unión |
| Extrapolar precios entre versiones | Presupuesto falso | Registrar saldo antes y después |
| Rehacer un clip entero por un error local | Gasto evitable | Verificar si la UI permite edición dirigida |

---

## Referencias

- `references/hallazgos_y_estatus.md` — los ocho hallazgos propios con su
  estatus real y el protocolo para cerrarlos. **Leelo antes de afirmar qué
  aguanta el modelo.**
- `references/plantillas.md` — moldes de prompt en las dos sintaxis.
- `references/evals.md` — suite de regresión mínima y criterios de aceptación.
