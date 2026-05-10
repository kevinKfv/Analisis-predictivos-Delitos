"""
Módulo para la carga y preprocesamiento inicial de datos.
Contiene funciones para leer datasets CSV utilizando pandas.
"""

import pandas as pd
import os

def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Carga un archivo CSV desde la ruta especificada y lo devuelve como un DataFrame de pandas.
    
    Args:
        filepath (str): La ruta al archivo CSV.
        
    Returns:
        pd.DataFrame: DataFrame que contiene los datos leídos.
    """
    # Verificar si el archivo existe
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se pudo encontrar el archivo en la ruta: {filepath}")
        
    try:
        # Cargar los datos usando pandas
        data = pd.read_csv(filepath)
        print(f"Datos cargados exitosamente desde {filepath}. Forma del dataset: {data.shape}")
        return data
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Ejemplo de uso (asegurarse de tener un CSV de prueba en data/raw/)
    print("Módulo data_loader listo para ser importado.")
