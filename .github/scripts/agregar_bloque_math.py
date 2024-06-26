import sys
import re
import shutil
import os

# * Pasos para agregar los bloques de código:
# * 1. Identificar los bloques de matemáticas `$$$$` y `math`.
# * 2. Identificar si ya existe un bloque de código para cada uno de los bloques de matemáticas.
# * 3. Si no existe, agregar un bloque de código inmediatamente después del bloque de matemáticas con el siguiente formato:
# ```md
# <!-- INICIA AUTOGENERADO - NO MODIFICAR -->
# ``\`
# <aqui la fórmula>
# ``\`
# <!-- FIN AUTOGENERADO - NO MODIFICAR -->
# ```
# * 3. Si existe, actualizar el bloque de código con la fórmula correspondiente.


def update_file(file_path, dest_folder = None):
    dest_file_path = file_path
    if dest_folder is not None:
        dest_file_path = os.path.join(
            dest_folder, os.path.basename(file_path))

    # RegEx para identificar los bloques de matemáticas
    inside_math_pattern = r"""
        (?:
            [^\\\$`]               # Cualquier caracter que no sea \ o $ o `
            |(?:\\\S)                  # Cualquier caracter escapado
            |(?:\n)          # Cualquier caracter que no sea espacio seguido de un salto de línea
        )+?
    """

    autogenerated_pattern = r"""
        (?:
            (?:\n)*?                                                # Salto de línea opcional
            <!----------------------------------------->\n
            <!--\sAUTOGENERADO\sINICIA\s-\sNO\sMODIFICAR\s--->\n
            (?:\n)*?                                                # Salto de línea opcional
            ```\n
    """ + inside_math_pattern + r"""\n
            ```\n
            (?:\n)*?                                                # Salto de línea opcional
            <!--\sAUTOGENERADO\sTERMINA\s-\sNO\sMODIFICAR\s-->\n
            <!----------------------------------------->\n
        )?
    """

    display_math_pattern = r"""
        (?P<math_block>
            \$\$((?:\n)?)
            (?P<math_content>        # Grupo 1: Contenido de la fórmula
    """ + inside_math_pattern + r"""
            )
            \2\$\$\n?
        )
    """ + autogenerated_pattern


    code_math_pattern = r"""
        (?P<math_block>
            ```math\n
            (?P<math_content>        # Grupo 1: Contenido de la fórmula
    """ + inside_math_pattern + r"""
            )
            \n
            ```\n
        )
    """ + autogenerated_pattern

    substitute = r"""\g<math_block>
<!----------------------------------------->
<!-- AUTOGENERADO INICIA - NO MODIFICAR --->

```
\g<math_content>
```

<!-- AUTOGENERADO TERMINA - NO MODIFICAR -->
<!----------------------------------------->
"""

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        content = re.compile(display_math_pattern, re.VERBOSE).sub(
            substitute, content)
        
        content = re.compile(code_math_pattern, re.VERBOSE).sub(
            substitute, content)

        # Escribir el contenido actualizado de vuelta al archivo
        with open(dest_file_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(content)


def main():
    if len(sys.argv) < 2:
        print("Uso: python update_markdown.py archivo_a_actualizar carpeta_destino")
        sys.exit(1)

    file_path = sys.argv[1]
    dest_folder = sys.argv[2] if len(sys.argv) > 2 else None

    # Crear la carpeta de destino si no existe
    if dest_folder and not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    update_file(file_path, dest_folder)


if __name__ == "__main__":
    main()
