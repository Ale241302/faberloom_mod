# FaberLoom para Claude Code

Marketplace de Claude Code con un solo plugin: **`faberloom`**. Lleva el catálogo de FaberLoom — **145 agentes y 293 skills** — y la cola de la Mesa a Claude Code, más el servidor MCP público de SICOP.

## Requisitos

- Claude Code **2.1.287 o posterior** (`claude --version`).
- Cuenta de MWT.ONE para la parte de empresa (opcional; el resto funciona sin ella).

## Instalar

```bash
claude plugin marketplace add <usuario>/<repo>
claude plugin install faberloom@faberloom
```

O en una sesión, sin instalar:

```bash
claude --plugin-dir ./faberloom
```

Al instalar, Claude Code pide tres datos (`/plugin configure faberloom@faberloom` si no aparecen):

| Dato | Para qué |
|---|---|
| Usuario MWT.ONE | Iniciar sesión en la consola |
| Contraseña MWT.ONE | Se guarda cifrada; nunca entra al chat ni al modelo |
| Consola (opcional) | Por defecto `https://consola.mwt.one/api` |

## Qué queda instalado

- **145 agentes** en `~/.claude/agents` → se invocan con `@agent-<nombre>`.
- **293 skills** en `~/.claude/skills` → se invocan con `/<nombre>`.
- El catálogo se copia una vez por versión de catálogo y **no pisa** lo que ya exista. `/faberloom-install` lo repite.
- El servidor MCP público de **SICOP** (71 herramientas de contratación pública).

## Comandos

| Comando | Qué hace |
|---|---|
| `/faberloom` | Informe del Space proyectado en la carpeta |
| `/agentes` y `/faberloom-skills` | Catálogo con la ruta de cada definición |
| `/mesa` | Cola real de la Mesa desde el storage del producto |
| `/mwt` | Inicia sesión en la consola y lista empresas; `/mwt <clave>` elige la activa |
| `/faberloom-install` | Reinstala el catálogo en `~/.claude` |

La herramienta `mcp__faberloom__mwt` llama cualquier herramienta MCP de la empresa activa:

```json
{ "name": "expediente_buscar", "input": { "proforma": "2487-2026" } }
```

## Licencia y atribución

MIT. El catálogo combina material propio de FaberLoom con el catálogo de **ECC** (MIT, Affaan Mustafa). Ver `LICENSE` y `NOTICE.md`.
