"""
MÓDULO: lexer.py
PROYECTO FINAL: COMPILADORES - FASE 1
"""

import re
from typing import List, Tuple, NamedTuple

# ==============================================================================
# 1. ESTRUCTURAS DE DATOS
# ==============================================================================

class Token(NamedTuple):
    """Estructura para representar un Token detectado."""
    type: str
    value: str
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"[TOKEN] Tipo: {self.type} | Lexema: '{self.value}' | "
            f"Posición: [Línea {self.line}, Col {self.column}]"
        )


class LexicalError(NamedTuple):
    """Estructura para representar un error léxico detectado."""
    message: str
    char: str
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"[ERROR LÉXICO] {self.message} '{self.char}' "
            f"en Posición: [Línea {self.line}, Col {self.column}]"
        )

# ==============================================================================
# 2. CLASE PRINCIPAL DEL ANALIZADOR LÉXICO
# ==============================================================================

class Lexer:
    """
    Analizador Léxico (Scanner).
    Transforma una cadena de código fuente en una lista de Tokens y Errores Léxicos.
    """

    # TODO: Definir los patrones de expresiones regulares en orden de prioridad.
    # Formato: ('NOMBRE_DEL_TOKEN', r'expresion_regular')
    TOKEN_SPECIFICATION = [
        ('COMMENT_MULTI',       r'/\*[\s\S]*?\*/'),
        ('COMMENT_SINGLE',      r'//[^\n]*'),
        ('NEWLINE',             r'\n'),
        ('SKIP',                r'[ \t\r]+'),

        ('FLOAT_LITERAL',       r'\d+\.\d+'),
        ('INT_LITERAL',         r'\d+'),
        ('STRING_LITERAL',      r'"([^"\n\\]|\\.)*"'),

        ('UNTERMINATED_STRING', r'"[^"\n]*'),

        ('ID',                  r'[a-zA-Z_][a-zA-Z0-9_]*'),

        ('OP_EQ',               r'=='),
        ('OP_NEQ',              r'!='),
        ('OP_LE',               r'<='),
        ('OP_GE',               r'>='),
        ('OP_LT',               r'<'),
        ('OP_GT',               r'>'),
        ('OP_ASSIGN',           r'='),
        ('OP_PLUS',             r'\+'),
        ('OP_MINUS',            r'-'),
        ('OP_MUL',              r'\*'),
        ('OP_DIV',              r'/'),

        ('LPAREN',              r'\('),
        ('RPAREN',              r'\)'),
        ('LBRACE',              r'\{'),
        ('RBRACE',              r'\}'),
        ('COMMA',               r','),
        ('SEMICOLON',           r';'),

        ('MISMATCH',            r'.'),
    ]

    KEYWORD_MAP = {
        'int':    'PR_INT',
        'float':  'PR_FLOAT',
        'if':     'PR_IF',
        'else':   'PR_ELSE',
        'while':  'PR_WHILE',
        'return': 'PR_RETURN',
        'void':   'PR_VOID',
        'string': 'PR_STRING',
    }

    def __init__(self, code: str):
        self.code = code
        # Compila la expresión regular combinando todos los grupos etiquetados
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION)
        self.regex = re.compile(tok_regex)

    def tokenize(self) -> Tuple[List[Token], List[LexicalError]]:
        """
        Procesa el código fuente completo y retorna una tupla con:
        - Lista de Tokens válidos
        - Lista de Errores Léxicos encontrados
        """
        tokens: List[Token] = []
        errors: List[LexicalError] = []

        line_num = 1
        line_start = 0

        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            position = mo.start()
            col_num = position - line_start + 1

            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue

            elif kind == 'SKIP':
                continue

            # TODO: Manejar la lógica de actualización de líneas para comentarios multilínea
            # elif kind == 'COMMENT_MULTI':
            #     ...

            # TODO: Convertir tipo KEYWORD al token específico usando KEYWORD_MAP
            # elif kind == 'KEYWORD':
            #     ...

            # TODO: Manejar casos de errores léxicos
            elif kind == 'MISMATCH':
                errors.append(LexicalError("Carácter no reconocido", value, line_num, col_num))

            # TODO: Guardar los tokens válidos restantes en la lista 'tokens'
            # else:
            #     tokens.append(Token(kind, value, line_num, col_num))

        return tokens, errors