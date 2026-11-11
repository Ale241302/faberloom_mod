---
name: ver-video
description: Ver y analizar un video de verdad, no sólo su transcripción — descarga el video, extrae los fotogramas donde cambia la escena y los lee junto con los subtítulos, para captar lo que sólo se ve en pantalla (interfaces, dashboards, código, diagramas, slides). Usar SIEMPRE que el usuario diga "ve este video", "mirá/mira este video", "analizá este video", "revisá este video", "qué muestra este video", "resumí este video", "scraping de este video", o pegue una URL de YouTube, Loom, Vimeo, TikTok, X o Instagram esperando análisis. Usar también cuando ya se obtuvo una transcripción y resulta insuficiente porque el contenido es visual.
---

# ver-video — análisis visual + transcripción

## Por qué existe

Leer la transcripción de un video no es ver el video. En un tutorial de software, un
demo de producto, una review de interfaz o una charla con slides, **lo que importa está
en pantalla y el audio no lo nombra**: layouts, nombres de campos, valores de
configuración, código, diagramas, estados de una UI.

Esta skill cierra esa brecha: baja el video, corta fotogramas en cada cambio de escena,
y los entrega junto con los subtítulos y los capítulos para que el análisis cruce **lo
que se dice** con **lo que se muestra**.

## Regla de origen

Esta skill **no instala ni ejecuta código de terceros**. Existen skills públicas
parecidas; el mecanismo se reimplementó desde cero bajo estas restricciones, que
conviene mantener si alguien la modifica:

| Restricción | Por qué |
|---|---|
| Sólo `yt-dlp` + `ffmpeg`, instalados por gestor de paquetes oficial | Cero repos de terceros clonados |
| **Cero API keys.** La transcripción sale de los subtítulos que el propio sitio publica | Otras skills mandan el audio a Whisper vía Groq/OpenAI: eso saca el contenido a un tercero y deja credenciales en disco |
| Todo el trabajo en un directorio temporal propio | No toca nada del usuario |
| El video se borra al terminar | Sólo sobreviven transcripción, fotogramas e índice |
| Dos archivos legibles de punta a punta: `ver_video.ps1` / `ver_video.sh` + `proc_subs.py` | Auditable antes de correr. Nada minificado, nada descargado en runtime |

## Paso 0 — elegir dónde corre

**Importante:** muchos sitios (YouTube en particular) responden `429 Too Many Requests`
o *"Sign in to confirm you're not a bot"* a las peticiones que salen de IPs de
datacenter. Por eso el orden de preferencia es:

1. **La máquina del usuario**, si hay puente disponible — herramientas `mcp__remote-devices__*`
   (`Windows-MCP__PowerShell`, `device_bash`) o un `Desktop_Commander` conectado.
   Es una IP residencial: funciona sin fricción. **Preferir siempre esta vía.**
2. **El entorno local de ejecución** (`Bash`) si la skill corre en una sesión con shell propia.
3. Si sólo hay entorno cloud y el sitio bloquea, decirlo con claridad y pedir al usuario
   el archivo de video directo, o la URL de otro origen. **No exportar cookies del
   navegador del usuario a la skill.**

Scripts incluidos: `scripts/ver_video.ps1` (Windows/PowerShell) y `scripts/ver_video.sh`
(Linux/macOS). Hacen exactamente lo mismo.

> Estado de verificación: el `.ps1` está probado de punta a punta (28 fotogramas + 708
> líneas de subtítulos sobre un video de 21 min). El `.sh` está verificado en sintaxis y
> en manejo de error — su camino feliz no pudo probarse porque desde el contenedor
> YouTube devuelve bot-check, que es justamente el motivo del orden del Paso 0.

### Prerequisitos

```
yt-dlp   →  python -m pip install -U yt-dlp     (o: pipx install yt-dlp)
ffmpeg   →  winget install Gyan.FFmpeg  ·  apt install ffmpeg  ·  brew install ffmpeg
```

Verificar antes de correr; si falta alguno, instalarlo es parte del trabajo.

## Paso 1 — lanzar

**Windows**
```powershell
powershell -ExecutionPolicy Bypass -File "<ruta>\scripts\ver_video.ps1" -Url "<URL>" -MaxFrames 40
```

**Linux / macOS**
```bash
bash <ruta>/scripts/ver_video.sh --url "<URL>" --max-frames 40
```

Parámetros: `Url` (requerido) · `MaxFrames` (default 40) · `Scene` (umbral de cambio de
escena, default 0.30) · `Keep` (no borrar el video descargado).

**La descarga suele tardar más que el timeout de una llamada de herramienta.** Lanzar en
segundo plano y consultar después:

```powershell
Start-Process powershell -ArgumentList "-ExecutionPolicy","Bypass","-File","<script>","-Url","<URL>" -WindowStyle Hidden
# esperar, luego:
Get-Content "$env:TEMP\ver-video\<id>\STATUS.txt"
```

```bash
nohup bash ver_video.sh --url "<URL>" >/dev/null 2>&1 &
cat "${TMPDIR:-/tmp}/ver-video/<id>/STATUS.txt"
```

## Paso 2 — leer la salida

Todo queda en `<temp>/ver-video/<video_id>/`:

| Archivo | Contenido |
|---|---|
| `STATUS.txt` | `RUNNING` / `DONE` / `ERROR: <detalle>` — **consultar esto primero** |
| `meta.json` | título, canal, fecha, duración, vistas, capítulos |
| `transcript.txt` | subtítulos deduplicados, con timestamp por línea |
| `frames/f_###.jpg` | fotogramas en los cambios de escena, 900 px de ancho |
| `frames_index.txt` | `f_001.jpg⇥00:01:23` — mapea cada fotograma a su momento |
| `desc.txt` | descripción del video (links, timestamps del autor) |

## Paso 3 — analizar

1. Leer `meta.json` y `frames_index.txt` — dan estructura y mapa.
2. Leer `transcript.txt`.
3. **Leer los fotogramas.** Este es el paso que distingue esta skill de una simple
   transcripción, y el que no hay que saltarse:
   - con `Desktop_Commander__read_file` sobre el `.jpg` (devuelve la imagen);
   - o con la herramienta `Read` si el archivo está en el entorno local;
   - o subiéndolos al contexto por el medio que la sesión ofrezca.
4. **Elegir cuáles leer cruzando `frames_index.txt` con los `chapters` de `meta.json`.**
   No leerlos en orden: leer los de las secciones que importan para lo que el usuario preguntó.
5. Sintetizar cruzando lo que se dice con lo que se muestra. Cuando difieren, **lo que
   se ve manda** — y vale la pena decirlo explícitamente.

### Cuántos fotogramas leer

| Duración | Leer | Criterio |
|---|---|---|
| < 5 min | todos | son pocos |
| 5–20 min | 15–25 | uno o dos por capítulo, más los de pantallas densas |
| > 20 min | 20–30 | guiado por capítulos y por la pregunta del usuario |

Cada fotograma cuesta contexto. Uno de una persona hablando no aporta nada; uno de una
pantalla con datos vale por diez líneas de transcripción. **Elegir por contenido, no por
orden.**

## Paso 4 — cerrar

El script borra el video solo. Los fotogramas y la transcripción quedan en temporal para
el resto de la sesión. Si el usuario los quiere conservar, copiarlos a una carpeta suya
con nombre descriptivo y decirle dónde quedaron.

## Errores conocidos

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `Sign in to confirm you're not a bot` / `429` al bajar el video | Corriendo desde IP de datacenter | Correr en la máquina del usuario (Paso 0) |
| `429` sólo al bajar subtítulos | Se pidió el mismo video varias veces seguidas | Ya contemplado: los subtítulos son best-effort y no abortan el análisis visual. Reintentar en unos minutos si hacen falta |
| `frames/` vacío | `-vsync` está deprecado en ffmpeg ≥ 7 | Ya resuelto: los scripts usan `-fps_mode vfr` |
| El script aborta con `ERROR: ERROR: …` | En PowerShell, `$ErrorActionPreference='Stop'` convierte el stderr de yt-dlp en excepción | Ya resuelto: corre en `Continue` y valida con `throw` explícito |
| 0 subtítulos | El video no tiene subs ni autogenerados | Seguir sólo con fotogramas. **No mandar el audio a un servicio externo.** Avisar al usuario que no hay transcripción |
| Muy pocos fotogramas | Video estático (una sola pantalla fija) | Bajar `Scene` a 0.15 |
| Cientos de fotogramas | Mucho corte, cámara en mano, o gameplay | Subir `Scene` a 0.5 |

## Alcance

Cualquier sitio soportado por `yt-dlp`: YouTube, Loom, Vimeo, TikTok, X, Instagram y
varios cientos más. Para contenido que requiere sesión iniciada, pedir al usuario el
archivo directo — nunca exportar sus cookies.
