# Suite de regresión

Sin evals, un skill de prompting es una colección de opiniones. Esta suite es lo
que separa una regla de una preferencia.

Se corre cuando cambia la versión del modelo, el plan de la cuenta, o una regla
del skill.

---

## Qué se registra en cada corrida

Sin esto, la corrida no cuenta.

| Campo | Por qué |
|---|---|
| Prompt literal | Reproducibilidad. Es el requisito de nivel O |
| Plataforma y **versión que muestra la UI** | Distingue 1.5 / 2.0 / 2.5 |
| Modo, resolución, aspect ratio, toggle de audio | Son la mitad del resultado |
| Duración seleccionada | La del selector, no la del texto |
| Hash de cada archivo de referencia y su slot | `@image1` es el primero cargado |
| Optimizador on / off | Puede reescribir el prompt entero |
| Model ID devuelto, si la superficie lo expone | Prueba de qué corrió de verdad |
| Créditos antes y después | Base del costo por segundo útil |
| Duración y resolución del archivo de salida | Detecta que el selector mandó |
| Archivo generado, conservado | Sin archivo no hay evidencia |
| n de la celda | Una corrida no es un umbral |

---

## Los siete casos

| # | Caso | Qué mide | Aprueba si |
|---|---|---|---|
| **E1** | Producto estático, cámara fija | Herencia base | Geometría, color, gráfico y canto idénticos en el 100% de los frames |
| **E2** | Corte duro entre dos planos | Identidad a través del corte | El producto antes y después del corte es el mismo SKU |
| **E3** | Producto manipulado por manos | Anatomía y contacto | Cinco dedos, contacto físicamente posible, sin fusión con el objeto |
| **E4** | Texto y relieve bajo movimiento | El techo del sistema | OCR correcto en el 100% de los frames donde el texto es visible |
| **E5** | Dos referencias que compiten | Resolución de conflicto | Cada referencia gobierna solo su rol declarado |
| **E6** | Silencio | Control de capacidades | El archivo **no tiene pista de audio** |
| **E7** | Locución en post | Flujo completo | El clip se monta con voz externa sin problema de lipsync |

---

## Cómo se audita un clip

**Siempre en el último frame, no en el primero.** El primero casi siempre sale
bien; la degradación aparece al final.

Extraer frames y revisar en este orden — el primero que falla es el techo:

1. **Texto.** Caracteres, orden, forma de las letras, separación entre palabras.
   Comparar contra la fotografía maestra, no contra la memoria.
2. **Gráfico.** Trazos, medios tonos, límites de color.
3. **Geometría.** Contorno, grosor del canto, silueta. Superponer normalizado.
4. **Relieve.** Profundidad y continuidad bajo luz rasante. Es lo primero que se
   aplana.
5. **Color.** Contra los valores de la KB, no a ojo.
6. **Cámara.** Un solo movimiento, sin deriva lateral ni rotación no pedida.
7. **Personas**, si hay: dedos, ojos, textura de piel, continuidad de vestuario.

Comandos útiles:

```
ffprobe -v error -show_entries stream=codec_type,width,height,duration \
  -of default=noprint_wrappers=1 clip.mp4

ffmpeg -i clip.mp4 -vf "fps=2" frames/%03d.png

ffmpeg -i clip.mp4 -af volumedetect -f null - 2>&1 | grep max_volume
```

La presencia de un stream `codec_type=audio` con `max_volume` por encima de
−40 dB reprueba E6.

---

## Criterios de aceptación por tipo de pieza

| Tipo | Umbral |
|---|---|
| Producto con marca en cuadro | **100% de frames visibles correctos.** Un frame discrepante reprueba |
| Producto sin texto en cuadro | Geometría y color dentro de tolerancia visual |
| Claims legales o cifras | **POST_ONLY.** No se evalúa: no se genera |
| Persona | Sin defecto anatómico en ningún frame |
| Pieza de oficio sin producto | Criterio estético; sin rostro, sin texto legible, sin logos |

---

## Costo por segundo útil

```
costo_por_segundo_util = créditos_debitados / segundos_aprobados
```

Los descartes se cuentan. Registrar la tasa de descarte por tipo de pieza — es
el número que decide si conviene cambiar de modelo, y el único que hace
comparable a Seedance con Kling o Veo.

**Trampa a evitar:** ocho clips de 4 s son 32 s, no 30. Normalizar por segundo
antes de comparar contra una toma larga.

---

## Cuándo se vuelve a correr todo

- Cambia la versión del modelo que muestra la UI
- Cambia el plan o la región de la cuenta
- Cambia una regla del skill
- Un clip de producción falla de una forma que la suite no predijo — ese caso
  se agrega como E8, E9, y así
