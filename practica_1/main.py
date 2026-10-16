import matplotlib.pyplot as plt
from modelos import ModeloBaseStrategy, ModeloAjustadoStrategy, SimuladorAtmosferico

if __name__ == "__main__":
    # Datos de entrada
    horas = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]
    humedad = [65, 70, 68, 60, 75, 85, 92, 88, 80]
    nubosidad = [40, 50, 45, 30, 70, 85, 95, 90, 75]
    temperatura = [14, 16, 18, 22, 20, 18, 16, 17, 15]

    # Ejecución del Modelo Base
    simulador = SimuladorAtmosferico(ModeloBaseStrategy())
    indices_base, estados_base = simulador.ejecutar(horas, humedad, nubosidad, temperatura)

    # Ejecución del Modelo Ajustado
    simulador.set_estrategia(ModeloAjustadoStrategy())
    indices_ajustados, estados_ajustados = simulador.ejecutar(horas, humedad, nubosidad, temperatura)

    # Imprimir consola
    print("\n--- RESULTADOS MODELO BASE ---")
    for h, i, est in zip(horas, indices_base, estados_base):
        print(f"Hora: {h} | Índice: {i:.3f} | Estado: {est}")

    print("\n--- RESULTADOS MODELO AJUSTADO ---")
    for h, i, est in zip(horas, indices_ajustados, estados_ajustados):
        print(f"Hora: {h} | Índice: {i:.3f} | Estado: {est}")

    # Gráfica para las practicas
    plt.figure(figsize=(10, 5))
    plt.plot(horas, indices_base, label="Modelo Base")
    plt.plot(horas, indices_ajustados, label="Modelo Ajustado")
    plt.axhline(
        y=0.75,
        linestyle="--",
        label="Umbral de lluvia"
    )
    plt.xlabel("Hora del día")
    plt.ylabel("Índice de lluvia")
    plt.title("Simulación de posibilidad de lluvia")
    plt.grid(True)
    plt.legend()

    plt.savefig("grafico_simulacion.png")
    plt.show()