"""Localiza los datos y lee las redes diarias. Lo comparten scripts y notebooks."""
from pathlib import Path

import pandas as pd


def find_data_dir():
    for base in [Path.cwd(), *Path.cwd().parents]:
        c = base / "data_garrido" / "gwq6u-osfstorage-archive"
        if c.is_dir():
            return c
    raise FileNotFoundError("No encontre data_garrido/gwq6u-osfstorage-archive")


def leer_dia(fecha):
    """Viajes crudos por par para una fecha. El mínimo de w equivale a un viaje."""
    a = pd.read_csv(find_data_dir() / "Networks" / f"od_cvegeo_09_01_{fecha.replace('-', '_')}.csv",
                    dtype={"source": str, "target": str})
    a["v"] = (a.w / a.w.min()).round().astype(int)
    return a[["source", "target", "v"]]
