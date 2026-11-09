import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

/** Punto de entrada Java. Su única función coordina toda la práctica. */
public final class Main {
    public static void main(String[] args) throws Exception {
        Locale.setDefault(Locale.ROOT);
        System.setProperty("java.awt.headless", "true");
        if (args.length > 1) {
            throw new IllegalArgumentException("Uso: java -cp java/bin Main [N]");
        }
        int[] tamanos = args.length == 1
                ? new int[]{Integer.parseInt(args[0])}
                : new int[]{1000, 10000, 100000, 1000000};
        final int k = 10;
        final double alfa = 0.05;
        Config[] configuraciones = {
            new Config("glibc", 1103515245L, 12345L, 4294967296L, 1L),
            new Config("numerical_recipes", 1664525L, 1013904223L, 4294967296L, 42L)
        };
        Path salida = Path.of("resultados", "java");
        List<FilaResumen> filas = new ArrayList<>();
        System.out.println("JAVA: LCG + Chi-cuadrado + KS + rachas + estimacion de pi");
        for (Config config : configuraciones) {
            for (int n : tamanos) {
                long inicio = System.nanoTime(); // Excluye CSV y gráficas.
                double[] numeros = LCG.generar(n, config);
                ResultadoChi chi = ChiCuadrado.calcular(numeros, k, alfa);
                ResultadoKS ks = KolmogorovSmirnov.calcular(numeros, alfa);
                ResultadoRachas rachas = Rachas.calcular(numeros, alfa);
                double piEstimado = EstimarPi.calcular(numeros);
                double segundos = (System.nanoTime() - inicio) / 1_000_000_000.0;
                filas.add(new FilaResumen(config.nombre(), n, piEstimado,
                    Math.abs(piEstimado - Math.PI), segundos, chi.estadistico(),
                    chi.gl(), chi.p(), chi.rechazar(), ks.d(), ks.dMas(),
                    ks.dMenos(), ks.p(), ks.rechazar(), rachas.rachas(),
                    rachas.z(), rachas.p(), rachas.rechazar()));
                System.out.printf(Locale.ROOT,
                    "%-18s N=%7d chi2=%9.4f p(chi)=%.6f D=%.6f p(KS)=%.6f p(rachas)=%.6f tiempo=%.3fs%n",
                    config.nombre(), n, chi.estadistico(), chi.p(), ks.d(),
                    ks.p(), rachas.p(), segundos);
                if (n == 10000 || tamanos.length == 1) {
                    GuardarSecuencia.guardar(numeros,
                        salida.resolve("secuencia_" + config.nombre() + "_N" + n + ".csv"));
                    GraficaKS.guardar(numeros,
                        salida.resolve("ks_" + config.nombre() + "_N" + n + ".png"),
                        "KS | " + config.nombre() + " | N=" + n);
                    System.out.printf("  Frecuencias observadas: %s | esperada: %.1f%n",
                        Arrays.toString(chi.frecuencias()), chi.esperada());
                    System.out.printf("  Decisiones H0: Chi=%s, KS=%s, Rachas=%s%n",
                        chi.rechazar() ? "RECHAZAR" : "NO rechazar",
                        ks.rechazar() ? "RECHAZAR" : "NO rechazar",
                        rachas.rechazar() ? "RECHAZAR" : "NO rechazar");
                }
            }
        }
        GuardarResumen.guardar(filas, salida.resolve("resumen.csv"));
        System.out.println("Resultados guardados en: " + salida.toAbsolutePath());
    }
}
