"""Una función: estadístico KS y valor p (aproximación asintótica corregida)."""

from math import sqrt
from scipy.stats import kstwobign


def prueba_ks(numeros: list[float], alfa: float = 0.05) -> dict:
    n = len(numeros)
    if n < 35 or not (0 < alfa < 1):
        raise ValueError("Se requiere N>=35 y 0<alfa<1.")
    ordenados = sorted(numeros)
    d_mas = 0.0
    d_menos = 0.0
    for i, valor in enumerate(ordenados, start=1):
        if not (0.0 <= valor < 1.0):
            raise ValueError("Los valores deben pertenecer a [0,1).")
        d_mas = max(d_mas, i / n - valor)
        d_menos = max(d_menos, valor - (i - 1) / n)
    d = max(d_mas, d_menos)
    lam = (sqrt(n) + 0.12 + 0.11 / sqrt(n)) * d
    p = float(kstwobign.sf(lam))
    return {"d_mas": d_mas, "d_menos": d_menos, "d": d,
            "p": p, "rechazar": p < alfa,
            "d_critico_aprox": 1.36 / sqrt(n)}
