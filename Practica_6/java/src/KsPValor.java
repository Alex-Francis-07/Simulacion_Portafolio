/** Una función: supervivencia de Kolmogorov asintótica con corrección de N. */
public final class KsPValor {
    public static double calcular(double lambda) {
        if (lambda <= 0.0) return 1.0;
        double p;
        if (lambda <= 0.9) {
            // Fórmula dual, evita cancelación cerca de lambda=0.
            double suma = 0.0;
            for (int j = 1; j <= 1000; j++) {
                double b = (2.0 * j - 1.0);
                double termino = Math.exp(-b * b * Math.PI * Math.PI / (8.0 * lambda * lambda));
                suma += termino;
                if (termino < 1e-15) break;
            }
            p = 1.0 - Math.sqrt(2.0 * Math.PI) / lambda * suma;
        } else {
            // Serie alternada de la cola de Kolmogorov.
            double suma = 0.0;
            for (int j = 1; j <= 1000; j++) {
                double termino = Math.exp(-2.0 * j * j * lambda * lambda);
                suma += (j % 2 == 1 ? 1.0 : -1.0) * termino;
                if (termino < 1e-15) break;
            }
            p = 2.0 * suma;
        }
        return Math.max(0.0, Math.min(1.0, p));
    }
}
