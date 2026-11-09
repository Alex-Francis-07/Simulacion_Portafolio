import java.util.Arrays;

/** Una función: número de rachas y Z, excluyendo empates con la mediana. */
public final class Rachas {
    public static ResultadoRachas calcular(double[] numeros, double alfa) {
        int n = numeros.length;
        if (n < 3 || alfa <= 0 || alfa >= 1) {
            throw new IllegalArgumentException("Muestra demasiado pequeña o alfa inválido.");
        }
        double[] ordenados = Arrays.copyOf(numeros, n);
        Arrays.sort(ordenados);
        double mediana = n % 2 == 1 ? ordenados[n / 2]
                : (ordenados[n / 2 - 1] + ordenados[n / 2]) / 2.0;
        int previo = 0, rachas = 0, n1 = 0, n2 = 0;
        for (double valor : numeros) {
            int signo = valor > mediana ? 1 : (valor < mediana ? -1 : 0);
            if (signo == 0) continue;
            if (signo > 0) n1++;
            else n2++;
            if (signo != previo) {
                rachas++;
                previo = signo;
            }
        }
        double total = (double) n1 + n2;
        if (n1 == 0 || n2 == 0 || total < 3) {
            throw new IllegalArgumentException("Faltan observaciones a ambos lados de la mediana.");
        }
        double producto = (double) n1 * n2;
        double media = 1.0 + 2.0 * producto / total;
        double varianza = 2.0 * producto * (2.0 * producto - total)
                / (total * total * (total - 1.0));
        double z = (rachas - media) / Math.sqrt(varianza);
        double p = NormalPValor.bilateral(z);
        return new ResultadoRachas(rachas, n1, n2, mediana, z, p, p < alfa);
    }
}
