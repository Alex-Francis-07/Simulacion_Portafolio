import matplotlib.pyplot as plt

import estocastico
import deterministico
import discreto
import continuo
import comparacion


def mostrar_grafica(tiempos, poblacion, nombre, r):
    plt.figure(figsize=(8, 5))

    if nombre == "Discreto":
        plt.step(
            tiempos, poblacion,
            where="post", label=nombre, color="blue"
        )
        plt.plot(tiempos, poblacion, "o", color="blue")

    elif nombre == "Estocástico":
        plt.plot(tiempos, poblacion, "o--", label=nombre)

    else:
        plt.plot(tiempos, poblacion, label=nombre)

    plt.title(f"Modelo {nombre} | r = {r}")
    plt.xlabel("Tiempo (períodos)")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    print(f"Población inicial: {poblacion[0]:.2f}")
    print(f"Población final: {poblacion[-1]:.2f}")

    plt.show()


def main():
    # Datos indicados en el documento.
    datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

    p0 = datos[0]
    tiempo = len(datos) - 1

    # Parámetros de ejemplo que puedes modificar.
    sigma = 50
    dt = 0.1

    while True:
        print("\n--- MENÚ DE SIMULACIÓN ---")
        print("1. Modelo estocástico")
        print("2. Modelo determinístico")
        print("3. Modelo discreto")
        print("4. Modelo continuo mediante Euler")
        print("5. Comparar los cuatro modelos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "6":
            print("Programa terminado.")
            break

        if opcion not in ["1", "2", "3", "4", "5"]:
            print("Error: ingrese una opción del 1 al 6.")
            continue

        print("\nEjemplos de tasa:")
        print("0.12 para crecimiento.")
        print("-0.12 para decrecimiento.")

        try:
            r = float(input("Ingrese la tasa r: "))
        except ValueError:
            print("Error: ingrese un número utilizando punto decimal.")
            continue

        if opcion == "5":
            comparacion.comparar(p0, r, sigma, dt, tiempo)
            continue

        if opcion == "1":
            tiempos, poblacion = estocastico.simular(
                p0, r, sigma, tiempo
            )
            nombre = "Estocástico"

        elif opcion == "2":
            tiempos, poblacion = deterministico.simular(
                p0, r, tiempo
            )
            nombre = "Determinístico"

        elif opcion == "3":
            tiempos, poblacion = discreto.simular(
                p0, r, tiempo
            )
            nombre = "Discreto"

        elif opcion == "4":
            tiempos, poblacion = continuo.simular(
                p0, r, tiempo, dt
            )
            nombre = "Continuo (Euler)"

        mostrar_grafica(tiempos, poblacion, nombre, r)


if __name__ == "__main__":
    main()