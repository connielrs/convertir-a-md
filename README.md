# convertir-a-md

Skill para Claude Code que convierte PDF, Word, PowerPoint, Excel, HTML y CSV a Markdown en tu computador antes de que Claude los lea. Así se gastan muchos menos tokens: en un PDF de 6 páginas, unos 5.000 tokens en vez de 14.000.

- Los PDF se convierten con [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm), que reconoce títulos y tablas.
- El resto se convierte con [MarkItDown](https://github.com/microsoft/markitdown) de Microsoft.
- Todo corre en local: los archivos no se mandan a ningún lado.

## Instalar

Abre Claude Code y escribe:

> Instálame esta skill: https://github.com/connielrs/convertir-a-md

Después abre una sesión nueva. Listo.

<details>
<summary>Instalación a mano (o instrucciones para Claude)</summary>

1. Descargar el repo en la carpeta de skills personales:
   ```bash
   git clone https://github.com/connielrs/convertir-a-md ~/.claude/skills/convertir-a-md
   ```
2. Instalar las librerías (crea un entorno propio dentro de la carpeta, no toca el resto del sistema):
   ```bash
   bash ~/.claude/skills/convertir-a-md/instalar.sh
   ```
   Necesita Python 3.10 o más nuevo. En Mac, si falta: `brew install python@3.12`.
3. Abrir una sesión nueva de Claude Code.

Si el paso 2 se salta, la skill lo hace sola la primera vez que se usa.
</details>

## Usar

No hay que hacer nada especial: pide las cosas como siempre, escribiendo la ruta del archivo.

> Resume el PDF que está en Descargas/contrato.pdf

> Revisa la presentación Documentos/plan-2027.pptx y dime qué le falta

Claude convierte el archivo, deja el `.md` al lado del original y lee solo eso. Si alguna vez no la usa, se puede forzar con `/convertir-a-md <ruta>`.

Ojo: si adjuntas el archivo con `@`, la app ya lo carga entero y no hay ahorro. Mejor escribir la ruta.

## Qué no hace

- No lee PDF escaneados (fotos de páginas sin texto).
- No describe imágenes ni gráficos.
- No sirve para `.doc` ni `.ppt` antiguos: guardarlos antes como `.docx` o `.pptx`.
- Funciona en Mac y Linux. En Windows hay que crear el entorno a mano con los mismos pasos del instalador.

## Actualizar

```bash
git -C ~/.claude/skills/convertir-a-md pull && bash ~/.claude/skills/convertir-a-md/instalar.sh
```
