#!/usr/bin/env bash
# Instala las librerías de la skill en su propio entorno (.venv), sin tocar el resto del sistema.
# Se puede correr de nuevo sin problema: actualiza lo que falte.
set -euo pipefail

carpeta="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Busca un Python 3.10 o más nuevo.
python=""
for candidato in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$candidato" >/dev/null 2>&1 &&
     "$candidato" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
    python="$candidato"
    break
  fi
done

if [ -z "$python" ]; then
  echo "Falta Python 3.10 o más nuevo." >&2
  echo "En Mac: brew install python@3.12  (si no hay Homebrew: https://brew.sh)" >&2
  echo "En Linux: instalar python3.12 con el gestor de paquetes del sistema." >&2
  exit 1
fi

echo "Usando $("$python" --version)"
if [ ! -x "$carpeta/.venv/bin/python" ]; then
  "$python" -m venv "$carpeta/.venv"
fi
"$carpeta/.venv/bin/python" -m pip install --quiet --upgrade pip
"$carpeta/.venv/bin/python" -m pip install --quiet -r "$carpeta/requirements.txt"
"$carpeta/.venv/bin/python" -c "import pymupdf4llm, markitdown"
echo "Listo. Abre una sesión nueva de Claude Code para que reconozca la skill."
