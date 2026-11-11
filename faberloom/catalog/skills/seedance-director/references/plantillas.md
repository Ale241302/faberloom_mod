# Plantillas de prompt

Dos sintaxis. **La conservadora es la que se usa por defecto**; la de campos
solo cuando el operador confirma que esos campos existen en su panel.

---

## Estructura común — orden global → local

```
1. Formato y estilo global
2. Mapa de referencias: identificador + rol + exclusión
3. Escena
4. Timeline: un beat por intervalo
5. Audio (solo si aplica)
6. Preservaciones e invariantes
7. Exclusiones
```

---

# SINTAXIS A — conservadora (por defecto)

Es el patrón que ByteDance publica y que funciona en todas las superficies:
narrativa cronológica enlazada a referencias `@`.

## A1 · Producto quieto

```
@image1 is the sole source of truth for the product. Preserve its geometry,
printed graphics, colour, textile texture, coloured edge and engraved relief
exactly. Do not use its background.

Overhead product macro on a plain neutral grey surface with a soft contact
shadow. Soft directional key light from the upper left with a gentle bounce
fill from the right. Matte surfaces and fine even film grain.

The product opens completely still on the surface as a very slow push-in begins
toward its centre. The push-in continues at constant speed while the product
holds its exact position and contact shadow. Light drifts almost imperceptibly
across the surface from left to right. The push-in slows to a stop and holds.

No redrawn lettering. No altered graphics. No rotation. No mirroring. No added
objects. No hands. No people. No generated text. No subtitles. No watermarks.
```

## A2 · Macro de material con dedo

El molde que más vende: la compresión y el retorno **son** el argumento.

```
@image1 is the sole source of truth for the product. Preserve its geometry,
printed graphics, colour, textile texture and [la zona específica] exactly.

Extreme product macro in vertical format on a worn wooden workbench. Hard
raking light from the right that reveals surface texture and relief. Very
shallow depth of field with a razor thin plane of focus. Matte surfaces and
rich film grain. One bare adult index finger with a short unpainted nail.

The frame opens as a tight macro and slowly racks focus onto [la zona]. A
fingertip enters from the right and presses firmly into it, and the material
compresses deeply under the pressure. The fingertip lifts and the material
slowly recovers its full shape.

No redrawn lettering. No altered graphics. No torn material. No permanent dent.
No extra fingers. No malformed hands. No long nails. No faces. No people. No
generated text. No subtitles. No watermarks.
```

> Si el selector ofrece 10-12 s, usalos acá. Los cuatro tiempos —entra,
> presiona, se hunde, recupera— apretados en 4 s se ven baratos.

## A3 · Dos planos con corte

```
@image1 is the sole source of truth for the product in both shots. Preserve
identical geometry, colours, graphics, texture, edge thickness and relief
before and after the cut.

[Global style]

Shot one is a locked top-down macro of the product. HARD CUT. Shot two is a
locked side macro of the same product from the coloured edge.

No morphing transition. No dissolve. No wipe. No redesign. No new text.
No speed ramps. No watermarks.
```

## A4 · Presentador a cámara

Requiere retrato de referencia generado antes y fijo para todos los clips.

```
@image1 is the sole source of truth for the presenter. Her face, skin tone,
hair, build and clothing are exact and unchanged for the entire clip. Do not
use its background.

Documentary interview realism in vertical format. A warm dim workshop softly
out of focus behind her. Soft window light from the left with a gentle bounce
fill from the right. Natural skin texture with visible pores and no
retouching. Shallow depth of field on an 85mm lens. Fine film grain. She is
framed from the waist up and stays centred. Handheld with very subtle operator
breathing.

She looks straight into the lens and begins to speak, calm and direct. She
continues speaking and gestures once with an open hand while her eyes stay on
the lens. She finishes the thought and holds the look.

No changed face. No changed hair. No changed clothing. No other people. No
closed eyes. No looking away. No extra fingers. No malformed hands. No
jewellery. No brand logos. No readable text. No subtitles. No watermarks.
```

**Prompt del retrato de referencia**, a generar una sola vez:

```
Portrait photograph of [fenotipo] in [rango de edad]. [Rasgos]. [Vestuario
plano y neutro]. Neutral background, softly out of focus. Soft window light
from the left with a gentle bounce fill from the right. Natural skin texture
with visible pores, no retouching, fine film grain. Shot on an 85mm lens at
f2, waist up, vertical 9:16 framing.
```

Generar cuatro o cinco, elegir una, no cambiarla nunca más.

## A5 · Escena sin producto, varias referencias

Sin producto en cuadro no hay riesgo de infidelidad de marca: **se puede usar
stock**.

```
@image1 defines the scene: [qué gobierna]. Do not use its background and do
not use any text or insignia on it.
@image2 defines the character: [vestuario y encuadre corporal]. Do not use its
background and do not use anything above [el límite].
@image3 defines the ground: [superficie]. Do not use any object resting on it.
@image4 defines the camera blocking: [altura y reparto del encuadre]. Do not
use its subject and do not use its lighting.

[Global style con el límite de encuadre explícito]

[Narrativa cronológica: posición inicial → espera → gesto → resolución →
frame vacío]

No faces. No heads. No torsos above the belt. No other people. No brand logos.
No readable text. No license plates. No passing vehicles. No subtitles.
No watermarks.
```

---

# SINTAXIS B — campos de Director mode

**Solo si el operador confirma que estos campos existen en su panel.**
Feature flag `director_fields`.

```
Duration: [N] s

References:
@image1 defines [rol]. [qué se hereda]. Do not use [exclusión].

Global style: [plano]. [superficie]. [luz]. [textura y grano]. [herencia].

Visual Development:
0 s~1 s: @image1 ，[una acción] ，Subject's actions develop further
1 s~2 s: @image1 ，[una acción] ，Subject's actions develop further
[último]: @image1 ，[una acción] ，Subject's actions complete naturally

Prohibited content: [lista separada por comas]
```

Anatomía de un intervalo, según lo observado:

```
0 s~1 s: @image1 ，the product rests still ，Subject's actions develop further
         └─ ancla ─┘  └───── acción ─────┘  └──── progresión ────┘
```

Vocabulario de progresión observado: `Subject's actions develop further` en
intervalos intermedios · `Subject's actions complete naturally` en el último.

**Advertencias que van con esta sintaxis:**

- `Duration:` acá **no controla nada**. La duración sigue estando en el selector.
- Frases cortas sin comas internas. Regla asimétrica: barata de seguir.
- `Prohibited content` no apaga el audio. El audio se apaga con el toggle.

---

## Checklist antes de entregar

- [ ] ¿Se preguntó la superficie? Plataforma, versión de la UI, modo,
      resolución, opciones del selector
- [ ] ¿Hay marca, texto o relieve en cuadro? ¿Se declaró vía —foto, generación
      con gate, o POST_ONLY?
- [ ] ¿Algún nombre de tecnología, material o medida que no venga del brief o
      de la KB? — **borrarlo**
- [ ] ¿Alguna línea describe el aspecto del producto en vez de su rol? —
      borrarla
- [ ] ¿Cada referencia declara rol **y** exclusión?
- [ ] ¿La cuenta de intervalos coincide con la duración real del selector?
- [ ] ¿Un solo beat por intervalo?
- [ ] ¿Se entregó la lista de archivo → slot, en orden de carga?
- [ ] ¿Se entregaron los **dos planes** de producción?
- [ ] ¿Se recordó fijar aspect ratio y desactivar audio en la UI?
- [ ] ¿Se dijo qué mirar en el **último** frame?
