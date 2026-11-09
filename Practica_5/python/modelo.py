from dataclasses import dataclass


@dataclass(frozen=True)
class ParametrosLCG:
    a: int
    c: int
    m: int
    semilla: int

    def __post_init__(self):
        valores = (self.a, self.c, self.m, self.semilla)

        if any(type(valor) is not int for valor in valores):
            raise ValueError("Todos los parámetros deben ser enteros.")

        if self.m <= 1:
            raise ValueError("El módulo m debe ser mayor que 1.")

        if not 0 <= self.a < self.m:
            raise ValueError("a debe cumplir: 0 <= a < m.")

        if not 0 <= self.c < self.m:
            raise ValueError("c debe cumplir: 0 <= c < m.")

        if not 0 <= self.semilla < self.m:
            raise ValueError("La semilla debe cumplir: 0 <= semilla < m.")


class GeneradorLCG:
    def __init__(self, parametros: ParametrosLCG):
        self.parametros = parametros

    def generar(self, cantidad: int) -> list[int]:
        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

        # Cada llamada comienza nuevamente desde X0.
        x = self.parametros.semilla
        secuencia = []

        for _ in range(cantidad):
            x = (
                self.parametros.a * x + self.parametros.c
            ) % self.parametros.m

            secuencia.append(x)

        return secuencia