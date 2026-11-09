from pathlib import Path

import matplotlib.pyplot as plt

from servicios import leer_csv


def graficar_archivo(
    ruta_csv: Path,
    carpeta_salida: Path,
    lenguaje: str,
    semilla: int,
) -> None:
    datos = leer_csv(ruta_csv)
    indices = [fila[0] for fila in datos]
    valores = [fila[2] for fila in datos]

    carpeta_salida.mkdir(parents=True, exist_ok=True)

    figura, ejes = plt.subplots(2, 2, figsize=(12, 8))

    figura.suptitle(
        f"Generador LCG - {lenguaje} - semilla {semilla}"
    )

    ejes[0, 0].scatter(indices, valores, s=2, alpha=0.5)
    ejes[0, 0].set_title("Secuencia completa")
    ejes[0, 0].set_xlabel("n")
    ejes[0, 0].set_ylabel("U(n)")
    ejes[0, 0].set_ylim(0, 1)

    limite = min(100, len(valores))
    ejes[0, 1].plot(
        indices[:limite],
        valores[:limite],
        marker=".",
        linewidth=0.7,
    )
    ejes[0, 1].set_title("Primeros 100 valores")
    ejes[0, 1].set_xlabel("n")
    ejes[0, 1].set_ylabel("U(n)")
    ejes[0, 1].set_ylim(0, 1)

    ejes[1, 0].hist(
        valores,
        bins=20,
        range=(0, 1),
        edgecolor="black",
    )
    ejes[1, 0].set_title("Histograma")
    ejes[1, 0].set_xlabel("U(n)")
    ejes[1, 0].set_ylabel("Frecuencia")

    ejes[1, 1].scatter(
        valores[:-1],
        valores[1:],
        s=2,
        alpha=0.5,
    )
    ejes[1, 1].set_title("Pares consecutivos")
    ejes[1, 1].set_xlabel("U(n)")
    ejes[1, 1].set_ylabel("U(n+1)")
    ejes[1, 1].set_xlim(0, 1)
    ejes[1, 1].set_ylim(0, 1)

    figura.tight_layout(rect=(0, 0, 1, 0.95))

    destino = carpeta_salida / f"{lenguaje}_{semilla}.png"
    figura.savefig(destino, dpi=180)
    plt.close(figura)

    print(f"Gráfica guardada en: {destino}")


def comparar_semillas(
    series: dict[int, list[int]],
    modulo: int,
    carpeta_salida: Path,
) -> None:
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    figura, eje = plt.subplots(figsize=(11, 4))

    for semilla, valores in series.items():
        primeros = valores[:100]

        eje.plot(
            range(1, len(primeros) + 1),
            [x / modulo for x in primeros],
            label=f"Semilla {semilla}",
            linewidth=0.9,
            alpha=0.8,
        )

    eje.set_title("Comparación de semillas: primeros 100 valores")
    eje.set_xlabel("n")
    eje.set_ylabel("U(n)")
    eje.set_ylim(0, 1)
    eje.legend()

    figura.tight_layout()
    destino = carpeta_salida / "comparacion_semillas.png"
    figura.savefig(destino, dpi=180)
    plt.close(figura)

    print(f"Gráfica guardada en: {destino}")