# Gramática propuesta — Fase 2

**Nota:** el catedrático proporcionó una plantilla que remite a `GRAMATICA.md`, pero no entregó ese archivo. Esta gramática es una propuesta del equipo y debe validarse con él. No se implementa `for` porque no está confirmado que `lexer.py` reconozca esa palabra reservada.

Notación: `*` significa cero o más repeticiones; `?` significa opcional; `|` significa alternativa.

```ebnf
programa         = sentencia* ;
sentencia        = declaracion | funcion | asignacion | llamada ";" | bloque | if | while | retorno ;
declaracion      = tipo ID ("=" expresion)? ";" ;
funcion          = (tipo | "void") ID "(" parametros? ")" bloque ;
parametros       = parametro ("," parametro)* ;
parametro        = tipo ID ;
tipo             = "int" | "float" | "string" ;
asignacion       = ID "=" expresion ";" ;
bloque           = "{" sentencia* "}" ;
if               = "if" "(" expresion ")" sentencia ("else" sentencia)? ;
while            = "while" "(" expresion ")" sentencia ;
retorno          = "return" expresion? ";" ;
expresion        = igualdad ;
igualdad         = comparacion (("==" | "!=") comparacion)* ;
comparacion      = termino ((">" | ">=" | "<" | "<=") termino)* ;
termino          = factor (("+" | "-") factor)* ;
factor           = unario (("*" | "/" | "%") unario)* ;
unario           = ("!" | "-") unario | primario ;
primario         = INT_LITERAL | FLOAT_LITERAL | STRING_LITERAL | ID | llamada | "(" expresion ")" ;
llamada          = ID "(" argumentos? ")" ;
argumentos       = expresion ("," expresion)* ;
```

## Contrato AST para la Fase 3

- `Programa`: `children` son sentencias.
- `Bloque`: `children` son sentencias y abre ámbito.
- `Declaracion`: `value` es tipo; `children[0]` es `Identificador`; `children[1]` opcional es inicializador.
- `Asignacion`: `value` es nombre; `children[0]` es expresión.
- `Identificador`: `value` es nombre.
- `Entero`, `Flotante`, `Cadena`: `value` es lexema literal.
- `OpBinaria`: `value` es operador; `children` son operandos izquierdo y derecho.
- `OpUnaria`: `value` es operador; `children[0]` es operando.
- `If`: `children[0]` es `Condicion`, `children[1]` es `Entonces`, `children[2]` opcional es `SiNo`.
- `While`: `children[0]` es `Condicion`; `children[1]` es sentencia cuerpo.
- `Funcion`: `value` es nombre; `children` son `TipoRetorno`, `Parametros`, `Bloque`.
- `Parametro`: `value` es tipo; `children[0]` es `Identificador`.
- `Return`: cero o un hijo expresión.
- `Llamada`: `value` es nombre; `children` son argumentos.
- `ExpresionSentencia`: `children[0]` es una llamada.

La verificación semántica se realizará después; el archivo `Verificador.py` del docente usa tuplas y necesita un adaptador para este AST.
