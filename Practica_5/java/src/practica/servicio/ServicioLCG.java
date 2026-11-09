package practica.servicio;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public final class ServicioLCG {

    private ServicioLCG() {
    }

    public static void exportarCSV(
            Path ruta,
            long[] valores,
            long modulo
    ) throws IOException {

        Path padre = ruta.toAbsolutePath().getParent();
        Files.createDirectories(padre);

        try (BufferedWriter escritor = Files.newBufferedWriter(
                ruta,
                StandardCharsets.UTF_8
        )) {
            escritor.write("n,x,u");
            escritor.newLine();

            for (int i = 0; i < valores.length; i++) {
                double u = valores[i] / (double) modulo;

                escritor.write(
                        (i + 1)
                        + ","
                        + valores[i]
                        + ","
                        + Double.toString(u)
                );

                escritor.newLine();
            }
        }
    }

    public static void mostrarPrimeros(
            long[] valores,
            long modulo
    ) {
        System.out.println("\nPRIMERAS 20 OBSERVACIONES");

        System.out.printf(
                "%3s %12s %14s%n",
                "n", "X(n)", "U(n)"
        );

        int limite = Math.min(20, valores.length);

        for (int i = 0; i < limite; i++) {
            double u = valores[i] / (double) modulo;

            System.out.printf(
                    Locale.ROOT,
                    "%3d %12d %14.10f%n",
                    i + 1,
                    valores[i],
                    u
            );
        }
    }

    public static void analizar(
            long a,
            long c,
            long m,
            long semilla,
            long[] valores
    ) {
        double suma = 0.0;
        double minimo = Double.POSITIVE_INFINITY;
        double maximo = Double.NEGATIVE_INFINITY;

        for (long x : valores) {
            double u = x / (double) m;

            suma += u;
            minimo = Math.min(minimo, u);
            maximo = Math.max(maximo, u);
        }

        System.out.println("\nSemilla: " + semilla);
        System.out.println("Cantidad: " + valores.length);

        System.out.printf(
                Locale.ROOT,
                "Media de U: %.10f%n",
                suma / valores.length
        );

        System.out.printf(
                Locale.ROOT,
                "Minimo de U: %.10f%n",
                minimo
        );

        System.out.printf(
                Locale.ROOT,
                "Maximo de U: %.10f%n",
                maximo
        );

        Map<Long, Integer> posiciones = new HashMap<>();
        posiciones.put(semilla, 0);

        boolean repetido = false;

        for (int i = 0; i < valores.length; i++) {
            int paso = i + 1;

            Integer anterior = posiciones.putIfAbsent(
                    valores[i], paso
            );

            if (anterior != null) {
                System.out.println(
                        "Primera repeticion en el paso "
                        + paso
                        + "; longitud del ciclo detectado: "
                        + (paso - anterior)
                );

                repetido = true;
                break;
            }
        }

        if (!repetido) {
            System.out.println(
                    "Observacion: no se repitieron estados "
                    + "en los pasos evaluados."
            );
        }

        // Hull-Dobell para m = 2^k, con k >= 2.
        boolean potenciaDeDos =
                m >= 4 && (m & (m - 1)) == 0;

        if (potenciaDeDos) {
            boolean cImpar = c % 2 == 1;
            boolean condicionA = (a - 1) % 4 == 0;

            System.out.println(
                    "Condicion c impar: " + cImpar
            );

            System.out.println(
                    "Condicion (a - 1) divisible por 4: "
                    + condicionA
            );

            if (cImpar && condicionA) {
                System.out.println(
                        "Periodo teorico completo: " + m
                );
            } else {
                System.out.println(
                        "Los parametros no tienen "
                        + "periodo completo m."
                );
            }
        } else {
            System.out.println(
                    "El analisis teorico implementado "
                    + "se aplica a modulos 2^k, con k >= 2."
            );
        }
    }
}