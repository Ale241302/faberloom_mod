---
name: amazon-assets
description: "Produce el paquete visual y audiovisual de un listing de Amazon — imagen principal, galería secundaria, A+ Content, Brand Story y video — con gates deterministas de archivo. Úsalo cuando el usuario pida imágenes para Amazon, fotos de producto para un listing, infografías de galería, A+, Brand Story, video de PDP, o diga que su listing \"se ve pobre\", \"no convierte\" o \"me rechazaron la imagen\". Complementa a design-loop: misma familia, distinto artefacto."
---

# amazon-assets

design-loop produce algo navegable. Esto produce **archivos**. Los gates son
distintos: no hay viewport ni consola, hay peso, perfil de color, fondo blanco
puro y OCR. Se verifican con script, no con criterio.

Tres reglas de cabecera:

> **La MAIN no vende, filtra.** Su único trabajo es ganar el clic en una
> cuadrícula de resultados a 200 px. Lo que vende es PT01.

> **Prueba del pulgar.** Toda pieza se juzga primero al tamaño en que se va a
> ver por primera vez, no al tamaño en que se produjo. Si a 200 px no se lee, no
> existe — por más correcta que esté a 2000.

> **Píxeles congelados.** Ningún modelo generativo toca los píxeles del
> producto. Nunca. Ver A2.

## De dónde salen las specs

**Este skill no contiene medidas.** Las medidas cambian y viven como dato:

| Dato | Dónde |
|---|---|
| px, peso, perfil, límites de módulo | `.brand/amazon.yaml` |
| paleta, tipografía, lockup, voz | `.brand/brand.yaml` |
| cifras publicables y su respaldo | `.brand/evidencia.yaml` |
| qué se dice de cada producto y tecnología, y con qué atributo va | `.brand/mensajes.yaml` |
| qué es visible en cada vista del producto | `.brand/productos/<sistema>.yaml` |

Si no existe `.brand/`, el primer paso es construirlo o pedir las specs. **No
inventes una medida ni la traigas de memoria**: las de Amazon se verifican en el
Category Style Guide de la categoría del producto, que es distinto por
categoría. Una regla de calzado no aplica a un accesorio de calzado.

## Ledger

Todo vive en `.amazon/<asin-o-slug>/`:

```
guion.md          A1 - el trabajo asignado a cada slot
fuentes/          A0 - las fotos reales de las que se parte
mascaras/         A2 - las segmentaciones, versionadas
salida/           las piezas finales con nomenclatura de bulk
preflight.json    A6 - la última corrida del validador
changelog.md      cada cambio con su motivo
```

---

## A0 — INVENTARIO

Antes de producir nada, **listá la fotografía real que existe**. Esta fase
decide el resto: la mitad de los listings malos son un problema de materia
prima, no de diseño.

Por cada foto: qué muestra, resolución, si tiene fondo aislable, si la luz es
consistente con las demás.

**Gate:** existe al menos un packshot del producto en resolución suficiente para
la MAIN. Si no existe, el ciclo se detiene acá y se pide una sesión de fotos.
Ninguna cantidad de diseño arregla la falta de un packshot.

**Lo que falta se declara, no se genera.** Si no hay foto del producto en uso,
la pieza se resuelve con tratamiento gráfico o no se hace. Una foto generada del
producto presentada como real es el mismo problema que un testimonio inventado.

---

## A1 — GUIÓN DE GALERÍA

La galería es una **secuencia argumental**, no una carpeta de fotos bonitas. Se
escribe antes de producir.

Cada slot recibe **un solo trabajo**. Si dos slots hacen el mismo trabajo, uno
sobra. El error típico es tener nueve fotos del producto desde nueve ángulos:
eso es un slot, no nueve.

Los trabajos que suelen hacer falta, en orden de a cuál cuesta más renunciar:

| Slot | Trabajo | Por qué ahí |
|---|---|---|
| MAIN | ganar el clic | única pieza que compite fuera del listing |
| PT01 | el diferenciador | la segunda más vista con enorme diferencia |
| PT02 | de qué está hecho | responde "por qué cuesta más" |
| PT03 | en uso / escala | resuelve "¿me sirve a mí?" |
| PT04 | variedad de aplicación | amplía el mercado percibido |
| PT05 | cómo elegir (talla, medida) | quita la fricción de compra |
| PT06 | beneficios | refuerza, no convence |
| PT07 | detalle macro | señal de calidad |
| PT08 | qué llega a la caja | quita la última duda |

Este orden es un punto de partida, no un dogma. **Cuestionalo contra lo que
hace dudar al comprador de ese producto.** Si la objeción principal es la talla,
esa pieza sube.

**Regla del argumento:** si el visitante ve solo MAIN y PT01 y cierra, ¿entendió
la propuesta? Si no, el diferenciador no está en PT01.

**Gate:** `guion.md` con los 9 slots, un trabajo por slot, sin repetidos.

---

## A2 — PRODUCCIÓN · píxeles congelados

Este es el núcleo técnico del skill.

**El pipeline, sin excepciones:**

```
foto real
  → segmentación (rembg u2net + alpha matting)
  → máscara guardada y versionada
  → el generativo produce SOLO fondo / escena / luz
  → composición del producto original sobre la escena
  → verificación SSIM sobre la región enmascarada vs el packshot
```

El generativo **nunca** recibe la instrucción de dibujar el producto. Recibe la
instrucción de dibujar el mundo alrededor de un hueco.

**Umbral:** SSIM > 0.98 sobre la región del producto. Por debajo de eso, el
producto se movió o se redibujó y la pieza se descarta. No se negocia el umbral;
se rehace la composición.

### La única excepción

Cuando en la vista **solo son visibles marcas planas** — un lockup, una
tipografía, un degradado — y no una ilustración con estructura, los modelos las
reproducen correctamente y componer es innecesario. La prueba es OCR + muestreo
de color, no la impresión visual.

Si en la vista es visible cualquier ilustración, arte figurativo o patrón con
geometría, **no hay excepción**.

### La regla de prompt que evita el 90 % de los desastres

> **Describí únicamente lo que la vista declara visible.**

Mencionar en el prompt un elemento que en esa vista está tapado no lo preserva:
le pide al modelo que lo invente. El resultado es arte que se parece al producto
sin serlo — el peor error posible, porque pasa desapercibido.

Por eso la ficha de producto en `.brand/productos/<sistema>.yaml` declara
`vistas` con `visible` y `oculto`. **Leela antes de escribir un prompt.** Si el
producto no tiene ficha de vistas, escribila primero.

**Gate:** cada pieza con producto tiene su máscara en `mascaras/` y su SSIM
registrado.

---

## A3 — TEXTO EN PIEZA

Amazon no es una landing. El texto de una infografía se lee en tres segundos, de
lado, en un teléfono.

- **Máximo 6 palabras por bloque.** Si necesitás una oración, es copy de
  bullets, no de imagen.
- **Cuerpo mínimo: 1/20 del lado corto.** En 2000×2000 eso es 100 px. Suena
  enorme en el archivo; es lo correcto en pantalla.
- **Una jerarquía por pieza.** Un titular, un apoyo. No tres niveles.
- **Nada de texto en la MAIN.** Cero. Ni el logo.

### Claims

### Cruces de atributo

Antes de los claims, una verificación que ningún validador atrapa. Toda pieza
que nombre una tecnología, un componente o un material **junto a** un animal,
una cifra, un beneficio o un modelo biológico, pasa por `.brand/mensajes.yaml`
y se verifica dos veces:

- **la asociación**: que el atributo sea el de ese componente y no el del de al lado
- **la pertenencia**: que ese componente esté en ESTE producto

Una infografía que muestra la tecnología correcta con el animal equivocado se ve
perfecta, pasa el preflight, y es falsa. El OCR no la detecta porque el texto
está bien escrito. Este check es humano y va antes de producir, no después.

**Lo que NO verificás: la metáfora en sí.** Una asociación de marca declarada en
`mensajes.yaml` está aprobada; no le pidas literatura científica. "Inspirado en
el elefante" invoca lo que el lector ya asocia, no afirma un mecanismo, y una
metáfora no necesita paper. Auditar una analogía aprobada bloquea trabajo
resuelto y no encuentra nada.

La frase cambia de registro, y ahí sí necesita fuente, **cuando el número se le
cuelga al animal en vez de a la tecnología**: "PORON absorbe el 90 %" es un dato
del material y se respalda en `evidencia.yaml`; "el pájaro carpintero amortigua
el 90 %" es una afirmación sobre un ave y hay que probarla. Misma cifra, dos
registros, dos estándares.

### Claims

Todo texto pasa por `.brand/evidencia.yaml` antes de existir:

- Una cifra sin respaldo documentado **no se publica**, por más que sea del
  fabricante. "Lo dijo el proveedor" no es una fuente hasta que está por escrito.
- Los claims médicos o de salud se reescriben a lenguaje defendible. Describir
  qué hace el producto es legal; prometer un efecto en el cuerpo, no.
- **Lo que está prohibido por Amazon está en `.brand/amazon.yaml`** — badges,
  citas de reseñas, precios, garantías, contacto. El validador lo verifica.

**Gate:** OCR de todas las piezas contrastado contra la lista negra. Cero
coincidencias.

---

## A4 — A+ Y BRAND STORY

La galería responde "¿es este el producto?". A+ responde **"¿es esta la marca?"**.

Si el A+ repite la galería, no está haciendo nada. Cambia el trabajo:

| Galería | A+ |
|---|---|
| el producto | el sistema al que pertenece |
| esta unidad | por qué existe la línea |
| specs | criterio |
| convencer | dar permiso para pagar más |

**Restricciones que rompen A+ más seguido:** garantías, envío, QR, comparar con
competidores por nombre, precio, llamados a la acción, cualquier cosa con
fecha de vencimiento, y **reutilizar imágenes de la galería** — eso último es
el error más común y el más fácil de evitar.

Brand Story es una tira horizontal que se desplaza. Se diseña como **secuencia
con continuidad**, no como cinco tarjetas sueltas: si el fondo o el ritmo no
conectan, se lee como un carrusel de banners.

---

## A5 — AUDIOVISUAL

Un video de PDP no es un comercial. Reglas duras:

1. **Los primeros 3 segundos muestran el producto.** No el logo, no una escena
   de estilo de vida, no un fundido. Producto, en cuadro, reconocible.
2. **Se diseña sin sonido.** Asumí que nadie lo escucha. Todo lo que el audio
   diría va en texto quemado. Si el video no funciona en silencio, no funciona.
3. **Un solo mensaje.** Un video que explica cinco beneficios no explica ninguno.
4. **Sin cierre.** No hay CTA, no hay pantalla final de logo con música. El
   usuario ya está en la página de compra; sacarlo de ahí no tiene destino.
5. **Loop limpio** si dura poco: el último cuadro debe poder empalmar con el
   primero.

Duración útil: la mínima que cuente el mensaje. Un plano de 12 segundos bien
elegido supera a 60 segundos de montaje.

**Personas generadas por IA:** si el video o la imagen contienen una persona
fotorrealista generada, hay obligación de declararla en metadatos. El campo, el
valor y el comando están en `.brand/amazon.yaml > politica_ia`. No aplica a
producto, fondos ni escenas. **Declararlo es barato; que te lo detecten sin
declarar, no.**

---

## A6 — PREFLIGHT

Acá no hay criterio. Corre el script y pasa o no pasa.

```bash
python scripts/preflight_amazon.py salida/ --specs .brand/amazon.yaml
```

Verifica, por pieza:

| Check | Aplica a | Falla si |
|---|---|---|
| dimensión | todas | lado largo bajo el mínimo |
| perfil de color | todas | no es sRGB |
| peso | todas | sobre el límite del tipo de pieza |
| fondo blanco puro | MAIN | algún píxel del borde ≠ (255,255,255) |
| ocupación | MAIN | bounding box fuera del rango de área |
| sin texto | MAIN | OCR devuelve cualquier cadena |
| sin bordes | MAIN | línea continua distinta en el perímetro |
| nomenclatura | todas | no coincide con el patrón de bulk |
| lista negra | todas | OCR contiene un término prohibido |
| etiqueta IA | declaradas | falta el valor en XMP |

**Gate de entrega:** `preflight.json` sin fallos. Un rechazo de Amazon en 2026
es automático y silencioso — la pieza simplemente no aparece, y a veces suprime
el listing entero. Verificar antes cuesta un minuto.

### Criterio de salida

- [ ] las 9 piezas existen y cada una hace un trabajo distinto
- [ ] MAIN cumple la regla de la categoría, **verificada en su Style Guide**
- [ ] toda pieza con producto tiene máscara y SSIM > 0.98
- [ ] ningún prompt describió un elemento no visible en la vista
- [ ] texto legible a 1/20 del lado corto
- [ ] cero cifras sin respaldo en `evidencia.yaml`
- [ ] cada tecnología nombrada verificada en `mensajes.yaml`: su atributo es el suyo y pertenece a este producto
- [ ] A+ no reutiliza imágenes de la galería
- [ ] video funciona en silencio y muestra producto en los primeros 3 s
- [ ] personas sintéticas declaradas en XMP
- [ ] `preflight.json` limpio
- [ ] prueba del pulgar hecha a 200 px, mirando, no midiendo

---

## Cuando el listing no convierte

| Síntoma | Causa casi siempre | Movida |
|---|---|---|
| Impresiones sí, clics no | la MAIN no se distingue a 200 px | A1: la MAIN es un problema de silueta y contraste, no de detalle |
| Clics sí, ventas no | PT01 no muestra el diferenciador | A1: reordenar el guión |
| "Se ve barato" | fotos con luz inconsistente entre sí | A0: falta materia prima, no diseño |
| El producto se ve raro | el generativo lo tocó | A2: el prompt describió algo no visible |
| Amazon rechazó la imagen | fondo casi blanco, o texto en MAIN | A6: correr el preflight |
| A+ no aporta | repite la galería | A4: cambiar el trabajo, no las fotos |
| Devoluciones por talla | la pieza de medida está enterrada | A1: subirla de slot |

## Señales de que el ciclo se está trabando

- **Estás iterando prompts.** Tres generaciones fallidas seguidas no se arreglan
  con una cuarta. El problema está en A2 o en la ficha de vistas.
- **Estás produciendo sin guión.** Si no podés decir qué trabajo hace la pieza
  que estás montando, volvé a A1.
- **Vas a publicar una cifra que no encontraste.** Parás y la marcás como
  faltante. Una cifra inventada en una imagen de Amazon es un riesgo legal, no
  un detalle de copy.
