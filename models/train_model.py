import pandas as pd
from prophet import Prophet
import os
import pickle

def train():
    data_path = 'data/processed/snic-pais-clean.csv'
    model_dir = 'models'
    model_path = os.path.join(model_dir, 'prophet_model.pkl')
    
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"Cargando datos desde {data_path}...")
    df = pd.read_csv(data_path)
    
    # Agrupamos por año para tener el total de delitos a nivel nacional por año
    df_agg = df.groupby('anio')['cantidad'].sum().reset_index()
    
    # Prophet requiere las columnas 'ds' (fecha) y 'y' (valor objetivo)
    # Convertimos el anio a un formato de fecha válido (e.g., "2000-01-01")
    df_agg['ds'] = pd.to_datetime(df_agg['anio'], format='%Y')
    df_agg['y'] = df_agg['cantidad']
    
    print("Entrenando modelo predictivo con Prophet...")
    # Como es un dato anual, desactivamos las estacionalidades menores
    m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df_agg[['ds', 'y']])
    
    # Guardamos el modelo
    with open(model_path, 'wb') as f:
        pickle.dump(m, f)
        
    print(f"Modelo guardado exitosamente en {model_path}")

if __name__ == '__main__':
    train()
