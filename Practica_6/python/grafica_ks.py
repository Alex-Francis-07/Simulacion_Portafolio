"""Una función: dibuja F_n(x) y F(x)=x en PNG, sin interfaz gráfica."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def graficar_ks(numeros: list[float], archivo: Path, titulo: str) -> None:
    ordenados = sorted(numeros)
    n = len(ordenados)
    x = [0.0, *ordenados, 1.0]
    y = [0.0, *(i / n for i in range(1, n + 1)), 1.0]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.step(x, y, where="post", label="F empírica (escalones)", linewidth=1.5)
    ax.plot([0, 1], [0, 1], "--", label="F teórica = x", linewidth=1.4)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Número pseudoaleatorio",
           ylabel="Probabilidad acumulada", title=titulo)
    ax.grid(alpha=0.2)
    ax.legend()
    fig.tight_layout()
    archivo.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(archivo, dpi=140)
    plt.close(fig)
