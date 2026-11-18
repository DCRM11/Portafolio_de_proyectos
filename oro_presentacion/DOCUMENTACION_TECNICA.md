# Documentación técnica · Recuperación de oro

## Alcance
Copia de presentación independiente. El original se conserva sin cambios. El contexto empresarial pertenece al caso del bootcamp; no es un proyecto del Ministerio de Minas y Energía. El código se revisó y se comprobó con ejemplos sintéticos; no se reentrenó ni se validó con los CSV del caso.

## Ejecución
1. Crear un entorno Python e instalar `requirements.txt`. Las versiones no están fijadas mediante una ejecución completa.
2. Obtener de una fuente autorizada `gold_recovery_train.csv`, `gold_recovery_test.csv` y `gold_recovery_full.csv` y colocarlos en `data/`, o ajustar `DATA_DIR`.
3. Abrir el notebook desde esta carpeta, revisar fechas y esquema y ejecutar en orden.
4. Revisar los registros excluidos por objetivos faltantes o no válidos y documentar la cobertura. No se imputan objetivos.
5. Comparar modelos exclusivamente con validación temporal del entrenamiento. Los hiperparámetros propuestos son configuraciones de partida, no valores optimizados.
6. Usar el conjunto de prueba una vez para evaluar el modelo elegido y la referencia. No ajustar modelos a partir de sus resultados.

## Hallazgos y cambios
| Hallazgo del original | Tratamiento en la copia |
|---|---|
| En la celda 62 se eliminan solo los dos objetivos y quedan 88 predictores, incluidos resultados de proceso ausentes en test y `calculated_recovery` | Usar el esquema de predictores disponible en test y rechazar columnas de salida o cálculo; revisar disponibilidad temporal real |
| Se imputan también las variables objetivo | Entrenar y evaluar solo donde los objetivos están observados y son válidos; informar exclusiones |
| Imputación y normalización previas a validación cruzada; imputación independiente en test | Imputación y escalado en un Pipeline ajustado dentro de cada partición y reutilizado en prueba |
| Interpolación sin particiones y sin una política causal documentada | No interpolar con información futura; usar medianas aprendidas en entrenamiento |
| Selección por MAE y evaluación posterior con sMAPE | Comparar modelos con el mismo sMAPE ponderado: 25 % rougher y 75 % final |
| Divisiones internas de train presentadas como evaluación final de prueba | Mantener test separado y recuperar solo sus etiquetas desde full mediante date, con relación uno a uno |
| IQR aplicado sucesivamente y por separado reduce train a 1.228 registros y test a 200 | No depurar test mediante filtros estadísticos aprendidos en test; preservar sus filas y reportar cobertura |
| Fórmula de recuperación produce infinito y luego se modifica con epsilon | Comprobar la fórmula en datos sin imputar, con denominador válido y condiciones físicas explícitas; reportar filas no comparables |
| No hay referencia simple | Comparar también con un predictor de la media |

El filtro `dropna(thresh=...)` de la celda 20 exige un mínimo de valores presentes; el 30 % usado allí no equivale a eliminar las filas con más de 30 % de ausentes. La copia evita esa regla ambigua y documenta explícitamente los objetivos excluidos.

Las cifras anteriores describen las salidas y el código del original, no resultados de esta versión. No se reutilizan el MAE 0,6405 ni el sMAPE total 1,1242 como evidencia de desempeño validado.

## Evaluación y límites
- sMAPE = media de 200 × |predicción − observación| / (|observación| + |predicción|). El par (0,0) aporta cero por convención explícita. Valores no finitos generan error.
- Orden de objetivos: rougher.output.recovery, final.output.recovery. Menor sMAPE es mejor.
- TimeSeriesSplit preserva el orden temporal dentro de train; no garantiza independencia ni elimina toda fuga. Deben revisarse el horizonte, la autocorrelación, el posible gap entre particiones y la disponibilidad de cada sensor en el instante de predicción.
- El esquema de test delimita las columnas; no certifica que todas estén disponibles antes del resultado objetivo. Requiere validación con el diccionario de datos y el proceso industrial.
- full nunca se usa para entrenar ni imputar; únicamente permite asociar por fecha las etiquetas de prueba.
- Verificar que las fechas de train y test no se solapen. La prueba suministrada puede intercalar periodos: su resultado no demuestra por sí solo predicción de un periodo completamente futuro.
- No se recortan predicciones a 0–100 para mejorar la métrica; se cuenta cuántas filas salen de ese rango.
- No se atribuye causalidad, optimización operacional, ahorro ni despliegue. Faltan los datos para establecer resultados y conclusiones.
