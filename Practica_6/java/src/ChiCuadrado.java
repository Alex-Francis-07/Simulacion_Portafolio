/** Una función: calcula Chi-cuadrado, frecuencias observadas y p-valor. */
public final class ChiCuadrado {
    public static ResultadoChi calcular(double[] numeros, int k, double alfa) {
        int n = numeros.length;
        if (k < 2 || n / (double) k < 5.0 || alfa <= 0 || alfa >= 1) {
            throw new IllegalArgumentException("Se requiere k>=2, N/k>=5 y 0<alfa<1.");
        }
        int[] observadas = new int[k];
        for (double valor : numeros) {
            if (!(valor >= 0.0 && valor < 1.0)) {
                throw new IllegalArgumentException("Se requieren valores en [0,1).");
            }
            observadas[Math.min((int) (valor * k), k - 1)]++;
        }
        double esperada = n / (double) k;
        double chi = 0.0;
        for (int frecuencia : observadas) {
            chi += (frecuencia - esperada) * (frecuencia - esperada) / esperada;
        }
        int gl = k - 1;
        double p = ChiPValor.calcular(chi, gl);
        return new ResultadoChi(observadas, esperada, chi, gl, p, p < alfa);
    }
}
