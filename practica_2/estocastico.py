import numpy as np


def simular(p0, r, sigma, tiempo):
    tiempos = list(range(tiempo + 1))
    poblacion = [p0]

    for periodo in range(1, tiempo + 1):
        ruido = np.random.normal(0, sigma)
        actual = poblacion[-1]

        # P(t+1) = P(t) + r * P(t) + ruido
        nueva = actual + r * actual + ruido

        if nueva < 0:
            nueva = 0

        poblacion.append(nueva)

    return tiempos, poblacion