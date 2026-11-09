/** Resultado de la prueba Kolmogorov-Smirnov. */
public record ResultadoKS(double dMas, double dMenos, double d,
                          double p, boolean rechazar, double dCriticoAprox) {}
