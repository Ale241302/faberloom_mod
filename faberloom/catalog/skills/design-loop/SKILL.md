---
name: design-loop
description: "Ciclo de diseño con fases y gates: carril funcional vs marketing, catálogo de fuentes y recursos, shortlist de referencias propuesta antes de preguntar, QA ejecutable en Playwright, linter anti-slop, claims.json y handoff."
---

# design-loop

Un ciclo de diseño con **fases, gates y evidencia**. Dos reglas de cabecera:

> La primera pasada es el 80 %. El 20 % restante no sale de "mejorá el diseño"
> sino de mediciones concretas contra capturas reales. Pero ese 80 % se muestra
> **por bloques y en el momento**, no como una entrega completa al final.

> El ciclo termina. Son 6 fases y **máximo 2 pasadas de refinamiento**.
> Un bucle abierto de auto-QA empeora lo que una revisión dirigida arregla.

## Las tres palancas, en orden de impacto

Cuando algo "se ve hecho con IA", casi siempre falla una de estas tres, en
este orden. Atacalas en orden; no empieces por la tercera.

1. **Tipografía.** Una sola familia distintiva, usada con decisión, es la
   palanca más grande que existe contra el aspecto generado. Antes que
   cualquier ajuste de color o sombra, preguntá qué tipografía carga la página.
2. **Referencias concretas.** Sin tres URLs reales y qué se toma de cada una,
   el modelo colapsa a su promedio. Los adjetivos no anclan nada. Que el usuario
   no las haya dado nunca es excusa: el **Catálogo de fuentes** de más abajo
   existe para que siempre haya de dónde sacarlas.
3. **Contenido real.** Lorem, "Jane Doe" y stock genérico delatan más que
   cualquier decisión visual.

---

## Los dos carriles

**Esta es la primera decisión del ciclo y condiciona todas las fases.** Se
resuelve en F0, antes del brief, con una pregunta: **¿esta pieza la mira
alguien, o la usa alguien?**

- **Carril M (marketing).** Landing, sitio institucional, portfolio, página de
  producto, campaña. El diseño *es* parte del producto. Se juzga por si
  convence.
- **Carril F (funcional).** Dashboard, panel de administración, herramienta
  interna, app de trabajo, formulario largo, tabla operativa. El diseño
  *sostiene* al producto. Se juzga por si alguien puede trabajar ocho horas
  ahí sin odiarlo.

Correr el carril equivocado es el error más caro del ciclo, porque no se ve:
produce un dashboard bonito e inusable, o una landing correcta y muerta.

**Piezas mixtas.** Un producto con landing y aplicación son **dos ciclos**, no
uno con criterio promediado. Comparten `tokens.json` y nada más. La landing
puede ser arriesgada; la app no. Si un mismo ciclo tiene que cubrir las dos,
declaralo y corré F3 a F5 por separado para cada superficie.

### Qué cambia en cada carril

| Fase | Carril M | Carril F |
|---|---|---|
| F1 dials | `DESIGN_VARIANCE` manda, 5-9 | `VISUAL_DENSITY` manda; `DESIGN_VARIANCE` ≤ 3 |
| F1 referencias | 3 sitios reales | 3 herramientas reales que la gente usa a diario |
| F2 origen | tipografía distintiva primero | biblioteca de componentes primero |
| F3 gate de entrada | el hero | **la vista más densa**, no la más linda |
| F3 copy | promesa, CTA único, SEO | etiquetas, microcopy de error, estados vacíos |
| F4 | un momento firmado | **cero momentos firmados**; solo estado y feedback |
| F5 | 3 viewports × 2 temas | + los cuatro estados y la prueba de volumen |
| Anti-slop | gate estético | gate de densidad y escaneabilidad |

Todo lo que sigue vale para los dos carriles salvo donde diga **[M]** o **[F]**.

**El consejo de diseño que circula asume carril M sin declararlo.** Tutoriales,
hilos y videos sobre "webs hechas con IA" están calibrados para landings de
agencia: movimiento constante, scroll coreografiado, hero animado. Importar eso
a una herramienta produce exactamente el dashboard bonito e inusable. Antes de
adoptar una técnica de una fuente externa, preguntá para qué carril fue escrita.

---

## Quién decide qué

Esta es la regla de cabecera número tres, y va antes que cualquier fase.

**Decisiones del ciclo.** Las tomás vos. Si el usuario no responde, proponés,
declarás la hipótesis y seguís:

referencias estéticas · dials · escala tipográfica · espaciado · easing y
duraciones · retícula · nombres de las direcciones exploradas · orden interno de
un bloque · elección de sustituto tipográfico

**Decisiones del dueño.** Nunca se resuelven por hipótesis, ni aunque las hayas
preguntado cinco veces:

si el sitio vende o posiciona · cuál es el CTA primario · la dirección visual de
la marca · el precio y cómo se muestra · qué claims se publican · qué fuentes de
contenido se usan y cuáles se descartan · la arquitectura de información ·
reescribir o reemplazar copy aprobado

Si falta una del dueño, **el ciclo se detiene ahí**. No se declara hipótesis, no
se avanza a la fase siguiente con un supuesto: se dice en una línea qué decisión
falta, qué bloquea, y se para. Un ciclo detenido con la pregunta clara vale más
que un entregable construido sobre un supuesto que hay que tirar.

**Si el usuario descarta una fuente, queda descartada para todo el ciclo.** No
vuelve como argumento, ni en el changelog, ni como "pero coincide con". Descartada
significa que deja de existir para este proyecto.

### Cuando el dueño no está en la conversación

En trabajo para cliente, quien opera la sesión suele ser un intermediario que
no puede aprobar una decisión del dueño. Si parás el ciclo esperando a alguien
que no está, lo trabás indefinidamente.

En F0, una sola línea en el brief: **quién aprueba, y qué puede aprobar quien
te está hablando.** Con eso, una decisión del dueño que el interlocutor no
puede tomar deja de ser una parada y pasa a ser un **pendiente declarado**: se
anota en `changelog.md` como bloqueante con fecha, se sigue con el resto del
alcance que no dependa de ella, y **no se construye encima**. La diferencia
entre parar y seguir con un pendiente es si lo que falta bloquea la fase
siguiente o solo un bloque.

Lo que nunca cambia: nadie aprueba por hipótesis una decisión del dueño.

---

## Carriles transversales

No son fases: aplican en todas. Cada uno tiene su gate en F5.

**Verdad.** Nada se inventa: ni testimonios, ni métricas, ni logos, ni
certificaciones, ni fotografía generada presentada como producto real. Lo que
falta se marca como faltante. Si redactás una celda, un dato o una cifra que no
salió de una fuente del usuario, **declaralo en el changelog y avisale**, aunque
sea plausible. Una foto generada del producto es el mismo problema que un
testimonio inventado.

**Los cruces de atributo.** Este es el error que no se ve, y merece su propio
carril. Un dato inventado suena raro y se detecta. Un atributo cruzado suena
perfecto: poner la tecnología A junto al atributo de la tecnología B produce una
frase impecable, publicable y falsa, que solo detecta quien conoce el producto.
Es peor que un placeholder, porque el placeholder se nota.

Verificá dos cosas distintas, y las dos fallan por separado:

1. **La asociación.** Que el atributo que estás poniendo junto a un componente
   sea el suyo y no el del de al lado.
2. **La pertenencia.** Que el componente que estás nombrando de verdad esté en
   el producto del que estás hablando. Una grilla de características es el lugar
   donde más fácil entra una que pertenece a otro modelo de la línea.

### `claims.json` — el mensaje como dato

La verificación de arriba es imposible de sostener de memoria a lo largo de un
ciclo. Necesita archivo. **Antes de escribir una línea de copy en F3, el ledger
tiene que tener `claims.json`.** Si el proyecto ya declara sus afirmaciones en
algún lado, derivalo de ahí. Si no existe, escribilo: sale más barato que
publicar la página y descubrirlo después.

```json
[
  {
    "sujeto": "qué producto, modelo, plan, servicio o componente",
    "atributo": "qué se afirma de él, tal como se publicaría",
    "registro": "afirmacion | inspiracion",
    "fuente": "de dónde salió: documento, URL, persona, o 'sin fuente'",
    "estado": "aprobado | pendiente | descartado"
  }
]
```

Reglas de uso:

- Nada con `estado: pendiente` o `fuente: sin fuente` entra en una pieza que se
  entrega. Se marca como faltante y se avisa.
- `estado: descartado` es definitivo para todo el ciclo.
- Cada afirmación aparece **una sola vez** en el archivo y todas sus apariciones
  en la pieza tienen que coincidir con esa entrada. La inconsistencia entre dos
  bloques es un fallo de F5, no una variante de redacción.
- Sirve igual para un SaaS con features, un despacho con áreas de práctica, un
  fabricante con especificaciones o una app con permisos por plan. Si la pieza
  afirma algo sobre algo, va acá.

### Registro de inspiración y registro de afirmación

Antes de verificar nada, mirá **en qué registro está escrita la frase**. Son dos
cosas distintas y se juzgan con estándares distintos.

**Inspiración.** "Inspirado en", "actúa como", "emulando", una metáfora, un
nombre. No afirma un mecanismo: invoca lo que el lector ya tiene en la cabeza
cuando escucha esa palabra. Se juzga por si la asociación funciona para quien la
lee, no por si existe literatura. Una metáfora no necesita paper.

**Afirmación.** Le atribuye al sujeto de la analogía una cifra o un mecanismo
verificable. "El cráneo del pájaro carpintero amortigua el 90 %". Eso ya no es
metáfora: es un dato, y necesita fuente como cualquier otro.

La línea entre los dos está en **a quién se le cuelga el número**. Las cifras
pertenecen al componente técnico y se respaldan ahí. Si una cifra migra desde el
componente hacia la metáfora, la frase cambió de registro y ahora hay que
probarla.

**El error inverso es igual de caro y menos evidente.** Pedirle evidencia
científica a una metáfora bloquea copy aprobado, hace perder días y erosiona la
confianza del usuario, que ya resolvió ese punto y lo argumentó. Si el material
del proyecto declara una asociación como aprobada, **está aprobada**: tu trabajo
no es auditarla, es mantenerla consistente.

Lo que sí verificás sobre una metáfora es la **consistencia interna**: que la
misma asociación aparezca igual en todas partes. Si el componente A está
asociado al animal X, no puede aparecer con el animal Y tres bloques más abajo.
Eso no es un juicio sobre la metáfora, es control de calidad del sistema.

**Buscabilidad [M].** Si la métrica de éxito del proyecto es tráfico orgánico, el
H1 es un activo de posicionamiento antes que un eslogan. Ver F3.

**Accesibilidad.** Contraste AA en ambos modos, foco visible, objetivos
táctiles de 44 px, `prefers-reduced-motion` real. No es una pasada final: se
verifica en F5 y bloquea la entrega.

---

## Ledger

Todo vive en `.design-loop/<slug>/`:

```
brief.md          F0 - el brief respondido, con carril y aprobador
refs/             F1 - capturas de las 3 referencias
design-read.md    F1 - lectura de diseño, dials, referencias
tokens.json       F2 - tipografía, espaciado, color, radios, sombras
claims.json       F3 - el mensaje como dato (ver arriba)
qa/pass-N/        F5 - capturas, findings.json y hallazgos por pasada
changelog.md      cada cambio con su motivo y su medida
handoff/          F7 - solo si la pieza se entrega a un tercero
```

Si el usuario dice `continuar`, leé el ledger y retomá donde quedó. No rehagas
fases cerradas.

## Skills complementarias

Usalas si están en el entorno. Si no, el ciclo corre con los criterios de acá.

| Skill | Fase |
|---|---|
| `design-taste-frontend` | F1 — dials, catálogo anti-slop |
| `impeccable` | F3, F6 — construcción y auditoría |
| `emil-design-eng` | F4 — springs, easing, interrumpibilidad |
| skill de GSAP, si existe | F4 — **solo** si `MOTION_INTENSITY` ≥ 7 o hay coreografía de scroll |
| Figma (MCP) | F2 — variables reales |
| Playwright / navegador | F1 y F5 — capturas y medición |

---

## Catálogo de fuentes

La palanca 2 dice que sin tres URLs reales el modelo colapsa a su promedio.
Este catálogo existe para que eso **nunca** sea la razón por la que un ciclo se
traba. Se usa en dos momentos distintos y no hay que mezclarlos:

| | Qué es | Fase | Pregunta que responde |
|---|---|---|---|
| **Referencia** | un sitio real terminado | F1 | ¿a qué aspira esta pieza? |
| **Recurso** | una pieza que se usa | F2, F4 | ¿de dónde sale este componente? |

Una referencia no se copia, se roba parcialmente: se declara qué se toma de
ella. Un recurso sí se usa tal cual, con los tokens aplicados encima.

**Vigencia.** Este catálogo envejece. Un sitio puede caer, cambiar de modelo o
volverse de pago. Verificá que carga antes de citarlo, y si algo murió,
reemplazalo por su equivalente y decilo. No cites de memoria un sitio que no
abriste en esta sesión.

### Referencias — galerías de sitios terminados [M]

| Fuente | Qué tiene | Cuándo va |
|---|---|---|
| `awwwards.com` | premiados: site of the day / month / year, honorable mentions, nominados; filtro por categoría e industria | el techo de ambición. `DESIGN_VARIANCE` alto |
| `godly.design` | curaduría por pieza: websites, heroes, CTAs, footers, logos, OG images, app screenshots | cuando falta un bloque puntual, no la página entera |
| `land-book.com` | landings reales de producto y SaaS, ordenadas por categoría | carril M convencional que igual tiene que convencer |
| `siteinspire.com` | curaduría sobria, filtro por tipo y por estilo | cuando la marca pide contención, no espectáculo |
| `onepagelove.com` | one-pagers y páginas cortas | pieza de un solo scroll |

### Referencias — herramientas reales [F]

En carril funcional las referencias no son sitios de agencia: son productos que
la gente usa ocho horas al día. Lo que se toma es distinto — densidad de tabla,
jerarquía de barra lateral, tratamiento de estado vacío, cómo resuelven un
filtro con doce opciones.

| Fuente | Qué tiene |
|---|---|
| `mobbin.com` | capturas de flujos reales de apps web y móviles, navegables por patrón |
| `refero.design` | patrones de interfaz de productos reales, buscables por componente |
| **la competencia directa del usuario** | la referencia más honesta que existe en carril F, y casi nunca se mira |

Si ninguna sirve, la regla de oro: nombrá tres herramientas que el usuario ya
tiene abiertas todos los días y mirá cómo resuelven **la vista que estás por
construir**, no su home.

### Recursos — componentes

Se consumen en F2, después de declarar el origen de componentes. Si el proyecto
ya tiene design system o registry propio, **este bloque no aplica**: no se
hand-buildea ni se importa lo que ya existe adentro.

| Fuente | Qué tiene | Nota |
|---|---|---|
| `ui.shadcn.com` | componentes base sobre Radix, copiados al repo, no dependencia | el default sensato en React. Accesibilidad ya resuelta |
| `21st.dev` | componentes de marketing con prompt copiable: backgrounds, borders, CTAs, heroes, galerías, shaders | expone MCP server. Ideal para bloques de carril M |
| `magicui.design` | componentes animados sobre shadcn | subordinado al techo de `MOTION_INTENSITY` |
| `hyperui.dev` | bloques Tailwind sin dependencias | cuando no hay React |
| `base-ui.com` / `radix-ui.com` | primitivos sin estilo, accesibles | la base cuando el diseño es propio pero el comportamiento no se negocia |

**La regla de F2 manda sobre el catálogo.** Un `select`, un date picker, un
dialog con foco atrapado o un combobox con teclado no se regeneran nunca: se
traen de acá y se les aplican los tokens.

### Recursos — tipografía

La palanca número uno. Buscar acá antes de aceptar la stack por defecto del
framework.

| Fuente | Qué tiene |
|---|---|
| `fontshare.com` | familias contemporáneas de uso libre, muchas con carácter real |
| `uncut.wtf` | tipografía libre con criterio editorial, poco vista |
| `velvetyne.fr` | display experimental libre, para `DESIGN_VARIANCE` alto |
| `fonts.google.com` | el fondo del barril, pero filtrable; sirve como sustituto declarado |
| fundiciones comerciales | cuando hay presupuesto y la marca lo justifica |

`Inter`, `Geist`, `system-ui` y las stacks por defecto **no cuentan como
decisión**: si la pieza carga una de esas, tiene que estar escrito por qué.

### Recursos — color, iconos, movimiento

| Necesito | Fuente | Nota |
|---|---|---|
| escala neutra y semánticos | `radix-ui.com/colors`, `oklch.com` | escalas ya verificadas en AA, ahorra la mitad de F5 |
| explorar paleta | `huemint.com`, `realtimecolors.com` | probar el acento sobre fondo claro **y** oscuro antes de fijarlo |
| iconos | `lucide.dev`, `phosphoricons.com`, `tabler.io/icons` | **una sola familia**. Mezclar dos es fallo del gate anti-slop |
| curvas de easing | `easings.net`, `cubic-bezier.com` | entradas ease-out, salidas ease-in |
| librería de motion | ver la tabla de F4 | la elección la fija `MOTION_INTENSITY`, no el gusto |

### Recursos — imágenes

Subordinados al carril transversal de **Verdad**, que manda sobre todo lo de
acá. Una foto generada del producto real es el mismo problema que un testimonio
inventado.

| Origen | Cuándo es legítimo | Cuándo no |
|---|---|---|
| fotografía propia del usuario | siempre. Es la primera opción y casi nunca se pide | — |
| generación por IA (agregadores tipo `fal.ai`, o el generador que el entorno ofrezca) | ambiente, textura, abstracción, escenas ilustrativas declaradas | **nunca** el producto, la planta, el equipo, el local o un cliente |
| banco de stock | último recurso | si se reconoce como stock, delata más que cualquier decisión visual |
| tratamiento gráfico sin foto | cuando no hay imagen buena disponible | — |

Regla dura: si una imagen puede leerse como documental y no lo es, se declara en
`changelog.md` y se le avisa al usuario. Sin excepción.

---

## F0 — INTAKE

**Primero el carril.** Una pregunta, antes de todo lo demás: ¿esta pieza la mira
alguien o la usa alguien? Anotá `carril: M` o `carril: F` en `brief.md`. Si es
mixta, declaralo y separá superficies.

Después completá `reference/brief-premium.md` con lo que el usuario ya dijo.
Antes de preguntarle nada, **buscá lo que ya existe**: manuales de marca,
sistemas cromáticos, fotografía de producto, documentos de contenido. En
proyectos reales la mitad del brief suele estar en el disco del usuario, no en
su cabeza.

Dos campos que el brief de referencia no trae y hay que anotar igual:

- **carril** (M / F / mixta, con superficies separadas)
- **aprobador**: quién decide, y qué puede decidir quien te está hablando

**Gate:** no se pasa a F1 con más de 2 campos críticos vacíos (negocio,
audiencia, páginas, referencias, marca, CTA único) ni sin carril declarado. Si
faltan, **una** pregunta agrupada. No adivines y no inventes marca.

Las referencias son el único campo crítico que **no** se pregunta acá: se
resuelven en F1 con una shortlist propuesta. No trabes F0 esperando URLs.

**Preguntá también la métrica de éxito.** Un número a 6 meses. Cambia
decisiones concretas: conversión sube el producto en el home, tráfico orgánico
convierte el H1 en activo de SEO, leads B2B reordena la jerarquía entera. En
carril F la métrica no es tráfico: es tiempo por tarea, errores por sesión o
tickets de soporte evitados, y reordena la interfaz igual de fuerte.

---

## F1 — DIRECCIÓN

Producí un **Design Read**: una línea que declare qué tipo de pieza es, para
quién y con qué actitud. Después fijá tres dials con valor numérico:

- **DESIGN_VARIANCE** (1-10): cuánto se aleja de lo convencional
- **MOTION_INTENSITY** (1-10): techo de movimiento para F4
- **VISUAL_DENSITY** (1-10): información por pantalla

**[F]** En carril funcional, `DESIGN_VARIANCE` por encima de 3 es un error, no
una decisión de gusto: una herramienta que sorprende al usuario le cuesta
tiempo cada día. El dial que hay que discutir es `VISUAL_DENSITY`, y se define
contra la tarea más frecuente, no contra la pantalla más vacía.

### Referencias: proponer primero, preguntar después

**El orden importa y va al revés de lo que parece.** No arranques pidiéndole
referencias al usuario. Andá al **Catálogo de fuentes**, abrí la galería que
corresponde al carril, y **llegá con una shortlist de tres candidatas ya
capturadas**, cada una con su razón en una línea.

Reaccionar es mucho más fácil que generar. Un usuario que ve tres capturas
responde en treinta segundos — "esta sí, esta no, esta a medias" — y esa
respuesta ancla más que cualquier respuesta a "¿tenés referencias?", que casi
siempre es "no sé, algo limpio y moderno".

Si el usuario **sí** trajo referencias, esas mandan y el catálogo solo completa
hasta llegar a tres.

Cómo se arma la shortlist:

1. Elegí la galería según carril: sitios terminados en M, herramientas reales en F.
2. Filtrá por la categoría del cliente **y** buscá dos fuera de ella. Las de la
   propia categoría suelen ser el promedio del que hay que escapar.
3. **Capturá las tres a `refs/`** antes de escribir `design-read.md`. Una
   referencia descrita en prosa ancla la mitad que una que podés mirar mientras
   construís, y en F5 sirve para comparar contra lo que se dijo que se iba a tomar.
4. De cada una, escribí **qué se toma** — retícula, escala tipográfica,
   tratamiento de imagen, ritmo de secciones — y qué no. "Se ve limpio" no es
   un dato.

La elección de las candidatas es **decisión del ciclo**: la tomás vos y la
declarás como hipótesis. La dirección visual de la marca sigue siendo del dueño
y no se resuelve por shortlist.

Si el usuario no responde a la shortlist, seguí con ella declarada como
hipótesis. Pero dejá escrito que si el resultado no convence, ese es el primer
lugar donde mirar, no el CSS.

### Nombrar las direcciones

Si explorás variantes, **nombrá cada dirección** — "editorial severo",
"catálogo técnico", "producto como espécimen" — y desarrollalas por separado.
Pedir "tres versiones" sin nombrarlas produce tres versiones de lo mismo:
convergen al promedio. Nombrarlas las obliga a divergir.

**Gate:** `design-read.md` con el design read, los 3 dials con valor, las 3
referencias con qué se toma de cada una y de dónde salieron, y `refs/` con sus
capturas si el entorno las permitió.

---

## F2 — SISTEMA

Acá hay una bifurcación real, y elegir mal cuesta caro.

### ¿Hay marca previa?

**Sí — manual, sistema cromático, tipografía licenciada, logo.**
Los tokens van **antes** de escribir UI. No estás inventando dirección, estás
respetando una. Derivalos de la fuente existente y no de tu criterio.

**No — marca por definir, o proyecto exploratorio.**
Los tokens van **después** de elegir dirección en F3. Fijar un sistema estricto
antes de saber qué se está construyendo mata la creatividad que hace que una
landing funcione. Construí con decisiones locales, elegí la dirección, y recién
ahí consolidá el sistema y aplicalo de vuelta a todo. Una vez consolidado, se
cierra: nada de medidas ad-hoc después.

**[F]** En carril funcional esta bifurcación casi no aplica: la app hereda la
marca que ya existe y el sistema va antes, siempre. Lo que sí se decide antes
de construir es de dónde salen los componentes.

### Qué contiene el sistema

- **tipografía**: máximo 5 tamaños con ratio explícito, 2 familias como techo.
  Una de ellas debe ser distintiva — es la palanca número uno. Si la familia de
  marca no está disponible todavía, declará el sustituto y dejá el cambio a una
  sola regla `@font-face`. Dónde buscarla: **Catálogo → tipografía**.
- **espacio**: base 8, o 4 si la densidad es alta. El espaciado entre secciones
  es **un solo valor**.
- **color**: 1 acento, 1 neutro con 5+ pasos, semánticos aparte, AA verificado.
  Cuidado con los acentos claros: un color que funciona sobre fondo oscuro
  puede fallar el contraste sobre blanco y necesitar una variante más profunda.
  Partir de una escala ya verificada (**Catálogo → color**) ahorra media F5.
- **radios y sombras**: 2 valores cada uno. No hay tercero.

Si hay Figma conectado, traé variables y contexto del frame en vez de inventar.

### Decisión de tipografía, declarada

La skill entera dice que la tipografía es la palanca número uno, así que no
puede quedar como un valor más de `tokens.json`. En `design-read.md`, tres
líneas:

- **qué familia** carga la pieza
- **por qué esa** y no otra, en una frase atada al design read
- **qué se descartó** y por qué

Una familia sin justificación es la señal más fiable de que la pieza va a salir
genérica. `Inter`, `Geist`, `system-ui` y las stacks por defecto del framework
no se descartan por snobismo, pero **no cuentan como decisión**: si la pieza
carga una de esas, tiene que estar escrito por qué, y en carril M eso casi
nunca se sostiene.

### Origen de los componentes

Los tokens dicen cómo se ve un componente. No dicen de dónde sale. Declaralo en
`tokens.json` o al lado, porque cambia todo lo que se construye después:

- **Hay biblioteca** (registry de componentes, design system interno, librería
  de UI del framework). **No se hand-buildea lo que ya existe ahí.** Un `select`
  accesible, un date picker, un dialog con foco atrapado y un combobox con
  teclado son trabajo de meses hecho por gente que lo hizo bien; regenerarlos
  produce versiones peores que además hay que mantener. Se traen y se les
  aplican los tokens.
- **No hay biblioteca.** Elegí una del **Catálogo → componentes** y declarala,
  o construí — pero se construye **una vez**: el componente vive en un solo
  lugar y las vistas lo consumen. La segunda copia de un botón es deuda
  inmediata.

Un componente traído del catálogo llega con sus propios estilos. **Se le aplican
los tokens del proyecto antes de usarlo**, nunca al revés: si el componente
impone su radio, su sombra o su tipografía, el sistema de F2 dejó de existir y
la pieza va a parecer una demo de la librería.

**[F]** En carril funcional esto es lo primero que se decide en F2, antes que
el color. La mayor parte de una app son componentes resueltos; lo que la
distingue es cómo se ordena la información, no cómo se dibuja un `switch`.

**Gate:** `tokens.json` existe, la decisión de tipografía está escrita con su
descarte, el origen de componentes está declarado, y toda medida posterior sale
de ahí.

---

## F3 — CONSTRUCCIÓN

### Gate de entrada: un bloque, no la página

**Antes de construir la pieza completa, construí UNA cosa y mostrala.**

- **[M]** el hero. Con tipografía real, color real y copy real.
- **[F]** **la vista más densa que exista**: la tabla peor, el formulario más
  largo, la pantalla con más estado. No la más linda. Un dashboard se rompe en
  su peor pantalla, y esa es la que hay que ver antes de construir ocho.

Esperá respuesta. No sigas por tu cuenta.

Ese bloque es la única forma barata de verificar que el sistema de F2 y la
dirección de F1 son los correctos. Si están mal, se descubre en un bloque y no
en ocho. Construir la pieza entera y mostrarla al final convierte cualquier
corrección en una discusión sobre trabajo ya hecho, y eso desgasta al usuario
mucho más que esperar.

Aplica también al rediseño: si vas a corregir algo existente, corregí un bloque
y mostralo antes de tocar el resto.

Construí con brief, design read, dials, tokens y `claims.json` como contexto
explícito. En rediseño: auditar antes de tocar; estructura, copy y rutas no
cambian en silencio.

**Completo.** Nada de placeholders. Contenido real del usuario, o contenido
plausible del negocio marcado como tal.

### El orden de los bloques no es sagrado **[M]**

Si el usuario trae una arquitectura de una agencia, respetala como punto de
partida y **cuestionala contra la métrica**. Un catálogo en el sexto bloque
tiene sentido si el sitio posiciona y la venta ocurre en otro canal; no lo
tiene si el sitio vende. Si el concepto diferenciador de la marca vive en el
bloque cuatro, el hero está prometiendo algo que el visitante tarda en ver.
Proponé el cambio con su razón y dejalo en el changelog.

### Copy del hero **[M]**

- Una sola promesa, en el idioma del usuario, no en el de la empresa.
- Un solo CTA primario por página.
- **Si la métrica es tráfico orgánico**, el H1 lleva la palabra que la gente
  busca. Un eslogan sin keyword en un sitio que vive del orgánico es un activo
  desperdiciado. El eslogan de marca puede vivir como kicker sobre el titular.
- El concepto que diferencia a la marca debería ser legible en el hero. Si el
  titular lo podría firmar cualquier competidor, todavía no es el titular.

### Copy funcional **[F]**

El copy de una herramienta no persuade, orienta. Se escribe igual de en serio:

- **Etiquetas** con la palabra que usa quien trabaja ahí, no la del modelo de
  datos. Si el equipo dice "expediente", la etiqueta no dice "registro".
- **Estado vacío** que diga qué hacer, no "no hay datos". Es la primera
  pantalla que ve un usuario nuevo y casi siempre está sin escribir.
- **Errores** que digan qué pasó y cuál es el siguiente paso. "Error 400" no es
  copy.
- **Acciones destructivas** que nombren lo que se destruye: "Eliminar 12
  líneas", no "¿Está seguro?".

### SEO y AEO, cuando aplica **[M]**

- indexar lo perenne donde la intención de búsqueda coincide con la promesa
- `noindex` en páginas de campaña y ofertas con vencimiento
- title y meta description escritos, no derivados
- enlaces internos desde el home hacia las páginas de producto
- FAQ en texto plano, no dentro de un acordeón que dependa de JS

---

## F4 — MOVIMIENTO

**[M] Un solo momento firmado por página.** Esa es la regla. El resto del
movimiento es utilitario: hover, foco, feedback, transición de estado.

El momento firmado tiene que **argumentar algo de la marca**, no decorar. Si no
podés explicar en una frase por qué esa animación y no otra, no la pongas.
Una plantilla que absorbe impacto merece un asentamiento con spring; un sitio
de cine merece una marquesina. Copiar el gesto de otra categoría resta
autoridad.

**[F] Cero momentos firmados.** En una herramienta, la animación que llama la
atención es una animación que interrumpe. Todo el movimiento es utilitario y
por debajo de 200 ms: cambio de estado, entrada de panel, feedback de guardado,
skeleton mientras carga. Una transición que el usuario ve cuarenta veces por
día tiene que ser invisible a la décima.

**Cuidado con el catálogo acá.** Las galerías de referencia premian el
espectáculo y las librerías de componentes animados vienen con el movimiento ya
puesto. Un componente traído del catálogo **no eleva `MOTION_INTENSITY`**: si su
animación pasa el techo del dial, se le baja o se le saca antes de usarlo. El
dial se fijó en F1 y no se renegocia por lo que trae una librería.

Marco de decisión, en orden:

1. ¿Debe animar? Si no está claro, no anima.
2. ¿Cuál es el propósito? Orientar, dar feedback u ocultar latencia.
3. ¿Qué easing? Entradas ease-out, salidas ease-in, spring si hay gesto.
4. ¿Qué duración? Enter y exit son asimétricos.

**Reglas duras, verificadas en F5:**

- solo `transform` y `opacity`
- `prefers-reduced-motion` implementado, no comentado
- nada anima desde `scale(0)`
- popovers con `transform-origin` consistente con su disparador
- transiciones CSS interrumpibles, no `@keyframes`, en UI que responde a hover

**Nunca animes el elemento LCP.** La imagen grande del hero suele serlo. Si la
métrica del proyecto es orgánica, animarla degrada Core Web Vitals y con eso el
posicionamiento — te disparás en la misma métrica que estás tratando de mover.
Animá el texto, o disparala en el `load` de la imagen.

**El peso cuenta, y la elección de herramienta es una regla, no un gusto.**

| `MOTION_INTENSITY` | Herramienta |
|---|---|
| 1-4 | CSS: `transition`, `@starting-style`, `linear()`. Nada más |
| 5-6 | CSS + Web Animations API para lo interrumpible |
| ≥ 7, o coreografía de scroll real | GSAP + ScrollTrigger, y **cargá la skill de GSAP si está en el entorno** |

Una librería de 50 KB para dos transiciones no se justifica. Pero pelear una
coreografía de scroll con CSS puro cuesta más tiempo que el peso que ahorra.

`MOTION_INTENSITY` del F1 es el techo. Pero ojo con el piso **[M]**: un dial en
2 o 3 produce páginas correctas y muertas. Si el brief pide que además se vea
bien, 5 con un momento firmado supera a 3 con nada.

---

## F5 — QA REAL

Nada de "creo que se ve bien". Se mide, y se mira. **Y se mide con un script,
no a ojo**: la fase más cara en manos es la que más fácil se automatiza, y una
verificación que depende de acordarse es una verificación que a veces no pasa.

### El script

Guardá esto como `.design-loop/<slug>/qa.mjs` la primera vez y reusalo en cada
pasada. Requiere Playwright en el entorno.

```js
// node qa.mjs <url> <pass-n>
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const [url, pass = 'pass-1'] = process.argv.slice(2);
const out = `qa/${pass}`;
mkdirSync(out, { recursive: true });

const VIEWPORTS = [
  ['desktop', 1440, 900], ['laptop', 1280, 800], ['mobile', 390, 844],
];
const SWEEP = [320, 375, 414, 600, 768, 900, 1024, 1280, 1440, 1728, 1920];

const findings = [];
const browser = await chromium.launch();

for (const scheme of ['light', 'dark']) {
  const ctx = await browser.newContext({ colorScheme: scheme });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('requestfailed', r => errors.push(`404/fail ${r.url()}`));

  for (const [name, w, h] of VIEWPORTS) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: `${out}/${name}-${scheme}.png`, fullPage: true });

    // tap targets y texto chico, solo en móvil
    if (name === 'mobile') {
      const bad = await page.evaluate(() => {
        const r = { taps: [], tiny: [] };
        for (const el of document.querySelectorAll('a,button,[role=button],input,select')) {
          const b = el.getBoundingClientRect();
          if (b.width && (b.width < 44 || b.height < 44)) r.taps.push(el.outerHTML.slice(0, 80));
        }
        for (const el of document.querySelectorAll('p,li,span,td')) {
          if (parseFloat(getComputedStyle(el).fontSize) < 14 && el.textContent.trim())
            r.tiny.push(el.textContent.trim().slice(0, 40));
        }
        return r;
      });
      if (bad.taps.length) findings.push({ check: 'tap-target<44px', scheme, items: bad.taps.slice(0, 10) });
      if (bad.tiny.length) findings.push({ check: 'texto<14px', scheme, items: bad.tiny.slice(0, 10) });
    }

    // líneas demasiado largas
    const long = await page.evaluate(() => [...document.querySelectorAll('p,li')]
      .filter(el => el.textContent.trim().length > 20)
      .filter(el => el.getBoundingClientRect().width /
        (parseFloat(getComputedStyle(el).fontSize) * 0.5) > 75)
      .map(el => el.textContent.trim().slice(0, 50)).slice(0, 5));
    if (long.length) findings.push({ check: 'linea>75ch', viewport: name, scheme, items: long });
  }

  // barrido continuo de overflow, no solo en los tres cortes
  for (const w of SWEEP) {
    await page.setViewportSize({ width: w, height: 900 });
    const over = await page.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (over > 0) findings.push({ check: 'overflow-x', width: w, scheme, px: over });
  }

  // fallback tipográfico: la familia declarada tiene que estar cargada
  const fonts = await page.evaluate(async () => {
    await document.fonts.ready;
    return [...document.fonts].map(f => `${f.family} ${f.weight} ${f.status}`);
  });
  writeFileSync(`${out}/fonts-${scheme}.txt`, fonts.join('\n'));
  if (!fonts.some(f => f.endsWith('loaded')))
    findings.push({ check: 'fuentes-no-cargan', scheme });

  if (errors.length) findings.push({ check: 'consola', scheme, items: errors.slice(0, 20) });
  await ctx.close();
}

await browser.close();
writeFileSync(`${out}/findings.json`, JSON.stringify(findings, null, 2));
console.log(findings.length ? findings : 'sin hallazgos automáticos');
```

Lo que el script **no** ve: contraste real percibido, jerarquía, si una foto
quedó recortada donde importa, si tres secciones se repiten. Para eso están los
ojos, abajo.

### Linter anti-slop

Corre antes de las capturas, sobre el código fuente. Es más barato y más
confiable que pedirle al modelo que se auto-audite:

```bash
# desde la raíz del proyecto
echo "— em-dashes en copy:"    ; grep -rn "—" --include="*.{html,jsx,tsx,md,astro,vue,svelte}" src/ | head
echo "— gradiente morado-azul:"; grep -rniE "gradient\([^)]*(#[68][0-9a-f]{2}[0-9a-f]{3}|purple|violet|indigo)" --include="*.{css,scss,js,jsx,tsx}" . | head
echo "— emoji en markup:"      ; grep -rnP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" --include="*.{html,jsx,tsx,astro,vue,svelte}" src/ | head
echo "— familias tipográficas:"; grep -rhoP "font-family:\s*\K[^;]+" --include="*.css" . | sort -u
echo "— valores de radius:"    ; grep -rhoP "border-radius:\s*\K[^;]+" --include="*.css" . | sort -u | wc -l
echo "— valores de sombra:"    ; grep -rhoP "box-shadow:\s*\K[^;]+" --include="*.css" . | sort -u | wc -l
echo "— nombres de relleno:"   ; grep -rniE "lorem ipsum|john doe|jane doe|foo ?bar|placeholder\.com|via\.placeholder" src/ | head
```

**Falla y no se entrega si:** aparece cualquier em-dash en copy · hay gradiente
morado-azul · hay emoji usado como ícono · hay más de 2 familias tipográficas ·
hay más de 2 valores de `border-radius` o de `box-shadow` · aparece cualquier
nombre de relleno.

Los que el linter no puede ver siguen siendo gate manual: tres secciones
seguidas con la misma estructura · imágenes de stock obvias · iconografía de dos
familias mezcladas · una tipografía que no distingue nada · **un componente del
catálogo que quedó con sus estilos de origen** en vez de los tokens del proyecto.

### Lo que miran los ojos

**Mirá las capturas, no solo `findings.json`.** El overflow en cero no detecta
un título que se sale de su tarjeta ni una foto recortada en la zona vacía. Las
métricas encuentran lo estructural; los ojos, lo que se ve mal.

**Comparalas contra `refs/`.** Ahí está lo que en F1 dijiste que ibas a tomar de
cada referencia. Si la captura de la pieza no se parece en eso concreto — la
retícula, el ritmo, el tratamiento de imagen — la referencia se declaró y no se
usó, y eso es un hallazgo como cualquier otro.

### Los tres de Meng To

Pasada rápida antes del gate: **espacio, contraste, moderación.**
Si algo se ve mal y no sabés por qué, casi siempre falta espacio, falta
contraste, o sobra.

### Prueba de esfuerzo

Un layout correcto en un solo tamaño y un solo idioma no está probado. El
barrido de 320 a 1920 ya lo hace el script; falta lo que no automatiza:

- **Traducí.** El alemán y el francés alargan; el español alarga sobre el
  inglés. Si la pieza es multi-idioma, probá el idioma más largo.
- **Espejá** para RTL si aplica.
- Posición, espaciado y alineación cargan jerarquía antes de que se lea una
  palabra. Si al redimensionar la jerarquía se pierde, el problema es
  estructural, no de tamaño de fuente.

### Gate adicional del carril funcional **[F]**

Una app no se prueba con datos lindos. Las cuatro pantallas que casi nadie
diseña y todo el mundo ve:

| Estado | Falla si |
|---|---|
| **Vacío** | dice "sin datos" y no dice qué hacer |
| **Cargando** | salto de layout al llegar los datos, o spinner sin forma |
| **Error** | no dice qué pasó ni cuál es el siguiente paso |
| **Parcial** | permisos o plan reducido rompen la retícula |

Más la **prueba de volumen**: la tabla con 300 filas, el nombre de 80
caracteres, el número de 12 dígitos, el filtro con 40 opciones. Un dashboard
probado con seis filas de ejemplo no está probado.

### Limitaciones del entorno

Si corrés el QA en un contenedor sin salida a red, las fuentes web no cargan y
las capturas salen con tipografía de reemplazo. **Declaralo** en vez de dar por
verificado lo que no viste, y repetí esa parte donde haya red.

**Gate:** existen `qa/pass-N/findings.json`, las capturas de los 3 viewports en
ambos temas, y la salida del linter. Sin evidencia no hay avance.

---

## F6 — REFINAMIENTO (máximo 2 pasadas)

Cada ajuste se escribe **como medida, no como sensación**:

| Mal | Bien |
|---|---|
| "dale más aire al hero" | "padding vertical del hero a 160px, título a 72px" |
| "se ve apretado" | "espaciado entre secciones uniforme a 96px" |
| "arreglá el móvil" | "corregí el desbordamiento de la nav en 390px" |
| "más contraste" | "texto secundario de #999 a #666, AA en fondo claro" |

Registrá cada uno en `changelog.md` con su motivo.

### Criterio de salida

Comunes a los dos carriles:

- [ ] `findings.json` de la última pasada sin `overflow-x`, sin `consola`, sin
      `tap-target`, sin `texto<14px`, sin `fuentes-no-cargan`
- [ ] linter anti-slop pasado, y los checks manuales revisados a ojo
- [ ] contraste AA en texto, estados y modo oscuro
- [ ] `prefers-reduced-motion` funciona de verdad
- [ ] espaciado entre secciones = un solo valor de `tokens.json`
- [ ] decisión de tipografía escrita, con su descarte
- [ ] las 3 referencias declaradas en F1 se ven usadas en la pieza
- [ ] los componentes traídos del catálogo llevan los tokens del proyecto
- [ ] `claims.json` sin `pendiente` ni `sin fuente` en lo que se publica
- [ ] todo dato inventado marcado o eliminado, imágenes generadas declaradas
- [ ] capturas antes/después entregadas

**[M]** además:

- [ ] un solo CTA primario por página
- [ ] un solo momento firmado, y no es el LCP
- [ ] title, meta y enlaces internos escritos, si la métrica es orgánica

**[F]** además:

- [ ] los cuatro estados diseñados y capturados
- [ ] prueba de volumen pasada
- [ ] ningún movimiento por encima de 200 ms ni decorativo
- [ ] etiquetas en el vocabulario de quien usa la herramienta

Si tras 2 pasadas algo sigue fallando, **decilo** y proponé la decisión que lo
destraba. No sigas puliendo.

---

## F7 — HANDOFF (opcional)

Solo si la pieza la recibe alguien que no estuvo en el ciclo: un cliente, otro
equipo, el desarrollador que la mantiene. **No es una fase más del ciclo** y no
se cobra tiempo de refinamiento: es empaquetar lo que ya existe.

El ledger está hecho para reanudar, no para entregar. En `handoff/`:

- `tokens.json` exportado en el formato que consume quien recibe (CSS custom
  properties, variables de Figma, JSON plano)
- **las decisiones y su razón**: dirección, tipografía con su descarte, dials,
  origen de componentes. Sin esto, el primer cambio que haga el que recibe
  rompe el sistema, porque no sabe qué lo sostenía
- **de dónde salió cada cosa**: las 3 referencias con qué se tomó de cada una,
  y la procedencia y licencia de tipografías, componentes, iconos e imágenes.
  Quien mantiene la pieza necesita saber qué puede cambiar sin romper una
  licencia
- antes/después de F5, y qué quedó fuera de alcance
- lo declarado como faltante o pendiente en `claims.json`, explícito

Lo que **no** va al handoff: hipótesis internas, referencias descartadas,
discusiones del ciclo.

---

## Si sigue viéndose genérico

| Síntoma | Causa casi siempre | Movida |
|---|---|---|
| Parece hecho por IA | tipografía sin carácter | volvé a F2: una familia distintiva del catálogo, usada con decisión |
| Sigue pareciéndolo | F1 flojo, referencias en adjetivos | volvé a F1 con 3 URLs del catálogo y qué se roba de cada una |
| Se parece a una demo de librería | los componentes trajeron sus estilos | volvé a F2: los tokens se aplican encima, no al revés |
| Apretado o desalineado | espaciado ad-hoc | volvé a F2, un solo valor de sección |
| Correcto pero muerto **[M]** | dial de movimiento demasiado bajo | F4: subí a 5 y definí el momento firmado |
| Imágenes falsas | stock o generación | fotografía propia, o tratamiento gráfico sin foto |
| Fuentes no cargan | probado solo en dev | F5 sobre el build de producción |
| Todo pesa igual | sin jerarquía | escala tipográfica más agresiva, un foco por sección |
| Se ve bien y no se puede usar **[F]** | corriste carril M en una herramienta | volvé a F0, redeclará el carril |
| Cada pantalla parece otra app **[F]** | componentes regenerados por vista | volvé a F2: origen de componentes, uno solo |

## Señales de que el ciclo se está trabando

- **Pediste lo mismo dos veces y no llegó.** Mirá de quién es la decisión. Si es
  del ciclo, proponé vos, declarala como hipótesis y seguí; no pidas por tercera
  vez. Si es del dueño, parás y decís qué bloquea. La regla de avanzar por
  hipótesis nunca cubre una decisión del dueño.
- **Pediste referencias en vez de proponerlas.** Es la forma más común de trabar
  F1 y es evitable: el catálogo está para llegar con tres candidatas capturadas.
- **El usuario dice que insistís, que no lo escuchás, o que hacés lo que querés.**
  Eso no es una queja de tono: es la señal de que interpretaste su silencio o su
  corrección como permiso. Parás de producir. No entregás nada más, no arreglás
  el reclamo con más trabajo. Reconocés qué hiciste concretamente y preguntás qué
  quería. Volver con un entregable más grande es el peor movimiento posible.
- **Te corrigió el rumbo y seguiste construyendo.** Una corrección no es una
  aclaración para incorporar mientras seguís: es una parada. Aplicala y mostrá
  el bloque afectado antes de continuar.
- **Estás puliendo sin medir.** Si el último cambio no salió de una captura o
  una medición, parás.
- **El usuario corrige un dato tuyo.** Revisá si hay más contenido sin fuente
  en la página; suele venir en grupo.
- **Vas por la pasada 3.** No existe. Entregá con lo que falta declarado.