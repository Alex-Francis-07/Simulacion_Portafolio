"""Punto de entrada Python. Su única función coordina la práctica completa."""

from math import pi
from pathlib import Path
from time import perf_counter
import sys

from configuraciones import ALFA, INTERVALOS, TAMANOS, CONFIGURACIONES
from lcg import generar_lcg
from chi_cuadrado import prueba_chi_cuadrado
from kolmogorov_smirnov import prueba_ks
from rachas import prueba_rachas
from estimar_pi import estimar_pi
from grafica_ks import graficar_ks
from guardar_secuencia import guardar_secuencia
from guardar_resumen import guardar_resumen


def main() -> None:
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and not sys.argv[1].isdigit()):
        raise SystemExit("Uso: python python/main.py [N] (sin N prueba los cuatro tamaños)")
    tamanos = (int(sys.argv[1]),) if len(sys.argv) == 2 else TAMANOS
    salida = Path(__file__).resolve().parent.parent / "resultados" / "python"
    salida.mkdir(parents=True, exist_ok=True)
    filas = []
    print("PYTHON: LCG + Chi-cuadrado + KS + rachas + estimación de pi")
    for nombre, parametros in CONFIGURACIONES.items():
        for n in tamanos:
            inicio = perf_counter()  # No incluye escribir CSV ni crear gráficos.
            numeros = generar_lcg(n, **parametros)
            chi = prueba_chi_cuadrado(numeros, INTERVALOS, ALFA)
            ks = prueba_ks(numeros, ALFA)
            rachas = prueba_rachas(numeros, ALFA)
            pi_estimado = estimar_pi(numeros)
            segundos = perf_counter() - inicio
            filas.append({
                "configuracion": nombre, "N": n,
                "pi_estimado": pi_estimado, "error_pi_absoluto": abs(pi_estimado - pi),
                "tiempo_segundos": segundos,
                "chi2": chi["estadistico"], "chi2_gl": chi["gl"],
                "chi2_p": chi["p"], "chi2_rechazar": chi["rechazar"],
                "ks_d": ks["d"], "ks_d_mas": ks["d_mas"],
                "ks_d_menos": ks["d_menos"], "ks_p": ks["p"],
                "ks_rechazar": ks["rechazar"], "rachas_r": rachas["rachas"],
                "rachas_z": rachas["z"], "rachas_p": rachas["p"],
                "rachas_rechazar": rachas["rechazar"],
            })
            print(f"{nombre:18} N={n:>7} chi²={chi['estadistico']:>9.4f} "
                  f"p(chi)={chi['p']:.6f} D={ks['d']:.6f} p(KS)={ks['p']:.6f} "
                  f"p(rachas)={rachas['p']:.6f} tiempo={segundos:.3f}s")
            # Generar evidencias completas solo para N=10_000 o cuando se pide uno.
            if n == 10000 or len(tamanos) == 1:
                guardar_secuencia(numeros, salida / f"secuencia_{nombre}_N{n}.csv")
                graficar_ks(numeros, salida / f"ks_{nombre}_N{n}.png", f"KS | {nombre} | N={n}")
                print(f"  Frecuencias observadas: {chi['frecuencias']} | esperada: {chi['esperada']:.1f}")
                print(f"  Decisiones H0: Chi={'RECHAZAR' if chi['rechazar'] else 'NO rechazar'}, "
                      f"KS={'RECHAZAR' if ks['rechazar'] else 'NO rechazar'}, "
                      f"Rachas={'RECHAZAR' if rachas['rechazar'] else 'NO rechazar'}")
    guardar_resumen(filas, salida / "resumen.csv")
    print(f"Resultados guardados en: {salida}")


if __name__ == "__main__":
    main()
