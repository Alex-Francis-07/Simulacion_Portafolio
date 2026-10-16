def simular(p0, r, tiempo, dt):
    tiempos = [0]
    poblacion = [p0]

    while tiempos[-1] < tiempo:
        actual = poblacion[-1]

        # Acortar el último paso para terminar en el tiempo indicado.
        paso = min(dt, tiempo - tiempos[-1])

        # Euler: P(t+dt) = P(t) + dt * (r * P(t))
        cambio = r * actual
        nueva = actual + paso * cambio

        nuevo_tiempo = min(tiempo, tiempos[-1] + paso)

        tiempos.append(nuevo_tiempo)
        poblacion.append(nueva)

    return tiempos, poblacion