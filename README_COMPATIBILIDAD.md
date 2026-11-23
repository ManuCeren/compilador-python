# Ajustes de compatibilidad para las Fases 3 y 4

Reemplazar `sintactico.py` y `GRAMATICA.md` en la raíz del proyecto. `main.py` es copia del existente y no necesita reemplazarse.

Cambios: `Declaracion` -> hijos `Variable`; `Funcion.value` -> `tipo nombre`, hijos `[Parametros, Bloque]`; `SentenciaExpresion` y `SentenciaVacia`.

No se modificó `lexer.py`. `For` no está implementado; requiere definir su gramática y reconocer `for` en el lexer. `semantico.py` e `intermedio.py` son plantillas con TODO y no pueden funcionar aún.

Comprobar:
`python main.py tests/sintactico_valido.txt`
`python main.py tests/sintactico_error.txt`
`python main.py tests/compatibilidad_ast.txt`

Ejecutar también los tests léxicos y de precedencia previos.
