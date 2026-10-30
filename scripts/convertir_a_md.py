"""Convierte un archivo a Markdown en local y estima cuántos tokens cuesta leerlo.

Uso: convertir_a_md.py archivo [salida.md]

Los PDF se convierten con pymupdf4llm, que reconoce títulos y tablas.
Word, PowerPoint, Excel, HTML, CSV y otros se convierten con MarkItDown.
Guarda el .md al lado del archivo (o en la ruta indicada) e imprime un
resumen corto. No imprime el contenido, para no gastar tokens.
"""

import math
import re
import sys
from pathlib import Path

# Aproximación para texto en español con el tokenizador de Claude.
CARACTERES_POR_TOKEN = 3.5
# Límites con que Claude reduce una imagen antes de leerla.
LADO_MAXIMO = 1568
AREA_MAXIMA = 1_150_000
# Menos texto que esto por página indica un PDF escaneado.
MINIMO_CARACTERES_POR_PAGINA = 100
# Líneas que empiezan algo nuevo y no se pegan a la anterior: listas, títulos, tablas.
INICIO_DE_BLOQUE = re.compile(r"^\s*([-*+●•▪]\s|#|\||\d+[.)]\s)")
# Línea con sangría y sin viñeta: la viñeta del PDF usaba un símbolo que no se pudo leer.
VINETA_PERDIDA = re.compile(r"^\s{2,}(?![-*+●•▪|#])\S")


def tokens_texto(texto):
    return math.ceil(len(texto) / CARACTERES_POR_TOKEN)


def tokens_imagen_pagina(pagina):
    """Tokens de la imagen de una página, como la reduce Claude (ancho x alto / 750)."""
    ancho, alto = pagina.rect.width, pagina.rect.height
    escala = min(LADO_MAXIMO / max(ancho, alto), math.sqrt(AREA_MAXIMA / (ancho * alto)))
    return math.ceil((ancho * escala) * (alto * escala) / 750)


def unir_lineas(markdown):
    """Junta las líneas que el PDF cortó a mitad de frase.

    pymupdf4llm separa cada línea del PDF con una línea en blanco y los
    párrafos con dos o más. Una sola línea en blanco se pega con un espacio;
    dos o más quedan como fin de párrafo.
    """
    resultado = []
    blancos = 0
    for linea in markdown.splitlines():
        if not linea.strip():
            blancos += 1
            continue
        if VINETA_PERDIDA.match(linea):
            linea = "  - " + linea.strip()
        anterior = resultado[-1] if resultado else ""
        es_tabla = linea.startswith("|") or anterior.startswith("|")
        # Una línea entera en negrita seguida de otra en negrita suelen ser dos títulos.
        es_titulo = anterior.startswith("**") and anterior.endswith("**") and linea.startswith("**")
        if es_tabla and blancos == 0:
            resultado.append(linea)
        elif (blancos <= 1 and anterior and not es_tabla and not es_titulo and not anterior.startswith("#")
              and not INICIO_DE_BLOQUE.match(linea)):
            resultado[-1] = anterior.rstrip() + " " + linea.strip()
        else:
            if resultado:
                resultado.append("")
            resultado.append(linea.rstrip())
        blancos = 0
    return "\n".join(resultado) + "\n"


def convertir_pdf(archivo):
    """Devuelve el markdown y las líneas extra del resumen."""
    import pymupdf
    import pymupdf4llm

    doc = pymupdf.open(archivo)
    paginas = doc.page_count
    texto_plano = "".join(p.get_text() for p in doc)
    tokens_pdf = tokens_texto(texto_plano) + sum(tokens_imagen_pagina(p) for p in doc)
    markdown = unir_lineas(pymupdf4llm.to_markdown(str(archivo), show_progress=False))
    tokens_md = tokens_texto(markdown)

    resumen = [
        f"Páginas: {paginas}",
        f"Tokens leyendo el PDF directo (aprox.): {tokens_pdf:,}",
        f"Ahorro: {100 * (1 - tokens_md / tokens_pdf) if tokens_pdf else 0:.0f}%",
    ]
    if paginas and len(texto_plano.strip()) / paginas < MINIMO_CARACTERES_POR_PAGINA:
        resumen.append("AVISO: casi no hay texto, parece un PDF escaneado. El .md puede salir vacío.")
    return markdown, resumen


def convertir_otro(archivo):
    from markitdown import MarkItDown

    return MarkItDown().convert(str(archivo)).text_content, []


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: convertir_a_md.py archivo [salida.md]")

    archivo = Path(sys.argv[1]).expanduser().resolve()
    salida = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else archivo.with_suffix(".md")
    if archivo.suffix.lower() == ".md":
        sys.exit("El archivo ya es Markdown.")

    if archivo.suffix.lower() == ".pdf":
        markdown, resumen = convertir_pdf(archivo)
        motor = "pymupdf4llm"
    else:
        markdown, resumen = convertir_otro(archivo)
        motor = "MarkItDown"
    salida.write_text(markdown, encoding="utf-8")

    print(f"Markdown guardado en: {salida} (con {motor})")
    print(f"Líneas del .md: {markdown.count(chr(10)) + 1}")
    print(f"Tokens leyendo el .md (aprox.): {tokens_texto(markdown):,}")
    for linea in resumen:
        print(linea)
    if not markdown.strip():
        print("AVISO: el .md quedó vacío.")


if __name__ == "__main__":
    main()
