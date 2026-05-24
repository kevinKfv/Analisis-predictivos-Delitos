import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
import os

# Configuración Premium de la página
st.set_page_config(
    page_title="Dashboard Criminalidad Argentina",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para diseño de alto nivel
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .metric-card {
        background-color: #ffffff;
        border-left: 5px solid #1f77b4;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .business-card {
        background-color: #ebf5fb;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #d4e6f1;
        margin-bottom: 25px;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 2px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.title("⚖️ Análisis y Predicción de Criminalidad en Argentina")
st.markdown("Plataforma interactiva de inteligencia territorial para la toma de decisiones comerciales y técnicas en seguridad y seguros.")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    path_pais = 'data/processed/snic-pais-clean.csv'
    path_prov = 'data/processed/snic-provincias-clean.csv'
    
    df_pais = pd.read_csv(path_pais) if os.path.exists(path_pais) else None
    df_prov = pd.read_csv(path_prov) if os.path.exists(path_prov) else None
    
    return df_pais, df_prov

df_pais, df_prov = load_data()

if df_pais is None:
    st.error("❌ No se encontró el dataset procesado a nivel país. Por favor ejecuta el script ETL primero.")
    st.stop()

# --- SECCIÓN: CONTEXTO DE NEGOCIO ---
with st.expander("💼 Ver Hipótesis y Valor de Negocio (Gerencia Comercial y Técnica)", expanded=False):
    st.markdown("""
    <div class="business-card">
        <h4>🎯 Hipótesis de Negocio</h4>
        <p><strong>"La centralización de los datos históricos del SNIC junto con el modelado predictivo mediante series temporales permite segmentar el riesgo geográfico por provincia y anticipar la tendencia delictiva nacional a mediano plazo, optimizando la asignación de recursos y maximizando la rentabilidad comercial del negocio de seguridad y seguros."</strong></p>
        <hr>
        <h5>📈 Valor para la Gerencia Comercial</h5>
        <ul>
            <li><strong>Optimización de Ventas:</strong> Identificar qué provincias tienen mayor volumen absoluto de delitos para priorizar la venta de sistemas de alarmas y cámaras.</li>
            <li><strong>Expansión Estratégica:</strong> Detectar provincias con tendencias crecientes para expandir centros de monitoreo.</li>
        </ul>
        <h5>🛠️ Valor para la Gerencia Técnica (Suscripción y Riesgo)</h5>
        <ul>
            <li><strong>Cálculo de Primas Técnicas:</strong> Utilizar las tasas por 100k habitantes (no solo volumen absoluto) para tarifar seguros de hogar y automotor basándose en riesgo real.</li>
            <li><strong>Predicciones de Siniestralidad:</strong> Modelar la tendencia futura de delitos con intervalos de incertidumbre para prever costos de siniestros a 5 años.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Filtros Globales ---
st.sidebar.header("🔍 Filtros y Configuración")

# Filtro de rango de años
min_year = int(df_pais['anio'].min())
max_year = int(df_pais['anio'].max())
year_range = st.sidebar.slider("Rango de Años para Análisis Histórico", min_year, max_year, (min_year, max_year))

# Aplicar filtros históricos
df_pais_filt = df_pais[(df_pais['anio'] >= year_range[0]) & (df_pais['anio'] <= year_range[1])]
if df_prov is not None:
    df_prov_filt = df_prov[(df_prov['anio'] >= year_range[0]) & (df_prov['anio'] <= year_range[1])]

# Configuración del Modelo Predictivo en Sidebar
st.sidebar.markdown("---")
st.sidebar.header("🔮 Parámetros de Predicción")
pred_years = st.sidebar.slider("Años a Predecir", 1, 5, 5)
handle_outlier = st.sidebar.checkbox("Tratar Outlier del 2020 (COVID-19)", value=True, 
                                     help="Ignora el año de cuarentena estricta (2020) para evitar desviar la tendencia a futuro hacia abajo.")

# --- KPIs SUPERIORES (Basados en el periodo filtrado) ---
col1, col2, col3 = st.columns(3)

total_delitos = df_pais_filt['cantidad'].sum()
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Delitos Registrados</div>
            <div class="metric-value">{total_delitos:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

if not df_pais_filt.empty:
    top_delito_name = df_pais_filt.groupby('delito')['cantidad'].sum().idxmax()
    top_delito_val = df_pais_filt.groupby('delito')['cantidad'].sum().max()
else:
    top_delito_name, top_delito_val = "N/A", 0
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Delito Más Común (Nacional)</div>
            <div class="metric-value" style="font-size: 1.3rem; margin-top: 10px; height: 40px; overflow: hidden;">{top_delito_name}</div>
            <div style="color: #e74c3c; font-weight: bold; font-size: 0.95rem;">({top_delito_val:,.0f} casos)</div>
        </div>
    """, unsafe_allow_html=True)

if df_prov is not None and not df_prov_filt.empty:
    top_prov = df_prov_filt.groupby('provincia')['cantidad'].sum().idxmax()
    top_prov_val = df_prov_filt.groupby('provincia')['cantidad'].sum().max()
else:
    top_prov, top_prov_val = "N/A", 0
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Provincia con Mayor Frecuencia</div>
            <div class="metric-value" style="font-size: 1.5rem; margin-top: 10px; height: 40px;">{top_prov}</div>
            <div style="color: #e74c3c; font-weight: bold; font-size: 0.95rem;">({top_prov_val:,.0f} casos)</div>
        </div>
    """, unsafe_allow_html=True)

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🇦🇷 Panorama Nacional", "🗺️ Análisis Provincial", "🔮 Predicciones Predictivas (ML)"])

with tab1:
    st.markdown("### Evolución Histórica de la Criminalidad Nacional")
    df_evol = df_pais_filt.groupby('anio')['cantidad'].sum().reset_index()
    fig_evol = px.line(df_evol, x='anio', y='cantidad', markers=True, 
                       labels={'anio': 'Año', 'cantidad': 'Cantidad de Delitos'},
                       color_discrete_sequence=['#1f77b4'])
    fig_evol.update_traces(hovertemplate="<b>Año:</b> %{x}<br><b>Delitos:</b> %{y:,.0f}<extra></extra>")
    fig_evol.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#e9ecef"))
    st.plotly_chart(fig_evol, use_container_width=True)
    
    st.markdown("### Distribución por Categoría de Delitos (Top 10)")
    df_top = df_pais_filt.groupby('delito')['cantidad'].sum().reset_index()
    df_top = df_top.sort_values(by='cantidad', ascending=False).head(10)
    
    fig_bar = px.bar(df_top, x='cantidad', y='delito', orientation='h',
                     labels={'cantidad': 'Casos Registrados', 'delito': ''},
                     color='cantidad', color_continuous_scale='Blues')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)")
    fig_bar.update_traces(hovertemplate="<b>%{y}</b><br>Cantidad: %{x:,.0f}<extra></extra>")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    if df_prov is None:
        st.warning("⚠️ No se encontraron datos provinciales. Asegúrate de procesar `snic-provincias.csv`.")
    else:
        st.markdown("### Incidencia Criminal Total por Provincia")
        df_prov_tot = df_prov_filt.groupby('provincia')['cantidad'].sum().reset_index()
        df_prov_tot = df_prov_tot.sort_values(by='cantidad', ascending=False)
        
        fig_prov = px.bar(df_prov_tot, x='provincia', y='cantidad',
                          labels={'provincia': 'Provincia', 'cantidad': 'Cantidad de Delitos'},
                          color='cantidad', color_continuous_scale='Reds')
        fig_prov.update_layout(xaxis={'categoryorder':'total descending'}, plot_bgcolor="rgba(0,0,0,0)")
        fig_prov.update_traces(hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>")
        st.plotly_chart(fig_prov, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Perfil Delictivo por Provincia")
        selected_prov = st.selectbox("Selecciona una provincia para explorar su composición de delitos", df_prov_tot['provincia'].unique())
        
        df_prov_spec = df_prov_filt[df_prov_filt['provincia'] == selected_prov]
        df_prov_spec_top = df_prov_spec.groupby('delito')['cantidad'].sum().reset_index().sort_values('cantidad', ascending=False).head(10)
        
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            fig_pie = px.pie(df_prov_spec_top, names='delito', values='cantidad', hole=0.4,
                             title=f"Composición de Delitos en {selected_prov}",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            fig_pie.update_traces(textposition='inside', textinfo='percent', hovertemplate="<b>%{label}</b><br>Casos: %{value:,.0f}<extra></extra>")
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_chart2:
            st.markdown(f"##### Resumen de Delitos en **{selected_prov}**")
            st.dataframe(
                df_prov_spec_top.rename(columns={'delito': 'Tipo de Delito', 'cantidad': 'Casos Registrados'}),
                hide_index=True,
                use_container_width=True
            )

with tab3:
    st.markdown("### 🔮 Proyecciones del Delito con Machine Learning (Prophet)")
    st.info("Esta sección genera proyecciones automatizadas a futuro basadas en los datos de la serie de tiempo histórica. Permite estimar tendencias para planificación técnica y de suscripción de riesgos.")

    # Selección de Nivel para predecir
    predict_level = st.radio("Selecciona el Nivel de Predicción", ["Nacional", "Provincial"], horizontal=True)

    # Filtrar datos de acuerdo al nivel seleccionado
    if predict_level == "Nacional":
        df_target = df_pais.copy()
        target_name = "Nacional (Argentina)"
    else:
        if df_prov is None:
            st.warning("Datos provinciales no disponibles.")
            st.stop()
        prov_list = sorted(df_prov['provincia'].unique())
        selected_pred_prov = st.selectbox("Selecciona la provincia a proyectar", prov_list)
        df_target = df_prov[df_prov['provincia'] == selected_pred_prov].copy()
        target_name = f"Provincia de {selected_pred_prov}"

    # Botón para ejecutar predicción
    if st.button(f"⚡ Generar Predicción para {target_name}"):
        with st.spinner("Entrenando modelo de serie temporal en tiempo real..."):
            try:
                # Agrupar y preparar para Prophet
                df_agg = df_target.groupby('anio')['cantidad'].sum().reset_index()
                df_agg['ds'] = pd.to_datetime(df_agg['anio'], format='%Y')
                df_agg['y'] = df_agg['cantidad']

                # Manejo de outlier COVID-19 en 2020
                if handle_outlier:
                    # En Prophet, poner en None (NaN) los puntos atípicos hace que el modelo ignore esa fecha
                    # al ajustar la tendencia, interpolándola correctamente entre 2019 y 2021.
                    df_agg.loc[df_agg['anio'] == 2020, 'y'] = None

                # Ajustar modelo Prophet
                m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
                m.fit(df_agg[['ds', 'y']])

                # DataFrame a futuro
                future = m.make_future_dataframe(periods=pred_years, freq='YS')
                forecast = m.predict(future)
                forecast['year'] = forecast['ds'].dt.year

                # Gráfico premium de predicciones
                fig_pred = go.Figure()

                # Datos históricos reales
                df_hist = df_target.groupby('anio')['cantidad'].sum().reset_index()
                fig_pred.add_trace(go.Scatter(
                    x=df_hist['anio'], y=df_hist['cantidad'],
                    mode='markers+lines', name='Histórico Real',
                    line=dict(color='#2c3e50', width=2.5),
                    marker=dict(size=8, symbol='circle'),
                    hovertemplate="<b>Año:</b> %{x}<br><b>Delitos reales:</b> %{y:,.0f}<extra></extra>"
                ))

                # Predicción futura
                pred_only = forecast[forecast['year'] > df_hist['anio'].max()]
                fig_pred.add_trace(go.Scatter(
                    x=pred_only['year'], y=pred_only['yhat'],
                    mode='lines+markers', name='Predicción Esperada',
                    line=dict(color='#e74c3c', width=3, dash='dash'),
                    marker=dict(size=8, symbol='diamond'),
                    hovertemplate="<b>Año Estimado:</b> %{x}<br><b>Predicción:</b> %{y:,.0f} casos<extra></extra>"
                ))

                # Intervalo de confianza / Banda de Incertidumbre
                fig_pred.add_trace(go.Scatter(
                    x=list(pred_only['year']) + list(pred_only['year'])[::-1],
                    y=list(pred_only['yhat_upper']) + list(pred_only['yhat_lower'])[::-1],
                    fill='toself', fillcolor='rgba(231, 76, 60, 0.15)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip", showlegend=True, name='Banda de Riesgo/Incertidumbre (80%)'
                ))

                fig_pred.update_layout(
                    title=f"Proyección de Criminalidad a futuro para {target_name} ({pred_years} años)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Año", yaxis_title="Cantidad de Delitos",
                    hovermode="x unified",
                    xaxis=dict(tickmode='linear', tick0=min_year, dtick=1),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_pred, use_container_width=True)

                # Tabla de predicciones y descarga
                st.markdown("##### 📄 Reporte de Datos Predichos")
                report_df = pred_only[['year', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                report_df.columns = ['Año Proyectado', 'Predicción Media', 'Límite Inferior (Riesgo Min)', 'Límite Superior (Riesgo Max)']
                
                # Formatear números
                st.dataframe(
                    report_df.style.format({
                        'Año Proyectado': '{:.0f}',
                        'Predicción Media': '{:,.0f}',
                        'Límite Inferior (Riesgo Min)': '{:,.0f}',
                        'Límite Superior (Riesgo Max)': '{:,.0f}'
                    }),
                    hide_index=True,
                    use_container_width=True
                )

                # Botón de Descarga
                csv_data = report_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar Reporte de Predicciones en CSV",
                    data=csv_data,
                    file_name=f"reporte_prediccion_{target_name.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    help="Permite a la Gerencia Comercial exportar los datos para cotizaciones en Excel o Looker."
                )

            except Exception as e:
                st.error(f"Ocurrió un error al generar las predicciones: {e}")
                st.info("Asegúrate de tener instalada la librería `prophet` en tu entorno virtual.")
