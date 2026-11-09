"""Parámetros reproducibles usados en ambos lenguajes."""

ALFA = 0.05
INTERVALOS = 10
TAMANOS = (1000, 10000, 100000, 1000000)
CONFIGURACIONES = {
    "glibc": {"a": 1103515245, "c": 12345, "m": 2**32, "semilla": 1},
    "numerical_recipes": {"a": 1664525, "c": 1013904223, "m": 2**32, "semilla": 42},
}
