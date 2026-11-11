---
name: sicop-pipeline
description: Pipeline vivo de la compra publica de Costa Rica - procedimientos filtrados por rango de fecha de publicacion y rango de fecha de apertura, clasificados por estado real (publicado sin ofertas, cerrado sin adjudicar, recurrido, adjudicado no firme, en firme, muerto). Responde que abre hoy, que abre esta semana, que sigue vivo y donde todavia se puede ofertar. Usar cuando el usuario pregunte por aperturas de hoy o proximas, carteles vigentes, procesos abiertos, que esta vivo, que se puede ofertar, procesos no adjudicados, recurridos, o adjudicados pendientes de firmeza.
---

# Pipeline vivo SICOP

Carga primero `sicop-base`.

Esta skill existe porque el MCP **no tiene un indice por fecha**. Ninguna herramienta filtra por `FECHA_APERTURA` ni por `FECHA_PUBLICACION`. La skill reconstruye ese indice con la propiedad estructural del identificador. No improvises otro camino: los dos atajos obvios estan cerrados y se documentan abajo.

## Lo que responde

- Que abre hoy / esta semana / entre dos fechas
- Que se publico entre dos fechas y cuando abre
- Que sigue vivo: publicado, cerrado sin adjudicar, adjudicado pero no en firme
- Que esta recurrido y por lo tanto congelado
- Que ya murio para efectos comerciales (contratado, recibido)

## Callejones sin salida — no los repitas

**`sicop_tiempos_por_etapa` sin `nro_sicop` no sirve para fechas recientes.** Devuelve un barrido crudo ordenado ascendente desde 2020 y **no tiene parametro de offset**. Con `limit=20000` la respuesta pesa 10.3 MB y llega apenas a apertura 2020-10-12. La tabla `etapas` tiene 1.2M filas: paginar hasta 2026 es imposible por esta via.

**`sicop_senales` no es un feed de aperturas.** El ciclo diario solo emite `cartel_objetado_nuevo` y `sancion_nueva`. Usarlo como proxy de "que abre hoy" produce un subconjunto sesgado hacia carteles con recurso. Sirve como semilla de nros SICOP, nada mas.

**`sicop_lineas_procedimiento` viene vacio en carteles no adjudicados.** `lineas_cartel` no esta poblado para procedimientos vivos. **Consecuencia dura: en un cartel abierto no se puede saber que producto pide desde este MCP.** No inventes el objeto contractual ni lo infieras del nombre de la institucion. Marca `objeto = NO MEDIBLE (lineas_cartel vacio en procedimientos vivos)` y, si el usuario necesita el objeto, dile que hay que abrir el expediente en el portal SICOP.

## La clave: el identificador es un indice de fecha

`NRO_SICOP` tiene formato `AAAA MM NNNNN` — anio, mes de publicacion, y un serial de 5 digitos **monotono creciente con la fecha de publicacion dentro de ese mes**.

Verificado: `20260800001` → publicado 2026-08-01 · `20260802200` → publicado 2026-08-19 · `20260802500` → no existe (fin del mes).

De ahi salen dos cosas gratis:

- El **mes de publicacion se lee del identificador**, sin consultar nada.
- Un rango de fechas de publicacion se traduce a un **rango contiguo de seriales** por busqueda binaria: ~12 llamadas por extremo en vez de barrer miles.

## Traducir apertura a publicacion

El filtro que pide el usuario suele ser por **apertura**, pero el indice es por **publicacion**. El puente es el rezago publicacion→apertura, que en los casos verificados va de **7 a 22 dias**.

Regla operativa: para cubrir aperturas en `[A1, A2]`, barre publicaciones en `[A1 - 45, A2]`. El margen de 45 dias absorbe prorrogas y modificaciones de cartel. **Barrer menos pierde carteles con plazo largo.** Despues del barrido filtras por `FECHA_APERTURA` real, asi que el margen extra no ensucia el resultado, solo cuesta llamadas.

## Rutina

### 1. Acotar el rango de seriales (binaria)

Para cada mes tocado por `[A1-45, A2]`, busca por binaria el serial minimo con `FECHA_PUBLICACION >= d1` y el maximo con `<= d2`. Sonda con `sicop_tiempos_por_etapa(nro_sicop=...)`.

Cotas del serial: el minimo es `00001`; el maximo real de un mes ronda **2300**. Arranca la binaria con hi=3000 y trata "sin resultados" como *pasado el fin del mes* — es decir, retrocede hi.

Ojo: hay seriales huecos (procedimientos anulados). Si una sonda cae en un hueco, desplaza +1/-1 hasta encontrar vecino con datos antes de decidir el lado.

### 2. Barrer el rango

`sicop_tiempos_por_etapa` por cada serial del rango. Quedate con `FECHA_PUBLICACION`, `FECHA_APERTURA`, `FECHA_ADJUDICACION`, `CEDULA_INSTITUCION`, `NUMERO_PROCEDIMIENTO`. **Deduplica**: la herramienta repite la misma fila una vez por tramo (`N_TRAMOS`).

Filtra por `FECHA_APERTURA` dentro de `[A1, A2]`. Ese es el universo.

En chat, si el rango supera ~150 seriales, **delega a subagentes en paralelo** por bloques, con instruccion de devolver tabla en texto plano y no JSON. En el harness local, es un loop.

### 3. Clasificar el estado

`sicop_expediente` por cada superviviente. Los flags dan el estado directo:

| Estado | Condicion | Vivo |
|---|---|---|
| `PUBLICADO` | `T_CARTEL=S`, `T_OFERTAS` null | si — apertura pendiente, **aun se puede ofertar** |
| `CERRADO_SIN_ADJUDICAR` | `T_OFERTAS=S`, `T_ADJUDICADO` null | si — en evaluacion |
| `ADJUDICADO_NO_FIRME` | `T_ADJUDICADO=S`, `T_ACTO_FIRME` null | si — ventana de apelacion abierta |
| `EN_FIRME` | `T_ACTO_FIRME=S`, `T_CONTRATO` null | parcial — firme, sin contrato |
| `CONTRATADO` | `T_CONTRATO=S` | no |
| `EJECUTADO` | `T_RECIBIDO=S` | no |

`T_ADJUDICADO` sin `T_ACTO_FIRME` es la fila mas valiosa del tablero: hay adjudicacion pero el acto no quedo firme. Ahi todavia se mueve la aguja.

### 4. Cruzar recurrido y objetado

`sicop_recursos_procedimiento` por nro (recursos con su desenlace) y `sicop_carteles_objetados` una sola vez para la lista completa (665 filas, cabe entera). Marca dos banderas independientes del estado: `RECURRIDO` y `OBJETADO`. Un procedimiento recurrido esta congelado — el plazo real de apertura o de firmeza no es el que dice la fecha.

### 5. Filtrar al perimetro

Los procedimientos **vivos no traen lineas** (ver callejones). En vivos solo puedes filtrar por institucion y por tipo de procedimiento (`LE`, `LD`, `LR`… en `NUMERO_PROCEDIMIENTO`). El filtro por familia UNSPSC o por producto **solo aplica a los ya adjudicados**, via `sicop_adjudicaciones`.

Dilo asi en el entregable en vez de fingir un filtro de producto que no existe.

## Formato de salida

```
PIPELINE SICOP — publicados [d1..d2] · apertura [A1..A2]
Universo: N procedimientos · barridos S seriales · huecos H

ABRE HOY
  nro | institucion | tipo | publicado | banderas

ABRE EN LOS PROXIMOS 7 DIAS
  nro | institucion | tipo | apertura | banderas

EN EVALUACION (cerrado, sin adjudicar)
  nro | institucion | apertura | dias desde apertura

ADJUDICADO NO FIRME
  nro | institucion | fecha adjudicacion | recurrido?

EN FIRME SIN CONTRATO
  nro | institucion | fecha adjudicacion

NO MEDIBLE: objeto contractual de los procedimientos vivos (lineas_cartel vacio)
```

Ordena cada bloque por fecha ascendente. Banderas: `REC` recurrido, `OBJ` cartel objetado.

Declara siempre tres numeros: seriales barridos, huecos encontrados, procedimientos que quedaron tras el filtro de apertura. Sin eso el lector no sabe si el tablero esta completo.

## Cota honesta

Este metodo reconstruye por fuerza bruta acotada un indice que la fuente ya tiene. Cuesta entre 30 y 400 llamadas segun el rango. Funciona, y es lo correcto mientras el MCP no exponga el filtro.

**La solucion real es una herramienta nueva en el servidor**, no mas skill. Spec minima:

```
sicop_procedimientos_por_fecha(
    publicacion_desde, publicacion_hasta,
    apertura_desde,    apertura_hasta,
    estado,        # publicado | cerrado_sin_adjudicar | adjudicado_no_firme | en_firme | vivo | todos
    institucion,   # opcional
    limit
)
```

Es un `SELECT` sobre `etapas` con dos `BETWEEN` y un `LEFT JOIN` contra `adjudicaciones`, `adjudicaciones_firme`, `contratos` y `recursos` para derivar el estado. Sustituye las 400 llamadas por una. **Si el usuario va a usar el pipeline de forma recurrente, recomiendale construir esa herramienta antes que seguir barriendo** — y cuando exista, esta skill se reduce a llamarla y formatear.

## Programacion

Para uso recurrente, tarea programada diaria temprano con ventana `apertura = [hoy, hoy+7]` y `publicacion = [hoy-45, hoy]`. Usa las herramientas de scheduling del entorno, nunca cron local. El parte de aperturas es complementario al parte de senales de `sicop-vigilancia`: uno mira adelante, el otro mira lo que se movio.
