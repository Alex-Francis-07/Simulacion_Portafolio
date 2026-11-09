import csv
from pathlib import Path
from statistics import fmean

from modelo import ParametrosLCG


def exportar_csv(
    ruta: Path,
    valores: list[int],
    modulo: int,
) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["n", "x", "u"])

        for n, x in enumerate(valores, start=1):
            escritor.writerow([n, x, x / modulo])


def leer_csv(ruta: Path) -> list[tuple[int, int, float]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return [
            (int(fila["n"]), int(fila["x"]), float(fila["u"]))
            for fila in csv.DictReader(archivo)
        ]


def analizar(
    parametros: ParametrosLCG,
    valores: list[int],
) -> None:
    normalizados = [x / parametros.m for x in valores]

    print(f"\nSemilla: {parametros.semilla}")
    print(f"Cantidad: {len(valores)}")
    print(f"Media de U: {fmean(normalizados):.10f}")
    print(f"Mínimo de U: {min(normalizados):.10f}")
    print(f"Máximo de U: {max(normalizados):.10f}")

    # Incluimos X0 para detectar también un retorno a la semilla.
    posiciones = {parametros.semilla: 0}
    repeticion = None

    for n, x in enumerate(valores, start=1):
        if x in posiciones:
            repeticion = (n, n - posiciones[x])
            break

        posiciones[x] = n

    if repeticion is None:
        print(
            "Observación: no se repitieron estados "
            "en los pasos evaluados."
        )
    else:
        paso, periodo = repeticion
        print(
            f"Primera repetición en el paso {paso}; "
            f"longitud del ciclo detectado: {periodo}."
        )

    # Hull-Dobell simplificado para m = 2^k, con k >= 2.
    potencia_de_dos = (
        parametros.m >= 4
        and (parametros.m & (parametros.m - 1)) == 0
    )

    if potencia_de_dos:
        c_impar = parametros.c % 2 == 1
        a_menos_uno_multiplo_de_cuatro = (
            (parametros.a - 1) % 4 == 0
        )

        print(f"Condición c impar: {c_impar}")
        print(
            "Condición (a - 1) divisible por 4: "
            f"{a_menos_uno_multiplo_de_cuatro}"
        )

        if c_impar and a_menos_uno_multiplo_de_cuatro:
            print(f"Período teórico completo: {parametros.m}")
        else:
            print("Los parámetros no tienen período completo m.")
    else:
        print(
            "El análisis teórico implementado se aplica "
            "a módulos 2^k, con k >= 2."
        )


def comparar(
    ruta_python: Path,
    ruta_java: Path,
    ruta_salida: Path,
    cantidad_esperada: int,
) -> None:
    datos_python = leer_csv(ruta_python)
    datos_java = leer_csv(ruta_java)

    if not (
        len(datos_python)
        == len(datos_java)
        == cantidad_esperada
    ):
        raise ValueError(
            "Los archivos no tienen la cantidad esperada de datos."
        )

    diferencias = 0
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with ruta_salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow([
            "n",
            "x_python",
            "x_java",
            "u_python",
            "u_java",
            "coinciden",
        ])

        print("\nCOMPARACIÓN DE LAS PRIMERAS 20 OBSERVACIONES")
        print(
            f"{'n':>3} {'X Python':>12} {'X Java':>12} "
            f"{'U Python':>14} {'U Java':>14} {'Iguales':>8}"
        )

        for esperado, (py, ja) in enumerate(
            zip(datos_python, datos_java), start=1
        ):
            n_py, x_py, u_py = py
            n_ja, x_ja, u_ja = ja

            iguales = (
                n_py == n_ja == esperado
                and x_py == x_ja
                and u_py == u_ja
            )

            if not iguales:
                diferencias += 1

            escritor.writerow([
                esperado, x_py, x_ja, u_py, u_ja, iguales
            ])

            if esperado <= 20:
                print(
                    f"{esperado:>3} {x_py:>12} {x_ja:>12} "
                    f"{u_py:>14.10f} {u_ja:>14.10f} "
                    f"{str(iguales):>8}"
                )

    print(
        f"\nComparación completa: "
        f"{cantidad_esperada - diferencias}/{cantidad_esperada} "
        "observaciones iguales."
    )
    print(f"Tabla guardada en: {ruta_salida}")

    if diferencias:
        raise ValueError(
            f"Se encontraron {diferencias} diferencias."
        )