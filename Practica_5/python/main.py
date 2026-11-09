from pathlib import Path

from graficas import comparar_semillas, graficar_archivo
from modelo import GeneradorLCG, ParametrosLCG
from servicios import analizar, comparar, exportar_csv


A = 1664525
C = 1013904223
M = 2**32
CANTIDAD = 10000
SEMILLAS = (12345, 54321)

RAIZ = Path(__file__).resolve().parents[1]
RESULTADOS = RAIZ / "resultados"


def main() -> None:
    series = {}

    for semilla in SEMILLAS:
        parametros = ParametrosLCG(A, C, M, semilla)
        generador = GeneradorLCG(parametros)
        valores = generador.generar(CANTIDAD)

        # Comprobación de reproducibilidad.
        if valores != generador.generar(CANTIDAD):
            raise AssertionError(
                "La misma semilla no reprodujo la secuencia."
            )

        series[semilla] = valores

        ruta_python = (
            RESULTADOS / "python" / f"lcg_{semilla}.csv"
        )
        ruta_java = (
            RESULTADOS / "java" / f"lcg_{semilla}.csv"
        )

        exportar_csv(ruta_python, valores, M)
        analizar(parametros, valores)

        graficar_archivo(
            ruta_python,
            RESULTADOS / "graficas",
            "python",
            semilla,
        )

        if ruta_java.exists():
            comparar(
                ruta_python,
                ruta_java,
                RESULTADOS
                / "comparaciones"
                / f"comparacion_{semilla}.csv",
                CANTIDAD,
            )

            graficar_archivo(
                ruta_java,
                RESULTADOS / "graficas",
                "java",
                semilla,
            )
        else:
            print(
                f"\nFalta el CSV de Java para la semilla {semilla}."
                "\nEjecuta Java y después vuelve a ejecutar Python "
                "para completar la comparación."
            )

    comparar_semillas(
        series,
        M,
        RESULTADOS / "graficas",
    )

    primera, segunda = SEMILLAS
    coincidencias = sum(
        x == y
        for x, y in zip(series[primera], series[segunda])
    )

    print(
        "\nCoincidencias entre las dos semillas "
        f"en la misma posición: {coincidencias}/{CANTIDAD}"
    )


if __name__ == "__main__":
    main()