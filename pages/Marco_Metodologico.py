import streamlit as st
from models.UI import UI
from utils.estilos import cargar_estilos


UI.setup_page()
cargar_estilos()


st.markdown(
    """
    <div class="hero-header">
        <span class="hero-badge">Fundamentos Metodológicos</span>
        <div class="hero-title">Marco Metódico</div>
        <p style="color: #94A3B8; margin: 0;">Metodología de procesamiento de datos, técnicas estadísticas y arquitectura analítica del proyecto (2022-2026).</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


st.subheader("Procedimientos Analíticos")
st.write(
    "Para responder a los objetivos específicos de la investigación, se implementaron técnicas de análisis descriptivo, análisis de frecuencias, segmentación y agregación de datos:"
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="kpi-card" style="margin-bottom: 20px;">
            <div class="kpi-title" style="font-size: 1.1rem; color: #38BDF8; margin-bottom: 8px;">
                1. Caracterización de Frecuencia, Duración y Distribución de Lesiones
            </div>
            <p style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.5;">
                Se aplicaron medidas de tendencia central y dispersión (medias, desviaciones estándar y conteos absolutos/relativos) sobre la duración de las bajas médicas y la frecuencia de las lesiones. Estos indicadores se cruzaron con las características antropométricas de los jugadores y su carga acumulada de minutos jugados, para así identificar perfiles de riesgo y patrones de fatiga física a lo largo de las temporadas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title" style="font-size: 1.1rem; color: #38BDF8; margin-bottom: 8px;">
                3. Análisis de Aportes y Rendimiento por Líneas Posicionales
            </div>
            <p style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.5;">
                La parte estructural de los equipos se abordó con la segmentación del rendimiento colectivo por líneas posicionales (arqueros, defensas, mediocampistas y delanteros). Se calcularon los aportes porcentuales promedio de cada posición específica que ocupa un jugador dentro del campo de juego respecto a los indicadores globales del equipo, permitiendo contrastar la importancia y eficiencia individual de cada línea dentro de la estructura táctica.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="kpi-card" style="height: 100%;">
            <div class="kpi-title" style="font-size: 1.1rem; color: #38BDF8; margin-bottom: 8px;">
                2. Distribución y Concentración de Talento y Rendimiento Ofensivo
            </div>
            <p style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.5;">
                Para estudiar la concentración de jugadores de alto rendimiento en los equipos de los clubes, se emplearon análisis de distribución porcentual, rangos de rendimiento ofensivo y métricas de consistencia competitiva inter-temporada. Esto permitió visualizar si el talento y la producción ofensiva se concentran en un grupo reducido de elementos o si existe una distribución equilibrada dentro de la profundidad de los planteles.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


st.subheader("Técnicas de Visualización de Datos y Arquitectura del Dashboard")
st.write(
    "La representación gráfica se estructuró para facilitar la toma de decisiones de cuerpos técnicos y analistas mediante cuatro ejes fundamentales:"
)

st.markdown(
    """
- **Gráficos de Distribución y Dispersión:** Sirven para contrastar la relación entre la carga de minutos, las características antropométricas y la incidencia de lesiones entre las temporadas 2022-2026.
- **Gráficos de Tendencia Temporal:** Se implementan para seguir la evolución clínica del rendimiento y la concentración de talento a lo largo de las temporadas del periodo evaluado.
- **Diagramas Comparativos por Líneas Posicionales:** Diseñados para contrastar el aporte porcentual y las medias del rendimiento entre defensas, mediocampistas, delanteros y arqueros de manera simultánea.
"""
)