"""Una función: escribe la tabla de comparación y todos los estadísticos."""

from pathlib import Path
import pandas as pd


def guardar_resumen(filas: list[dict], archivo: Path) -> None:
    archivo.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(filas).to_csv(archivo, index=False, float_format="%.12g")
