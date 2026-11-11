#!/usr/bin/env python3
"""
preflight_amazon.py - validador determinista de piezas para un listing de Amazon.

No opina. Mide el archivo y devuelve pasa / falla.

    python preflight_amazon.py salida/ --specs .brand/amazon.yaml
    python preflight_amazon.py salida/ --specs .brand/amazon.yaml --json preflight.json

Dependencias:
    obligatoria : Pillow
    opcionales  : pytesseract (checks de texto), exiftool en PATH (checks XMP)
Si una opcional falta, el check se reporta como 'omitido' con su motivo.
NUNCA reporta 'pasa' un check que no pudo ejecutar.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Falta Pillow.  pip install Pillow")

try:
    import pytesseract
    _OCR = shutil.which("tesseract") is not None
except ImportError:
    _OCR = False

_EXIFTOOL = shutil.which("exiftool") is not None

PATRON_BULK = re.compile(r"^([A-Z0-9]{10})\.(MAIN|PT0[1-8])\.(jpe?g|png|tiff?)$", re.I)

# Valores por defecto. --specs los sobreescribe con lo que diga amazon.yaml.
DEF = {
    "lado_largo_min_px": 1000,
    "peso_max_mb": 10,
    "ocupacion_min": 0.85,
    "ocupacion_max": 1.00,
    "tolerancia_blanco": 0,      # 0 = blanco exacto exigido en MAIN
    "margen_muestreo_px": 8,     # ancho del marco que se muestrea como "fondo"
    "lista_negra": [
        "prime", "best seller", "amazon's choice", "amazons choice",
        "garantia", "garantía", "warranty", "envio gratis", "envío gratis",
        "free shipping", "www.", "http", "@", "5 estrellas", "5 stars",
        "oferta", "descuento", "% off", "compra ahora", "buy now",
    ],
}


def cargar_specs(ruta):
    """Lee amazon.yaml sin depender de PyYAML: extrae solo las claves que usa."""
    cfg = dict(DEF)
    if not ruta or not os.path.exists(ruta):
        return cfg, "specs no encontradas - usando valores por defecto"
    txt = open(ruta, encoding="utf-8").read()
    for clave, patron in (
        ("lado_largo_min_px", r"lado_largo_min_px:\s*(\d+)"),
        ("peso_max_mb", r"peso_max_mb:\s*(\d+)"),
    ):
        m = re.search(patron, txt)
        if m:
            cfg[clave] = int(m.group(1))
    return cfg, None


def bbox_producto(im, tol=8):
    """Bounding box de lo que no es fondo blanco."""
    gris = im.convert("RGB")
    fondo = Image.new("RGB", gris.size, (255, 255, 255))
    dif = ImageChops.difference(gris, fondo).convert("L")
    dif = dif.point(lambda p: 255 if p > tol else 0)
    return dif.getbbox()


def borde_pixeles(im, margen):
    """Devuelve el set de colores presentes en el marco exterior."""
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    colores = set()
    for x in range(w):
        for y in list(range(margen)) + list(range(h - margen, h)):
            colores.add(px[x, y])
    for y in range(h):
        for x in list(range(margen)) + list(range(w - margen, w)):
            colores.add(px[x, y])
    return colores


def ocr(ruta):
    if not _OCR:
        return None
    try:
        return pytesseract.image_to_string(Image.open(ruta)).strip()
    except Exception:
        return None


def xmp_subjects(ruta):
    if not _EXIFTOOL:
        return None
    try:
        out = subprocess.run(
            ["exiftool", "-s3", "-XMP-dc:Subject", ruta],
            capture_output=True, text=True, timeout=20,
        )
        return out.stdout.strip()
    except Exception:
        return None


def revisar(ruta, cfg, declara_persona_ia=False):
    nombre = os.path.basename(ruta)
    r = {"archivo": nombre, "checks": {}}

    def marcar(cid, estado, detalle=""):
        r["checks"][cid] = {"estado": estado, "detalle": detalle}

    m = PATRON_BULK.match(nombre)
    if m:
        marcar("nomenclatura", "pasa", "")
        tipo = m.group(2).upper()
    else:
        marcar("nomenclatura", "falla",
               "no coincide con ASIN.MAIN.jpg / ASIN.PT0N.jpg")
        tipo = "MAIN" if "MAIN" in nombre.upper() else "PT"

    r["tipo"] = tipo
    es_main = tipo == "MAIN"

    try:
        im = Image.open(ruta)
    except Exception as e:
        marcar("apertura", "falla", str(e))
        return r

    w, h = im.size
    lado = max(w, h)
    if lado >= cfg["lado_largo_min_px"]:
        marcar("dimension", "pasa", f"{w}x{h}")
    else:
        marcar("dimension", "falla",
               f"{w}x{h} - lado largo bajo {cfg['lado_largo_min_px']}")

    mb = os.path.getsize(ruta) / 1_048_576
    if mb <= cfg["peso_max_mb"]:
        marcar("peso", "pasa", f"{mb:.2f} MB")
    else:
        marcar("peso", "falla", f"{mb:.2f} MB sobre {cfg['peso_max_mb']} MB")

    icc = im.info.get("icc_profile")
    if icc is None:
        marcar("perfil_color", "advertencia",
               "sin perfil ICC embebido - se asume sRGB pero no se puede probar")
    else:
        marcar("perfil_color", "pasa" if b"sRGB" in icc else "advertencia",
               "sRGB" if b"sRGB" in icc else "perfil no identificado como sRGB")

    if es_main:
        colores = borde_pixeles(im, cfg["margen_muestreo_px"])
        malos = [c for c in colores if c != (255, 255, 255)]
        if not malos:
            marcar("fondo_blanco_puro", "pasa", "")
        else:
            marcar("fondo_blanco_puro", "falla",
                   f"{len(malos)} color(es) distintos en el borde, ej {malos[:3]}")

        bb = bbox_producto(im)
        if bb is None:
            marcar("ocupacion", "falla", "no se detecto producto")
        else:
            area = ((bb[2] - bb[0]) * (bb[3] - bb[1])) / float(w * h)
            ok = cfg["ocupacion_min"] <= area <= cfg["ocupacion_max"]
            marcar("ocupacion", "pasa" if ok else "falla", f"{area:.1%} del area")

        borde = borde_pixeles(im, 2)
        marcar("sin_bordes", "pasa" if borde == {(255, 255, 255)} else "falla",
               "" if borde == {(255, 255, 255)} else "perimetro no uniforme blanco")

    texto = ocr(ruta)
    if texto is None:
        motivo = "pytesseract/tesseract no disponible"
        marcar("sin_texto", "omitido", motivo) if es_main else None
        marcar("lista_negra", "omitido", motivo)
    else:
        if es_main:
            marcar("sin_texto", "pasa" if not texto else "falla",
                   "" if not texto else f"OCR: {texto[:60]!r}")
        bajo = texto.lower()
        hits = [t for t in cfg["lista_negra"] if t in bajo]
        marcar("lista_negra", "pasa" if not hits else "falla",
               "" if not hits else f"terminos prohibidos: {hits}")

    if declara_persona_ia:
        subj = xmp_subjects(ruta)
        if subj is None:
            marcar("etiqueta_ia", "omitido", "exiftool no disponible en PATH")
        elif "contains-synthetic-performer" in subj:
            marcar("etiqueta_ia", "pasa", "")
        else:
            marcar("etiqueta_ia", "falla",
                   "declara persona sintetica pero falta el valor en XMP dc:Subject")

    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directorio")
    ap.add_argument("--specs", default=".brand/amazon.yaml")
    ap.add_argument("--json", dest="salida_json")
    ap.add_argument("--persona-ia", nargs="*", default=[],
                    help="nombres de archivo que contienen personas sinteticas")
    a = ap.parse_args()

    cfg, aviso = cargar_specs(a.specs)
    if aviso:
        print(f"[aviso] {aviso}")
    if not _OCR:
        print("[aviso] OCR no disponible - los checks de texto quedan OMITIDOS, no aprobados")
    if not _EXIFTOOL:
        print("[aviso] exiftool no disponible - el check de etiqueta IA queda OMITIDO")

    exts = (".jpg", ".jpeg", ".png", ".tif", ".tiff")
    archivos = sorted(
        os.path.join(a.directorio, f)
        for f in os.listdir(a.directorio)
        if f.lower().endswith(exts)
    )
    if not archivos:
        sys.exit(f"No hay imagenes en {a.directorio}")

    resultados = [
        revisar(f, cfg, os.path.basename(f) in a.persona_ia) for f in archivos
    ]

    fallas = omitidos = 0
    for r in resultados:
        print(f"\n{r['archivo']}  [{r.get('tipo','?')}]")
        for cid, c in r["checks"].items():
            simbolo = {"pasa": "  ok ", "falla": " FALLA", "advertencia": " aviso",
                       "omitido": " omit "}[c["estado"]]
            print(f" {simbolo}  {cid:<20} {c['detalle']}")
            if c["estado"] == "falla":
                fallas += 1
            if c["estado"] == "omitido":
                omitidos += 1

    print(f"\n{'='*54}\n{len(resultados)} pieza(s) · {fallas} falla(s) · {omitidos} omitido(s)")
    if omitidos:
        print("Hay checks OMITIDOS: el paquete NO esta verificado por completo.")

    if a.salida_json:
        with open(a.salida_json, "w", encoding="utf-8") as fh:
            json.dump({"fallas": fallas, "omitidos": omitidos,
                       "piezas": resultados}, fh, indent=2, ensure_ascii=False)
        print(f"-> {a.salida_json}")

    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
