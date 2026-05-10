# Proyecto Criminalidad Argentina 📊🇦🇷

## Objetivo del Proyecto
Este proyecto de ciencia de datos tiene como objetivo analizar las estadísticas criminales de Argentina utilizando datasets públicos proporcionados por el Sistema Nacional de Información Criminal (SNIC). A través del procesamiento de datos, análisis exploratorio y modelos predictivos, buscamos extraer insights relevantes sobre las tendencias y patrones delictivos en el país.

## Datasets Utilizados
Los datos utilizados en este proyecto provienen de los datasets en formato CSV del **SNIC (Sistema Nacional de Información Criminal)**. Los archivos originales deben ubicarse en la carpeta `data/raw/` para su posterior procesamiento.

## Tecnologías Utilizadas
El proyecto está desarrollado principalmente en Python y utiliza las siguientes librerías:
- **Manipulación de datos:** Pandas, NumPy
- **Visualización:** Matplotlib, Seaborn, Plotly
- **Machine Learning & Predicción:** Scikit-learn, Prophet
- **Desarrollo de Interfaz/Dashboard:** Streamlit
- **Entorno de Experimentación:** Jupyter Notebook

## Estructura del Proyecto
```text
proyecto-criminalidad/
├── data/
│   ├── raw/           # Datasets originales inmutables
│   └── processed/     # Datasets limpios listos para modelar
├── notebooks/         # Jupyter notebooks para EDA y experimentación
├── app/               # Archivos de la aplicación Streamlit
├── models/            # Modelos entrenados y guardados
├── images/            # Gráficos y figuras generadas
├── docs/              # Documentación adicional
├── src/               # Código fuente del proyecto (ETL, utilidades)
├── requirements.txt   # Dependencias del proyecto
├── README.md          # Este archivo
├── .gitignore         # Archivos y carpetas ignorados por git
└── main.py            # Script principal
```

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/kevinKfv/Analisis-predictivos-Delitos.git
cd Analisis-predictivos-Delitos
```

### 2. Configurar el Entorno Virtual (Recomendado)
Es una buena práctica utilizar un entorno virtual para aislar las dependencias del proyecto.

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**En macOS y Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
Con el entorno virtual activado, instala las librerías requeridas:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación Streamlit
Para ver el dashboard interactivo de manera local:
```bash
streamlit run app/app.py
```

### 5. Iniciar Jupyter Notebooks
Para explorar los datos y ver los análisis paso a paso:
```bash
jupyter notebook
```

---
*Proyecto listo para abrir en VS Code y comenzar a trabajar inmediatamente.*
