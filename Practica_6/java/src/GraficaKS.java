import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import javax.imageio.ImageIO;

/** Una función: escribe un PNG de las CDF empírica y teórica sin librerías externas. */
public final class GraficaKS {
    public static void guardar(double[] numeros, Path archivo, String titulo) throws IOException {
        double[] x = Arrays.copyOf(numeros, numeros.length);
        Arrays.sort(x);
        int ancho = 900, alto = 560, izq = 85, der = 35, arriba = 72, abajo = 80;
        int w = ancho - izq - der, h = alto - arriba - abajo;
        BufferedImage imagen = new BufferedImage(ancho, alto, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, ancho, alto);
        g.setColor(new Color(25, 34, 46));
        g.setFont(new Font("SansSerif", Font.BOLD, 19));
        g.drawString(titulo, izq, 35);
        g.setFont(new Font("SansSerif", Font.PLAIN, 13));
        g.setColor(new Color(225, 230, 235));
        for (int j = 0; j <= 10; j++) {
            int px = izq + (int) Math.round(j * w / 10.0);
            int py = arriba + (int) Math.round(j * h / 10.0);
            g.drawLine(px, arriba, px, arriba + h);
            g.drawLine(izq, py, izq + w, py);
        }
        g.setColor(new Color(32, 40, 50));
        g.drawRect(izq, arriba, w, h);
        g.drawString("U generado (0 a 1)", ancho / 2 - 65, alto - 25);
        g.drawString("F(x)", 38, arriba + h / 2);
        // F(x)=x, línea teórica roja.
        g.setColor(new Color(204, 56, 63));
        g.setStroke(new BasicStroke(2.2f));
        g.drawLine(izq, arriba + h, izq + w, arriba);
        // Distribución empírica: escalones verdaderos (sin conectar por diagonales).
        g.setColor(new Color(32, 123, 185));
        g.setStroke(new BasicStroke(1.3f));
        int pxPrev = izq, pyPrev = arriba + h;
        for (int i = 0; i < x.length; i++) {
            int px = izq + (int) Math.round(x[i] * w);
            int py = arriba + h - (int) Math.round((i + 1.0) * h / x.length);
            g.drawLine(pxPrev, pyPrev, px, pyPrev);
            g.drawLine(px, pyPrev, px, py);
            pxPrev = px;
            pyPrev = py;
        }
        g.drawLine(pxPrev, pyPrev, izq + w, pyPrev);
        g.setColor(new Color(32, 123, 185));
        g.fillRect(izq + 15, arriba + 15, 22, 8);
        g.setColor(new Color(32, 40, 50));
        g.drawString("F empírica", izq + 47, arriba + 25);
        g.setColor(new Color(204, 56, 63));
        g.fillRect(izq + 170, arriba + 15, 22, 8);
        g.setColor(new Color(32, 40, 50));
        g.drawString("F teórica = x", izq + 202, arriba + 25);
        g.dispose();
        Files.createDirectories(archivo.getParent());
        if (!ImageIO.write(imagen, "png", archivo.toFile())) {
            throw new IOException("No se puede crear archivo PNG.");
        }
    }
}
