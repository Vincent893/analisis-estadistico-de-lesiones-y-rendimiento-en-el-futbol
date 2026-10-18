from database.DB import DB
from models.UI import UI
from database.Query import get_player_season_performance
from utils.graficos import calcular_metricas_equipo, generar_grafico_rating_titulares
from components.simulador_ui import (
    renderizar_encabezado,
    renderizar_filtros_laterales,
    renderizar_panel_seleccion_jugadores,
    renderizar_tarjetas_kpi,
    renderizar_tabla_titulares
)
import streamlit as st

# Setup general de interfaz
UI.setup_page()
UI.render_sidebar()

# Renderizar Encabezado Principal
renderizar_encabezado()

conexion_base_datos = DB.get_connection()

if conexion_base_datos:
    
    datos_jugadores_temporada = get_player_season_performance(conexion_base_datos)
    lista_temporadas = datos_jugadores_temporada['season_label'].unique().tolist()
    
    # Filtros Laterales (obtenemos los estados)
    temporada_seleccionada, formacion_tactica = renderizar_filtros_laterales(lista_temporadas)
    
    datos_temporada_actual = datos_jugadores_temporada[
        datos_jugadores_temporada['season_label'] == temporada_seleccionada
    ].copy()

    # listas por categoría
    lista_arqueros = datos_temporada_actual[datos_temporada_actual['primary_category'] == 'GOALKEEPER']['name'].tolist()
    lista_defensas = datos_temporada_actual[datos_temporada_actual['primary_category'] == 'DEFENDER']['name'].tolist()
    lista_mediocampistas = datos_temporada_actual[datos_temporada_actual['primary_category'] == 'MIDFIELDER']['name'].tolist()
    lista_delanteros = datos_temporada_actual[datos_temporada_actual['primary_category'] == 'ATTACKER']['name'].tolist()

    columna_constructora, columna_campo_tactico = st.columns([1, 2])

    with columna_constructora:
        
        
        # Selector de Jugadores
        jugadores_seleccionados = renderizar_panel_seleccion_jugadores(
            formacion_tactica, lista_arqueros, lista_defensas, lista_mediocampistas, lista_delanteros
        )

    with columna_campo_tactico:
        st.subheader("🏟️ Resumen Táctico y Estadístico Colectivo")
        
        datos_alineacion_titular = datos_temporada_actual[
            datos_temporada_actual['name'].isin(jugadores_seleccionados)
        ]

        if len(datos_alineacion_titular) > 0:
            # Tarjetas KPI
            metricas_colectivas = calcular_metricas_equipo(datos_alineacion_titular)
            renderizar_tarjetas_kpi(metricas_colectivas)

            st.markdown("---")
            
            # Tabla
            renderizar_tabla_titulares(datos_alineacion_titular)

            # Gráfico 
            figura_grafico = generar_grafico_rating_titulares(datos_alineacion_titular)
            st.plotly_chart(figura_grafico, use_container_width=True)
        else:
            st.info("Selecciona los jugadores en el panel izquierdo para visualizar el rendimiento simulado.")

else:
    st.error("Error al intentar conectar con la base de datos.")