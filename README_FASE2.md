# Integración Fase 2

Copiar `sintactico.py`, `main.py` y `GRAMATICA.md` a la raíz del repositorio existente. Copiar los archivos de `tests/` a su carpeta `tests/`. **No reemplazar `lexer.py`**.

## Ejecutar

```powershell
python main.py tests/sintactico_valido.txt
python main.py tests/sintactico_error.txt
```

## Nota

Se utiliza `Token` y `Lexer` del `lexer.py` del proyecto existente. El parser no valida tipos, declaraciones previas, valores de retorno ni ámbito: son comprobaciones de Fase 3. La gramática es propuesta del equipo; el catedrático no suministró `GRAMATICA.md`.

## Limitaciones

No incluye `for`, operadores lógicos `&&` / `||`, `break`, `continue` ni asignaciones encadenadas. La recuperación de errores es por puntos de sincronización y puede generar errores adicionales en entradas malformadas.
