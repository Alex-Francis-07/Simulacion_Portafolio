import java.nio.file.Files;
import java.nio.file.Path;
import java.io.BufferedWriter;
import java.io.IOException;
import java.util.Locale;

/** Una función: exporta cada número del LCG a CSV. */
public final class GuardarSecuencia {
    public static void guardar(double[] numeros, Path archivo) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (BufferedWriter salida = Files.newBufferedWriter(archivo)) {
            salida.write("indice,valor\n");
            for (int i = 0; i < numeros.length; i++) {
                salida.write(String.format(Locale.ROOT, "%d,%.17g%n", i + 1, numeros[i]));
            }
        }
    }
}
