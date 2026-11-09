/** Resultado de la prueba Chi-cuadrado. */
public record ResultadoChi(int[] frecuencias, double esperada, double estadistico,
                           int gl, double p, boolean rechazar) {}
