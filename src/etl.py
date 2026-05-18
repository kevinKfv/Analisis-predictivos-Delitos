import pandas as pd
import os

def run_etl():
    raw_pais_path = 'data/raw/snic-pais.csv'
    raw_prov_path = 'data/raw/snic-provincias.csv'
    
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)
    
    print("--- Procesando Datos a Nivel País ---")
    if os.path.exists(raw_pais_path):
        df_pais = pd.read_csv(raw_pais_path)
        # Seleccionar columnas relevantes
        cols_pais = ['anio', 'codigo_delito_snic_nombre', 'cantidad_hechos']
        df_pais = df_pais[cols_pais].copy()
        
        # Renombrar para mayor simplicidad
        df_pais.rename(columns={'codigo_delito_snic_nombre': 'delito', 'cantidad_hechos': 'cantidad'}, inplace=True)
        
        # Limpiar nulos y agrupar por si hay duplicados
        df_pais = df_pais.dropna(subset=['cantidad'])
        df_pais = df_pais.groupby(['anio', 'delito'], as_index=False)['cantidad'].sum()
        
        path_clean_pais = os.path.join(processed_dir, 'snic-pais-clean.csv')
        df_pais.to_csv(path_clean_pais, index=False)
        print(f"Guardado: {path_clean_pais} ({len(df_pais)} filas)")
    else:
        print(f"Archivo no encontrado: {raw_pais_path}")

    print("--- Procesando Datos a Nivel Provincia ---")
    if os.path.exists(raw_prov_path):
        # snic-provincias tiene columnas extra, las leeremos como string donde corresponda si hay issues,
        # pero podemos especificar low_memory=False
        df_prov = pd.read_csv(raw_prov_path, low_memory=False)
        
        cols_prov = ['anio', 'provincia_nombre', 'codigo_delito_snic_nombre', 'cantidad_hechos']
        # Validar si las columnas existen
        if all(c in df_prov.columns for c in cols_prov):
            df_prov = df_prov[cols_prov].copy()
            df_prov.rename(columns={'provincia_nombre': 'provincia', 'codigo_delito_snic_nombre': 'delito', 'cantidad_hechos': 'cantidad'}, inplace=True)
            
            # Limpiar nulos
            df_prov = df_prov.dropna(subset=['cantidad'])
            # Convertir a numérico por si las dudas
            df_prov['cantidad'] = pd.to_numeric(df_prov['cantidad'], errors='coerce').fillna(0)
            
            df_prov = df_prov.groupby(['anio', 'provincia', 'delito'], as_index=False)['cantidad'].sum()
            
            path_clean_prov = os.path.join(processed_dir, 'snic-provincias-clean.csv')
            df_prov.to_csv(path_clean_prov, index=False)
            print(f"Guardado: {path_clean_prov} ({len(df_prov)} filas)")
        else:
            print("El dataset de provincias no tiene las columnas esperadas.")
    else:
        print(f"Archivo no encontrado: {raw_prov_path}")

if __name__ == '__main__':
    run_etl()
