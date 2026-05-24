# Administración del Proyecto (Metodologías Ágiles)

Este documento detalla la gestión del proyecto mediante metodologías ágiles (**Scrum / Kanban**), demostrando la organización del equipo para cumplir con las expectativas del trabajo.

---

## 1. Estructura de Roles en el Equipo
Para asegurar el éxito del proyecto, dividimos el equipo en los siguientes roles Scrum:
- **Product Owner (PO):** Responsable de priorizar el Product Backlog en función del valor para el negocio (representando la perspectiva de la Gerencia Comercial y Actuarial).
- **Scrum Master (SM):** Encargado de remover impedimentos del equipo, guiar las ceremonias ágiles y facilitar el tablero Kanban.
- **Data Engineering / Analytics Team (Developers):** Desarrolladores encargados del pipeline ETL, modelado predictivo (`Prophet`) y la interfaz interactiva en Streamlit.

---

## 2. Planificación de Sprints (Sprints Backlog)
El proyecto se dividió en **3 Sprints** de 1 semana de duración cada uno:

### Sprint 1: Ingesta de Datos y Pipeline ETL
* **Objetivo del Sprint:** Garantizar que los datos crudos del SNIC se limpien, unifiquen y guarden en un formato optimizado.
- **Entregables:** Scripts `data_loader.py` y `etl.py` con datasets limpios listos para modelar en la carpeta `processed/`.

### Sprint 2: EDA y Modelado Predictivo
* **Objetivo del Sprint:** Extraer conclusiones iniciales de los datos históricos y ajustar el algoritmo de predicción a 5 años.
- **Entregables:** Notebook `EDA.ipynb` completamente documentado y el modelo serializado `prophet_model.pkl`.

### Sprint 3: Aplicación Interactiva y Soporte de Exposición
* **Objetivo del Sprint:** Crear la interfaz interactiva en Streamlit y preparar el material visual e hipótesis de valor de negocio para las gerencias.
- **Entregables:** Dashboard interactivo `app.py`, documentación en la carpeta `docs/` y guion de presentación.

---

## 3. Tablero Kanban & Historias de Usuario (User Stories)

A continuación se muestran ejemplos de las historias de usuario que guiaron el desarrollo:

### Historia de Usuario 1: Visualización Provincial
* **Como** suscriptor técnico de seguros de hogar,  
* **quiero** ver la composición porcentual de delitos por cada provincia argentina en una gráfica interactiva,  
* **para** poder calibrar las pólizas según el tipo de robo más común en cada jurisdicción.
- **Criterios de Aceptación:**
  1. El usuario debe poder seleccionar cualquier provincia de un menú desplegable.
  2. Debe graficarse un gráfico de torta (Pie Chart) con el top 10 de delitos.
  3. Los datos deben actualizarse instantáneamente al cambiar de provincia.

### Historia de Usuario 2: Proyecciones a Futuro
* **Como** gerente comercial de seguridad privada,  
* **quiero** proyectar la cantidad esperada de crímenes a nivel nacional y provincial para los próximos 5 años junto con bandas de riesgo,  
* **para** decidir de forma justificada en qué provincias conviene expandir las sucursales.
- **Criterios de Aceptación:**
  1. Utilizar un modelo predictivo Prophet.
  2. Mostrar gráficamente la línea histórica unida a la línea proyectada discontinua.
  3. Incluir un botón de descarga que exporte la tabla de predicciones en CSV.
  4. Tratar estadísticamente el outlier del 2020 (pandemia) mediante interpolación.
