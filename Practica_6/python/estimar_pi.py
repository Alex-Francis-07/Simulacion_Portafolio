"""Una función adicional: estima pi con pares consecutivos del LCG."""


def estimar_pi(numeros: list[float]) -> float:
    pares = len(numeros) // 2
    if pares == 0:
        raise ValueError("Se requieren al menos dos números.")
    dentro = 0
    for i in range(0, pares * 2, 2):
        if numeros[i] ** 2 + numeros[i + 1] ** 2 <= 1.0:
            dentro += 1
    return 4.0 * dentro / pares
