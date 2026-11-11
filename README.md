# FaberLoom para Claude Code

FaberLoom es un **harness que crea harness**: cada Space arma su propio conjunto de agentes, skills, contexto y reglas, y lo proyecta como archivos que cualquier cliente puede leer. Este repositorio publica su **mod para Claude Code**: el catálogo como agentes y skills nativos, la cola de la Mesa, MWT.ONE por empresa y el servidor público de SICOP.

Instalás un plugin y Claude Code pasa a trabajar con el catálogo de FaberLoom, sin la aplicación FaberLoom ni el harness de DeepSeek.

---

## Índice

1. [Qué es cada pieza](#qué-es-cada-pieza)
2. [Requisitos](#requisitos)
3. [Instalar](#instalar)
4. [Configurar MWT.ONE](#configurar-mwtone)
5. [El catálogo: 145 agentes y 293 skills](#el-catálogo-145-agentes-y-293-skills)
6. [Comandos](#comandos)
7. [MCP de SICOP](#mcp-de-sicop)
8. [MCP de MWT.ONE](#mcp-de-mwtone)
9. [Lo que vive en FaberLoom, no en el mod](#lo-que-vive-en-faberloom-no-en-el-mod)
10. [Cómo trabajar un Space desde Claude](#cómo-trabajar-un-space-desde-claude)
11. [Seguridad](#seguridad)
12. [Licencia y atribución](#licencia-y-atribución)

---

## Qué es cada pieza

| Pieza | Qué es | Dónde |
|---|---|---|
| **FaberLoom** | El producto: Spaces, Mesa de trabajo, agentes, skills, flujos, rutinas, memoria, contexto, correo y conexiones. Corre sobre DeepSeek Harness. | Aplicación de escritorio o `https://harness.mwt.one` |
| **DeepSeek Harness** | La base: un *harness de harnesses* donde cada perfil compone sus módulos como plugins. FaberLoom es uno de esos productos. | [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) |
| **Este repo** | El **mod para Claude Code**: catálogo nativo, proyección del Space, cola de la Mesa, MWT.ONE y SICOP. | GitHub: `Ale241302/faberloom_mod` |
| **MWT Knowledge Hub** | La base de conocimiento canónica de Muito Work: Rana Walk, representaciones B2B, MWT.one y FaberLoom. Alimenta el contexto de los Spaces. | Repositorio privado de MWT |
| **ECC** | Catálogo de agentes, skills y comandos de ingeniería (MIT) que forma parte del catálogo que este mod instala. | [affaan-m/ECC](https://github.com/affaan-m/ECC) |

En una frase: **FaberLoom crea el harness; el Knowledge Hub le da el conocimiento; ECC aporta el catálogo de ingeniería; este repo lo lleva a Claude Code.**

---

## Requisitos

- **Claude Code 2.1.287 o posterior** (`claude --version`). Los mods existen desde esa versión.
- Cuenta de **MWT.ONE** sólo si vas a usar la parte de empresa (clientes, expedientes, pedidos). El resto funciona sin cuenta.
- No hace falta instalar FaberLoom ni DeepSeek Harness.

---

## Instalar

### Desde el marketplace de GitHub (recomendado)

```bash
claude plugin marketplace add Ale241302/faberloom_mod
claude plugin install faberloom@faberloom
```

### Para una sola sesión, sin instalar

```bash
git clone https://github.com/Ale241302/faberloom_mod
claude --plugin-dir ./faberloom_mod/faberloom
```

### Comprobar que cargó

```bash
claude plugin list          # faberloom@faberloom · enabled
```

Dentro de una sesión: `/plugin` → pestaña **Installed** → `faberloom`, y bajo las pestañas `1 mod active · faberloom`.

### Actualizar

```bash
claude plugin update faberloom@faberloom
```

---

## Configurar MWT.ONE

La primera vez, Claude Code pide tres datos. Si no aparece el diálogo:

```
/plugin configure faberloom@faberloom
```

| Dato | Para qué | Secreto |
|---|---|---|
| Usuario MWT.ONE | Iniciar sesión en la consola | No |
| Contraseña MWT.ONE | Emitir un DeviceToken por empresa | **Sí**: se guarda cifrada |
| Consola (opcional) | Base de la API; por defecto `https://consola.mwt.one/api` | No |

La contraseña **nunca** entra al chat, al modelo ni a `settings.json`. Sólo viaja del formulario a la consola.

Después:

```
/mwt                      # inicia sesión y lista empresas
/mwt sondel-s-a           # elige la empresa activa
```

---

## El catálogo: 145 agentes y 293 skills

El plugin trae el catálogo y lo instala en **tu** Claude, como propio:

| Qué | Dónde queda | Cómo se invoca |
|---|---|---|
| 145 agentes | `~/.claude/agents/*.md` | `@agent-<nombre>` |
| 293 skills | `~/.claude/skills/<nombre>/SKILL.md` | `/<nombre>` |

- Se copia **una vez por versión de catálogo**, en la primera sesión, en segundo plano.
- **Nunca pisa** lo que ya exista: tus ediciones sobreviven a las actualizaciones.
- `/faberloom-install` lo repite cuando quieras.
- Claude usa una skill solo cuando la tarea coincide con su descripción; también puede llamar a un agente por su cuenta.

El catálogo combina el material propio de FaberLoom (SICOP, llave compartida, expedientes, MWT) con el catálogo de ingeniería de ECC.

---

## Comandos

| Comando | Qué hace |
|---|---|
| `/faberloom` | Informe del Space proyectado en la carpeta: título, fecha, agentes, skills, flujos, rutinas, memoria y contexto |
| `/agentes` | Agentes del Space con la ruta de su definición |
| `/faberloom-skills` | Skills del Space con su `SKILL.md` |
| `/mesa` | Cola real de la Mesa: ítems abiertos, severidad, estado, Space y vencimiento |
| `/mwt` | Inicia sesión en la consola y lista empresas; `/mwt <clave>` elige la activa |
| `/faberloom-install` | Reinstala el catálogo en `~/.claude` |

**Línea de estado**: bajo el prompt, `FaberLoom · <Space> · N agentes · N skills`, actualizada al terminar cada turno.

> `/skills` ya existe en Claude Code, por eso la lista del Space es `/faberloom-skills`.

---

## MCP de SICOP

SICOP es la plataforma de contratación pública de Costa Rica. El plugin declara su servidor MCP **público**: no pide credenciales ni identidad, y aporta **71 herramientas** sobre licitaciones, carteles, ofertas, adjudicaciones, contratos, proveedores, precios, sanciones y series históricas.

- Servidor: `sicop` en `https://sicop.vlinte.work/mcp`. Claude Code lo muestra como **`plugin:faberloom:sicop`** en `/mcp`.
- Herramientas: `mcp__plugin_faberloom_sicop__<herramienta>`. El prefijo lleva el nombre del plugin porque el servidor viene de un plugin, no de tu configuración.
- Comprobación: `claude mcp list` debe mostrar `plugin:faberloom:sicop: https://sicop.vlinte.work/mcp (HTTP) - ✔ Connected`.
- Antes de la primera consulta conviene cargar la skill `sicop-contratacion-publica`, que fija cómo se reporta cada cifra.

### Las herramientas, por área

| Área | Herramientas |
|---|---|
| Entrada en lenguaje natural | `sicop_preguntar` (router: clasifica la intención y llama a la tool correcta), `sicop_kb_buscar` (base de conocimiento y normativa), `sicop_resumen`, `sicop_diagnostico` |
| Resolver nombres y códigos | `sicop_resolver` (nombre/alias/typo → cédula), `sicop_campo_buscar`, `sicop_catalogo_campo`, `sicop_proveedor_dim` |
| Proveedores | `sicop_ficha_proveedor`, `sicop_representantes`, `sicop_representante_competencia`, `sicop_ordenes_proveedor`, `sicop_ficha_esosa` |
| Procedimientos | `sicop_buscar_procedimiento`, `sicop_expediente`, `sicop_verificar_procedimiento`, `sicop_lineas_procedimiento`, `sicop_recursos_procedimiento`, `sicop_invitaciones_procedimiento`, `sicop_invitados_vs_ofertantes`, `sicop_tiempos_por_etapa`, `sicop_regimen`, `sicop_regimen_evaluacion`, `sicop_procedimientos_familia`, `sicop_mes_publicacion` |
| Ofertas y competencia | `sicop_adjudicaciones`, `sicop_competencia_procedimiento`, `sicop_competencia_por_regimen`, `sicop_cara_a_cara`, `sicop_precios_identicos`, `sicop_perdidas_baratas`, `sicop_grafo_competidores` |
| Producto y precios | `sicop_producto`, `sicop_producto_historia`, `sicop_producto_specs`, `sicop_producto_firma`, `sicop_buscar_productos`, `sicop_precios_institucion`, `sicop_mercado_familia` |
| Integridad | `sicop_sanciones`, `sicop_carteles_objetados`, `sicop_excepciones`, `sicop_integridad`, `sicop_senales`, `sicop_vigilancia`, `sicop_ctl_deriva` |
| Hechos y series | `sicop_fact_requerimiento`, `sicop_fact_oferta`, `sicop_fact_adjudicacion`, `sicop_fact_contrato`, `sicop_fact_orden`, `sicop_fact_recepcion`, `sicop_gold_status`, `sicop_resultado` |
| Otras fuentes | `sicop_cgr_buscar` (Contraloría), `sicop_bccr_tc` (tipo de cambio BCCR) |
| Operación del servidor | `sicop_corrida_pasos`, `sicop_reconciliar`, `sicop_autocorregir`, `sicop_reparar_mes`, `sicop_ciclo_diario`, `sicop_politica`, `sicop_registro`, `sicop_actividad_mcp`, `sicop_carril`, `sicop_pendientes`, `sicop_backtest_invitaciones`, `sicop_holdout` |

### Ejemplos

Todos se pueden pedir en lenguaje natural; el agente elige las herramientas.

**1. Proveedor: qué ganó y de qué tamaño**

```
¿En qué licitaciones ganó Sondel?
```

Cadena real: `sicop_resolver("sondel")` → cédula `3101095926`; `sicop_adjudicaciones(cedula)` → líneas adjudicadas. Devuelve, por ejemplo, SICOP `20181103002`, precio unitario `₡32.072,73`, IVA `₡4.169,45`, moneda `CRC`. Para el panorama completo: `sicop_ficha_proveedor("sondel")`, que agrega adjudicaciones por año, cartera de ejecución frente a captación, desempeño de entrega y familias principales.

**2. Un procedimiento concreto**

```
Mostrame la trazabilidad del procedimiento 20181103002
```

`sicop_expediente(nro_sicop)` responde qué tramos están completos: cartel, ofertas, acto firme, adjudicado, contrato, garantía y recibido. Para la ficha del cartel: `sicop_buscar_procedimiento`; para las líneas: `sicop_lineas_procedimiento`.

**3. Competencia y precios**

```
¿Quién más ofertó en ese procedimiento y a qué precio?
¿Qué institución paga más por este producto?
```

`sicop_competencia_procedimiento` y `sicop_cara_a_cara` enfrentan oferentes; `sicop_precios_institucion` calcula el ratio máximo/mínimo entre instituciones para la misma marca, modelo, firma y año; `sicop_producto_historia` da la serie por año.

**4. Integridad**

```
¿Sondel tiene sanciones o carteles objetados?
```

`sicop_sanciones(cedula o alias)` devuelve inhabilitaciones y multas; `sicop_carteles_objetados` la cola de revisión con monto estimado, institución y si se adjudicó después.

**5. Empezar sin saber qué herramienta existe**

```
Preguntale a SICOP: cómo se comportó el mercado de calzado en 2025
```

`sicop_preguntar` es el router: clasifica la intención (ficha, mercado, competencia, procedimiento, precio, specs o KB) y llama a la herramienta correcta.

> Cada cifra viaja con su sobre: `nivel_medicion` (captación, ejecución o entrega), `cobertura`, `moneda` y `caveats`. Si una herramienta no devolvió el dato, no existe para la respuesta.

---

## MCP de MWT.ONE

MWT.ONE es la consola de operación: clientes, empresas, expedientes, proformas, pedidos, inventario, pagos, finanzas y correo. En la empresa de prueba, el servidor expone **183 herramientas**.

### Conectar

```
/plugin configure faberloom@faberloom     # usuario y contraseña de la consola
/mwt                                      # inicia sesión y lista empresas
/mwt sondel-s-a                           # elige la empresa activa
```

La consola emite un **DeviceToken por empresa**. El mod guarda uno por cada empresa alcanzable y usa el de la activa; la contraseña sólo se usa en el login y nunca llega al modelo.

### Llamar una herramienta

El agente usa una sola herramienta de Claude, `mcp__faberloom__mwt`, con el nombre de la herramienta MWT y sus argumentos:

```json
{ "name": "expediente_buscar", "input": { "proforma": "2487-2026" } }
```

No hace falta escribir el JSON: se lo pedís en castellano y el agente arma la llamada.

### Las herramientas, por área

| Área | Herramientas (ejemplos) |
|---|---|
| Expedientes (25) | `expediente_listar`, `expediente_obtener`, `expediente_buscar`, `expediente_lineas`, `expediente_buscar_por_producto`, `expediente_resolve_oc_preview` |
| Correo (12) | `correo_mensaje_listar`, `correo_mensaje_obtener`, `correo_contacto_listar`, `correo_contacto_crear`, `correo_envio_listar`, `correo_envio_crear` |
| Transferencias (11) | `transferencia_listar`, `transferencia_crear`, `transferencia_avanzar`, `transferencia_aprobar`, `transferencia_despachar`; costos y liquidación: `transfer_costos_listar`, `transfer_liquidacion_preview` |
| Clientes (10) | `cliente_listar`, `cliente_obtener`, `cliente_crear`, `cliente_editar`, `cliente_subsidiarias`, `cliente_kpis_pool` |
| Tareas (10) | `tarea_listar`, `tarea_crear`, `tarea_completar`, `tarea_reprogramar`, `tarea_catalogo_listar` |
| Finanzas (9) | `finanzas_overview`, `finanzas_comisiones`, `finanzas_commission_by_month`, `finanzas_margin_scatter`, `finanzas_cliente`, `finanzas_comisiones_por_marca` |
| Productos (8) | `producto_listar`, `producto_buscar`, `producto_ficha_tecnica`, `producto_precio_cliente`, `producto_crear` |
| Pagos (8) | `pago_applicables`, `pago_listar`, `pago_dry_run`, `pago_registrar`, `pago_conciliar` |
| Documentos y artefactos (6+3) | `documento_subir`, `documento_listar`, `documento_descargar`, `documento_registrar_archivo`; `artefacto_publicar`, `artefacto_editar` |
| SAP (6) | `sap_analizar`, `sap_confirmar`, `sap_upsert`, `sap_obtener`, `sap_sincronizar_discrepancias` |
| Inventario (5) | `inventario_saldos_por_expediente`, `inventario_expedientes_con_pendiente`, `inventario_lineas_en_nodo`, `inventario_transferir_asignaciones` |
| OC, proformas y portal (3+3+3) | `oc_listar`, `oc_obtener`, `oc_editar`; `proforma_generar`, `proforma_html`, `proforma_documento`; `portal_embarques`, `portal_subir_documento` |
| Builder y plantillas (8) | `builder_templates_listar`, `builder_structure_construir`, `builder_artefacto_crear` |
| Nodos (6) | `nodo_listar`, `nodo_crear`, `nodo_artefactos_listar`, `nodo_artefacto_crear` |
| Identidad y auditoría (6) | `mwt_health`, `mwt_whoami`, `mwt_guia_rol`, `mwt_audit_write_registry`, `mwt_auditoria_listar` |
| Precios y storage (4) | `pricelist_listar`, `pricelist_por_vencer`, `storage_subir_archivo`, `storage_subir_base64` |

### Ejemplos

**1. Estado de un expediente**

```
Decime el estado del expediente 2487-2026
```

`expediente_buscar(proforma: "2487-2026")` devuelve la proforma, la OC `505244`, el SAP `282479`, estado `EN_DESTINO`, monto cliente `USD 28.658,30` y 90 días de crédito. Para el detalle: `expediente_lineas`, `expediente_obtener`.

**2. Cliente y su cartera**

```
¿Qué le vendimos a Sondel este año? ¿Cómo viene su crédito?
```

`cliente_listar` / `cliente_obtener` para la ficha, `expediente_listar` filtrado por cliente, `finanzas_cliente` para márgenes y `cliente_kpis_pool` para el agregado del grupo.

**3. Inventario y pendientes**

```
¿Qué expedientes tienen líneas pendientes de entrega?
```

`inventario_expedientes_con_pendiente`, `inventario_saldos_por_expediente`, `inventario_lineas_en_nodo`.

**4. Pagos y conciliación**

```
¿Qué pagos puedo aplicar a este expediente?
```

`pago_applicables`, `pago_dry_run` (simula sin escribir), `pago_registrar`, `pago_conciliar`.

**5. Correo de la cuenta**

```
Listame los correos sin leer y proponeme una respuesta
```

`correo_mensaje_listar`, `correo_mensaje_obtener`, `correo_contacto_listar`, `correo_envio_crear`. La cuenta IMAP/SMTP se configura en FaberLoom → **Conexiones**; el MCP sólo opera sobre lo ya configurado.

**6. Finanzas**

```
Mostrame el margen por cliente y las comisiones del mes
```

`finanzas_overview`, `finanzas_margin_scatter`, `finanzas_comisiones_por_marca`.

> **Herramientas que escriben.** Varias terminan en `_crear`, `_editar`, `_registrar`, `_aprobar`, `_avanzar` o `_publicar`: crean o modifican datos reales. Pedilas en modo lectura primero (`_listar`, `_obtener`, `_dry_run`) y revisá el resultado antes de confirmar. El rol de la cuenta en la consola decide qué podés escribir.

---

## Lo que vive en FaberLoom, no en el mod

El mod **no** reimplementa el producto: lee lo que FaberLoom ya produce y lo pone a la vista de Claude. Estas funciones se configuran y se operan en **FaberLoom** (aplicación o `harness.mwt.one`), y llegan a Claude por la proyección del Space:

| Función | Dónde se configura | Cómo la ve Claude |
|---|---|---|
| **Correo IMAP/SMTP** | FaberLoom → **Conexiones**: cuenta IMAP, servidor SMTP, credenciales y política de envío | Las herramientas de correo viven en el producto; en Claude se trabaja el correo con el MCP de MWT.ONE y los archivos del Space |
| **Mesa de trabajo (workbench)** | FaberLoom → **Mesa de trabajo**: la cola, severidades, revisiones y aprobaciones | `/mesa` lee la cola real del storage del producto |
| **Flujos (workflows)** | FaberLoom → **Flujos**: nodos, conexiones, ejecución | `/faberloom` y `/mesa` listan los flujos proyectados; el editor vive en el producto |
| **Rutinas** | FaberLoom → **Rutinas**: disparadores, pasos y programación | `/faberloom` las lista |
| **Memoria** | FaberLoom → **Memoria**: correcciones y enseñanzas por Space | `/faberloom` cuenta las entradas; el contenido viaja en la proyección |
| **Contexto** | FaberLoom → **Contexto**: entradas curadas con versiones y aprobación | `/faberloom` cuenta las entradas; el contenido viaja en la proyección |
| **Spaces** | FaberLoom → **Espacios**: ámbito, agentes, skills, reglas y carpeta | `/faberloom` identifica el Space de la carpeta |
| **Agentes y skills** | FaberLoom → **Agentes y Skills** | Se instalan como nativos en `~/.claude` |
| **Conexiones MWT.ONE** | FaberLoom → **Conexiones** (usuario y contraseña de consola) | `/mwt` repite el mismo flujo desde Claude |

### La proyección: el puente

FaberLoom escribe el harness de cada Space **dentro de su carpeta**. Eso es lo que Claude Code lee de forma nativa:

| Archivo | Qué contiene |
|---|---|
| `CLAUDE.md` | Instrucciones del ámbito: agentes, skills, flujos, rutinas y reglas |
| `.claude/agents/<slug>.md` | Un subagente por agente del Space |
| `.claude/skills/<nombre>/SKILL.md` | Las skills del Space |
| `.faberloom/harness.json` | Manifiesto: qué se escribió, cuándo y con qué conteos |

Por eso, al abrir la carpeta de un Space en Claude Code, el Space ya está activo: sus reglas, agentes y skills se cargan solos.

---

## Cómo trabajar un Space desde Claude

1. En FaberLoom, creá el Space y asignale agentes, skills, contexto y reglas.
2. Abrí en Claude Code **la carpeta del Space** (la misma que muestra FaberLoom).
3. Comprobá el ámbito:

```
/faberloom
```

4. Trabajá con el catálogo del Space:

```
@agent-analista-sicop    revisá este cartel
/sicop-contratacion-publica
```

5. Consultá datos de empresa cambiando de empresa si hace falta:

```
/mwt sondel-s-a
Decime el estado del expediente 2487-2026
```

6. Revisá la cola de la Mesa:

```
/mesa
```

---

## Seguridad

- El mod corre con tus permisos, como cualquier plugin de Claude Code instalado. Revisá `hooks/register.ts` antes de confiar: son ~350 líneas y no hay ofuscación.
- La contraseña de MWT.ONE es `sensitive`: se guarda cifrada, nunca en el chat ni en `settings.json`.
- Los DeviceToken viven en el store del plugin; para revocarlos, ejecutá `/mwt` de nuevo tras cambiar la contraseña, o borrá `~/.claude/plugins/store/faberloom_faberloom-*.json`.
- El mod no escribe en la Mesa ni en el producto: sólo lee (storage, proyección) y llama al MCP de la empresa activa.
- SICOP es público y no lleva identidad: cualquier instalación lo alcanza igual.

---

## Licencia y atribución

MIT. Ver [`LICENSE`](LICENSE) y [`NOTICE.md`](NOTICE.md).

El catálogo combina material propio de FaberLoom con el catálogo de **ECC** (MIT, Copyright 2026 Affaan Mustafa), cuyo aviso se reproduce en `NOTICE.md`.
