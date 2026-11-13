
"""
MÓDULO: main.py
PROYECTO FINAL: COMPILADORES
Punto de entrada del programa.
"""

import sys
from pathlib import Path

from lexer import Lexer


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo_fuente.txt>")
        sys.exit(1)

    ruta = Path(sys.argv[1])

    try:
        codigo = ruta.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        print(f"Error al leer el archivo: {error}")
        sys.exit(1)

    print("=== ANÁLISIS LÉXICO ===")

    tokens, errores = Lexer(codigo).tokenize()

    for token in tokens:
        print(token)

    for error in errores:
        print(error)

    print(f"\nTokens encontrados: {len(tokens)}")
    print(f"Errores léxicos: {len(errores)}")

    if errores:
        sys.exit(1)


if __name__ == "__main__":
    main()
