"""Punto de entrada para las Fases 1 y 2 del compilador."""
import sys
from pathlib import Path
from lexer import Lexer
from sintactico import Parser

def main():
    if len(sys.argv) != 2:
        print('Uso: python main.py <archivo_fuente.txt>')
        return 1
    try:
        codigo = Path(sys.argv[1]).read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        print(f'Error al leer el archivo: {exc}')
        return 1
    tokens, lex_errors = Lexer(codigo).tokenize()
    print('=== FASE 1: ANÁLISIS LÉXICO ===')
    print(f'Tokens: {len(tokens)} | Errores léxicos: {len(lex_errors)}')
    for err in lex_errors:
        print(err)
    if lex_errors:
        print('No se ejecuta el análisis sintáctico hasta corregir los errores léxicos.')
        return 1
    print('\n=== FASE 2: ANÁLISIS SINTÁCTICO ===')
    ast, parse_errors = Parser(tokens).parse()
    print(ast.pretty())
    for err in parse_errors:
        print(err)
    print(f'Errores sintácticos: {len(parse_errors)}')
    return 1 if parse_errors else 0

if __name__ == '__main__':
    sys.exit(main())
