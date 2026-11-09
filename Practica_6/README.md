# Práctica 6 — Simulación (UNL): Python y Java en Linux

**Documentos usados:** Guía APE 006 (7 páginas) y presentación de Semana 6 (25 páginas).

## Alcance

Implementaciones paralelas de un LCG, Chi-cuadrado con 10 intervalos, Kolmogorov-Smirnov, rachas alrededor de la mediana, valor p, gráficos PNG y comparación de tiempos. Se usan dos configuraciones reproducibles:

- **glibc (según la diapositiva, no la implementación real de `rand()` de glibc):** `a=1103515245`, `c=12345`, `m=2^32`, `semilla=1`.
- **numerical_recipes:** `a=1664525`, `c=1013904223`, `m=2^32`, `semilla=42`.

Con la misma configuración, ambos programas deben producir **exactamente los mismos números en punto flotante**. Los valores p de KS usan en ambos lenguajes **la misma aproximación asintótica con corrección finita** `lambda=(sqrt(N)+0.12+0.11/sqrt(N))*D`, con supervivencia de Kolmogorov. No deben confundirse con p-valores exactos. Los valores p de rachas usan una aproximación normal.

### Aclaración de los documentos
La guía exige principalmente LCG, Chi-cuadrado, KS y gráfico CDF; las diapositivas amplían con rachas y mencionan otras pruebas (póker, serial, Diehard/TestU01). **Póker, serial y baterías completas se mencionan, pero no se implementan aquí**, pues no hay algoritmos concretos detallados en la guía práctica y excederían sus tres actividades. La tabla `π estimado / error / tiempo Python / tiempo Java` de la página 6 no corresponde directamente al procedimiento Chi/KS; se añade un estimador π con parejas (u[0],u[1]), (u[2],u[3]), ... para satisfacer ese formato. No es una prueba de uniformidad y el error de π no debe confundirse con el valor p.

## 1. Estructura esperada con el entorno compartido

```text
Simulacion/
├── env/                    # entorno Python existente, NO se vuelve a crear
├── practica_1/
├── practica_2/
├── practica_3/
├── practica_4/
├── practica_5/
└── Practica_6_Simulacion/   # descomprime aquí la carpeta del ZIP
    ├── python/
    ├── java/src/
    ├── java/bin/           # se crea tras compilar
    ├── scripts/
    ├── resultados/
    ├── ejecutar.sh
    └── README.md
```

## 2. Comprobar tu instalación antes de hacer cambios

Abre Terminal en Linux y ejecuta:

```bash
python3 --version
java -version
javac -version
ls -l env/bin/python
```

Desde la carpeta **Simulacion** comprueba el entorno previo:

```bash
source env/bin/activate
python --version
python -m pip --version
python -m pip show numpy scipy matplotlib pandas
```

El JDK debe ser 17 o superior (se utilizan `record`). Si Python o pip faltan en Ubuntu/Debian, instalar solo lo que falte:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip default-jdk
```

No hagas `python3 -m venv env` si ya existe. Instala las dependencias en el **mismo entorno**:

```bash
python -m pip install -r Practica_6_Simulacion/python/requirements.txt
```

Si ese entorno ya tiene NumPy, SciPy, Matplotlib y Pandas, no hace falta reinstalarlas. Java usa solo bibliotecas estándar de JDK (sin Maven, Gradle ni JAR externos).

## 3. Compilar y ejecutar manualmente

Desde `Simulacion/`:

```bash
source env/bin/activate
cd Practica_6_Simulacion

# Versión Python
python python/main.py

# Versión Java
mkdir -p java/bin
javac -encoding UTF-8 -d java/bin java/src/*.java
java -Djava.awt.headless=true -cp java/bin Main

# Comparar ambas versiones
python scripts/comparar_resultados.py
```

**Sin argumento** se ejecutan los cuatro tamaños (1000, 10000, 100000, 1000000) para las dos configuraciones; las secuencias completas y PNG se guardan solo para `N=10000`. Para ejecutar un tamaño concreto:

```bash
python python/main.py 10000
java -Djava.awt.headless=true -cp java/bin Main 10000
python scripts/comparar_resultados.py
```

## 4. Ejecución automática reutilizando `../env`

Desde `Practica_6_Simulacion/`:

```bash
chmod +x ejecutar.sh
./ejecutar.sh
# o para una prueba breve
./ejecutar.sh 10000
```

`ejecutar.sh` usa directamente `../env/bin/python`. Esa ruta funciona cuando `env` y `Practica_6_Simulacion` son **carpetas hermanas**, como has descrito. Si tu carpeta existente tiene otro nombre o ruta, cambia la variable `PYTHON` de `ejecutar.sh`.

## 5. Resultados

Los scripts generan:

```text
resultados/
├── python/
│   ├── resumen.csv
│   ├── secuencia_glibc_N10000.csv
│   ├── secuencia_numerical_recipes_N10000.csv
│   ├── ks_glibc_N10000.png
│   └── ks_numerical_recipes_N10000.png
├── java/
│   └── [los mismos nombres de archivos]
├── tabla_comparativa.csv
└── comparacion_primeros_20.csv
```

`resumen.csv`: estadístico Chi-cuadrado, gl, p, decisión; KS D+/D−/D/p, decisión; rachas R/Z/p, decisión; π estimado, error absoluto y tiempo. `tabla_comparativa.csv`: una fila por tamaño y configuración con columnas independientes para ambos tiempos. `comparacion_primeros_20.csv`: 20 números cotejados de cada secuencia guardada. La comparación verifica **todos los valores** de las secuencias CSV, además de las 20 filas del ejemplo.

### Cómo hacer una comparación justa

- Se cronometra exclusivamente la generación y el cálculo de pruebas (incluye cálculo de π), **no** los PNG ni CSV.
- Los tiempos dependen del equipo, el sistema, el uso de bibliotecas optimizadas, el arranque/calentamiento de la JVM y las cargas de fondo; repetir varias veces permite estimar mejor su variabilidad.
- Los p-valores asumen un modelo continuo e independiente bajo H₀; un LCG es determinista y los tests no prueban aleatoriedad verdadera.
- La prueba de rachas omite los valores exactamente iguales a la mediana.
- El generador Java usa aritmética `long`: el producto no desborda con **las dos configuraciones incluidas**, pero parámetros arbitrarios más grandes sí pueden desbordarse. Para grandes parámetros habría que emplear `BigInteger` o multiplicación modular segura.

## 6. Un archivo = una responsabilidad

Cada archivo `.py` con lógica contiene una sola función `def` propia. Cada clase Java de comportamiento contiene **un único método estático público** propio. Los archivos Java `record` solamente almacenan datos; `Config.java` y `configuraciones.py` guardan configuración. `main.py` y `Main.java` son los coordinadores.

## 7. Guía de informe

1. **Objetivo:** validar uniformidad e independencia de secuencias LCG en Python y Java.
2. **Métodos:** LCG, diez intervalos de Chi-cuadrado, KS empírico y teórico, rachas y alfa=0.05.
3. **Experimentos:** parámetros y semillas de ambos generadores; N=1000, 10000, 100000, 1000000.
4. **Evidencias:** capturas de terminal, PNG KS, frecuencias y tablas CSV.
5. **Resultados:** valores p, decisiones (rechazar/no rechazar), concordancia Python-Java y tiempos.
6. **Conclusiones:** diferencias entre uniformidad e independencia y límites de las pruebas.
7. **Preguntas de control:** consultar `PREGUNTAS_DE_CONTROL.md`.
