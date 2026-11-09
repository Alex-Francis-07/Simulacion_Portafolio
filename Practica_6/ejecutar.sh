#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# El env se comparte con las prácticas 1 a 5: carpeta hermana de Practica_6_Simulacion.
PYTHON="../venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    echo "No existe ../venv/bin/python. Activa/verifica tu entorno virtual compartido."
    echo "Puedes ejecutar manualmente: source ../venv/bin/activate"
    exit 1
fi
if ! command -v javac >/dev/null 2>&1 || ! command -v java >/dev/null 2>&1; then
    echo "Falta JDK (javac/java). Instala un JDK 17 o superior."
    exit 1
fi
"$PYTHON" -c 'import scipy, matplotlib, pandas, numpy' || {
    echo "Dependencias incompletas: ejecuta $PYTHON -m pip install -r python/requirements.txt"
    exit 1
}

mkdir -p java/bin
javac -encoding UTF-8 -d java/bin java/src/*.java

if (( $# > 1 )); then
    echo "Uso: ./ejecutar.sh [N]"
    exit 1
fi
if (( $# == 1 )); then
    "$PYTHON" python/main.py "$1"
    java -Djava.awt.headless=true -cp java/bin Main "$1"
else
    "$PYTHON" python/main.py
    java -Djava.awt.headless=true -cp java/bin Main
fi
"$PYTHON" scripts/comparar_resultados.py
