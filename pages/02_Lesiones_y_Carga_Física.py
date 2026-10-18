from database.DB import DB
from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme
import plotly.express as px


UI.setup_page()
UI.render_sidebar()
cargar_estilos()



st.title("⚽ Análisis de Lesiones y Carga Física (2022-2026)")
st.markdown("""
Esta sección explora la frecuencia y duración de las lesiones de los jugadores en relación con sus 
características antropométricas (**altura y peso**) y su **carga de minutos jugados** durante el ciclo analizado.
""")

conn = DB.get_connection()

if conn:
    # Consulta optimizada utilizando nuestro esquema en estrella OLAP
    query = """
        SELECT 
            p.name,
            p.primary_category,
            d.season_label,
            f.age,
            f.height_cm,
            f.weight_kg,
            f.mins,
            f.starts,
            f.total_injuries,
            f.total_days_lost,
            f.average_rating,
            f.goals_per_90
        FROM fact_player_season_performance f
        INNER JOIN dim_player p ON f.player_id = p.player_id
        INNER JOIN dim_season d ON f.season_id = d.season_id
    """
    
    # Cargamos los datos en un DataFrame de Pandas usando la conexión de DuckDB
    df = conn.execute(query).df()
    
    # --- FILTROS LATERALES EN STREAMLIT ---
    st.sidebar.header("Filtros de Análisis")
    
    # Filtro por Temporada
    seasons_list = df['season_label'].unique().tolist()
    selected_season = st.sidebar.selectbox("Seleccionar Temporada", ["Todas"] + seasons_list)
    
    # Filtro por Categoría Posicional
    categories_list = df['primary_category'].unique().tolist()
    selected_category = st.sidebar.selectbox("Línea Posicional", ["Todas"] + categories_list)
    
    # Aplicar filtros al DataFrame
    filtered_df = df.copy()
    if selected_season != "Todas":
        filtered_df = filtered_df[filtered_df['season_label'] == selected_season]
    if selected_category != "Todas":
        filtered_df = filtered_df[filtered_df['primary_category'] == selected_category]

    # --- MÉTRICAS GENERALES (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Jugadores Analizados", len(filtered_df))
    with col2:
        st.metric("Total Lesiones Registradas", int(filtered_df['total_injuries'].sum()))
    with col3:
        st.metric("Días Totales de Baja", int(filtered_df['total_days_lost'].sum()))
    with col4:
        avg_mins = filtered_df['mins'].mean()
        st.metric("Promedio Minutos Jugados", f"{avg_mins:.1f}" if not pd.isna(avg_mins) else "0")

    st.markdown("---")

    # --- VISUALIZACIONES ESTADÍSTICAS ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Relación: Minutos Jugados vs. Días de Baja por Lesión")
        fig_scatter = px.scatter(
            filtered_df, 
            x="mins", 
            y="total_days_lost", 
            color="primary_category",
            hover_name="name",
            labels={"mins": "Minutos Jugados en la Temporada", "total_days_lost": "Días Perdidos por Lesión"},
            title="Carga de Minutos vs Impacto de Lesiones"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.subheader("Distribución de Lesiones por Categoría Posicional")
        fig_box = px.box(
            filtered_df, 
            x="primary_category", 
            y="total_injuries",
            color="primary_category",
            labels={"primary_category": "Línea Posicional", "total_injuries": "Cantidad de Lesiones"},
            title="Frecuencia de Lesiones según Posición"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # --- TABLA DETALLADA ---
    with st.expander("Ver tabla de datos detallada"):
        st.dataframe(filtered_df)

else:
    st.error("No se pudo establecer la conexión con la base de datos.")