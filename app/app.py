"""
Aplicación principal de Streamlit para el proyecto-criminalidad.
Permite visualizar de manera interactiva los datos de criminalidad.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página de Streamlit
st.set_page_config(
    page_title="Dashboard - Criminalidad en Argentina",
    page_icon="📊",
    layout="wide"
)

# Título principal de la aplicación
st.title("📊 Análisis de Criminalidad en Argentina")
st.markdown("Esta aplicación permite explorar interactivamente estadísticas criminales utilizando datos del SNIC.")

# Sidebar para controles de usuario
st.sidebar.header("Configuración")
st.sidebar.markdown("Usa las opciones de abajo para interactuar con los datos.")

# Opción para cargar un archivo CSV desde la interfaz
uploaded_file = st.sidebar.file_uploader("Cargar dataset CSV", type=['csv'])

if uploaded_file is not None:
    # Si el usuario carga un archivo, lo leemos con pandas
    try:
        df = pd.read_csv(uploaded_file)
        st.success("¡Datos cargados exitosamente!")
        
        # Mostrar las primeras filas del dataset
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head())
        
        # Gráfico simple si existen columnas numéricas
        st.subheader("Gráfico Simple de Muestra")
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_columns) > 0:
            column_to_plot = st.selectbox("Selecciona una columna para graficar", numeric_columns)
            
            # Crear un gráfico de línea usando matplotlib
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df[column_to_plot].values)
            ax.set_title(f"Distribución de {column_to_plot}")
            ax.set_xlabel("Índice")
            ax.set_ylabel(column_to_plot)
            
            # Mostrar gráfico en Streamlit
            st.pyplot(fig)
        else:
            st.info("El dataset no contiene columnas numéricas para graficar.")
            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info("Por favor, carga un archivo CSV desde la barra lateral para comenzar.")
