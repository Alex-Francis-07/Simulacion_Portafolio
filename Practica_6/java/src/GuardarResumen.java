import java.nio.file.Files;
import java.nio.file.Path;
import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;
import java.util.Locale;

/** Una función: exporta los resultados a CSV con columnas idénticas a Python. */
public final class GuardarResumen {
    public static void guardar(List<FilaResumen> filas, Path archivo) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (BufferedWriter salida = Files.newBufferedWriter(archivo)) {
            salida.write("configuracion,N,pi_estimado,error_pi_absoluto,tiempo_segundos,"
                    + "chi2,chi2_gl,chi2_p,chi2_rechazar,ks_d,ks_d_mas,ks_d_menos,"
                    + "ks_p,ks_rechazar,rachas_r,rachas_z,rachas_p,rachas_rechazar\n");
            for (FilaResumen f : filas) {
                salida.write(String.format(Locale.ROOT,
                    "%s,%d,%.12g,%.12g,%.12g,%.12g,%d,%.12g,%s,%.12g,%.12g,%.12g,%.12g,%s,%d,%.12g,%.12g,%s%n",
                    f.configuracion(), f.n(), f.piEstimado(), f.errorPiAbsoluto(),
                    f.tiempoSegundos(), f.chi2(), f.chi2Gl(), f.chi2P(),
                    f.chi2Rechazar(), f.ksD(), f.ksDMas(), f.ksDMenos(), f.ksP(),
                    f.ksRechazar(), f.rachasR(), f.rachasZ(), f.rachasP(),
                    f.rachasRechazar()));
            }
        }
    }
}
