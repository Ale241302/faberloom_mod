<#
  ver_video.ps1  —  Descarga un video, extrae subtitulos y fotogramas de cambio de escena.

  Parte de la skill "ver-video" (MWT). Escrito desde cero: sin repos de terceros,
  sin API keys, sin trafico a servicios externos mas alla del propio sitio del video.
  Todo el trabajo queda en %TEMP%\ver-video\<video_id>\ y el .mp4 se borra al final.

  Dependencias: python -m yt_dlp   ·   ffmpeg en PATH
  Uso:
    powershell -ExecutionPolicy Bypass -File ver_video.ps1 -Url "<URL>" [-MaxFrames 40] [-Scene 0.30] [-Keep]
#>

param(
    [Parameter(Mandatory = $true)][string]$Url,
    [int]$MaxFrames = 40,
    [double]$Scene  = 0.30,
    [switch]$Keep
)

# 'Continue': yt-dlp y ffmpeg escriben avisos a stderr que NO son fallos del script.
# Los fallos reales se detectan con validaciones explicitas (throw) mas abajo.
$ErrorActionPreference = 'Continue'
$PSNativeCommandUseErrorActionPreference = $false
$root = Join-Path $env:TEMP 'ver-video'
New-Item -ItemType Directory -Force $root | Out-Null

function Write-Status([string]$dir, [string]$text) {
    Set-Content -Path (Join-Path $dir 'STATUS.txt') -Value $text -Encoding UTF8
}

try {
    # --- 1. Identificar el video (barato, sin descargar) -------------------
    $id = (& python -m yt_dlp --skip-download --print "%(id)s" --no-warnings $Url 2>$null | Select-Object -First 1)
    if ([string]::IsNullOrWhiteSpace($id)) { throw "No se pudo resolver el ID del video. Revisar la URL o si yt-dlp necesita actualizarse." }
    $id = ($id -replace '[^A-Za-z0-9_\-]', '_')

    $dir    = Join-Path $root $id
    $frames = Join-Path $dir 'frames'
    New-Item -ItemType Directory -Force $dir    | Out-Null
    New-Item -ItemType Directory -Force $frames | Out-Null
    Remove-Item (Join-Path $frames '*') -Force -ErrorAction SilentlyContinue

    Write-Status $dir "RUNNING - resolviendo metadatos ($id)"

    # --- 2. Metadatos + subtitulos (sin bajar el video) -------------------
    # Subtitulos: best-effort. Un 429 o la ausencia de subs NO debe abortar el analisis visual.
    & python -m yt_dlp --skip-download --ignore-errors --no-abort-on-error --sleep-requests 1 `
        --write-auto-sub --write-sub --sub-lang "en.*,es.*,pt.*" --sub-format vtt `
        --write-info-json --no-warnings `
        -o (Join-Path $dir 'v.%(ext)s') $Url *> (Join-Path $dir '_ytdlp_meta.log')

    Write-Status $dir "RUNNING - descargando video"

    # --- 3. Video a <=480p, solo imagen (liviano; el audio no se usa) -----
    $mp4 = Join-Path $dir 'v.mp4'
    & python -m yt_dlp --no-warnings `
        -f "bv*[height<=480][ext=mp4]/bv*[height<=480]/b[height<=480]" `
        -o $mp4 $Url *> (Join-Path $dir '_ytdlp_video.log')

    if (-not (Test-Path $mp4)) { throw "La descarga del video no produjo v.mp4. Ver _ytdlp_video.log" }

    # --- 4. Metadatos legibles -------------------------------------------
    Write-Status $dir "RUNNING - procesando metadatos y subtitulos"
    $subLines = (& python (Join-Path $PSScriptRoot 'proc_subs.py') $dir 2>&1 | Select-Object -Last 1)

    # --- 5. Fotogramas en los cambios de escena ---------------------------
    Write-Status $dir "RUNNING - extrayendo fotogramas"
    $ffLog = Join-Path $dir '_ffmpeg.log'
    & ffmpeg -hide_banner -loglevel info -i $mp4 `
        -vf "select='gt(scene,$Scene)',showinfo,scale=900:-2" `
        -fps_mode vfr -q:v 4 (Join-Path $frames 'f_%03d.jpg') 2> $ffLog

    # timestamps desde showinfo -> frames_index.txt
    $times = @()
    if (Test-Path $ffLog) {
        foreach ($m in [regex]::Matches((Get-Content $ffLog -Raw), 'pts_time:([0-9]+\.?[0-9]*)')) {
            $times += [double]$m.Groups[1].Value
        }
    }
    $files = Get-ChildItem $frames -Filter 'f_*.jpg' | Sort-Object Name

    # si hay mas frames que MaxFrames, quedarse con una muestra pareja
    if ($files.Count -gt $MaxFrames -and $MaxFrames -gt 0) {
        $step = [math]::Ceiling($files.Count / $MaxFrames)
        for ($i = 0; $i -lt $files.Count; $i++) {
            if ($i % $step -ne 0) { Remove-Item $files[$i].FullName -Force -ErrorAction SilentlyContinue }
        }
        $files = Get-ChildItem $frames -Filter 'f_*.jpg' | Sort-Object Name
    }

    $idx = foreach ($f in $files) {
        $n = [int]([regex]::Match($f.Name, 'f_(\d+)\.jpg').Groups[1].Value)
        $t = if ($times.Count -ge $n) { [timespan]::FromSeconds($times[$n-1]).ToString('hh\:mm\:ss') } else { '--:--:--' }
        "{0}`t{1}" -f $f.Name, $t
    }
    Set-Content -Path (Join-Path $dir 'frames_index.txt') -Value $idx -Encoding UTF8

    # --- 6. Limpieza (POL_EPHEMERAL_OUTPUT) -------------------------------
    if (-not $Keep) { Remove-Item $mp4 -Force -ErrorAction SilentlyContinue }
    Remove-Item (Join-Path $dir '*.vtt') -Force -ErrorAction SilentlyContinue

    Write-Status $dir "DONE - frames=$($files.Count) subtitulos=$subLines dir=$dir"
}
catch {
    $d = if ($dir) { $dir } else { $root }
    Write-Status $d "ERROR: $($_.Exception.Message)"
    exit 1
}
