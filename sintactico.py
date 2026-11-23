"""Analizador sintáctico descendente recursivo (Fase 2)."""
from typing import List, Optional, Tuple
from lexer import Token

class ASTNode:
    def __init__(self, kind: str, value: Optional[str] = None,
                 children: Optional[List['ASTNode']] = None, line: int = 0, column: int = 0):
        self.kind, self.value = kind, value
        self.children = children if children is not None else []
        self.line, self.column = line, column

    def pretty(self, prefix: str = "", is_last: bool = True, is_root: bool = True) -> str:
        label = self.kind if self.value is None else f"{self.kind}: {self.value}"
        if is_root:
            lines, child_prefix = [label], ""
        else:
            lines = [prefix + ("└── " if is_last else "├── ") + label]
            child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            lines.append(child.pretty(child_prefix, i == len(self.children) - 1, False))
        return "\n".join(lines)

class ParseError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message, self.line, self.column = message, line, column
    def __str__(self):
        return f"[ERROR SINTÁCTICO] Línea {self.line}, Col {self.column}: {self.message}"

LITERALS = {'INT_LITERAL': 'Entero', 'FLOAT_LITERAL': 'Flotante', 'STRING_LITERAL': 'Cadena'}
TYPES = {'int', 'float', 'string'}
STATEMENT_START = TYPES | {'if', 'while', 'return', '{', 'void'}

class Parser:
    def __init__(self, tokens: List[Token]):
        last = tokens[-1] if tokens else Token('EOF', '', 1, 0)
        eof = Token('EOF', '', last.line, last.column + len(last.value))
        self.tokens = list(tokens) + [eof]
        self.pos = 0
        self.errors: List[ParseError] = []

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, k: int = 1) -> Token:
        return self.tokens[min(self.pos + k, len(self.tokens) - 1)]

    def check(self, *values: str) -> bool:
        tok = self.current
        return tok.type not in ('ID', 'EOF') and tok.type not in LITERALS and tok.value in values

    def at_end(self) -> bool:
        return self.current.type == 'EOF'

    def advance(self) -> Token:
        tok = self.current
        if not self.at_end():
            self.pos += 1
        return tok

    @staticmethod
    def describe(tok: Token) -> str:
        return 'fin de archivo' if tok.type == 'EOF' else f"'{tok.value}'"

    def error(self, message: str, tok: Optional[Token] = None) -> ParseError:
        tok = tok or self.current
        return ParseError(message, tok.line, tok.column)

    def expect(self, value: str, context: str = '') -> Token:
        if self.check(value):
            return self.advance()
        msg = f"Se esperaba '{value}'{' ' + context if context else ''} pero se encontró {self.describe(self.current)}"
        if value in (';', ')') and self.pos > 0:
            prev = self.tokens[self.pos - 1]
            raise ParseError(msg, prev.line, prev.column + len(prev.value))
        raise self.error(msg)

    def expect_id(self, context: str = '') -> Token:
        if self.current.type == 'ID':
            return self.advance()
        raise self.error(f"Se esperaba un identificador{' ' + context if context else ''} pero se encontró {self.describe(self.current)}")

    def synchronize(self):
        """Recuperación: hasta ';', '}', o un nuevo inicio reconocible."""
        if self.at_end():
            return
        start = self.pos
        if self.check(';'):
            self.advance()
            return
        while not self.at_end():
            if self.check(';'):
                self.advance()
                return
            if self.check('}'):
                # Un cierre inesperado en nivel superior debe consumirse para progresar.
                return
            if self.pos > start and (self.current.value in STATEMENT_START or self.current.type == 'ID'):
                return
            self.advance()

    def parse(self) -> Tuple[ASTNode, List[ParseError]]:
        program = ASTNode('Programa')
        while not self.at_end():
            start = self.pos
            try:
                program.children.append(self.statement())
            except ParseError as exc:
                self.errors.append(exc)
                self.synchronize()
                if self.pos == start and not self.at_end():
                    self.advance()
                if self.check('}'):
                    self.errors.append(self.error("Llave de cierre '}' sin bloque correspondiente"))
                    self.advance()
        return program, self.errors

    def statement(self) -> ASTNode:
        if self.check('{'):
            return self.block()
        if self.check('if'):
            return self.if_statement()
        if self.check('while'):
            return self.while_statement()
        if self.check('return'):
            return self.return_statement()
        if self.current.value in TYPES | {'void'} and self.current.type != 'ID':
            return self.declaration_or_function()
        if self.current.type == 'ID':
            if self.peek().value == '=':
                return self.assignment()
            if self.peek().value == '(':
                expr = self.primary()
                self.expect(';', 'después de la llamada')
                return ASTNode('ExpresionSentencia', children=[expr], line=expr.line, column=expr.column)
        raise self.error(f"Sentencia no válida: se encontró {self.describe(self.current)}")

    def declaration_or_function(self) -> ASTNode:
        tipo = self.advance()
        nombre = self.expect_id('después del tipo')
        if self.check('('):
            self.advance()
            parametros = []
            if not self.check(')'):
                while True:
                    if self.current.value not in TYPES:
                        raise self.error('Se esperaba un tipo de parámetro')
                    ptipo = self.advance()
                    pid = self.expect_id('del parámetro')
                    parametros.append(ASTNode('Parametro', ptipo.value, [ASTNode('Identificador', pid.value, line=pid.line, column=pid.column)], ptipo.line, ptipo.column))
                    if not self.check(','):
                        break
                    self.advance()
            self.expect(')', 'al cerrar los parámetros')
            cuerpo = self.block()
            return ASTNode('Funcion', nombre.value, [ASTNode('TipoRetorno', tipo.value), ASTNode('Parametros', children=parametros), cuerpo], tipo.line, tipo.column)
        if tipo.value == 'void':
            raise self.error("'void' solo puede usarse como tipo de retorno de una función", tipo)
        children = [ASTNode('Identificador', nombre.value, line=nombre.line, column=nombre.column)]
        if self.check('='):
            self.advance()
            children.append(self.expression())
        self.expect(';', 'al finalizar la declaración')
        return ASTNode('Declaracion', tipo.value, children, tipo.line, tipo.column)

    def assignment(self) -> ASTNode:
        nombre = self.expect_id()
        self.expect('=', 'en la asignación')
        valor = self.expression()
        self.expect(';', 'al finalizar la asignación')
        return ASTNode('Asignacion', nombre.value, [valor], nombre.line, nombre.column)

    def block(self) -> ASTNode:
        inicio = self.expect('{')
        children = []
        while not self.check('}') and not self.at_end():
            start = self.pos
            try:
                children.append(self.statement())
            except ParseError as exc:
                self.errors.append(exc)
                self.synchronize()
                if self.pos == start and not self.at_end() and not self.check('}'):
                    self.advance()
        self.expect('}', 'al cerrar el bloque')
        return ASTNode('Bloque', children=children, line=inicio.line, column=inicio.column)

    def if_statement(self) -> ASTNode:
        tok = self.advance()
        self.expect('(', "después de 'if'")
        cond = self.expression()
        self.expect(')', "al cerrar la condición del 'if'")
        children = [ASTNode('Condicion', children=[cond]), ASTNode('Entonces', children=[self.statement()])]
        if self.check('else'):
            self.advance()
            children.append(ASTNode('SiNo', children=[self.statement()]))
        return ASTNode('If', children=children, line=tok.line, column=tok.column)

    def while_statement(self) -> ASTNode:
        tok = self.advance()
        self.expect('(', "después de 'while'")
        cond = self.expression()
        self.expect(')', "al cerrar la condición del 'while'")
        return ASTNode('While', children=[ASTNode('Condicion', children=[cond]), self.statement()], line=tok.line, column=tok.column)

    def return_statement(self) -> ASTNode:
        tok = self.advance()
        children = [] if self.check(';') else [self.expression()]
        self.expect(';', 'al finalizar return')
        return ASTNode('Return', children=children, line=tok.line, column=tok.column)

    def expression(self) -> ASTNode:
        return self.equality()

    def equality(self) -> ASTNode:
        return self.binary(self.comparison, {'==', '!='})

    def comparison(self) -> ASTNode:
        return self.binary(self.term, {'<', '<=', '>', '>='})

    def term(self) -> ASTNode:
        return self.binary(self.factor, {'+', '-'})

    def factor(self) -> ASTNode:
        return self.binary(self.unary, {'*', '/', '%'})

    def binary(self, next_level, operators) -> ASTNode:
        node = next_level()
        while self.current.value in operators and not self.at_end():
            op = self.advance()
            right = next_level()
            node = ASTNode('OpBinaria', op.value, [node, right], op.line, op.column)
        return node

    def unary(self) -> ASTNode:
        if self.check('!', '-'):
            op = self.advance()
            return ASTNode('OpUnaria', op.value, [self.unary()], op.line, op.column)
        return self.primary()

    def primary(self) -> ASTNode:
        tok = self.current
        if tok.type in LITERALS:
            self.advance()
            return ASTNode(LITERALS[tok.type], tok.value, line=tok.line, column=tok.column)
        if tok.type == 'ID':
            self.advance()
            if self.check('('):
                self.advance()
                args = []
                if not self.check(')'):
                    while True:
                        args.append(self.expression())
                        if not self.check(','):
                            break
                        self.advance()
                self.expect(')', 'al cerrar los argumentos')
                return ASTNode('Llamada', tok.value, args, tok.line, tok.column)
            return ASTNode('Identificador', tok.value, line=tok.line, column=tok.column)
        if self.check('('):
            self.advance()
            node = self.expression()
            self.expect(')', 'al cerrar la expresión')
            return node
        raise self.error(f"Se esperaba una expresión pero se encontró {self.describe(tok)}")
