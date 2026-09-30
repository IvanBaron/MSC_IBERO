"""Descarga UNA VEZ un mapa base de la ZMVM y lo deja como PNG local.

Así el notebook no necesita red para dibujarlo. Tiles de OpenStreetMap,
convertidos a gris claro para que sirvan de fondo translúcido sin competir con
los colores de los datos.

Los estilos claros de CARTO ya exigen clave de API (devuelven tiles con marca de
agua), por eso se usa OSM directo. Son 48 tiles con User-Agent identificado, bien
dentro de su política de uso.
Licencia: © OpenStreetMap contributors (ODbL).
"""
import io
import json
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

ZOOM = 11
BBOX = (-99.62, 18.93, -98.62, 20.02)      # lon_min, lat_min, lon_max, lat_max
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
GRIS = 0.40      # cuánto se aclara hacia el blanco (0 = gris pleno, 1 = blanco)
SALIDA = Path("mapa_base_zmvm.png")


def lon_a_x(lon, n): return (lon + 180.0) / 360.0 * n
def lat_a_y(lat, n):
    r = np.radians(lat)
    return (1.0 - np.log(np.tan(r) + 1 / np.cos(r)) / np.pi) / 2.0 * n
def x_a_lon(x, n): return x / n * 360.0 - 180.0
def y_a_lat(y, n):
    return np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * y / n))))


def main():
    n = 2 ** ZOOM
    x0, x1 = int(np.floor(lon_a_x(BBOX[0], n))), int(np.floor(lon_a_x(BBOX[2], n)))
    y0, y1 = int(np.floor(lat_a_y(BBOX[3], n))), int(np.floor(lat_a_y(BBOX[1], n)))
    cols, filas = x1 - x0 + 1, y1 - y0 + 1
    print(f"zoom {ZOOM}: {cols} x {filas} = {cols*filas} tiles")

    lienzo = Image.new("RGB", (cols * 256, filas * 256), "white")
    for i, xt in enumerate(range(x0, x1 + 1)):
        for j, yt in enumerate(range(y0, y1 + 1)):
            url = URL.format(z=ZOOM, x=xt, y=yt)
            req = urllib.request.Request(url, headers={
                "User-Agent": "mapa-base-zmvm/1.0 (notebook academico; contacto: usuario local)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                tile = Image.open(io.BytesIO(r.read())).convert("L").convert("RGB")
                tile = Image.blend(tile, Image.new("RGB", tile.size, "white"), GRIS)
                lienzo.paste(tile, (i * 256, j * 256))
            time.sleep(0.12)
        print(f"  columna {i+1}/{cols}")

    lienzo.save(SALIDA, optimize=True)
    # La extensión real de la imagen: los bordes de los tiles, no el bbox pedido.
    extent = [float(x_a_lon(x0, n)), float(x_a_lon(x1 + 1, n)),
              float(y_a_lat(y1 + 1, n)), float(y_a_lat(y0, n))]
    SALIDA.with_suffix(".json").write_text(json.dumps({"extent": extent}, indent=1))
    print(f"{SALIDA} ({SALIDA.stat().st_size/1e6:.1f} MB, {lienzo.size[0]}x{lienzo.size[1]} px)")
    print(f"extensión [lon_min, lon_max, lat_min, lat_max] = {np.round(extent, 4).tolist()}")


if __name__ == "__main__":
    main()
