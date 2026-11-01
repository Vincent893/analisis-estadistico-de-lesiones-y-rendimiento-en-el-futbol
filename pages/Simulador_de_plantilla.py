from database.DB import DB
from models.UI import UI
from database.Query import get_player_season_performance
from utils.graficos import calcular_metricas_equipo, generar_grafico_rating_titulares, generar_grafico_radar_plantilla
from utils.estilos import cargar_estilos
from components.simulador_ui import (
    renderizar_encabezado,
    renderizar_filtros_laterales,
    renderizar_panel_seleccion_jugadores,
    renderizar_tarjetas_kpi,
)
from components.cancha_tactica import renderizar_cancha_tactica
import streamlit as st


UI.setup_page()
UI.render_sidebar()

cargar_estilos()


renderizar_encabezado()

conexion_base_datos = DB.get_connection()

if conexion_base_datos:
    datos_jugadores_temporada = get_player_season_performance(conexion_base_datos)

    if datos_jugadores_temporada is not None and not datos_jugadores_temporada.empty:
        lista_temporadas = datos_jugadores_temporada['season_label'].unique().tolist()

        # Filtros Laterales
        temporada_seleccionada, formacion_tactica = renderizar_filtros_laterales(lista_temporadas)

        datos_temporadas_actual = datos_jugadores_temporada[
            datos_jugadores_temporada['season_label'] == temporada_seleccionada
        ].copy()

        # Listas por categoría para los selects
        lista_arqueros = datos_temporadas_actual[datos_temporadas_actual['primary_category'] == 'GOALKEEPER']['name'].tolist()
        lista_defensas = datos_temporadas_actual[datos_temporadas_actual['primary_category'] == 'DEFENDER']['name'].tolist()
        lista_mediocampistas = datos_temporadas_actual[datos_temporadas_actual['primary_category'] == 'MIDFIELDER']['name'].tolist()
        lista_delanteros = datos_temporadas_actual[datos_temporadas_actual['primary_category'] == 'ATTACKER']['name'].tolist()

        columna_constructora, columna_campo_tactico = st.columns([1, 2])

        with columna_constructora:
           
            jugadores_seleccionados, boton_aplicar = renderizar_panel_seleccion_jugadores(
                formacion_tactica, 
                lista_arqueros, 
                lista_defensas, 
                lista_mediocampistas, 
                lista_delanteros
            )

        
        if boton_aplicar:
            st.session_state['alineacion_confirmada'] = jugadores_seleccionados

        with columna_campo_tactico:
            st.markdown('<h3 style="color: #f0f6fc; font-size: 20px;"><i class="fa-solid fa-chart-line" style="color: #58a6ff; margin-right: 8px;"></i>Resumen Táctico y Estadístico Colectivo</h3>', unsafe_allow_html=True)

           
            titulares_activos = st.session_state.get('alineacion_confirmada', [])

            datos_alineacion_titular = datos_temporadas_actual[
                datos_temporadas_actual['name'].isin(titulares_activos)
            ]

            if len(datos_alineacion_titular) > 0:
                # Tarjetas KPI
                metricas_colectivas = calcular_metricas_equipo(datos_alineacion_titular)
                renderizar_tarjetas_kpi(metricas_colectivas)

                st.markdown("---")

                
                st.markdown('<h3 style="color: #f0f6fc; font-size: 18px;"><i class="fa-solid fa-radar" style="color: #3fb950; margin-right: 8px;"></i>Perfil Táctico y Atributos Colectivos</h3>', unsafe_allow_html=True)

                col_radar, col_barras = st.columns(2)

                with col_radar:
                    # Gráfico de Radar de la plantilla
                    figura_radar = generar_grafico_radar_plantilla(datos_alineacion_titular)
                    st.plotly_chart(figura_radar, use_container_width=True)

                with col_barras:
                    # Gráfico de barras individuales que ya tenías
                    figura_barras = generar_grafico_rating_titulares(datos_alineacion_titular)
                    st.plotly_chart(figura_barras, use_container_width=True)

                renderizar_cancha_tactica(datos_alineacion_titular, formacion_tactica)
               

                
            else:
                st.markdown("""
                        <div style="background-color: rgba(227, 179, 65, 0.1); border: 1px solid #e3b341; border-radius: 8px; padding: 12px; color: #e3b341; font-size: 14px;">
                            <i class="fa-solid fa-triangle-exclamation" style="margin-right: 8px;"></i>
                            Configura tu plantilla en el panel izquierdo y presiona <b>"Aplicar Alineación"</b> para visualizar el rendimiento simulado.
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
                    <div style="background-color: rgba(248, 81, 73, 0.1); border: 1px solid #f85149; border-radius: 8px; padding: 12px; color: #f85149; font-size: 14px;">
                        <i class="fa-solid fa-circle-exclamation" style="margin-right: 8px;"></i>
                        No se encontraron datos en la consulta de rendimiento de jugadores.
                    </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
            <div style="background-color: rgba(248, 81, 73, 0.1); border: 1px solid #f85149; border-radius: 8px; padding: 12px; color: #f85149; font-size: 14px;">
                <i class="fa-solid fa-plug-circle-xmark" style="margin-right: 8px;"></i>
                Error al intentar conectar con la base de datos.
            </div>
        """, unsafe_allow_html=True)