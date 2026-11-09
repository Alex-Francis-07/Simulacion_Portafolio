/** Una función auxiliar: ln(Gamma(z)) por aproximación de Lanczos. */
public final class GammaLog {
    public static double calcular(double z) {
        if (z < 0.5) {
            throw new IllegalArgumentException("GammaLog requiere z >= 0.5.");
        }
        double[] coef = {
            0.99999999999980993, 676.5203681218851, -1259.1392167224028,
            771.32342877765313, -176.61502916214059, 12.507343278686905,
            -0.13857109526572012, 9.984369578019572e-6, 1.5056327351493116e-7
        };
        double y = z - 1.0;
        double suma = coef[0];
        for (int i = 1; i < coef.length; i++) {
            suma += coef[i] / (y + i);
        }
        double t = y + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (y + 0.5) * Math.log(t) - t + Math.log(suma);
    }
}
