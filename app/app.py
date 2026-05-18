import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
from prophet import Prophet
import os

# Configuración Premium de la página
st.set_page_config(
    page_title="Dashboard Criminalidad Argentina",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para darle un toque premium
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
        text-transform: uppercase;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ Análisis y Predicción de Criminalidad en Argentina")
st.markdown("Plataforma interactiva para el análisis de estadísticas del Sistema Nacional de Información Criminal (SNIC).")

# -- CARGA DE DATOS --
@st.cache_data
def load_data():
    path_pais = 'data/processed/snic-pais-clean.csv'
    path_prov = 'data/processed/snic-provincias-clean.csv'
    
    df_pais = pd.read_csv(path_pais) if os.path.exists(path_pais) else None
    df_prov = pd.read_csv(path_prov) if os.path.exists(path_prov) else None
    
    return df_pais, df_prov

@st.cache_resource
def load_model():
    model_path = 'models/prophet_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

df_pais, df_prov = load_data()
model = load_model()

if df_pais is None:
    st.error("❌ No se encontró el dataset a nivel país. Ejecuta `src/etl.py`.")
    st.stop()

# --- SIDEBAR: Filtros Globales ---
st.sidebar.header("🔍 Filtros Globales")
min_year = int(df_pais['anio'].min())
max_year = int(df_pais['anio'].max())
year_range = st.sidebar.slider("Selecciona el Rango de Años", min_year, max_year, (min_year, max_year))

# Aplicar filtros
df_pais_filt = df_pais[(df_pais['anio'] >= year_range[0]) & (df_pais['anio'] <= year_range[1])]
if df_prov is not None:
    df_prov_filt = df_prov[(df_prov['anio'] >= year_range[0]) & (df_prov['anio'] <= year_range[1])]

# --- KPIs SUPERIORES ---
st.markdown("### 📈 Resumen Rápido del Período Seleccionado")
col1, col2, col3 = st.columns(3)

# 1. Total Delitos en el periodo
total_delitos = df_pais_filt['cantidad'].sum()
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total de Delitos Registrados</div>
            <div class="metric-value">{total_delitos:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

# 2. Delito más frecuente
if not df_pais_filt.empty:
    top_delito_name = df_pais_filt.groupby('delito')['cantidad'].sum().idxmax()
    top_delito_val = df_pais_filt.groupby('delito')['cantidad'].sum().max()
else:
    top_delito_name, top_delito_val = "N/A", 0
    
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Delito Más Frecuente</div>
            <div class="metric-value" style="font-size: 1.2rem; margin-top: 10px;">{top_delito_name}</div>
            <div style="color: #e74c3c; font-weight: bold;">({top_delito_val:,.0f} casos)</div>
        </div>
    """, unsafe_allow_html=True)

# 3. Provincia con más delitos
if df_prov is not None and not df_prov_filt.empty:
    top_prov = df_prov_filt.groupby('provincia')['cantidad'].sum().idxmax()
    top_prov_val = df_prov_filt.groupby('provincia')['cantidad'].sum().max()
else:
    top_prov, top_prov_val = "N/A", 0

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Provincia Más Afectada</div>
            <div class="metric-value" style="font-size: 1.5rem; margin-top: 10px;">{top_prov}</div>
            <div style="color: #e74c3c; font-weight: bold;">({top_prov_val:,.0f} casos)</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🇦🇷 Panorama Nacional", "🗺️ Análisis Provincial", "🔮 Predicciones (Machine Learning)"])

with tab1:
    st.markdown("### Evolución Histórica Nacional")
    df_evol = df_pais_filt.groupby('anio')['cantidad'].sum().reset_index()
    fig_evol = px.line(df_evol, x='anio', y='cantidad', markers=True, 
                       labels={'anio': 'Año', 'cantidad': 'Cantidad de Delitos'},
                       color_discrete_sequence=['#1f77b4'])
    fig_evol.update_traces(hovertemplate="<b>Año:</b> %{x}<br><b>Delitos:</b> %{y:,.0f}<extra></extra>")
    fig_evol.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#e9ecef"))
    st.plotly_chart(fig_evol, use_container_width=True)
    
    st.markdown("### Top 10 Delitos Más Registrados")
    df_top = df_pais_filt.groupby('delito')['cantidad'].sum().reset_index()
    df_top = df_top.sort_values(by='cantidad', ascending=False).head(10)
    
    fig_bar = px.bar(df_top, x='cantidad', y='delito', orientation='h',
                     labels={'cantidad': 'Cantidad Registrada', 'delito': ''},
                     color='cantidad', color_continuous_scale='Blues')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)")
    fig_bar.update_traces(hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,.0f}<extra></extra>")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    if df_prov is None:
        st.warning("No hay datos provinciales disponibles. Revisa que `snic-provincias.csv` esté en `data/raw/`.")
    else:
        st.markdown("### Incidencia Criminal por Provincia")
        df_prov_tot = df_prov_filt.groupby('provincia')['cantidad'].sum().reset_index()
        df_prov_tot = df_prov_tot.sort_values(by='cantidad', ascending=False)
        
        fig_prov = px.bar(df_prov_tot, x='provincia', y='cantidad',
                          labels={'provincia': 'Provincia', 'cantidad': 'Cantidad de Delitos'},
                          color='cantidad', color_continuous_scale='Reds')
        fig_prov.update_layout(xaxis={'categoryorder':'total descending'}, plot_bgcolor="rgba(0,0,0,0)")
        fig_prov.update_traces(hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>")
        st.plotly_chart(fig_prov, use_container_width=True)
        
        st.markdown("### Composición de Delitos en una Provincia Específica")
        selected_prov = st.selectbox("Selecciona una provincia para ver el detalle", df_prov_tot['provincia'].unique())
        
        df_prov_spec = df_prov_filt[df_prov_filt['provincia'] == selected_prov]
        df_prov_spec_top = df_prov_spec.groupby('delito')['cantidad'].sum().reset_index().sort_values('cantidad', ascending=False).head(10)
        
        fig_pie = px.pie(df_prov_spec_top, names='delito', values='cantidad', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_traces(textposition='inside', textinfo='percent', hovertemplate="<b>%{label}</b><br>Casos: %{value:,.0f}<extra></extra>")
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.markdown("### 🔮 Proyección de Criminalidad a 5 Años")
    if model is None:
        st.error("No se encontró el modelo predictivo. Ejecuta `models/train_model.py`.")
    else:
        st.info("Utilizamos un algoritmo de series temporales (Prophet) para estimar la cantidad de crímenes a futuro en Argentina basándonos en los datos históricos.")
        
        # Generar proyecciones
        future = model.make_future_dataframe(periods=5, freq='YS')
        forecast = model.predict(future)
        
        # Extraer solo el anio para visualizarlo mejor
        forecast['year'] = forecast['ds'].dt.year
        
        # Construir un gráfico premium usando graph_objects
        fig_pred = go.Figure()
        
        # Datos históricos
        df_hist = df_pais.groupby('anio')['cantidad'].sum().reset_index()
        fig_pred.add_trace(go.Scatter(
            x=df_hist['anio'], y=df_hist['cantidad'],
            mode='markers+lines', name='Histórico Real',
            line=dict(color='#2c3e50', width=2),
            marker=dict(size=8),
            hovertemplate="<b>Año Real:</b> %{x}<br><b>Delitos:</b> %{y:,.0f}<extra></extra>"
        ))
        
        # Predicción
        pred_years = forecast[forecast['year'] > df_hist['anio'].max()]
        fig_pred.add_trace(go.Scatter(
            x=pred_years['year'], y=pred_years['yhat'],
            mode='lines+markers', name='Predicción Esperada',
            line=dict(color='#e74c3c', width=3, dash='dash'),
            marker=dict(size=8),
            hovertemplate="<b>Año Estimado:</b> %{x}<br><b>Predicción:</b> %{y:,.0f} casos<extra></extra>"
        ))
        
        # Margen de Error
        fig_pred.add_trace(go.Scatter(
            x=list(pred_years['year']) + list(pred_years['year'])[::-1],
            y=list(pred_years['yhat_upper']) + list(pred_years['yhat_lower'])[::-1],
            fill='toself', fillcolor='rgba(231, 76, 60, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip", showlegend=False, name='Margen de Incertidumbre'
        ))
        
        fig_pred.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Año", yaxis_title="Cantidad de Delitos",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
