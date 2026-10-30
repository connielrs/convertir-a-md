---
name: convertir-a-md
description: Convierte PDF, Word, PowerPoint, Excel, HTML o CSV a Markdown en local antes de leerlos, para gastar muchos menos tokens. Usar siempre que se pida leer, revisar, resumir o usar uno de esos archivos, o se pida "pasar a md" / "convertir a markdown". No usar si lo importante es lo visual (gráficos, diagramas, formularios), si el PDF es de 1 o 2 páginas o si es escaneado.
---

# Convertir a Markdown

Leer un PDF directo cuesta unos 1.500 tokens por página, porque cada página llega también como imagen. Word, PowerPoint y Excel no se pueden leer directo. El .md cuesta solo el texto, y la conversión corre en el computador sin gastar tokens.

En los comandos, `<skill>` es la carpeta de esta skill (la que aparece como "Base directory for this skill").

## Pasos

1. Si no existe `<skill>/.venv/bin/python`, instalar primero (una sola vez, tarda un par de minutos):
   ```bash
   bash "<skill>/instalar.sh"
   ```
   Si avisa que falta Python 3.10 o más nuevo, mostrar el mensaje a la persona y esperar a que lo instale.
2. Convertir sin abrir el archivo:
   ```bash
   "<skill>/.venv/bin/python" "<skill>/scripts/convertir_a_md.py" "<ruta del archivo>"
   ```
   Deja `<nombre>.md` al lado del original e imprime un resumen con los tokens. Para otra ruta de salida se agrega como segundo argumento.
3. Si el resumen trae un AVISO (PDF escaneado o .md vacío), avisarle a la persona y preguntarle cómo seguir.
4. Leer el .md. Si tiene más de 400 líneas, leerlo por partes (`offset` y `limit`), solo lo que haga falta. Los Excel suelen ser largos.
5. Revisar las primeras líneas: si en un PDF las tablas o las columnas quedaron mal, decirlo y leer solo esas páginas del PDF con `pages`.
6. Al terminar, contarle a la persona los tokens con las cifras que imprimió el script.

## Notas

- Si el .md ya existe y es más nuevo que el original, usarlo sin volver a convertir.
- Los PDF van con `pymupdf4llm` (reconoce títulos y tablas, MarkItDown no). Todo lo demás va con MarkItDown.
- No sirve para formatos antiguos `.doc` ni `.ppt`: pedir que se guarden como `.docx` o `.pptx`.
- Si el archivo se adjuntó con `@`, la app ya lo cargó entero y no hay ahorro: recordar que conviene pasar la ruta como texto.
- Si la conversión falla por las librerías, correr de nuevo `bash "<skill>/instalar.sh"`.
