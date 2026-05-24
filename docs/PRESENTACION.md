# Guion y Estructura de la Presentación (15 minutos)

Este documento contiene la estructura detallada diapositiva por diapositiva que debes plasmar en tu material de soporte (**Google Slides / PowerPoint**) y utilizar como guion durante la exposición ante la **Gerencia Comercial y Técnica**.

---

## Estructura de Diapositivas

### Diapositiva 1: Portada y Presentación del Proyecto
* **Título:** Inteligencia Territorial: Análisis y Predicción de Criminalidad en Argentina
* **Subtítulo:** Optimización de ventas de seguridad y tarificación de riesgos de seguros mediante Ciencia de Datos.
* **Contenido Visual:** Logo del proyecto o una balanza de la justicia con un gráfico ascendente.
* **Notas del Orador (1 min):** 
  > *"Buenas tardes a todos. Hoy les presentamos un proyecto de datos diseñado para transformar la manera en que tomamos decisiones de expansión comercial y fijación de precios en el sector de seguros y seguridad privada, pasando de decisiones reactivas a decisiones predictivas basadas en datos oficiales de la Nación."*

---

### Diapositiva 2: Definición del Dominio y Problemática
* **Título:** El Reto de la Toma de Decisiones en Seguridad y Seguros
* **Contenido:**
  - **El Problema:** La criminalidad en Argentina varía drásticamente según la provincia y el año. Las aseguradoras de hogar/autos pierden rentabilidad al cobrar primas idénticas en regiones con riesgos muy dispares (asimetría de información).
  - **La Oportunidad:** Centralizar y explotar los datos del Sistema Nacional de Información Criminal (SNIC) para predecir siniestros futuros y segmentar comercialmente el país.
* **Notas del Orador (2 min):**
  > *"Tradicionalmente, las tarifas de seguros de robos se definen de forma estática o por mera intuición. Esto genera que subestimemos el riesgo en zonas críticas, impactando en la rentabilidad de las pólizas, o que perdamos clientes en áreas de bajo delito por cobrar tarifas excesivas. Proponemos solucionar esto mediante la centralización y modelado de datos."*

---

### Diapositiva 3: Hipótesis de Negocio y Propuesta de Valor
* **Título:** Hipótesis del Proyecto: De los Datos a la Rentabilidad
* **Contenido:**
  - **Hipótesis:** *"La centralización de los datos del SNIC y su modelado predictivo con series temporales nos permite segmentar geográficamente el riesgo y anticipar la tendencia nacional, optimizando recursos y maximizando la rentabilidad comercial."*
  - **Audiencias Clave:**
    - **Gerencia Comercial:** Dónde vender más (volumen absoluto).
    - **Gerencia Técnica:** Cómo cobrar adecuadamente (tasa de siniestralidad por cada 100k hab.).
* **Notas del Orador (2 min):**
  > *"Nuestra hipótesis se divide en dos enfoques: el comercial y el técnico. La gerencia comercial necesita volumen de ventas. La gerencia técnica necesita precisión técnica de riesgo. Ambas necesidades son resueltas por nuestro dashboard analítico e interactivo."*

---

### Diapositiva 4: Arquitectura de la Solución (Pipeline)
* **Título:** Tubería de Datos Automatizada (ETL y ML)
* **Contenido:**
  - **Ingesta:** Carga automática de los CSVs oficiales del SNIC.
  - **ETL (Pandas):** Limpieza, tipado de datos y agregación.
  - **Modelo Predictivo (Prophet):** Modelo univariado ajustado de series de tiempo.
  - **Presentación (Streamlit + Plotly):** Interfaz interactiva para el usuario final.
* **Notas del Orador (2 min):**
  > *"Desarrollamos una tubería reproducible en Python. Los datos crudos pasan por un proceso de ETL con pandas para asegurar la calidad. El modelo Prophet genera las proyecciones y se sirve en una interfaz web liviana hecha en Streamlit para que cualquier ejecutivo comercial pueda interactuar con ella sin saber programar."*

---

### Diapositiva 5: Hallazgos Clave del EDA (Visualización y Storytelling)
* **Título:** Revelaciones de los Datos Históricos (EDA)
* **Contenido:**
  - **Volumen vs Tasa:** Buenos Aires tiene el mayor número absoluto de delitos (mercado masivo para ventas), pero provincias como Neuquén o CABA tienen tasas por habitante mucho más elevadas (mayor riesgo técnico de seguros).
  - **Tipología:** Los delitos contra la propiedad (robos y hurtos) abarcan más del 70% de las incidencias nacionales.
  - **El Outlier de 2020:** Desplome del registro delictivo por la cuarentena.
* **Notas del Orador (3 min):**
  > *"Aquí radica el núcleo del valor comercial: no debemos confundir cantidad de delitos con tasa de criminalidad. CABA y Neuquén tienen menor población y menos delitos absolutos que la Provincia de Buenos Aires, pero el riesgo por habitante es superior. Por ende, en Neuquén debemos cobrar primas más caras para compensar el riesgo. Asimismo, confirmamos que el robo común es el delito predominante."*

---

### Diapositiva 6: Modelado y Tratamiento Estadístico
* **Título:** Predicción mediante Series Temporales con Prophet
* **Contenido:**
  - **Algoritmo:** Prophet (desarrollado por Meta).
  - **Manejo del COVID-19:** Se neutralizó el año 2020 como valor atípico para evitar distorsiones negativas en la tendencia futura.
  - **Intervalos de Confianza (Banda de Riesgo):** Estimaciones superiores del 80% de certeza para previsión de fondos de siniestralidad.
* **Notas del Orador (2 min):**
  > *"A nivel técnico, la cuarentena del 2020 distorsionó las series temporales en todo el mundo. Si entrenamos un modelo convencional, proyectará una tendencia a la baja irreal. Con Prophet, marcamos 2020 como nulo, y el modelo interpola la tendencia real. Además, nos brinda intervalos de confianza al 80%, que la Gerencia Técnica puede usar como la banda de máxima delincuencia para resguardo de capital."*

---

### Diapositiva 7: Demostración de la Aplicación Streamlit
* **Título:** Demo en Vivo: Inteligencia delictiva en tiempo real
* **Contenido:**
  - Mostrar la aplicación Streamlit corriendo localmente.
  - Explicar las pestañas de Panorama Nacional, Análisis Provincial, y la pestaña de Predicciones.
  - Simular la predicción de una provincia y la descarga de los resultados en CSV.
* **Notas del Orador (2 min):**
  > *(Muestra la pantalla de Streamlit)* *"Como ven, el dashboard es totalmente interactivo. En la pestaña de predicciones, podemos elegir predecir a nivel Nacional o seleccionar una Provincia específica, ajustar los años de predicción y descargar la tabla de datos en CSV para que el equipo de suscripción pueda meter los datos en Excel de inmediato."*

---

### Diapositiva 8: Conclusión y Retorno de Negocio
* **Título:** Conclusiones y Próximos Pasos comerciales
* **Contenido:**
  - **Hipótesis Validada:** Los datos del SNIC y Prophet permiten tarificar con precisión técnica y dirigir comercialmente la venta de seguridad.
  - **Ventaja Competitiva:** Cotización dinámica de pólizas en segundos.
  - **Próximos pasos:** Integración de la API de predicciones en el cotizador web de la empresa.
* **Notas del Orador (1 min):**
  > *"En conclusión, la plataforma está lista para producción. Nos permite optimizar campañas comerciales en focos de volumen e incrementar las tarifas base de seguros en zonas de alta siniestralidad relativa. Estamos listos para sus preguntas. Muchas gracias."*
