/** Una función: supervivencia Chi-cuadrado = Q(gl/2, chi2/2). */
public final class ChiPValor {
    public static double calcular(double chi2, int gl) {
        if (chi2 < 0.0 || gl < 1) {
            throw new IllegalArgumentException("Chi-cuadrado o grados de libertad inválidos.");
        }
        if (chi2 == 0.0) return 1.0;
        double a = gl / 2.0;
        double x = chi2 / 2.0;
        double prefactor = Math.exp(a * Math.log(x) - x - GammaLog.calcular(a));
        double q;
        if (x < a + 1.0) {
            // Serie para P(a,x), luego Q(a,x)=1-P(a,x).
            double suma = 1.0 / a;
            double incremento = suma;
            double ap = a;
            for (int i = 1; i <= 2000; i++) {
                ap += 1.0;
                incremento *= x / ap;
                suma += incremento;
                if (Math.abs(incremento) < Math.abs(suma) * 1e-14) break;
            }
            q = 1.0 - prefactor * suma;
        } else {
            // Fracción continua estable para Q(a,x) (Lentz modificado).
            double b = x + 1.0 - a;
            double c = 1e300;
            double d = 1.0 / b;
            double h = d;
            for (int i = 1; i <= 2000; i++) {
                double an = -i * (i - a);
                b += 2.0;
                d = an * d + b;
                if (Math.abs(d) < 1e-300) d = 1e-300;
                c = b + an / c;
                if (Math.abs(c) < 1e-300) c = 1e-300;
                d = 1.0 / d;
                double delta = d * c;
                h *= delta;
                if (Math.abs(delta - 1.0) < 1e-14) break;
            }
            q = prefactor * h;
        }
        return Math.max(0.0, Math.min(1.0, q));
    }
}
