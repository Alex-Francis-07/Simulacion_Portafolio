"""Una función: generar N números pseudoaleatorios LCG en [0, 1)."""


def generar_lcg(n: int, semilla: int, a: int, c: int, m: int) -> list[float]:
    if n <= 0 or m <= 1 or not (0 <= semilla < m) or a < 0 or c < 0:
        raise ValueError("Parámetros inválidos para el LCG.")
    actual = semilla
    numeros = []
    for _ in range(n):
        actual = (a * actual + c) % m
        numeros.append(actual / m)
    return numeros
