# Daniel Rodríguez | Ciencia de datos y sector energético

Ingeniero de Petróleos y Magíster en Ingeniería de Petróleos, con formación en Ciencia de Datos. Mi interés profesional es integrar el conocimiento del sector energético con Python, análisis estadístico y machine learning para estudiar problemas industriales y aportar evidencia para la toma de decisiones.

Este portafolio reúne **12 notebooks formativos** desarrollados durante mi formación en TripleTen: diez casos de análisis y modelado y dos cuadernos de ejercicios. Los resultados pertenecen a contextos académicos; no representan implementaciones empresariales en producción.

[Perfil profesional en LinkedIn](https://www.linkedin.com/in/daniel-c-rodriguez-m/)

## Tres proyectos para empezar

### 1. Selección de regiones para perforación de pozos

Análisis de tres regiones petroleras para estimar reservas mediante regresión lineal y comparar rentabilidad y riesgo de inversión mediante remuestreo bootstrap. Integra conocimiento del negocio petrolero, evaluación predictiva con RMSE y análisis de incertidumbre.

[Ver presentación del proyecto](pozos_presentacion/README.md) · [Proyecto Sprint 11.ipynb](Proyecto%20Sprint%2011.ipynb)

### 2. Predicción de recuperación de oro

Caso académico de modelado de un proceso industrial. Incluye exploración y preparación de datos, comparación de modelos de regresión y validación cruzada para estudiar la recuperación de oro. El contexto empresarial corresponde al caso de estudio del bootcamp.

[Ver presentación de recuperación de oro](oro_presentacion/README.md) · [Proyecto - Sprint 12.ipynb](Proyecto%20-%20Sprint%2012.ipynb)

### 3. Predicción de pedidos de taxis por hora

Análisis de demanda horaria con series temporales, construcción de variables y comparación de modelos de machine learning para pronosticar pedidos.

[Ver presentación de demanda de taxis](taxis_presentacion/README.md) · [Proyecto Sprint 15.ipynb](Proyecto%20Sprint%2015.ipynb)

## Catálogo de casos de estudio

| Sector | Proyecto | Enfoque | Notebook |
|---|---|---|---|
| Petróleo | Selección de regiones para perforación | Regresión lineal, estimación de reservas y evaluación de rentabilidad y riesgo con bootstrap. | [Proyecto Sprint 11.ipynb](Proyecto%20Sprint%2011.ipynb) |
| Procesos industriales | Predicción de recuperación de oro | Preparación de datos de proceso, regresión y validación cruzada. | [Proyecto - Sprint 12.ipynb](Proyecto%20-%20Sprint%2012.ipynb) |
| Movilidad | Predicción de pedidos de taxis por hora | Series temporales, variables temporales y comparación de modelos predictivos. | [Proyecto Sprint 15.ipynb](Proyecto%20Sprint%2015.ipynb) |
| Telecomunicaciones | Abandono de clientes — Interconnect | Preparación e integración de datos y comparación de modelos de clasificación. | [Proyecto Final.ipynb](Proyecto%20Final.ipynb) |
| Banca | Abandono de clientes — Beta Bank | Clasificación, desequilibrio de clases y evaluación con F1 y AUC-ROC. | [Proyecto - Sprint 10.ipynb](Proyecto%20-%20Sprint%2010.ipynb) |
| Telecomunicaciones | Clasificación de planes — Megaline | Clasificación entre Smart y Ultra según consumo de llamadas, mensajes y datos. | [Proyecto Sprint 9.ipynb](Proyecto%20Sprint%209.ipynb) |
| Automoción | Precios de vehículos usados | Regresión y comparación de calidad predictiva y tiempos de entrenamiento. | [Proyecto Sprint 14.ipynb](Proyecto%20Sprint%2014.ipynb) |
| Seguros | Similitud de clientes y prestaciones | Vecinos cercanos, clasificación, regresión lineal y transformaciones matriciales. | [Proyecto Sprint 13.ipynb](Proyecto%20Sprint%2013.ipynb) |
| Comercio | Ventas y mercado de videojuegos | Análisis exploratorio por plataforma, género y región y pruebas de hipótesis. | [Proyecto - Sprint 6.ipynb](Proyecto%20-%20Sprint%206.ipynb) |
| Movilidad | Viajes en taxi — Chicago | Análisis de resultados de consultas SQL y contraste de duraciones según condiciones meteorológicas. | [Proyecto Sprint 8.ipynb](Proyecto%20Sprint%208.ipynb) |

## Cuadernos de ejercicios

| Cuaderno | Contenido verificado | Notebook |
|---|---|---|
| Procesamiento de lenguaje natural | Limpieza y lematización con spaCy; bolsas de palabras, n-gramas y TF-IDF; regresión logística para clasificar reseñas de IMDb. | [Sprint 16.ipynb](Sprint%2016.ipynb) |
| Redes neuronales y visión artificial | Prácticas con Keras y TensorFlow: regresión, clasificación, preparación de imágenes y aumento de datos. | [Sprint 17.ipynb](Sprint%2017.ipynb) |

## Herramientas

Según el notebook: Python, Pandas, NumPy, scikit-learn, SciPy, Matplotlib, Seaborn, XGBoost, LightGBM, CatBoost, spaCy, NLTK, Keras y TensorFlow. El caso de Chicago analiza resultados de consultas SQL exportados a CSV.

## Cómo explorar el portafolio

1. Abre un notebook desde las tablas anteriores para consultar su código, análisis y resultados guardados.
2. Para ejecutarlo localmente, descarga el archivo y ábrelo en un entorno compatible con Jupyter.
3. Revisa los imports y las rutas de datos de ese notebook; instala sus dependencias y adapta las rutas a tu entorno.
4. Ejecuta las celdas en orden y comprueba los resultados antes de reutilizar el análisis.

## Datos, reproducibilidad y alcance

- Esta actualización revisa la documentación y la correspondencia entre los temas y el código. **Los notebooks no se han reejecutado ni auditado de extremo a extremo.**
- Los conjuntos de datos no están incluidos en este repositorio. Varios notebooks utilizan rutas como `/datasets/`; el proyecto final requiere archivos CSV de contratos, servicios y clientes.
- Los resultados guardados corresponden a ejecuciones anteriores. No se añade una tabla de métricas hasta validar su cálculo, particiones de datos y ausencia de fuga de información.
- Se conservan los nombres, el código, las salidas y los comentarios originales del bootcamp. Los enlaces existentes siguen apuntando a los mismos archivos.
- Los cuadernos de ejercicios de textos y visión artificial se presentan según su contenido publicado, sin atribuirles técnicas o aplicaciones que no están documentadas allí.
- La transformación matricial del caso de seguros es un ejercicio de álgebra aplicada; no equivale a cifrado ni constituye una garantía de protección de datos.

## Próximos pasos técnicos

- Crear copias de presentación de los tres proyectos destacados, manteniendo intactos los originales.
- Documentar la procedencia y disponibilidad de los datos y las dependencias de cada caso.
- Verificar las particiones temporales, el preprocesamiento y las métricas antes de publicar resultados comparativos.
