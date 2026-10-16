from abc import ABC, abstractmethod
import numpy as np

# Patrón Strategy: Interfaces y clases de estrategias
class ModeloSimulacionStrategy(ABC):
    @abstractmethod
    def calcular_indice(self, H: float, N: float, Tf: float) -> float:
        pass

class ModeloBaseStrategy(ModeloSimulacionStrategy):
    def calcular_indice(self, H: float, N: float, Tf: float) -> float:
        return 0.5 * H + 0.3 * N + 0.2 * Tf

class ModeloAjustadoStrategy(ModeloSimulacionStrategy):
    def calcular_indice(self, H: float, N: float, Tf: float) -> float:
        return 0.55 * H + 0.35 * N + 0.10 * Tf


# Clase Principal del Simulador
class SimuladorAtmosferico:
    def __init__(self, estrategia: ModeloSimulacionStrategy):
        self._estrategia = estrategia

    def set_estrategia(self, estrategia: ModeloSimulacionStrategy):
        self._estrategia = estrategia

    @staticmethod
    def obtener_tf(temp: float) -> float:
        if temp <= 10: return 1.00
        if temp >= 28: return 0.10
        return round(1.0 - (temp - 10) * 0.05, 2)

    @staticmethod
    def clasificar_estado(indice: float) -> str:
        if indice < 0.40:
            return "Sin lluvia"
        elif indice < 0.60:
            return "Baja posibilidad"
        elif indice < 0.75:
            return "Lluvia probable"
        else:
            return "Lluvia"

    def ejecutar(self, horas, humedades, nubosidades, temperaturas):
        indices = []
        estados = []
        for h, n, t in zip(humedades, nubosidades, temperaturas):
            H_norm = h / 100.0
            N_norm = n / 100.0
            Tf = self.obtener_tf(t)
            
            I = self._estrategia.calcular_indice(H_norm, N_norm, Tf)
            estado = self.clasificar_estado(I)
            
            indices.append(I)
            estados.append(estado)
        return np.array(indices), estados