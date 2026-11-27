# Gramática propuesta — Fase 2

**Nota:** el catedrático proporcionó una plantilla que remite a `GRAMATICA.md`, pero no entregó ese archivo. Esta gramática es una propuesta del equipo y debe validarse con él. La rúbrica exige `for`; se incorpora según el contrato visible de intermedio.py.

Notación: `*` significa cero o más repeticiones; `?` significa opcional; `|` significa alternativa.

```ebnf
programa         = sentencia* ;
sentencia        = declaracion | funcion | asignacion | llamada ";" | bloque | if | while | for | retorno | ";" ;
declaracion      = tipo ID ("=" expresion)? ";" ;
funcion          = (tipo | "void") ID "(" parametros? ")" bloque ;
parametros       = parametro ("," parametro)* ;
parametro        = tipo ID ;
tipo             = "int" | "float" | "string" ;
asignacion       = ID "=" expresion ";" ;
bloque           = "{" sentencia* "}" ;
if               = "if" "(" expresion ")" sentencia ("else" sentencia)? ;
while            = "while" "(" expresion ")" sentencia ;
for              = "for" "(" (declaracion | asignacion | expresion? ";") expresion? ";" (ID "=" expresion | expresion)? ")" sentencia ;
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
- `Declaracion`: `value` es tipo; `children` contiene nodos `Variable`.
- `Variable`: `value` es nombre; `children[0]` opcional es inicializador.
- `Asignacion`: `value` es nombre; `children[0]` es expresión.
- `Identificador`: `value` es nombre.
- `Entero`, `Flotante`, `Cadena`: `value` es lexema literal.
- `OpBinaria`: `value` es operador; `children` son operandos izquierdo y derecho.
- `OpUnaria`: `value` es operador; `children[0]` es operando.
- `If`: `children[0]` es `Condicion`, `children[1]` es `Entonces`, `children[2]` opcional es `SiNo`.
- `While`: `children[0]` es `Condicion`; `children[1]` es sentencia cuerpo.
- `For`: hijos opcionales `Inicio`, `Condicion`, `Paso` (cada uno envuelve un nodo), en ese orden; el último hijo siempre es el cuerpo. `Inicio` puede contener una declaración, asignación o expresión; `Paso` una asignación o expresión. Las partes ausentes se omiten.
- `Funcion`: `value` es `"tipo nombre"` (por ejemplo, `"int sumar"`); `children[0]` es `Parametros` y `children[1]` es `Bloque`.
- `Parametro`: `value` es tipo; `children[0]` es `Identificador`.
- `Return`: cero o un hijo expresión.
- `Llamada`: `value` es nombre; `children` son argumentos.
- `SentenciaExpresion`: `children[0]` es una llamada.
- `SentenciaVacia`: no tiene hijos.

La verificación semántica se realizará después; el archivo `Verificador.py` del docente usa tuplas y necesita un adaptador para este AST.

## Compatibilidad con las plantillas posteriores

La Fase 3 debe decorar con `.type` los nodos de expresión; la Fase 2 no realiza análisis de tipos. La plantilla de Fase 4 contempla `For`; su TODO confirma los nombres de los envoltorios opcionales y el cuerpo final. El catedrático no entregó el enunciado completo al que hacen referencia los TODO, por lo que la integración definitiva debe validarse al desarrollar las Fases 3 y 4.
