package practica;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;

import practica.modelo.GeneradorLCG;
import practica.servicio.ServicioLCG;

public final class Main {

    private static final long A = 1664525L;
    private static final long C = 1013904223L;

    // En Java, ^ representa XOR, no potenciacion.
    private static final long M = 1L << 32;

    private static final int CANTIDAD = 10000;

    private static final long[] SEMILLAS = {
        12345L,
        54321L
    };

    public static void main(String[] args) throws IOException {

        Path carpetaSalida = Path.of(
                args.length > 0
                        ? args[0]
                        : "resultados/java"
        );

        long[] primeraSecuencia = null;

        for (long semilla : SEMILLAS) {
            GeneradorLCG generador = new GeneradorLCG(
                    A, C, M, semilla
            );

            long[] valores = generador.generar(CANTIDAD);

            if (!Arrays.equals(
                    valores,
                    generador.generar(CANTIDAD)
            )) {
                throw new IllegalStateException(
                        "La misma semilla no reprodujo la secuencia."
                );
            }

            ServicioLCG.mostrarPrimeros(valores, M);

            ServicioLCG.analizar(
                    A, C, M, semilla, valores
            );

            Path archivo = carpetaSalida.resolve(
                    "lcg_" + semilla + ".csv"
            );

            ServicioLCG.exportarCSV(
                    archivo, valores, M
            );

            System.out.println(
                    "CSV guardado en: "
                    + archivo.toAbsolutePath()
            );

            if (primeraSecuencia == null) {
                primeraSecuencia = valores;
            } else {
                int coincidencias = 0;

                for (int i = 0; i < CANTIDAD; i++) {
                    if (primeraSecuencia[i] == valores[i]) {
                        coincidencias++;
                    }
                }

                System.out.println(
                        "\nCoincidencias entre semillas "
                        + "en la misma posicion: "
                        + coincidencias
                        + "/"
                        + CANTIDAD
                );
            }
        }
    }
}