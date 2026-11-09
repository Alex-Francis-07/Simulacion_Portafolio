"""Una función: verifica resultados Python/Java y genera tablas comparativas."""

import csv
from pathlib import Path


def comparar() -> None:
    raiz = Path(__file__).resolve().parent.parent
    resumenes = {}
    for lenguaje in ("python", "java"):
        archivo = raiz / "resultados" / lenguaje / "resumen.csv"
        if not archivo.exists():
            raise SystemExit(f"Falta {archivo}. Ejecuta primero ambos programas.")
        with archivo.open(newline="", encoding="utf-8") as f:
            resumenes[lenguaje] = {(r["configuracion"], int(r["N"])): r
                                    for r in csv.DictReader(f)}
    if resumenes["python"].keys() != resumenes["java"].keys():
        raise AssertionError("Python y Java no tienen las mismas configuraciones y tamaños N.")
    columnas = ("pi_estimado", "error_pi_absoluto", "chi2", "chi2_gl",
                "chi2_p", "ks_d", "ks_d_mas", "ks_d_menos", "ks_p",
                "rachas_r", "rachas_z", "rachas_p")
    comparadas = []
    for clave in sorted(resumenes["python"]):
        py, ja = resumenes["python"][clave], resumenes["java"][clave]
        for columna in columnas:
            if abs(float(py[columna]) - float(ja[columna])) > 1e-5:
                raise AssertionError(f"Resultado diferente para {clave}, columna {columna}: "
                                     f"Python={py[columna]}, Java={ja[columna]}")
        for columna in ("chi2_rechazar", "ks_rechazar", "rachas_rechazar"):
            if py[columna].lower() != ja[columna].lower():
                raise AssertionError(f"Decisión diferente para {clave}: {columna}")
        comparadas.append({
            "configuracion": clave[0], "N": clave[1],
            "pi_estimado": py["pi_estimado"], "error_pi_absoluto": py["error_pi_absoluto"],
            "tiempo_python_s": py["tiempo_segundos"],
            "tiempo_java_s": ja["tiempo_segundos"],
            "chi2": py["chi2"], "p_chi2": py["chi2_p"],
            "D_KS": py["ks_d"], "p_KS": py["ks_p"],
            "Z_rachas": py["rachas_z"], "p_rachas": py["rachas_p"],
            "estadisticos_coinciden": "SI",
        })
        print(f"VALIDADO {clave[0]:18} N={clave[1]:>7} (tolerancia 1e-5)")
    salida = raiz / "resultados" / "tabla_comparativa.csv"
    with salida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(comparadas[0]))
        escritor.writeheader()
        escritor.writerows(comparadas)
    primeras = raiz / "resultados" / "comparacion_primeros_20.csv"
    with primeras.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(("configuracion", "N", "indice", "python", "java", "son_iguales"))
        for nombre, n in sorted(resumenes["python"]):
            path_python = raiz / "resultados" / "python" / f"secuencia_{nombre}_N{n}.csv"
            path_java = raiz / "resultados" / "java" / f"secuencia_{nombre}_N{n}.csv"
            if not path_python.exists() and not path_java.exists():
                continue
            if not path_python.exists() or not path_java.exists():
                raise AssertionError(f"Falta un archivo de secuencia para {nombre}, N={n}")
            with path_python.open(newline="", encoding="utf-8") as a, \
                 path_java.open(newline="", encoding="utf-8") as b:
                p_reader, j_reader = csv.DictReader(a), csv.DictReader(b)
                cantidad = 0
                for p, j in zip(p_reader, j_reader):
                    if int(p["indice"]) != int(j["indice"]) or float(p["valor"]) != float(j["valor"]):
                        raise AssertionError(f"Diferencia de secuencias en {nombre} N={n}: {p} vs {j}")
                    if cantidad < 20:
                        escritor.writerow((nombre, n, p["indice"], p["valor"],
                                          j["valor"], "SI"))
                    cantidad += 1
                if cantidad != n or next(p_reader, None) or next(j_reader, None):
                    raise AssertionError(f"Longitud incorrecta en CSV {nombre} N={n}")
                print(f"  Secuencias verificadas: {nombre} N={n}, {cantidad} números idénticos.")
    print(f"Tablas: {salida}\n        {primeras}")


if __name__ == "__main__":
    comparar()
