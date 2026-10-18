from database.DB import DB
from models.UI import UI
from models.Graphics import Graphics
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme

# setup db connection
connected = DB.connect()


UI.setup_page()
cargar_estilos()

supabase = DB.connect_supabase()

if connected or supabase:        
    UI.render_sidebar()
    
    st.markdown("""
        <div class="hero-header">
            <span class="hero-badge">Temporadas 2022 - 2026</span>
            <div class="hero-title">Panel de Estadísticas y Rendimiento</div>
            <p style="color: #94A3B8; margin: 0;">Resumen general y métricas clave del análisis de jugadores y lesiones.</p>
         </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    #==========INICIO KPIs=========
    st.subheader("📊 Indicadores Clave (KPIs)")
    kpi_equipo_mas_goleador, kpi_jugador_mas_goleador, kpi_posicion_destacada, kpi_minutos_jugados_top = st.columns(4)

    with kpi_equipo_mas_goleador:
     st.markdown("""
          <div class="kpi-card">
              <div class="kpi-title">Equipo Mas Goleador</div>
              <div class="kpi-value">Real Madrid</div>
              <div class="kpi-footer">48 goles</div>
          </div>
      """, unsafe_allow_html=True)
    with kpi_jugador_mas_goleador:
     st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Jugador Mas Goleador</div>
            <div class="kpi-value">K. Mbappe</div>
            <div class="kpi-footer">22 goles</div>
        </div>
    """, unsafe_allow_html=True)
    with kpi_posicion_destacada:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Posicion Destacada</div>
            <div class="kpi-value">Delantero (DC)</div>
        </div>
    """, unsafe_allow_html=True)
    with kpi_minutos_jugados_top:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Minutos Jugados</div>
            <div class="kpi-value">1,980 minutos</div>
            <div class="kpi-footer">98% minutos disputados</div>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("") 
    #==========FIN KPIs=========


    columna_grafico_de_dona_ligas_con_mayor_talento, columna_grafico_de_barras_rendimiento_por_posicion = st.columns(2)

    with columna_grafico_de_dona_ligas_con_mayor_talento:
        st.subheader("Ligas con Mayor Concentración de Talento")
        st.caption("Jugadores con rating superior a 7.0")
        
        df_ligas = pd.DataFrame({
            "Liga": ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"],
            "Jugadores": [45, 38, 30, 25, 18]
        })
        fig_donut = Graphics.create_talent_donut_chart(df_ligas)
        fig_donut = apply_theme(fig_donut)

        st.plotly_chart(fig_donut, use_container_width=True)

    with columna_grafico_de_barras_rendimiento_por_posicion:
        st.subheader("Rendimiento por Posición")
        st.caption("Cantidad de jugadores con media > 7 por demarcación")
        
        df_posiciones = pd.DataFrame({
            "Posicion": ["DC", "EI", "ED", "MC", "DFC", "POR"],
            "Cantidad": [35, 28, 26, 40, 32, 15]
        })
        fig_bar_pos = Graphics.create_position_performance_bar_chart(df_posiciones)
        fig_bar_pos = apply_theme(fig_bar_pos)
        st.plotly_chart(fig_bar_pos, use_container_width=True)

    st.divider()

    
    
    st.subheader("Evolución de Lesiones en el Fútbol Profesional (2022 - 2026)")
    
    dataframe_lesiones = pd.DataFrame({
        "Año": [2022, 2023, 2024, 2025, 2026],
        "Total Lesiones": [320, 350, 410, 390, 440]
    })
    fig_line = Graphics.create_injury_evolution_line_chart(dataframe_lesiones)
    fig_line = apply_theme(fig_line) 
    st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    
    st.subheader("Top 3 Mejores Jugadores de la Muestra")
    st.caption("Basado en valoración general ponderada")

    dataframe_top3 = pd.DataFrame({
        "Jugador": ["Jude Bellingham", "Rodri", "Erling Haaland"],
        "Rating General": [91.5, 90.8, 90.2]
    })
    fig_top3 = Graphics.create_top_players_bar_chart(dataframe_top3)
    fig_top3 = apply_theme(fig_top3)
    st.plotly_chart(fig_top3, use_container_width=True)
    

