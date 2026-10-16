def simular(p0, r, tiempo):
    tiempos = list(range(tiempo + 1))
    poblacion = [p0]

    for periodo in range(1, tiempo + 1):
        actual = poblacion[-1]
        incremento = r * actual

        # P(t+1) = P(t) + r * P(t)
        nueva = actual + incremento
        poblacion.append(nueva)

    return tiempos, poblacion