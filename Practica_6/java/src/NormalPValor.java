/** Una función: valor p bilateral de una normal estándar (aprox. 1e-7). */
public final class NormalPValor {
    public static double bilateral(double z) {
        double x = Math.abs(z);
        double t = 1.0 / (1.0 + 0.2316419 * x);
        double polinomio = t * (0.319381530 + t * (-0.356563782 + t *
                (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
        double cola = Math.exp(-x * x / 2.0) / Math.sqrt(2.0 * Math.PI) * polinomio;
        return Math.max(0.0, Math.min(1.0, 2.0 * cola));
    }
}
