
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
    """Estructura para representar un token detectado."""
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
    """Estructura para representar un error léxico."""
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
    Transforma código fuente en tokens y errores léxicos.
    """

    # Expresiones regulares en orden de prioridad
    TOKEN_SPECIFICATION = [
        # Comentarios y espacios
        ('COMMENT_MULTI',       r'/\*[\s\S]*?\*/'),
        ('COMMENT_UNCLOSED',    r'/\*[\s\S]*'),
        ('COMMENT_SINGLE',      r'//[^\n]*'),
        ('NEWLINE',             r'\n'),
        ('SKIP',                r'[ \t\r]+'),

        # Literales
        ('FLOAT_LITERAL',       r'\d+\.\d+'),
        ('INT_LITERAL',         r'\d+'),
        ('STRING_LITERAL',      r'"([^"\n\\]|\\.)*"'),

        # Cadenas sin cerrar
        ('UNTERMINATED_STRING', r'"([^"\n\\]|\\.)*(?:\\)?'),

        # Identificadores y palabras reservadas
        ('ID',                  r'[a-zA-Z_][a-zA-Z0-9_]*'),

        # Operadores relacionales
        ('OP_EQ',               r'=='),
        ('OP_NEQ',              r'!='),
        ('OP_LE',               r'<='),
        ('OP_GE',               r'>='),
        ('OP_LT',               r'<'),
        ('OP_GT',               r'>'),

        # Operadores de asignación y aritméticos
        ('OP_ASSIGN',           r'='),
        ('OP_PLUS',             r'\+'),
        ('OP_MINUS',            r'-'),
        ('OP_MUL',              r'\*'),
        ('OP_DIV',              r'/'),

        # Delimitadores
        ('LPAREN',              r'\('),
        ('RPAREN',              r'\)'),
        ('LBRACE',              r'\{'),
        ('RBRACE',              r'\}'),
        ('COMMA',               r','),
        ('SEMICOLON',           r';'),

        # Caracteres no reconocidos
        ('MISMATCH',            r'.'),
    ]

    # Palabras reservadas
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

    # ==========================================================================
    # 3. CONSTRUCTOR
    # ==========================================================================

    def __init__(self, code: str):
        self.code = code

        # Combinar los patrones en una expresión regular
        tok_regex = '|'.join(
            f'(?P<{name}>{pattern})'
            for name, pattern in self.TOKEN_SPECIFICATION
        )

        self.regex = re.compile(tok_regex)

    # ==========================================================================
    # 4. ANÁLISIS LÉXICO
    # ==========================================================================

    def tokenize(self) -> Tuple[List[Token], List[LexicalError]]:
        """
        Procesa el código fuente y devuelve:
        - Lista de tokens válidos.
        - Lista de errores léxicos.
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

            # Saltos de línea
            if kind == 'NEWLINE':
                line_num += 1
                line_start = mo.end()
                continue

            # Espacios y tabulaciones
            elif kind == 'SKIP':
                continue

            # Comentarios de una línea
            elif kind == 'COMMENT_SINGLE':
                continue

            # Comentarios multilínea
            elif kind == 'COMMENT_MULTI':
                newlines_count = value.count('\n')

                if newlines_count > 0:
                    line_num += newlines_count
                    last_newline_pos = value.rfind('\n')
                    line_start = position + last_newline_pos + 1

                continue

            # Comentarios multilínea sin cerrar
            elif kind == 'COMMENT_UNCLOSED':
                errors.append(
                    LexicalError(
                        "Comentario multilínea sin cerrar",
                        value,
                        line_num,
                        col_num
                    )
                )

                newlines_count = value.count('\n')
                if newlines_count > 0:
                    line_num += newlines_count
                    line_start = position + value.rfind('\n') + 1

            # Identificadores y palabras reservadas
            elif kind == 'ID':
                token_type = self.KEYWORD_MAP.get(value, 'ID')

                tokens.append(
                    Token(token_type, value, line_num, col_num)
                )

            # Cadenas sin cerrar
            elif kind == 'UNTERMINATED_STRING':
                errors.append(
                    LexicalError(
                        "Cadena sin cerrar",
                        value,
                        line_num,
                        col_num
                    )
                )

            # Caracteres desconocidos
            elif kind == 'MISMATCH':
                errors.append(
                    LexicalError(
                        "Carácter no reconocido",
                        value,
                        line_num,
                        col_num
                    )
                )

            # Literales, operadores y delimitadores
            else:
                tokens.append(
                    Token(kind, value, line_num, col_num)
                )

        return tokens, errors
