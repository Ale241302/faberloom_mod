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

SICOP es la plataforma de contratación pública de Costa Rica. El plugin declara su servidor MCP **público**: no pide credenciales ni identidad, y aporta **71 herramientas** de licitaciones, carteles, ofertas, adjudicaciones, contratos, proveedores, precios y sanciones.

- Servidor: `sicop` (`https://sicop.vlinte.work/mcp`).
- Herramientas: `mcp__sicop__*`. Se listan en `/mcp`.
- Antes de la primera consulta conviene cargar la skill `sicop-contratacion-publica`, que fija las reglas de reporte (nivel de medición, cobertura, moneda y caveats).

Ejemplos de pedidos que funcionan tal cual:

```
¿En qué licitaciones ganó Sondel?
Compará los oferentes del cartel 2024LA-000123-01
Serie de precios por año del proveedor 3101095926
¿Hay sanciones o carteles objetados para ese proveedor?
```

Cada cifra vuelve con su nivel de medición: no se inventan montos ni adjudicaciones que ninguna herramienta no devolvió.

---

## MCP de MWT.ONE

MWT.ONE es la consola de operación: clientes, empresas, expedientes, proformas, pedidos, inventario y facturas. La consola emite **un DeviceToken por empresa**, y el mod lo usa así:

1. `/mwt` inicia sesión y guarda un token por empresa.
2. `/mwt <clave>` elige la empresa activa (por ejemplo `muito-work-limitada` o `sondel-s-a`).
3. El agente llama la herramienta **`mcp__faberloom__mwt`**, que abre la sesión MCP de esa empresa y ejecuta la herramienta pedida.

Forma de la llamada:

```json
{ "name": "expediente_buscar", "input": { "proforma": "2487-2026" } }
```

Ejemplo real, con la empresa activa en Sondel:

```
Decime el estado del expediente 2487-2026
```

devuelve la proforma `2487-2026`, la OC `505244`, el SAP `282479`, estado `EN_DESTINO`, monto cliente `USD 28.658,30` y 90 días de crédito.

Detalles que importan:

- El token de cada empresa se guarda en el store del plugin (bajo `~/.claude`), no en el repositorio.
- La contraseña sólo se usa para el login de la consola; el modelo nunca la ve.
- Si el token caduca, `/mwt` lo vuelve a emitir.
- Otros clientes MCP pueden usar el mismo servidor con `Authorization: DeviceToken <token>`.

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
