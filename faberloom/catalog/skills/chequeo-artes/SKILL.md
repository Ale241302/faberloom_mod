---
name: chequeo-artes
description: "Chequear cualquier pieza gráfica antes de producirla o publicarla, con los umbrales reales de la industria y los requisitos vigentes de cada destino."
---

# Chequeo de artes

Revisar una pieza antes de que salga. El objetivo es encontrar lo que **no se ve mirando el
archivo**: dos versiones casi idénticas del mismo color de marca, un elemento que desaparece
sobre su fondo, un espacio de color que la fábrica va a reinterpretar por su cuenta.

Un humano revisando el archivo a ojo no detecta una diferencia de ΔE00 0.3. La máquina sí.
Ese es todo el valor de este chequeo — no reemplaza el criterio de diseño, cubre el punto
ciego del ojo.

## 1. Establecer el destino primero

El destino define qué se chequea y con qué umbral. No arrancar sin saberlo.

| Destino | Qué importa |
|---|---|
| Textil, empaque, impreso | Referencia de color ejecutable por la fábrica, tolerancia pactada, sangrado, troquel, resolución, mínimos tipográficos de etiquetado |
| Redes (post, story, reel) | Dimensiones y ratio, zonas seguras, contraste de texto, legibilidad en miniatura |
| Amazon (listing, A+) | Requisitos de la plataforma, fondo, ocupación del cuadro, texto sobre imagen |
| Web / e-mail | RGB, peso, contraste de accesibilidad, comportamiento en oscuro |

## 2. ΔE: cómo medir diferencia de color

**Usar CIEDE2000 (ΔE00), ponderación 1:1:1.** Es el estándar moderno, el que X-Rite y
Datacolor recomiendan y el que ISO TC130 usa para reemplazar a CIE76.

**No usar CIE76.** Sobre-pesa los azules y sub-pesa el resto. Y nunca comparar un número
calculado con una fórmula contra un umbral definido con otra — no son la misma escala, y esa
mezcla hace aprobar muestras que deberían rechazarse.

Un umbral sin **fórmula, iluminante y sustrato** declarados no es una tolerancia: es una
discusión futura.

### Umbrales de referencia (textil y calzado)

| ΔE00 | Lectura |
|---|---|
| ≤ 1.0 | Tolerancia de lote conforme — lo que se pacta en un tech pack |
| ≤ 1.2 | Ampliada para neones y saturados: el espectrofotómetro no es fiable en esa gama |
| 1.0 – 2.0 | Rango de trabajo común en apparel |
| > 2.0 | Deriva visible entre lotes |

En impresión comercial el pass/fail típico es mucho más holgado (ΔE CMC 2.0 o más). Exigir
una tolerancia que el proceso no puede sostener genera rechazos y costo, no mejor color.

## 3. Chequeos

### Colores irresolubles por el proceso — el más importante

Dos colores de la pieza separados por **menos que la tolerancia de lote** están más cerca
entre sí que la resolución del proceso. La fábrica no puede reproducirlos como distintos de
forma consistente: van a salir iguales o distintos según la tanda, al azar.

Este hallazgo no se argumenta como preferencia estética sino como **variación aleatoria metida
en el archivo**. Es el argumento que gana la discusión con el diseñador o la agencia.

### Deriva de color de marca

Comparar cada color contra la paleta oficial y marcar los que caen **cerca pero no encima**.
Dos versiones del mismo color de marca conviviendo en una pieza separan en dos tintas.

Informar siempre **cuántos usos tiene cada variante**: cuando la desviada tiene más usos que
la oficial, la mayoría de la pieza no está en color de marca, y eso cambia la urgencia.

### Contraste entre elementos

Medir ΔE00 entre todos los pares. Un color puede estar por encima de la tolerancia de lote
—el proceso lo distingue— y aun así ser ilegible para el ojo sobre su fondo. Son dos
preguntas distintas.

**El contraste se evalúa contra el fondo real del elemento, no en abstracto.** El mismo color
funciona sobre un fondo y desaparece sobre otro.

### Espacio de color y referencia de producción

Para pieza física, **el archivo digital no es una referencia de producción**. Ni RGB ni CMYK
bastan: una fábrica no puede teñir contra un color visto en una pantalla retroiluminada. Lo
que sirve es código de sistema físico + muestra aprobada + tolerancia escrita.

En textil la referencia es **Pantone FHI**: TCX (algodón) para producción, TPG (papel) para
comunicación. TPX está descontinuado desde 2019. PMS Coated/Uncoated **nunca** es
intercambiable con FHI aunque el color parezca igual.

### Gama alcanzable

Antes de pactar cualquier tolerancia, verificar que los colores **se puedan alcanzar** con el
proceso. Ninguna tolerancia contractual compensa un color fuera de gama. Los saturados y
neones son los sospechosos.

### Colores técnicos

Troqueles, líneas de registro, guías, marcas de corte: no son tinta de arte. Identificarlos y
excluirlos del conteo, o toda la lectura sale falsa.

### Texto

Contraste y tamaño real de impresión — un trazo fino se engorda en textil y se pierde en
offset chico. Si la pieza es empaque para venta internacional, el mínimo tipográfico puede
ser una obligación legal y no una decisión de diseño: verificar contra la normativa del
mercado destino antes de dar por buena la maqueta.

## 4. Reportar

Un hallazgo útil dice **qué pasa, dónde, y qué bloquea**. "Hay dos azules parecidos" no
sirve; "el mint oficial tiene 3 usos y una variante a ΔE00 0.26 tiene 6, o sea que la mayoría
del mint de la pieza no es el de marca, y ese par está por debajo de la tolerancia de lote:
la fábrica no puede distinguirlos" sí.

Ordenar por severidad real. Un color de marca desviado en una pieza que ya se produjo pesa
más que una paleta un poco grande.

## 5. Corregir

**Editar el archivo en su formato nativo.** No convertir a un formato intermedio para
corregir: el round-trip reescribe todo el archivo para cambiar un valor y puede rasterizar
efectos, reinterpretar fuentes y transformar trazados.

**Nunca sobrescribir el original**, sobre todo si es entregable de un tercero.

**Verificar visualmente.** Que el conteo diga que cambió algo no prueba que cambió lo
correcto.

**Distinguir salida de fuente.** Un PDF o JPG exportado es salida: corregir ahí resuelve esa
copia y el próximo export trae el defecto de vuelta. Toda corrección tiene que llegar al
archivo fuente — decirlo siempre, aunque el fuente esté en manos de otro.

## 6. Cuándo el chequeo del archivo no alcanza

Para pieza física, el archivo es solo el principio. Preguntar también:

- **¿Qué le hace el proceso al color después de imprimirlo?** Calor, laminado, adhesivo y
  acabado pueden mover el tono. Si hay un paso térmico posterior a la impresión, la
  aprobación de color debe hacerse **después** de ese paso: aprobar antes es aprobar un color
  que dejará de existir.
- **¿Sobre qué se aprueba?** Muestra sobre el sustrato real de producción, evaluada en cabina
  bajo dos iluminantes (D65 y uno de retail, para detectar metamerismo), firmada y archivada
  en duplicado.
- **¿Qué varía entre lotes?** El blanco del sustrato base mueve todos los colores claros.

## Dónde vive la data

El skill trae el método. Los valores de la marca —paleta oficial, colores técnicos, reglas de
sistema, tolerancias pactadas, requisitos por destino— se leen del brand pack o de la KB,
nunca de memoria y nunca del brand book cuando el archivo dice otra cosa. **El archivo es la
verdad**; el brand book es la intención, y la diferencia entre ambos suele ser el hallazgo.

Las especificaciones de plataforma caducan: verificarlas contra la fuente oficial antes de
citarlas, no reproducirlas de memoria.

Si falta un dato, marcarlo como pendiente. No inventar valores de color ni umbrales.