# Ajustes de Fases 1 y 2

Copiar los cuatro archivos principales y agregar los nuevos tests. Se conserva caso_valido.txt original; tras verificar el promedio con las fases 3 y 4, copiar caso_promedio_rubrica.txt a caso_valido.txt para cumplir la rúbrica.

--tokens imprime tokens y mantiene validación sintáctica; --ast imprime AST; juntos muestran ambos. Sin opciones se conserva la salida anterior. --cuadruplos y --asm quedan para Fase 4.

For usa envoltorios opcionales Inicio, Condicion, Paso y cuerpo final según TODO de intermedio.py. No se añade ++ ni --: se usa i = i + 1. Las expresiones de inicio/paso requieren soporte en las fases posteriores. % y ! ya estaban en la gramática del parser; verificar soporte semántico y MIPS.

Los casos de promedio, recursión y división solo se validan léxica y sintácticamente aquí; resultados previstos en MARS: 9; 1, 2, 6, 24, 120; error de división entre cero, respectivamente.
