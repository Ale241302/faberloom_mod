---
name: affinity-mcp
description: "Operar Affinity por su servidor MCP oficial — ejecutar scripts del SDK, renderizar y guardar workflows como herramientas reutilizables."
---

# Affinity por MCP

Affinity expone un servidor MCP oficial (beta gratuita, desde el release April '26). Es la
vía correcta para operar Affinity — **nunca pilotear la GUI con clics y screenshots**, que es
lento, frágil y deja el documento en estados imprevistos.

## Requisitos

- Affinity **April '26 o posterior**, instalado y **corriendo**
- MCP activado: menú `Edit` (Windows) / `Affinity` (Mac) → `Settings` → `Model Context
  Protocol` → `Enable MCP server`, y reiniciar Affinity
- Conector Affinity instalado en Claude Desktop (`Settings` → `Connectors`)

Si las tools responden *"The Affinity app is not running or MCP is not enabled"*, la app está
cerrada. Pedir que la abran; no reintentar en loop.

## Cómo funciona realmente

No son comandos discretos: es un **motor de scripting JavaScript** sobre el SDK de Affinity.
El trabajo se hace escribiendo scripts, no llamando a una tool por operación.

| Tool | Para qué |
|---|---|
| `list_sdk_documentation` / `read_sdk_documentation_topic` | La documentación del SDK |
| `execute_script` | Ejecuta JavaScript. **Leer la doc `preamble` antes de la primera llamada** |
| `render_spread` / `render_selection` | JPEG base64, máximo 1024px — para verificar visualmente |
| `list_library_scripts` / `read_library_script` | Scripts ya guardados en el panel |
| `save_script_to_library` | Guardar un workflow como script reutilizable |
| `search_sdk_hints` / `add_sdk_hint` | Pool global de soluciones de otras sesiones |

## Orden de trabajo

1. `list_sdk_documentation` y leer el `preamble` **antes** del primer `execute_script`.
2. Ante un error del SDK, `search_sdk_hints` antes de improvisar — alguien probablemente ya
   lo resolvió.
3. Ejecutar sobre un documento existente. El SDK rinde mal creando desde cero.
4. **Renderizar y mirar el resultado** antes de darlo por bueno.
5. Si el workflow se va a repetir, `save_script_to_library`. Ahí está el valor real: deja de
   ser un cambio puntual y pasa a ser una herramienta.

## Para qué rinde

Organización de capas y mesas de trabajo, redimensionado en lote a varios formatos, ajustes
masivos sobre documentos largos, limpieza de trazados, localización de texto, exportación
multi-formato con nomenclatura, y construcción de herramientas propias con interfaz.

## Advertencias de la beta

- Una tarea puede fallar en el primer intento y salir bien en el segundo. Reintentar una vez
  antes de declararla imposible.
- Si el asistente asume una versión vieja de Affinity, decirle explícitamente: *"estoy usando
  Affinity by Canva, release April '26"*.
- No hay soporte en móvil, ni en Affinity China.
- `save_script_to_library` no sobrescribe scripts existentes: guarda bajo nombre nuevo.

## Permisos a revisar con el usuario

El conector pide acceso a archivos del escritorio, red, lectura y escritura de scripts, y
memoria local de hints. El permiso de **Canva AI Studio consume la cuota mensual del plan
Canva** — dejarlo apagado salvo pedido explícito.

## Cuándo NO usar Affinity

Para un cambio quirúrgico sobre un archivo exportado —reemplazar un color, leer una paleta—
editar el archivo directo es más exacto y más rápido que abrirlo en Affinity. Affinity gana
cuando hace falta el modelo de documento: capas, objetos, texto, exportación multi-formato,
o cuando el workflow se va a repetir y conviene dejarlo como script.