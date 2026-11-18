# Documentación técnica · Demanda horaria de taxis

## Alcance y horizonte
Copia de presentación del caso académico, conservando el original. Se pronostica el total de pedidos de la hora t al comienzo de esa hora, suponiendo que el conteo de t−1 ya está disponible. Tras cada hora se incorpora el conteo observado para el siguiente pronóstico. El modelo permanece fijo durante la prueba.

Este flujo es de un paso con historia actualizada. No representa un pronóstico simultáneo de todo el bloque futuro ni un despliegue. Si los conteos llegan con retraso, deben desplazarse nuevamente las variables según la latencia real.

## Ejecución
1. Instalar `requirements.txt` en un entorno aislado. Las versiones quedan pendientes de fijar tras una ejecución completa.
2. Obtener `taxi.csv` de una fuente autorizada, colocar en `data/` o ajustar `DATA_DIR`. No se incluye el CSV.
3. Abrir el notebook desde esta carpeta y ejecutar en orden.
4. Revisar fechas, intervalos, horas incompletas y conteos. El cargador se detiene ante anomalías: no convierte huecos en demanda cero.
5. Reservar el 10 % final de las horas antes de explorar y comparar modelos. Eliminar solo la historia inicial insuficiente para construir variables.
6. Comparar modelos y referencias con TimeSeriesSplit en el 90 % anterior. Elegir por RMSE medio de validación, sin consultar el bloque de prueba.
7. Evaluar una vez el elegido y las dos referencias en el bloque reservado. No ajustar modelos a partir de este resultado.

## Hallazgos y cambios
| Hallazgo del original | Tratamiento en la copia |
|---|---|
| Celda 26: train_test_split sin shuffle=False mezcla fechas | División cronológica: último 10 % reservado |
| Celdas 22/27: rolling sin shift incluye el objetivo de la propia hora | Media móvil calculada sobre shift(1) |
| Celda 27: retardos creados después de definir X_train y X_test; la salida de celda 28 contiene solo cuatro predictores | Variables creadas antes de dividir, con funciones explícitas y controles |
| Celda 29: faltantes imputados usando la media de test | No imputar con estadísticas de prueba; retirar únicamente el periodo inicial sin historia |
| Se comparan seis modelos sobre la misma prueba | Elegir por validación temporal de train y consultar prueba al final |
| Celda 39: gráfico utiliza métricas escritas manualmente y mezcla escalas | Tablas y gráficos derivados de resultados calculados, con RMSE separado de R² |
| Repetición de métricas presentada como confirmación de estabilidad | Desviación entre particiones temporalmente ordenadas, sin confundirla con intervalo de confianza |
| Conteos repetidos se contabilizan como filas duplicadas | Un conteo repetido es válido; la clave temporal debe ser única |

No se reutilizan RMSE 20,62 ni R² 0,7845 del original como desempeño validado. La copia compara regresión lineal, árbol, bosque y HistGradientBoosting de scikit-learn; este último es una nueva configuración propuesta, no una reproducción de LightGBM/XGBoost/CatBoost ni un modelo ya validado.

## Decisiones y límites
- Retardos: 1, 2, 3, 6, 12 y 24 horas. Medias móviles: 24 y 168 horas. Calendario: hora y día de semana.
- La agregación utiliza únicamente num_orders. Se esperan seis observaciones por hora en una grilla regular de diez minutos; revisar el supuesto si cambia el dataset.
- EDA y selección se restringen al periodo de entrenamiento. La descomposición con filtros centrados es descriptiva y nunca se usa como predictor.
- Las variables de una hora pueden usar pedidos de horas de validación/prueba ya observadas, porque el escenario se define como secuencial de un paso. No pueden usar la hora actual ni horas futuras.
- Configuraciones de modelos propuestas, sin búsqueda de hiperparámetros. No se afirma que sean óptimas. El escalado de la regresión está dentro de un Pipeline y se aprende en cada partición.
- Referencias: repetir el conteo de la hora anterior o el de la misma hora del día anterior. Si una referencia gana, se comunica ese resultado.
- Predicciones negativas se reportan, sin recortarlas silenciosamente para mejorar métricas.
- Revisar zona horaria, horario de verano, latencia, deriva de demanda, cobertura temporal y estabilidad en periodos adicionales.
- No se fija un umbral de aceptación que no se haya confirmado en el enunciado. Un error bajo no demuestra ahorro ni una mejor asignación real de conductores.
- Faltan los datos para generar gráficos reales, métricas comparables y una conclusión de desempeño.
