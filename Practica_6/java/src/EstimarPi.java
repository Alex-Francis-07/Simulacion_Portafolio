/** Una función adicional: pi usando parejas consecutivas (x,y) del LCG. */
public final class EstimarPi {
    public static double calcular(double[] numeros) {
        int pares = numeros.length / 2;
        if (pares == 0) throw new IllegalArgumentException("Se necesitan dos valores.");
        int dentro = 0;
        for (int i = 0; i < pares * 2; i += 2) {
            if (numeros[i] * numeros[i] + numeros[i + 1] * numeros[i + 1] <= 1.0) {
                dentro++;
            }
        }
        return 4.0 * dentro / pares;
    }
}
