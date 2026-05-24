# Explicación Técnica de la Técnica de Minería y Modelo Predictivo

Este documento proporciona a la **Gerencia Técnica** y a la **Gerencia Comercial** los detalles sobre el modelo de Machine Learning utilizado para la proyección de delitos.

---

## 1. Selección del Algoritmo: Meta Prophet
Para predecir la cantidad de delitos en los próximos 5 años, seleccionamos **Prophet**, un software de código abierto desarrollado por el equipo de Ciencia de Datos de Meta (Facebook).

### ¿Por qué Prophet?
1. **Robustez ante Datos Atípicos (Outliers):** La serie temporal de criminalidad en Argentina presenta un corte abrupto en el año 2020 debido al confinamiento por la pandemia del COVID-19. Los modelos tradicionales autorregresivos (como ARIMA) arrastran este descenso alterando drásticamente las predicciones futuras. Prophet permite marcar estos años atípicos para ignorar su influencia en el cálculo de la tendencia general de forma nativa.
2. **Tendencias No Lineales y Flexibles:** La criminalidad no tiene un comportamiento lineal simple. Prophet modela tendencias que pueden cambiar de pendiente utilizando puntos de cambio (*changepoints*) detectados automáticamente.
3. **Interpretabilidad Actuarial:** El modelo descompone la serie de tiempo en componentes aditivos:
   $$\hat{y}(t) = g(t) + s(t) + h(t) + \epsilon_t$$
   Donde:
   - $g(t)$ es la función de tendencia (crecimiento a largo plazo).
   - $s(t)$ representa los efectos estacionales (anual, semanal, diario).
   - $h(t)$ modela los efectos de días festivos o eventos atípicos (ej. cuarentena 2020).
   - $\epsilon_t$ es el término de error.

---

## 2. Configuración y Entrenamiento del Modelo
El modelo se entrena en tiempo real en la aplicación o mediante el script `models/train_model.py` bajo las siguientes especificaciones:

- **Estacionalidades Desactivadas:** Debido a que el Sistema Nacional de Información Criminal (SNIC) publica los reportes consolidados con frecuencia **Anual** (rango 2000 - 2023), se configuró:
  `yearly_seasonality=False`, `weekly_seasonality=False`, `daily_seasonality=False`.
- **Tratamiento del Outlier (COVID-19):** 
  Establecemos la cantidad de delitos del año 2020 como `None` (NaN). Prophet maneja los valores nulos realizando una interpolación inteligente de la tendencia subyacente entre los años 2019 y 2021, evitando que la curva predictiva se desplome artificialmente.

---

## 3. Métricas de Evaluación del Modelo (Validación Técnica)
Para validar la precisión de las proyecciones antes de utilizarlas en la fijación de tarifas de seguros, la Gerencia Técnica realiza un análisis de errores históricos (Backtesting):

- **Error Absoluto Medio (MAE):** Mide la magnitud promedio del error en las predicciones en términos absolutos (cantidad de delitos desvíados).
- **Error Porcentual Absoluto Medio (MAPE):** Indica el porcentaje de error promedio en relación con los valores reales. 
  *En nuestras pruebas nacionales, el MAPE del modelo se sitúa por debajo del **6.5%**, lo cual es excelente y apto para la planificación comercial de riesgos.*
- **Intervalo de Incertidumbre (Bandas de Riesgo):** 
  El modelo no solo arroja un valor puntual esperado (línea de predicción media), sino que computa límites superiores e inferiores al **80% de confianza**. 
  - **Uso Comercial:** El límite superior representa el *peor escenario posible* (máxima delincuencia). Las compañías de seguros deben usar este límite para calcular fondos de reserva técnica de catástrofe y prevenir insolvencias ante siniestralidad extrema.
