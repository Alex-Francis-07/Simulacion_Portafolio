/** Una función: genera una secuencia LCG en [0,1). */
public final class LCG {
    public static double[] generar(int n, Config config) {
        if (n <= 0 || config.m() <= 1 || config.semilla() < 0
                || config.semilla() >= config.m() || config.a() < 0 || config.c() < 0) {
            throw new IllegalArgumentException("Parámetros inválidos del LCG.");
        }
        // Las dos configuraciones usan m=2^32; a*x+c no supera Long.MAX_VALUE.
        // Esta implementación no es segura para parámetros arbitrarios que desborden long.
        double[] numeros = new double[n];
        long actual = config.semilla();
        for (int i = 0; i < n; i++) {
            actual = (config.a() * actual + config.c()) % config.m();
            numeros[i] = (double) actual / config.m();
        }
        return numeros;
    }
}
