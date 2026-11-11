---
name: "plan-mercado"
description: "Convierte un estudio de mercado en plan de acción país, regional o global para cualquier marca que MWT maneje (propia, representada o distribuida), o evalúa una oportunidad de distribución antes de firmar."
---

# Plan de mercado (F4 y F6) — país, regional, global

v1.3 · 2026-10-28 · borrador. Cierra el hueco entre el estudio y la acción, para cualquier marca y cualquier rol de MWT frente a ella.
- v1.3: rol de socio constructor con participación en la sociedad operativa (§0, §4c lado C, cuatro conceptos separados); modelo económico del piloto con un motor y dos salidas, mensual desde la firma, lotes con hito y aprobación conjunta, tope de exposición, caja de inventario separada de caja operativa y convenciones de crédito de fábrica (§4d); fase F7 `entrega-tercero`. Sale del plan FootMaster Brasil y de las revisiones REV-BR-02 y 03.
- v1.2: rol de MWT frente a la marca (dueño, representante, distribuidor o controlador regional, marca ingrediente); evaluación de oportunidad antes de firmar; contrato visto desde los dos lados; posición de MWT en la cascada; conflicto de portafolio entre marcas que MWT maneja; separación de datos entre dueños de marca. Primer caso de tercero: FootMaster en Latinoamérica.
- v1.1.1: puerta regulatoria graduada (bloqueo frente a riesgo asumido), cascada con líneas `no_aplica` por canal, regla de cálculo hacia atrás compatible con "nunca un valor supuesto", y la decisión en la primera página.
- v1.1: agrega la economía de producto físico, el modo de entrada con puertas, el socio y su contrato, y la arquitectura regional y global. Sale de la investigación de Kimi del 25-oct-2026 (manual de internacionalización ICEX, ITC, CAGE, AAA, Integración–Respuesta local, OLI, Uppsala; casos Natura, Genomma, Alpargatas, Skechers, Falabella, Bimbo, Belcorp).
- v1.0: patrones absorbidos, no copiados, de `marketing-plan`, `launch`, `marketing-loops` y `attribution` (coreyhaines31/marketingskills, MIT) y de `icp-scoring`, `account-selection`, `abm-strategy`, `partnership-strategy` y `gtm-metrics` (LeadMagic/gtm-skills, MIT).

Se ejecuta completo con una sola IA; los obreros son opcionales.

## Principio rector

Cada línea del plan cambia una decisión o una acción. Un plan que no dice qué deja de hacer no es un plan. "Esperar que funcione" no es una jugada: toda acción nombra su mecanismo y su indicador adelantado. Si no se puede calcular el margen o falta evidencia regulatoria, la salida es **"no listo para invertir"**, no una recomendación optimista.

## Lugar en el harness de estrategia

| Fase | Skill | Sale |
|---|---|---|
| F0a | `interrogatorio-encargo` | `decisiones.md`, `encargo.yaml` |
| F1–F2 | `orden-obrero` | datos recibidos y validados |
| F3 | método del estudio (harness de estudio de mercado, `universal-analysis`) | mapa, cuadrantes, bandas de precio, competencia |
| **F4** | **`plan-mercado`** | **plan con jugadas, presupuesto, modelo económico y medición** |
| F5 | `presentar-resultados` | entregable ordenado por conclusión |
| F7 | `entrega-tercero` | qué sale, con qué protección, en qué orden y con qué correo |
| **F6** | **`plan-mercado` modo revisión** | jugadas seguidas, ajustadas, cortadas o escaladas |

`posicionamiento-marca` es la única fuente de cómo se habla de la marca. Este skill la lee; nunca la redefine. Si el plan necesita cambiar el posicionamiento, lo propone allá.

## Requisitos previos

1. Acta F0a válida con decisión 1 = plan (o posicionamiento + plan).
2. Estudio con estado por dato (verificado | estimado | pendiente). Sin estudio no se inventa mercado: devolver qué falta y qué orden de `orden-obrero` lo cierra.
3. Contexto de posicionamiento vigente. Los marcadores `conflicto` que tocan el plan se listan antes de empezar.
4. Rol de MWT frente a la marca declarado (§0) y registrado en `claude/marcas/REGISTRO_MARCAS.md`.
5. Insumos del CEO, uno por turno y solo los que bloquean, en este orden de peso:
   - costo de origen (FOB o precio de transferencia) por SKU o familia;
   - margen mínimo aceptable por eslabón;
   - capital disponible y payback objetivo;
   - inventario y capacidad del fabricante;
   - derechos de marca por país;
   - contratos vigentes con el fabricante;
   - apetito de control y riesgo;
   - en rol de socio constructor: participación que propone, honorario, gastos propios (viajes) y quién financia.

   Lo que falte produce plantilla y pendiente, nunca un valor supuesto. Un límite calculado hacia atrás desde un dato verificado (por ejemplo, el costo máximo admisible desde la banda de precio) no es un supuesto: se presenta como límite, marcado `estimado`.

## Método

### 0. Rol de MWT frente a la marca

El rol cambia quién decide, dónde está el margen de MWT, de qué lado del contrato está y qué riesgo corre. Se declara antes de todo y no se mezcla entre marcas.

| Rol | Ejemplo | Quién define posicionamiento, claims y precio | Margen de MWT | Contrato | Capital de MWT | Riesgo principal |
|---|---|---|---|---|---|---|
| **Dueño de marca** | Rana Walk | MWT | contribución completa del canal | MWT elige y contrata socios (§4c, lado A) | inventario, pauta, registros | demanda y caja |
| **Representante** | Marluvas, Tecmater | el fabricante; MWT adapta el mensaje al comprador local | comisión o sobreprecio sobre el precio del fabricante | MWT recibe la representación (§4c, lado B) | bajo | pérdida de la representación; concentración en pocas cuentas |
| **Distribuidor o controlador regional** | FootMaster en Latinoamérica | el dueño aprueba lo global; MWT propone la adaptación regional y, si el contrato lo dice, el precio de venta | margen sobre la venta cobrada (fijo, sobre referencia o híbrido) | MWT recibe la distribución (§4c, lado B) | según modelo: consignación del dueño o compra en firme | dependencia del dueño; registro de marca a nombre de otro; terminación |
| **Socio constructor** | FootMaster Brasil (propuesta 60/40 + honorario) | el dueño controla la marca; la sociedad operativa decide canales y ejecución con decisiones conjuntas | honorario de gestión + participación en la sociedad (no es caja personal) | acuerdo de socios (§4c, lado C) | trabajo, relaciones, gastos propios; capital según acuerdo | dilución, desacuerdo, dependencia del financiamiento del dueño |
| **Marca ingrediente o cobranding** | FootMaster Pro dentro del calzado de un fabricante | reglas de convivencia entre dos marcas, firmadas | licencia, regalía o venta del componente | acuerdo de cobranding | bajo | confusión de marcas; quién responde por el producto |

Reglas:
- Un plan, una marca, un rol. Si MWT tiene dos roles con la misma marca en territorios distintos, son dos planes.
- En marca de tercero, el plan propone; el dueño aprueba lo que el contrato le reserva. Lo que el contrato no dice se lista como decisión abierta con el dueño, no se asume.
- Datos de un dueño de marca (costos, listas, inventario, clientes) nunca entran al plan de otra marca ni a una pieza que vea otro dueño. Se tratan como N3 (`POL_DATA_CLASSIFICATION`).

#### 0b. Evaluar una oportunidad de marca de tercero (antes de firmar)

Cuando la pregunta es si conviene tomar una representación o una distribución, el plan arranca en modo evaluación y entrega una decisión, no jugadas:

| Pieza | Contenido |
|---|---|
| Mercado accesible del territorio | del estudio: países, canales y compradores que de verdad puede atender MWT, no el mercado total |
| Economía de MWT | margen por unidad y por año en tres escenarios de volumen, con la fórmula del margen que propone el dueño y la que propone MWT |
| Capital y riesgo de MWT | inventario, crédito a clientes, registros, costos fijos (bodega, viajes); quién paga cada uno |
| Términos mínimos | lo que MWT no puede ceder (lado B o C de §4c) y el punto en que MWT no firma |
| Dependencia | qué pasa con MWT si el dueño termina, vende directo o cambia de precio |
| Conflicto de portafolio | qué cambia para las marcas que MWT ya maneja |
| Decisión | firmar, negociar con contrapropuesta, o no firmar; con lo que tiene que pasar para cambiar de opinión |

### 1. Diagnóstico en una página

Situación, complicación, pregunta, respuesta. Máximo cinco hechos del estudio, cada uno con su consecuencia. Nada que no cambie una elección posterior. Si el mercado cae en un cuadrante débil del estudio, se dice en la primera línea.

Incluye capacidad propia y del fabricante o dueño de la marca: qué recursos dan ventaja y cuáles faltan (capital, abastecimiento, certificaciones, marca registrada y a nombre de quién, red de contactos). En marca de tercero, separar lo que aporta MWT de lo que aporta el dueño, con el historial de negocio que MWT ya generó para el dueño (cuentas presentadas que hoy compran).

### 2. Dónde jugar

1. Unidad: país × segmento × SKU o familia × canal × socio; en B2B con cuentas nombrables, la cuenta.
2. Reutilizar la matriz atractivo × capacidad de ganar del estudio. Contrastar el atractivo con la distancia del país (cultural, administrativa y regulatoria, geográfica, económica). Si se cambian pesos, decirlo y mostrar qué celdas cambian de cuadrante.
3. Escribir lo que **no** se ataca y por qué (patrón de `ENT_MKT_GTM_AMAZON` §C). Una jugada descartada con evidencia vale tanto como una elegida. El statu quo (no comprar, comprar lo de siempre) siempre figura como alternativa.
4. Potencial estadístico (importaciones, mapas de potencial exportador) no es venta accesible: se confirma con socio, canal y margen.

#### 2b. Cuentas B2B (activar si hay cuentas nombrables)

Puntaje por cuenta, graduado (100 / 60 / 20 / 0), nunca binario. Pesos y umbrales como variables editables en el plan.

| Bloque | Peso inicial | Mide | Señal en calzado de seguridad | Señal en distribución de consumo (FootMaster) | Señal en FaberLoom |
|---|---|---|---|---|---|
| Encaje | 35 | si la cuenta puede comprar | segmento CIIU, operarios en planta, norma que la obliga | importador, cadena o club de precio que vende plantillas o calzado en el país | pyme LATAM, proceso de cotización técnica |
| Necesidad operativa | 25 | tamaño y forma de la necesidad | dotación anual en pares, riesgo (eléctrico, químico, metatarsal), vida útil | peso de la categoría en su surtido; banda de precio que maneja | volumen de cotizaciones, equipo comercial |
| Acceso | 25 | si podemos llegar | cliente actual, distribuidor, contacto, registro como proveedor | contacto propio, lead derivado por el dueño de la marca, feria | contacto, referido, socio |
| Momento | 15 | si es el tiempo | licitación abierta (SICOP, SECOP), vencimiento de contrato, temporada | revisión de surtido, apertura de categoría, temporada | cambio de sistema, contratación, crecimiento |

Reglas:
- **Descalificación antes del puntaje:** segmento excluido, volumen bajo el mínimo o geografía no atendible → 0. Sin certificación exigida por la norma del país → máximo 20.
- Si falta un dato imprescindible, el bloque queda con techo de 40.
- Tiers: A ≥ 80 (atención uno a uno, 5–15 cuentas) · B 60–79 (grupo con mensaje por segmento) · C 40–59 (canal o distribuidor) · D < 40 (fuera).
- Encaje sin momento es lista de seguimiento, no lista objetivo.
- Cuentas de alto encaje, sin negocio previo y sin oportunidad abierta: cola de campaña.
- Prueba hacia atrás: ¿el modelo habría puntuado bien los ganados y perdidos conocidos? Si no, recalibrar antes de usar.
- Recalibrar cada seis meses o tras cada ronda de licitaciones relevante. No puntuar con datos que no se pueden obtener a escala.
- La forma de vender se decide por tamaño de la operación, no por tamaño de la empresa. Un comprador regulado (minería, eléctrica, sector público) compra como corporativo aunque sea chico.

#### 2c. Modo de entrada y puertas (por país)

| Campo | Contenido |
|---|---|
| Modo actual | exportación directa, importador o distribuidor, consignación, marketplace transfronterizo, venta directa, licencia, socio local, sociedad operativa conjunta |
| Alternativas | dos como mínimo, con control, recursos y riesgo de cada una |
| Reversibilidad | qué cuesta salir o cambiar de modo; cláusulas que lo permiten |
| Puerta de entrada | viabilidad regulatoria (registros, etiquetado, certificaciones) y margen positivo en la cascada de precio. **Bloquea** un requisito obligatorio que falta (registro sanitario, certificación exigida por norma, prohibición). **No bloquea** un riesgo de claim o de interpretación que el CEO asumió con decisión registrada: se lista en §9 con su referencia |
| Puerta de escala | repetición de compra o sell-out comprobado, cobro al día, socio que cumple metas de avance |
| Puerta de pausa o salida | qué señal hace pausar o cambiar de modo |

En marca de tercero, la puerta de entrada incluye además: acuerdo firmado o hoja de términos aceptada, y marca registrada o autorizada en el país (o plan alternativo decidido antes de imprimir empaques).

Reglas: modo reversible primero, más control solo cuando la evidencia lo pague (casos Natura, Skechers y Alpargatas: el control sube y baja según escala). Sin la puerta de entrada cumplida, el país queda "no listo para invertir" y el plan solo lleva jugadas de costo cero para cerrar lo que falta.

### 3. Cómo ganar

1. Traer del contexto de posicionamiento: alternativa que reemplazamos, diferencia demostrable, prueba, nivel de conciencia del comprador.
2. Por segmento elegido, una frase: "para <quién> que hoy usa <alternativa>, ganamos por <diferencia> y lo probamos con <prueba>".
3. Si la prueba no existe (`faltante`), la primera tarea de la jugada es conseguirla. No se reemplaza con adjetivos.
4. Núcleo y adaptación: qué es igual en todos los países (marca, promesa, especificación) y qué se adapta (surtido, presentación, idioma, certificación, canal), con el motivo de cada adaptación.

### 4. Canal

| Columna | Qué fija |
|---|---|
| Canal | marketplace, sitio propio, distribuidor, venta directa, compra pública, retail |
| Tipo | **propio** (sitio, base de clientes), **alquilado** (marketplace, redes), **prestado** (prensa, creadores, socios). Lo alquilado y lo prestado deben llevar a lo propio cuando la política del canal lo permite |
| Rol | adquisición, conversión, recompra, prueba social, aprendizaje |
| Economía | contribución por unidad (de 4b); costo de adquisición máximo; capital inmovilizado |
| Restricción | stock mínimo, claims, exclusividad, conflicto de precio entre canales |
| Fase | entrada, mantenimiento, crecimiento (`ENT_PLAT_CANALES` §B) |

Reglas:
- Un canal sin rol no entra. Dos o tres canales bien ejecutados valen más que ocho.
- Precio por canal coherente: el plan declara la regla que impide que un canal desancle o canibalice a otro.
- Costo de adquisición máximo = contribución por unidad × compras esperadas dentro del payback. Sin payback ni capital, el presupuesto queda `bloqueado` y el plan sigue con jugadas de costo cero.

#### 4b. Economía por SKU y canal (producto físico)

Cascada de precio, de origen a góndola, con estado por línea. La línea donde cobra MWT se marca explícitamente (contribución, comisión, sobreprecio, margen de distribución u honorario de gestión); la economía del plan es la de esa línea, no la del dueño. Las líneas que no existen en el canal se marcan `no_aplica` con motivo (en marketplace con fulfillment propio no hay importador ni distribuidor; la comisión y la tarifa logística del marketplace ocupan su lugar):

`costo de origen → flete y seguro → arancel y tasas → impuestos de importación → costo puesto → margen importador → margen distribuidor → margen canal o comisión del marketplace → impuestos al consumidor → precio de góndola`

Reglas:
- Cada línea con fuente y fecha (arancel por código HS y versión; comisión del marketplace vigente; tipo de cambio con dirección y fecha efectiva). Sin costo de origen, la cascada se calcula hacia atrás desde la banda de precio objetivo y muestra el costo máximo admisible; queda marcada como estimada.
- Devoluciones, descuentos y promociones entran en la contribución, no al final.
- La base de un honorario se declara una sola vez (por ejemplo, venta neta después de descuentos de canal) y es la misma en el documento y en el modelo; impuestos y devoluciones son otra partida.
- Tributos por fecha de llegada: si la llegada cae en un año con reforma (CBS/IBS en Brasil desde 2027), matriz fiscal por período antes de comprometer inversión.
- Precio de reventa: el plan sugiere bandas; no fija precios al socio (revisión de competencia local).

#### 4c. Socio y contrato

**Lado A — MWT elige al socio** (marca propia, o MWT como distribuidor que nombra subdistribuidores):

1. Socio ideal = quien tiene a nuestro comprador antes que nosotros. Lista larga → lista corta → revisión (registros, referencias, solvencia, conflictos con marcas competidoras) → piloto.
2. Separar venta originada por el socio de venta influida, con regla escrita.
3. Contrato, como lista de verificación para revisión legal local:
   - territorio y venta online;
   - exclusividad condicionada y reversible;
   - metas de avance;
   - datos de sell-out e inventario;
   - uso de la marca y registros;
   - precios y descuentos dentro de lo que permite la competencia local;
   - inventario al terminar;
   - salida y transición;
   - ley aplicable.

   El skill prepara la lista; no da consejo legal definitivo.
4. Corte: cero pedidos en seis meses, o sell-out que no acompaña al sell-in, → revisar. Revisión trimestral con el socio.

**Lado B — MWT es el socio** (representación o distribución de marca de tercero). Lista de lo que MWT necesita obtener, para revisión legal local:

| Tema | Qué se busca | Por qué |
|---|---|---|
| Territorio y exclusividad | países incluidos y excluidos; canales, incluida la venta online y los marketplaces | Sin territorio escrito, el dueño puede vender directo o nombrar a otro |
| Registro de clientes | quién registra, prueba requerida, vigencia, conflicto entre registros | Protege las cuentas que MWT abre |
| Seguimiento | parámetros de avance (plan y reportes) en vez de metas de volumen en mercado nuevo; incumplir lleva a revisión, no a pérdida automática | Las metas de volumen no se pueden fijar sin historia |
| Leads y eventos | qué contactos del territorio se derivan a MWT; participación en ferias del dueño | El rol de referente regional se construye con los contactos que llegan al dueño |
| Precio | quién fija el precio de venta y el precio de referencia; margen de MWT y cómo se calcula | Define el piso y el premio de MWT |
| Inventario y capital | consignación o compra; quién financia; plazo y destino del inventario sin venta | Define el capital y el riesgo de MWT |
| Crédito | quién decide la política de crédito por cliente; cómo se reparte una factura impaga; liquidación al dueño contra cobro | El riesgo de crédito es la pérdida más común de un distribuidor |
| Marca | registro por país y a nombre de quién; autorización de uso; plan alternativo si el registro se bloquea | Vender una marca no registrada en el país es riesgo de oposición |
| Datos | acceso a inventario y movimientos (libro abierto) | Sin datos no se mide sell-out ni se concilia |
| Exclusiones | marcas propias de MWT fuera de cualquier cláusula de no competencia | Protege el portafolio propio |
| Marcas adicionales | si las demás marcas del dueño entran con las mismas condiciones | Evita renegociar cada marca |
| Plazo y salida | duración, renovación, aviso; compensación sobre las cuentas desarrolladas si el dueño termina sin causa | Protege a MWT cuando el negocio ya rinde |

El skill prepara la lista; no da consejo legal definitivo. Si ya existe un acta de decisiones con el dueño (por ejemplo, `F0A_DECISIONES_RESPUESTA_BANGNI`), se parte de ella.

**Lado C — MWT como socio constructor** (sociedad operativa conjunta con el dueño de la marca):

1. Separar siempre cuatro conceptos, cada aporte contado una sola vez:

| Concepto | Qué es | Regla |
|---|---|---|
| Margen de fabricación | lo que gana el dueño al fabricar y vender a la sociedad | precio de transferencia entre partes relacionadas; revisión de precios de transferencia |
| Capital social | dinero aportado a cambio de acciones | define la participación |
| Financiación del socio | crédito de fábrica, préstamo de socio | se devuelve con la caja; devolverla no extingue acciones y prestar no crea acciones |
| Honorario de gestión | remuneración del trabajo continuo del socio que dirige | costo de la sociedad desde la primera venta; separado de dividendos |

2. La propuesta de reparto (por ejemplo 60/40) es una base de discusión razonada por aportes (capital y riesgo frente a mercado, relaciones, dirección y ejecución), no un estándar de mercado ni una valoración. Sin rangos alternativos en la pieza para el tercero.
3. Participar en la sociedad no transfiere marcas; los derechos de uso se acuerdan aparte. El alcance se limita al país; la expansión se evalúa juntos.
4. Decisiones a acordar: cuánto financia cada parte y cuándo; capital frente a deuda; devolución; dedicación; diluciones futuras; decisiones que requieren a ambos (endeudamiento, precios con la fábrica vinculada, dividendos, marcas, ampliaciones); incumplimiento, salida y desacuerdo. Adquisición gradual de acciones solo como alternativa a negociar.
5. Dividendos dependen de beneficio distribuible, caja, obligaciones y aprobación: nunca se muestra el 40% del resultado como ingreso del socio.
6. Validación: abogado del país (forma societaria, administrador residente o no, representación comercial frente a honorario) y contador (régimen elegible con socios extranjeros).

#### 4d. Modelo económico del piloto

Un solo motor de cálculo, dos salidas: la vista pública (para el tercero) y la vista privada CEO-ONLY (honorario personal, costo de la marca propia, margen de transferencia). Nunca dos modelos con lógicas distintas.

| Elemento | Regla |
|---|---|
| Calendario | mensual desde la firma (M0), con plazo de producción + tránsito + aduana; horizonte por defecto 36 meses de venta |
| Lotes | primer lote fijo; los siguientes con hito de ventas y cobro calibrado contra el plan (decir el %) **y** aprobación conjunta por lote; un hito cumplido hace elegible, no libera |
| Reposición | cubre los meses siguientes al ritmo observado; también decisión conjunta |
| Tope de exposición | CIF comprometido acumulado por etapa; si el modelo aún no lo aplica, decirlo |
| Stock | por SKU y talla antes de ordenar de verdad; el agregado sirve para planificar |
| Caja | separar caja de inventario (stock, cuentas por cobrar, impuestos por recuperar, anticipos) de caja operativa (gastos) |
| Pago a fábrica | estándar, a plazo (0–365 días) o según flujo; en "según flujo" declarar que la caja es flujo acumulado sin aportes modelados y que interés, techo, vencimiento y garantías se acuerdan |
| Créditos fiscales | recuperación limitada por débitos; supuesto declarado |
| Costos compartidos | reparto por volumen entre marcas declarado; si una marca no participa, no se le prorratea nada, tampoco el embarque |
| Honorario | devengado, pagado y pendiente, con identidad que cuadra |
| Alcance | etiquetar qué cubren los resultados (una marca, no "la empresa") |
| Prueba | puente contable que cuadra al final; escenarios bajo, base, alto y demanda 50 %, explicando por qué difieren |
| Exportación pública | por lista de campos permitidos; nada privado se carga y se oculta |

### 5. Jugadas en secuencia

Cada jugada es una apuesta que se puede perder:

| Campo | Contenido |
|---|---|
| Hipótesis | qué creemos y por qué (dato con estado) |
| Mecanismo | por qué la acción debería mover el indicador |
| Acción | qué se hace, en qué canal y segmento |
| Costo | dinero, inventario, horas |
| Indicador adelantado | qué se mueve primero si funciona |
| Señal de éxito | métrica, umbral y plazo |
| Señal de corte | cuándo se abandona |
| Qué se sabe después | información que produce aunque falle |
| Dueño y fecha | rol concreto y fecha o evento |
| Depende de | jugada previa o insumo |

Reglas:
- Secuencia explícita cuando una jugada financia o valida la siguiente (patrón `ENT_MKT_GTM_AMAZON` §D).
- Máximo tres jugadas abiertas por canal. Reparto de esfuerzo por defecto 70 / 20 / 10 (lo que funciona / lo siguiente / lo experimental), editable.
- Toda campaña pertenece a una jugada; no hay campañas huérfanas. Nombre de campaña con convención fija (`fecha-segmento-canal-pieza-versión`).
- Un lanzamiento no espera al producto perfecto: si la jugada se aplaza por "una mejora más", se registra como riesgo.
- Activación por asistentes de IA (catálogo legible, WebMCP, agentes de tienda) solo como jugada con medición propia.

### 6. Presupuesto

1. Escenarios: mínimo (costo cero), base, acelerado. Cada uno dice qué compra y qué deja sin hacer.
2. Tramos ligados a las puertas de 2c y a la aprobación conjunta de cada lote: el dinero del tramo siguiente se libera al cruzar la puerta, no por calendario.
3. Ningún gasto sin señal de corte. Los gastos propios del socio constructor (viajes, estadía) van como costo fijo explícito, en moneda declarada.
4. Estado: `asignable | bloqueado (motivo) | condicionado (a qué jugada o puerta)`.
5. Decisiones abiertas a la vista, ordenadas por impacto. Costo de adquisición desconocido y costo de origen desconocido son las de mayor impacto.

### 7. Medición

Tres niveles por jugada (patrón `ENT_MKT_GTM_AMAZON` §F):

| Nivel | Pregunta |
|---|---|
| Exposición | ¿nos ven? |
| Respuesta | ¿reaccionan? (por término, canal o segmento, nunca agregado) |
| Resultado | ¿deja contribución? (incluye devoluciones y costo de adquisición) |

Reglas:
- Una sola fuente de verdad para contar ventas por canal: Amazon → Seller Central y Brand Analytics; sitio → su backend; B2B → MWT ONE. Las plataformas de anuncios explican el origen; no redefinen el conteo. Nunca sumar conversiones entre plataformas.
- Con distribuidores, **sell-in no valida**: el tablero muestra sell-in, sell-out, inventario en canal, cobro y margen juntos (caso Genomma: el despacho inicial no prueba repetición).
- Amazon no tiene píxel propio: el tráfico externo se mide con Amazon Attribution y el límite se declara.
- Si dos fuentes internas del mismo dato difieren más de 2 % (MWT ONE frente a contabilidad), se concilia antes de leer la métrica.
- Tasas solo con ventanas cerradas: una cohorte con ventana abierta está pendiente, no fallida.
- Cifras de mercado en rangos con nivel de confianza, nunca un número único sin respaldo.
- Si la fuente de una métrica no existe, la primera tarea es construirla (por ejemplo, serie histórica propia desde el día uno).
- Un solo documento de umbrales (verde / amarillo / rojo) por marca y canal; los demás lo citan. Rojo si cualquier métrica primaria está en rojo, o dos en amarillo dos periodos seguidos.
- Cinco a ocho indicadores por plan, cada uno con línea base, fuente y dueño.

### 8. Calendario

90 días con jugadas y fechas; 12 meses con hitos, puertas y decisiones. Cada recomendación con quién, cuándo y qué se sabe después.

### 9. Riesgos y supuestos

Registro con estado y efecto si falla. Separar riesgo de mercado, de producto, de cumplimiento (claims, registros, certificaciones, marca), de socio y de ejecución. Lo legal, fiscal y aduanero se marca para revisión de un especialista local; el skill no lo resuelve. Las consultas a especialistas se redactan con preguntas abiertas ("clasificar", "comparar"), no con la respuesta inducida ("confirmar que").

## Escalas

| Escala | Entra | Agrega | Regla de paso |
|---|---|---|---|
| País | estudio del país, posicionamiento, insumos | todo el método | — |
| Regional | planes de país + mapa regional | ver abajo | Un país entra al regional con plan propio o con estado `no_planificado` declarado. No se promedian monedas, periodos ni definiciones sin normalizar |
| Global | planes regionales + cuadrantes | ver abajo | Las cifras globales son suma de las regionales; nada se estima arriba si no existe abajo |

### Regional

1. **Grupos de países** por parecido de comprador, canal, regulación y logística; comparativo normalizado de planes de país (atractivo, capacidad, distancia, confianza, madurez).
2. **Secuencia y pilotos:** qué país prueba primero, qué tiene que demostrar para promover al siguiente. Un país piloto bien documentado es la ruta replicable para los demás.
3. **Adaptar, agregar, arbitrar:** qué se adapta por país, qué se comparte (marca, catálogo, contenido, socio logístico) y de dónde se saca ventaja de costo o de abastecimiento.
4. **Corredor de precios** entre países y alerta de mercado gris, con revisión legal.
5. **Bodega o hub regional:** decisión con caso de negocio (volumen, nivel de servicio, costos) y validación fiscal y aduanera por jurisdicción. El skill no recomienda una jurisdicción sin ese estudio.
6. Estándares comunes de socio, contrato, datos y revisión trimestral; quién decide qué entre la región y cada país.
7. Presupuesto consolidado y capital de trabajo por escenario; asignación por evidencia, no por reparto parejo.

Puerta regional: no se agrega hub ni estructura compartida sin volumen, servicio y caso fiscal validados.

### Portafolio de marcas que MWT maneja

Corre siempre que dos marcas de MWT (propias o de terceros) compitan por la misma categoría, comprador o canal (ejemplo: Rana Walk y FootMaster en plantillas).

1. Mapa de portafolio: por marca, banda de precio, segmento, canal y territorio, con el rol de MWT en cada una.
2. Regla escrita que separa las marcas (banda, segmento o canal) y qué hace MWT cuando un cliente pide las dos.
3. Cláusulas contractuales que afectan a otra marca (no competencia, exclusiones, marca de respaldo en un país) listadas en una sola tabla.
4. Datos de cada dueño separados (§0). Si las marcas comparten operación, cada una lleva su libro (unidades, costos, inventario, cobros, pagos, parte de fijos) y la relación se declara abiertamente al otro dueño.

Puerta de portafolio: no se lanza una marca en un canal donde otra marca de MWT pierde venta sin decisión registrada del CEO.

### Global

1. **Rol de cada marca por región y arquitectura de marca:** marca paraguas, marca con respaldo, marca independiente, marca ingrediente o cobranding (ej. FootMaster, FootMaster Pro, Rana Walk).
2. **Integración o respuesta local por actividad:** qué se estandariza globalmente, qué es plataforma compartida y qué decide cada país, con el costo de cada excepción.
3. **Modo de compromiso por región** y límites de capital y riesgo; concentración en un mercado, socio o proveedor.
4. Política global de canales, precios y mercados grises compatible con cada ley local.
5. Indicadores comparables entre regiones, con moneda y tipo de cambio transparentes.

Puerta global: no se estandariza una actividad sin mostrar que el ahorro supera el costo de responder peor a lo local.

## Modo revisión (F6)

Cadencia fijada en el plan según la velocidad de la señal: anuncios cada 2–3 días en lanzamiento; posición orgánica y competencia semanal; socios y sell-out mensual; plan completo mensual en lanzamiento y trimestral en mantenimiento.

1. **Mirar no es actuar.** Cada corrida revisa; actúa solo si se cruza la señal de éxito o de corte. La mayoría de las corridas terminan en "revisado, sin cambios", y se entregan igual diciéndolo.
2. **Verificar antes de actuar:** descartar ruido, estacionalidad y error de medición.
3. Por jugada: `seguir | ajustar | cortar | escalar`, con motivo y dato. Por país: puerta cruzada o no.
4. **Qué hace la IA sola:** leer, analizar, redactar, dejar preparado. **Qué requiere al CEO:** gastar, mover presupuesto, publicar, enviar, cambiar configuración de campañas, cambiar de modo de entrada. Sin aprobación, ninguna corrida mueve más de 20 % del presupuesto.
5. Escalar siempre al CEO: crisis de marca o de reseñas, cuenta o socio estratégico en riesgo, anomalía de gasto, de ventas o de inventario en canal.
6. Una línea de registro por corrida, actúe o no. Si una revisión pasa semanas sin actuar o actúa en cada corrida, su umbral está mal.
7. Lo aprendido con evidencia se propone a la tabla de aprendizajes de `posicionamiento-marca`; lo aprendido entre países sube al plan regional.

## Gates antes de entregar

1. Cada jugada tiene mecanismo, señal de corte y dueño.
2. Hay sección de lo descartado.
3. Cada país tiene modo de entrada, alternativa y puertas; sin puerta de entrada cumplida, dice "no listo para invertir".
3b. El rol de MWT está declarado, la línea de la cascada donde cobra MWT está marcada y, en marca de tercero, lo que aprueba el dueño está separado de lo que decide MWT.
3c. Si otra marca de MWT comparte categoría, el plan trae la sección de portafolio.
3d. En rol de socio constructor, los cuatro conceptos de §4c lado C están separados y ningún dividendo se presenta como ingreso.
4. La cascada de precio está completa, con `no_aplica` justificado o marcada como estimada con el dato que falta.
4b. El modelo cumple §4d: un motor, cifras del documento que cuadran con el modelo, honorario con la misma base en ambos, lotes con aprobación conjunta, alcance de resultados etiquetado.
5. Ningún claim fuera del contexto de posicionamiento ni de `POL_CLAIMS_SCANNER`.
6. Datos CEO-ONLY (precios de fabricante, márgenes, competencia CEO-ONLY, honorario personal, costo de la marca propia) solo en anexo o vista CEO-ONLY; nunca en piezas para terceros ni en órdenes externas. Datos de un dueño de marca nunca en el plan de otra marca.
7. Todo número con estado y fuente; ningún estimado presentado como observado.
8. El plan declara qué deja de hacer.
9. Lo legal, fiscal y aduanero está marcado para revisión local, no resuelto.
10. El entregable pasa `presentar-resultados`.
11. Si va a un tercero, pasa `entrega-tercero` antes de salir.

## Salida

`claude/<dominio>/PLAN_<marca>_<escala>_<territorio>_<fecha>.md`. Incluye siempre estas piezas; la decisión va en la primera página, no al final (`presentar-resultados`):
- decisión;
- rol de MWT y lo que aprueba el dueño de la marca;
- tres supuestos críticos;
- economía por canal;
- socio o canal elegido y su alternativa;
- presupuesto por tramo;
- cinco a ocho indicadores con línea base;
- riesgos y revisiones profesionales pendientes;
- criterios de escala, pausa y salida;
- registro de fuentes y pendientes.

Modelo económico (§4d) con su vista pública si el plan va a un tercero. Anexo CEO-ONLY en archivo separado, sobre el mismo motor. Formato final según decisión 5 del acta.

## Formato

Español. Tablas para comparaciones, con columna MOTIVO para decisiones. Cada dato con estado y fuente en la misma línea. Sin jerga.