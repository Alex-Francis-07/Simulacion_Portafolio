"""Una función: prueba Chi-cuadrado de uniformidad con k intervalos."""

from scipy.stats import chi2


def prueba_chi_cuadrado(numeros: list[float], k: int = 10, alfa: float = 0.05) -> dict:
    n = len(numeros)
    if not (0 < alfa < 1) or k < 2 or n / k < 5:
        raise ValueError("Se requiere 0<alfa<1, k>=2 y frecuencia esperada N/k>=5.")
    observadas = [0] * k
    for valor in numeros:
        if not (0.0 <= valor < 1.0):
            raise ValueError("Los valores del LCG deben estar en [0,1).")
        observadas[min(int(valor * k), k - 1)] += 1
    esperada = n / k
    estadistico = sum((frecuencia - esperada) ** 2 / esperada for frecuencia in observadas)
    gl = k - 1
    p = float(chi2.sf(estadistico, gl))
    return {"frecuencias": observadas, "esperada": esperada,
            "estadistico": estadistico, "gl": gl, "p": p, "rechazar": p < alfa}
