package practica.modelo;

public final class GeneradorLCG {

    private final long a;
    private final long c;
    private final long m;
    private final long semilla;

    public GeneradorLCG(
            long a,
            long c,
            long m,
            long semilla
    ) {
        if (m <= 1) {
            throw new IllegalArgumentException(
                    "El modulo m debe ser mayor que 1."
            );
        }

        if (a < 0 || a >= m) {
            throw new IllegalArgumentException(
                    "a debe cumplir: 0 <= a < m."
            );
        }

        if (c < 0 || c >= m) {
            throw new IllegalArgumentException(
                    "c debe cumplir: 0 <= c < m."
            );
        }

        if (semilla < 0 || semilla >= m) {
            throw new IllegalArgumentException(
                    "La semilla debe cumplir: 0 <= semilla < m."
            );
        }

        this.a = a;
        this.c = c;
        this.m = m;
        this.semilla = semilla;
    }

    public long[] generar(int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException(
                    "La cantidad debe ser positiva."
            );
        }

        long[] valores = new long[cantidad];

        // Cada llamada comienza nuevamente desde X0.
        long x = semilla;

        for (int i = 0; i < cantidad; i++) {
            long producto = Math.multiplyExact(a, x);
            long suma = Math.addExact(producto, c);

            x = suma % m;
            valores[i] = x;
        }

        return valores;
    }
}