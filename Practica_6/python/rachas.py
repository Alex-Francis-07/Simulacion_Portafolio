"""Una función: prueba bilateral de rachas respecto a la mediana."""

from math import sqrt
from scipy.stats import norm


def prueba_rachas(numeros: list[float], alfa: float = 0.05) -> dict:
    n = len(numeros)
    if n < 3 or not (0 < alfa < 1):
        raise ValueError("Muestra demasiado pequeña o alfa inválido.")
    ordenados = sorted(numeros)
    mediana = ordenados[n // 2] if n % 2 else (ordenados[n // 2 - 1] + ordenados[n // 2]) / 2
    anterior = 0
    rachas = 0
    n1 = n2 = 0
    for valor in numeros:
        signo = (1 if valor > mediana else -1 if valor < mediana else 0)
        if signo == 0:  # Empates con la mediana excluidos explícitamente.
            continue
        if signo == 1:
            n1 += 1
        else:
            n2 += 1
        if signo != anterior:
            rachas += 1
            anterior = signo
    total = n1 + n2
    if n1 == 0 or n2 == 0 or total < 3:
        raise ValueError("No existen suficientes observaciones a ambos lados de la mediana.")
    media = 1 + 2 * n1 * n2 / total
    varianza = (2 * n1 * n2 * (2 * n1 * n2 - total)) / (total**2 * (total - 1))
    z = (rachas - media) / sqrt(varianza)
    p = float(2 * norm.sf(abs(z)))
    return {"rachas": rachas, "arriba": n1, "abajo": n2,
            "mediana": mediana, "z": z, "p": p, "rechazar": p < alfa}
