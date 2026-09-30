"""Deja una matriz ancha (aristas del núcleo x fechas) lista para modelar.

Estructura simple a propósito: filas = pares origen-destino, columnas = fechas,
valores = viajes crudos. Todo lo demás se deriva de ahí con operaciones de pandas.
"""
from pathlib import Path
import time

import numpy as np
import pandas as pd

from datos import find_data_dir, leer_dia

# Las conexiones estables se fijan con los 28 días previos al inicio de la prueba:
# así se eligen sin mirar ni un solo día de evaluación.
NUCLEO_FIN = "2020-11-30"
NUCLEO_DIAS = 28
K = 10          # viajes mínimos
FRAC = 0.9      # fracción de días en que debe superarlo

INICIO = "2020-05-04"   # 28 días de calentamiento antes del primer objetivo
FIN = "2021-03-31"


def main():
    DATA = find_data_dir()
    NET = DATA / "Networks"
    t0 = time.time()

    # --- paso 1: definir el núcleo -----------------------------------------
    dias_nucleo = pd.date_range(end=NUCLEO_FIN, periods=NUCLEO_DIAS).strftime("%Y-%m-%d")
    cuenta = pd.concat([leer_dia(f).query("v >= @K") for f in dias_nucleo])
    cuenta = cuenta.groupby(["source", "target"]).size()
    nucleo = cuenta[cuenta >= FRAC * NUCLEO_DIAS].index
    print(f"núcleo: {len(nucleo):,} aristas  [{time.time()-t0:.0f}s]")

    # --- paso 2: matriz ancha ----------------------------------------------
    fechas = pd.date_range(INICIO, FIN).strftime("%Y-%m-%d")
    columnas = {}
    for i, f in enumerate(fechas):
        columnas[f] = leer_dia(f).set_index(["source", "target"]).v.reindex(nucleo).fillna(0).to_numpy(dtype="float32")
        if (i + 1) % 60 == 0:
            print(f"  {i+1:3d}/{len(fechas)}  {f}  [{time.time()-t0:.0f}s]")

    M = pd.DataFrame(columnas, index=nucleo)
    M.columns = pd.to_datetime(M.columns)
    M.to_parquet("matriz_nucleo.parquet")
    print(f"matriz {M.shape[0]:,} x {M.shape[1]} -> matriz_nucleo.parquet "
          f"({Path('matriz_nucleo.parquet').stat().st_size/1e6:.0f} MB, {time.time()-t0:.0f}s)")

    # --- paso 3: dispositivos por día (para normalizar) ---------------------
    disp = {}
    for f in fechas:
        a = pd.read_csv(NET / f"od_cvegeo_09_01_{f.replace('-', '_')}.csv", usecols=["w"])
        disp[f] = 1e6 / a.w.min()
    pd.Series(disp, name="dispositivos").to_csv("dispositivos_dia.csv")
    print("dispositivos_dia.csv listo")


if __name__ == "__main__":
    main()
