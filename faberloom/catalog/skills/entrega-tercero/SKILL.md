---
name: "entrega-tercero"
description: "F7 del harness: prepara lo que se entrega a un tercero (fabricante, socio, cliente): piezas, orden, protección, lo CEO-ONLY y el correo que continúa la conversación; o redacta el documento de cooperación que pidió."
---

# Entrega a un tercero (F7)

v1.0 · 2026-10-28 · nace del envío del plan FootMaster Brasil a Bangni (Leo, Alaric), revisado por cuatro juicios y tres revisiones de Astra (REV-BR-01 a 03).

El análisis (F3), el plan (F4) y la presentación (F5) producen piezas. Esta fase decide **qué sale, en qué orden, con qué protección y con qué mensaje**. El CEO envía; Claude prepara y deja todo listo. Nada se envía desde aquí.

## Lugar en el harness

| Fase | Skill | Sale |
|---|---|---|
| F0a | `interrogatorio-encargo` | acta de decisiones |
| F1–F2 | `orden-obrero` | datos validados |
| F3–F4 | método del estudio, `plan-mercado` | plan y modelo económico |
| F5 | `presentar-resultados` | pieza ordenada por conclusión |
| **F7** | **`entrega-tercero`** | **manifiesto, protección, secuencia, correo, documento de cooperación** |
| F6 | `plan-mercado` modo revisión | seguimiento |

## Principio rector

Lo que sale es decisión del CEO. Claude propone la protección y la secuencia **una vez**, con su riesgo. Si el CEO decide enviar igual (por ejemplo, como muestra de capacidad), se registra la decisión y se ajusta el texto de las piezas para que no prometa una protección que no existe. No se insiste ni se repite el riesgo.

## Paso 0 — Leer el hilo antes de escribir

1. Pedir o buscar el **último mensaje intercambiado con el tercero, en los dos sentidos**, antes de redactar cualquier correo. Una sola pregunta si no está en el contexto.
2. El correo continúa la conversación: no repite saludos de presentación ni contexto ya dicho. Si el CEO anunció algo ("mañana te mando el plan"), el correo lo cumple y lo dice ("As promised…").
3. Registrar quién es el interlocutor y su rol (dueño, director comercial, responsable de marca). Cambia el orden de lectura sugerido.

## Paso 1 — Decodificar el pedido del tercero

| Qué pidió (literal) | Qué significa | Qué falta para responder |
|---|---|---|
| … | … | dato, decisión del CEO o pregunta al tercero |

Una referencia ambigua ("this customer", "the project") se aclara con el CEO en una pregunta antes de construir. Si el pedido es un documento de cooperación, aplicar el Paso 5.

## Paso 2 — Manifiesto de la entrega

| Pieza | Versión | Para quién | Clasificación | Condición para enviarla | Formato |
|---|---|---|---|---|---|

- Clasificación: `PUBLIC | PARTNER_B2B | INTERNAL | CEO-ONLY` y data class N0–N4 (`POL_VISIBILIDAD`, `POL_DATA_CLASSIFICATION`).
- Formato: PDF adjunto con nombre para el receptor (título del documento, sin "v6" ni sufijos internos); enlace a un artefacto **compartido por el CEO** (los artefactos son privados por defecto); nunca una carpeta.
- **Nunca salen:** calculadoras y anexos CEO-ONLY, notas internas, órdenes y entregas de obreros, veredictos de juicio, consultas a asesores, datasets de producto, costos de una marca propia frente a la marca del tercero.

## Paso 3 — Protección

| Opción | Cuándo |
|---|---|
| **Acuerdo firmado antes** (NNN o NDA) | se entregan datasets, contactos, condiciones de canal o estrategia que el tercero podría ejecutar sin MWT |
| **Envío en confianza** | muestra de capacidad decidida por el CEO; la pieza y el correo dicen "shared in confidence, for <tercero>'s internal evaluation, not to be circulated" y proponen firmar el acuerdo antes de pasar datos finos |
| Sin protección | solo material público |

Reglas:
- La aceptación por correo nunca reemplaza firma y sello.
- Lo fino (dataset, contactos, condiciones por canal) se retiene hasta que el acuerdo esté vigente, aunque el plan ya haya salido.
- El acuerdo se redacta en un documento limpio para negociar; la nota de diseño y las fuentes van en otro.

### Módulo contraparte china (activar si aplica)

| Punto | Regla |
|---|---|
| Formato | NNN (no divulgar, no usar, no eludir), no un NDA genérico en inglés |
| Ley y foro | ley china; tribunal con competencia sobre el domicilio **registral verificado**, sujeto a reglas de materia, grado y concentración (propiedad intelectual puede ir a otro tribunal) |
| Idioma | bilingüe, chino prevalente, revisado por jurista nativo |
| Partes | nombre chino registrado + código unificado de crédito social; firma + sello oficial (公章) + prueba de autoridad del firmante |
| Penalidad | monto acordado y sustentado; no se acumula por un mismo hecho; el tribunal puede ajustarla (art. 585 Código Civil, interpretación 2023) |
| No usar | protege el uso de la información; **no esconde exclusividad territorial**. La exclusividad se negocia aparte, con metas y contraprestación |
| No eludir | por oportunidad concreta aceptada **expresamente** en un anexo; el silencio no es aceptación |
| Relaciones existentes | excluidas por perímetro documentado (entidades, productos, arreglos) |
| Medidas urgentes | se pueden pedir sin esperar el plazo de negociación |
| Validación | abogado en China; el abogado del país del negocio revisa solo los efectos locales |

## Paso 4 — Coherencia entre lo que dice la pieza y lo que es

Antes de exportar, revisar en todas las piezas:
1. Frases sobre protección: ¿dicen "firmado" cuando está "por firmar"?
2. Cifras de la pieza contra el modelo: reproducir el motor con los valores por defecto y cuadrar al centavo.
3. Etiquetas de alcance: ¿"la empresa" cuando el modelo cubre una sola marca?
4. Promesas operativas: ¿"cada lote se libera al cumplir el hito" cuando además requiere aprobación conjunta?
5. Lo que el tercero dijo en su último mensaje (por ejemplo, el estado de la marca) está reflejado y no contradicho.

## Paso 5 — Documento de cooperación (cuando el tercero lo pide)

Hoja de términos no vinculante, 2–4 páginas, en el idioma del tercero, ordenada por conclusión (`presentar-resultados`). Estructura base, adaptable al pedido literal:

| # | Sección | Qué fija |
|---|---|---|
| 1 | Objeto y partes | qué se coopera, entidades exactas |
| 2 | Modelo de cooperación | rol y aporte de cada parte; quién importa, vende, cobra y factura |
| 3 | Territorio y canales | países, canales, venta online y marketplaces; exclusividad condicionada si se pide |
| 4 | Registro de clientes | quién registra, prueba requerida, vigencia, qué pasa si dos registran al mismo |
| 5 | Precios y margen | quién fija precio de venta y de referencia; línea donde cobra cada uno |
| 6 | Reparto de ganancias y riesgos | separar margen de fabricación, capital, financiación del socio y honorario de gestión; quién absorbe incobrables, devoluciones y tipo de cambio |
| 7 | Plan anual de trabajo | hitos, lotes con aprobación conjunta, indicadores y revisión trimestral |
| 8 | Gastos | quién paga qué, topes y aprobación |
| 9 | Inventario no vendido | recompra, consignación, liquidación, plazos y precio |
| 10 | Marca | registros por país, a nombre de quién, alternativa si se bloquea; no se transfiere marca |
| 11 | Datos e informes | sell-in, sell-out, inventario, cobro; frecuencia |
| 12 | Duración y salida | plazo, renovación, terminación, transición y compensación por cuentas desarrolladas |
| 13 | Ley y disputas | a validar por abogado |
| — | Decisiones abiertas | tabla con quién decide y para cuándo |

Parte de `plan-mercado` §4c (lados A, B y C). No inventa porcentajes ni montos: lo que no está decidido va a la tabla de decisiones abiertas.

## Paso 6 — Revisión adversaria, una por envío

- **Una** revisión de Astra por versión que sale, al final, con el módulo "Paquete de entrega" de `orden-obrero`.
- Juicio (`SKILL_COURT`) solo cuando hay una decisión del CEO discutible (enviar sin protección, pedir participación accionaria), no para pulir redacción; una corrida por decisión.
- Al recibir: verificar los hallazgos que cambian una decisión (abrir la fuente o reproducir el código) antes de aplicarlos; adoptar la redacción del obrero cuando es mejor.

## Paso 7 — Correo

En el idioma del tercero. Orden:
1. Cumple lo prometido o responde al último mensaje (Paso 0).
2. Valor del trabajo: tiempo y recursos propios invertidos, una frase, sin exagerar.
3. Qué adjunta y qué permite el modelo; enlace como `[LINK]` explícito.
4. Por dónde empezar a leer (tres o cuatro secciones).
5. Los temas que el tercero abrió (marca, precio), con la postura propuesta.
6. Confidencialidad, en una frase coherente con el Paso 3.
7. Tres pedidos accionables (precios FOB, marca, reacción a la propuesta).
8. Próximo paso con fecha.

Se entrega en el widget de redacción de correo. No se envía.

## Paso 8 — Antes de que el CEO envíe

- [ ] Enlaces compartidos desde el menú Compartir del artefacto.
- [ ] Adjuntos con nombre para el receptor.
- [ ] Nada CEO-ONLY en piezas ni enlaces (el código de una página también se lee).
- [ ] La frase de protección dice la verdad.
- [ ] Copias finales en la carpeta del plan del PC.

## Salida

`PAQUETE_ENVIO_<tercero>_<fecha>.md`: manifiesto, protección decidida, secuencia de envíos con condiciones, correo(s) y, si aplica, el documento de cooperación como documento aparte.

## Lecciones (FootMaster Brasil, oct-2026)

| Error | Regla que lo evita |
|---|---|
| NDA genérico en inglés, sin ley ni foro, frente a una fábrica china | Módulo contraparte china |
| "O con la aceptación de Leo por correo" | La aceptación por correo nunca reemplaza firma y sello |
| Cláusula de no uso leída como exclusividad sobre Brasil | No usar ≠ exclusividad |
| Alta de clientes protegidos por silencio de 10 días | Aceptación expresa por oportunidad |
| El documento decía que el NNN ya estaba firmado | Paso 4.1 |
| Correo que reiniciaba la conversación con Alaric | Paso 0 |
| Cuatro juicios y tres revisiones para un envío | Paso 6: una revisión por versión |
| Calculadora privada trimestral y panel mensual divergentes | `plan-mercado` §4d: un motor, dos salidas |
| Resultados rotulados "empresa" cuando eran solo FootMaster | Paso 4.3 |

## Formato

Español con el CEO; idioma del tercero en las piezas. Tablas para el manifiesto y las decisiones. Sin jerga.