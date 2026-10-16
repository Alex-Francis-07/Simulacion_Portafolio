import numpy as np


def simular(p0, r, tiempo):
    tiempos = np.linspace(0, tiempo, 100)
    poblacion = []

    for t in tiempos:
        # P(t) = P0 * e^(r*t)
        p = p0 * np.exp(r * t)
        poblacion.append(p)

    return tiempos, poblacion