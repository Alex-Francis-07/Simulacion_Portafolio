import matplotlib.pyplot as plt

import deterministico
import discreto
import estocastico
import continuo


def comparar(p0, r, sigma, dt, tiempo):
    # Ejecutar cada modelo y guardar sus resultados.
    t_deterministico, p_deterministico = deterministico.simular(
        p0, r, tiempo
    )

    t_discreto, p_discreto = discreto.simular(
        p0, r, tiempo
    )

    t_estocastico, p_estocastico = estocastico.simular(
        p0, r, sigma, tiempo
    )

    t_continuo, p_continuo = continuo.simular(
        p0, r, tiempo, dt
    )

    # Crear la gráfica comparativa.
    plt.figure(figsize=(10, 6))

    plt.plot(
        t_deterministico, p_deterministico,
        label="Determinístico", color="blue"
    )

    plt.step(
        t_discreto, p_discreto,
        where="post", label="Discreto", color="orange"
    )

    plt.plot(
        t_estocastico, p_estocastico,
        "o--", label="Estocástico", color="green"
    )

    plt.plot(
        t_continuo, p_continuo,
        label="Continuo (Euler)", color="red", linestyle="--"
    )

    plt.title(f"Comparación de los cuatro modelos | r = {r}")
    plt.xlabel("Tiempo (períodos)")
    plt.ylabel("Población")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    print("\nPoblación final de cada modelo:")
    print(f"Determinístico: {p_deterministico[-1]:.2f}")
    print(f"Discreto: {p_discreto[-1]:.2f}")
    print(f"Estocástico: {p_estocastico[-1]:.2f}")
    print(f"Continuo: {p_continuo[-1]:.2f}")

    plt.show()