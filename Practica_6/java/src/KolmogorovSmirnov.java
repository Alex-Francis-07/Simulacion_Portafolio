import java.util.Arrays;

/** Una función: calcula D+, D- y el valor p aproximado de KS. */
public final class KolmogorovSmirnov {
    public static ResultadoKS calcular(double[] numeros, double alfa) {
        int n = numeros.length;
        if (n < 35 || alfa <= 0 || alfa >= 1) {
            throw new IllegalArgumentException("Se requiere N>=35 y 0<alfa<1.");
        }
        double[] ordenados = Arrays.copyOf(numeros, n);
        Arrays.sort(ordenados);
        double dMas = 0.0;
        double dMenos = 0.0;
        for (int i = 0; i < n; i++) {
            double valor = ordenados[i];
            if (!(valor >= 0.0 && valor < 1.0)) {
                throw new IllegalArgumentException("Se requieren valores en [0,1).");
            }
            dMas = Math.max(dMas, (i + 1.0) / n - valor);
            dMenos = Math.max(dMenos, valor - (double) i / n);
        }
        double d = Math.max(dMas, dMenos);
        double raizN = Math.sqrt(n);
        double lambda = (raizN + 0.12 + 0.11 / raizN) * d;
        double p = KsPValor.calcular(lambda);
        return new ResultadoKS(dMas, dMenos, d, p, p < alfa, 1.36 / raizN);
    }
}
