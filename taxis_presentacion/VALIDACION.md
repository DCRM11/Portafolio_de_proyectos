# Validación realizada
- Sintaxis del módulo y de todas las celdas del notebook: comprobada.
- Causalidad: modificar el objetivo actual y el futuro no cambia los predictores de esa hora; comprobado con serie sintética.
- Lag de una hora y media móvil desplazada de 24 horas: comprobados contra cálculos explícitos.
- División cronológica con último 10 % reservado y alineación de índices: comprobadas.
- Flujo sintético de validación temporal, comparación de cuatro modelos y dos referencias, y evaluación final: completado.
- Agregación horaria: suma de seis observaciones; rechazo de huecos, fechas repetidas y horas incompletas: comprobados.
- No se ejecutó con taxi.csv real. Las pruebas sintéticas no son resultados del caso y no establecen desempeño ni modelo ganador.
- El notebook original no se modifica.
