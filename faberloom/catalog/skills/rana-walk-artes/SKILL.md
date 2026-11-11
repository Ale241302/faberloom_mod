---
name: rana-walk-artes
description: "Auditar y corregir los artes de plantilla Rana Walk: paleta, contraste, deriva de color de marca y reemplazos quirúrgicos sobre el PDF."
---

# Artes de plantilla Rana Walk

## Antes de tocar nada

Leer `ENT_MARCA_ARTES_PLANTILLA` en la KB. Contiene el principio constructivo, la paleta
declarada de los siete sistemas y las reglas D1-D4. No trabajar de memoria: los valores hex
se leen del archivo, no del brand book, porque difieren.

## El principio que hay que entender primero

El arte NO se diseña sobre la silueta. Se imprime en el textil como una lámina de dos campos
—uno claro, uno oscuro— y la plantilla se troquela dentro de un campo. Por eso el par es
bicolor: un pie sale en positivo y el otro en negativo. La rana completa solo existe en el
textil.

Consecuencia práctica: un color "funciona" o no **según el campo en que cae**, no en
abstracto. El disco del ojo en `#F8F8F8` funciona sobre cabeza de color y desaparece sobre
cabeza blanca — mismo valor, distinto resultado.

## Colores técnicos — excluir siempre

| Hex | Qué es |
|---|---|
| `#E6007E` | magenta del troquel (contorno de corte) |
| `#F8EA04` | amarillo de guía (líneas de registro) |

No son tinta de arte. Contarlos como paleta da lecturas falsas.

## Flujo

### 1. Leer antes de opinar

```
python rw_arte.py paleta "Plantilla ORCA.pdf"
```

Devuelve los colores declarados con conteo de usos y CMYK aproximado. Los valores salen del
content stream del PDF — es la verdad del archivo, no la del brand book.

### 2. Auditar

```
python rw_arte.py auditar "Plantilla ORCA.pdf"
```

Cuatro chequeos: espacio de color, contraste ΔE entre todos los pares, deriva contra la
paleta oficial, tamaño de paleta. Sale con código 1 si hay hallazgos.

ΔE es diferencia perceptual en espacio Lab, no distancia RGB. Referencia: <1 imperceptible,
<2.3 apenas visible, <5 cercano, >10 claramente distinto. Un par bajo 3 en la misma lámina
es un defecto latente.

### 3. Corregir

```
python rw_arte.py color "Plantilla ORCA.pdf" --de F8F8F8 --a FFD700
```

Edita los operadores de color en el content stream y deja el resto del archivo idéntico.
Informa cuántas ocurrencias cambió — si el número no es el esperado, revisar antes de seguir.

### 4. Verificar visualmente, siempre

```
python rw_arte.py render salida.pdf -o vista.png --dpi 300 --region 0.55,0.18,0.80,0.40
```

Región en fracciones de página. Mirar el render antes de dar por buena una corrección: el
conteo de ocurrencias dice que cambió algo, no que cambió lo correcto.

## Reglas que no se negocian

**El PDF es salida, no fuente.** Los PDF son export de Grizzly. Una corrección aplicada solo
al PDF se pierde en el siguiente export. Toda corrección tiene que llegar también al archivo
fuente — eso es un mensaje a Grizzly, no algo que se resuelva por código. Decirlo siempre.

**Nunca sobrescribir el original.** Escribir versión nueva al lado. El original es entregable
de un tercero y el rastro del antes importa.

**No convertir a SVG para editar.** El round-trip PDF→SVG→PDF reescribe el archivo entero
para cambiar un color y puede rasterizar efectos, reinterpretar fuentes y transformar
trazados. Editar el operador de color directo cambia decenas de bytes y no toca nada más.

**No inventar valores de color.** Si falta un dato, marcarlo `[PENDIENTE — NO INVENTAR]`.

## Al proponer una corrección de diseño

Dar opciones con su costo sistémico, no solo la que se ve mejor. La pregunta que decide es
si la solución **introduce un recurso gráfico nuevo** (un stroke, un color) que después hay
que replicar en los siete sistemas o queda como parche. La solución que reasigna algo que el
sistema ya tiene gana casi siempre.

Renderizar las opciones lado a lado antes de recomendar.