/** Una fila del CSV de resultados. */
public record FilaResumen(
        String configuracion, int n, double piEstimado, double errorPiAbsoluto,
        double tiempoSegundos, double chi2, int chi2Gl, double chi2P, boolean chi2Rechazar,
        double ksD, double ksDMas, double ksDMenos, double ksP, boolean ksRechazar,
        int rachasR, double rachasZ, double rachasP, boolean rachasRechazar) {}
