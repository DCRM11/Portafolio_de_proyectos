# Selección de regiones para perforación de pozos
Daniel Rodríguez · Ciencia de datos aplicada al sector energético

Copia de presentación de un caso académico de TripleTen. No corresponde a una implementación empresarial ni a un proyecto del Ministerio de Minas y Energía.

## Pregunta de negocio
¿Cómo comparar tres regiones al seleccionar 200 pozos según sus volúmenes predichos y evaluar el beneficio bajo los supuestos económicos del ejercicio?

El flujo combina exploración, regresión lineal, selección por predicción y remuestreo de pares para estimar la distribución del beneficio. `f0`, `f1` y `f2` son variables anónimas: no se les atribuye significado geológico sin un diccionario de datos.

## Estado de validación
El código del original fue revisado y la lógica económica se corrigió en esta copia. No se han reejecutado los modelos con los CSV del caso; no se publican métricas nuevas, probabilidades de pérdida ni una región ganadora. Las salidas y comentarios del notebook original permanecen intactos en el repositorio.

## Abrir y ejecutar
1. Instalar las dependencias de `requirements.txt` en un entorno aislado.
2. Obtener por medios autorizados `geo_data_0.csv`, `geo_data_1.csv` y `geo_data_2.csv`; no están incluidos.
3. Abrir `Seleccion_regiones_presentacion.ipynb` desde esta carpeta y ajustar `DATA_DIR`.
4. Revisar identificadores repetidos y documentar su tratamiento antes de dividir. El cargador se detiene si los detecta; no elimina observaciones automáticamente.
5. Confirmar en el enunciado cuántos candidatos se evalúan por réplica y el límite de riesgo admisible; completar las dos variables pendientes.
6. Ejecutar todas las celdas y revisar las tablas, gráficos y conclusiones antes de publicar resultados.

## Supuestos conservados del código original
- Presupuesto total: USD 100 millones.
- Selección: 200 pozos.
- Ingreso por unidad de `product`: USD 4.500; el original expresa `product` en miles de barriles.
- División de entrenamiento/validación: 75/25, semilla 42.
- Bootstrap: 1.000 réplicas, ahora con semilla explícita.

El umbral aritmético de equilibrio es 111,11 unidades por pozo seleccionado. Compararlo con el promedio regional completo no determina la rentabilidad de una selección de los mejores pozos.

## Correcciones de esta copia
| Hallazgo en el original | Tratamiento |
|---|---|
| Suma volúmenes predichos para valorar el resultado | Ordena por predicción y evalúa el volumen real de los seleccionados |
| Llama ganancia al ingreso sin restar USD 100 millones | Calcula beneficio simplificado = volumen real × ingreso unitario − presupuesto |
| Bootstrap sobre todas las predicciones de validación | Remuestrea pares, selecciona 200 por predicción dentro de cada muestra y evalúa beneficio |
| Bootstrap sin semilla | Generador reproducible |
| Riesgo de 0 % y recomendación basados en ese cálculo | Se retiran de la copia; se recalculan cuando estén los datos y parámetros confirmados |
| Atribución especulativa de significado a f2 | Variables tratadas como anónimas |
| Correlación que incluye identificador textual | Selección explícita de columnas numéricas |
| Cifra narrativa 38.881,46 frente a salida 30.881,46 | No se reutiliza ninguna como resultado validado |

## Límites
El beneficio es una simplificación del ejercicio: no es flujo de caja descontado, VAN, TIR ni valoración de reservas certificadas. No incluye un calendario de producción, impuestos, descuento, costos desagregados ni incertidumbre de precios. El bootstrap refleja variabilidad del conjunto de validación bajo un modelo fijo; no captura toda la incertidumbre de entrenamiento, geológica o económica. El remuestreo con reemplazo puede repetir observaciones y representa un experimento estadístico, no una lista física de pozos únicos. Una validación aleatoria no demuestra generalización espacial.

Los percentiles del 2,5 % y 97,5 % describen la distribución bootstrap del beneficio del escenario; no deben presentarse como garantía de rentabilidad ni como intervalo de confianza de la media sin un análisis adicional. La región 1 requiere revisar especialmente la relación casi determinista de sus variables con el objetivo y la procedencia de los datos.
