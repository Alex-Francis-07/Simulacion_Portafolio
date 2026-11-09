"""Una función: exporta toda la secuencia de una corrida a CSV."""

import csv
from pathlib import Path


def guardar_secuencia(numeros: list[float], archivo: Path) -> None:
    archivo.parent.mkdir(parents=True, exist_ok=True)
    with archivo.open("w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow(("indice", "valor"))
        for i, valor in enumerate(numeros, start=1):
            escritor.writerow((i, format(valor, ".17g")))
