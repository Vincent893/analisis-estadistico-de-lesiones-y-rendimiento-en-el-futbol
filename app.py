from database.DB import DB
from models.UI import UI
from models.Graphics import Graphics
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.estilos import cargar_estilos

class Main:

    @staticmethod
    def run():
        with st.spinner("Inicializando conexion"):
        # setup db connection
            connected = DB.connect()
            
            supabase = DB.connect_supabase()

            UI.setup_page()
            cargar_estilos()
        

            st.markdown("""
            <div class="hero-header">
                <span class="hero-badge">Temporadas 2022 - 2026</span>
                <div class="hero-title">Analisis Estadistico de Lesiones y Rendimiento Individual y Colectivo en Clubes de Futbol Profesional</div>
                <p style="color: #94A3B8; margin: 0;">Investigación sobre el impacto en clubes de fútbol profesional</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            ## Introducción
            El fútbol profesional contemporáneo es un deporte donde la exigencia es máxima, por lo que la intuición
            ya no puede ser la única medida para la toma de decisiones en el campo. Sin embargo, a pesar de la gran
            cantidad de registros sobre los partidos, los directores técnicos y analistas luchan para unificar en una
            misma herramienta dimensiones como la salud y disponibilidad de los jugadores, la eficiencia del
            rendimiento individual frente a la concentración de talento en plantillas colectivas y el aporte real de
            cada línea posicional. No tener esta información entorpece la optimización y la rotación de plantillas,
            la prevención de lesiones y el rendimiento colectivo.

            ## Justificación
            Este dashboard estadístico interactivo busca responder la necesidad de una herramienta cuantitativa que
            permita el análisis diagnóstico preciso para la mejora del rendimiento colectivo y la prevención de
            lesiones, tomando en cuenta las características antropométricas (altura y peso) y la edad de los
            jugadores. Este trabajo, además, contribuye a la línea de investigación estadística aplicada al deporte
            de la UCV, por lo que sienta un precedente metodológico aplicable para el estudio del rendimiento en el
            fútbol profesional.

            ## Objetivo General
            Describir y visualizar el comportamiento de las métricas físicas, de lesiones y de rendimiento
            individual y colectivo en el fútbol profesional durante el período comprendido entre el año 2022 y el
            año 2026, con el fin de caracterizar los patrones de rendimiento de los jugadores y la concentración
            de talento en los clubes.

            ## Objetivos Específicos
            1. Describir la frecuencia, duración y distribución de las lesiones en los jugadores entre las
               temporadas 2022 y 2026, relacionándolas con sus características antropométricas (altura y peso)
               y su carga de minutos jugados.
            2. Cuantificar la distribución y concentración de jugadores de alto rendimiento dentro de las
               plantillas de los clubes, evaluando su comportamiento ofensivo y consistencia competitiva a lo
               largo de las temporadas 2022-2026.
            3. Examinar el aporte porcentual y el promedio de rendimiento de las diferentes líneas posicionales
               (arqueros, defensas, mediocampistas y delanteros) dentro de la estructura de los equipos durante
               el ciclo 2022-2026.

            ## Preguntas de Investigación
            1. ¿Cuál ha sido la frecuencia, duración y distribución de las lesiones en los jugadores de fútbol
               profesional entre las temporadas 2022-2026, y qué relación guardan con sus características
               antropométricas (altura y peso) y su carga de minutos jugados?
            2. ¿Cómo se distribuyen y concentran los jugadores de alto rendimiento dentro de las plantillas de los
               clubes, y cuál ha sido su comportamiento ofensivo y consistencia competitiva a lo largo de las
               temporadas del ciclo 2022-2026?
            3. ¿Cuál es el aporte porcentual y el promedio de rendimiento de las diferentes líneas posicionales
               (arqueros, defensas, mediocampistas y delanteros) dentro de la estructura colectiva de los equipos
               durante el período 2022-2026?

            ## Alcance del Estudio
            Se trata de un estudio longitudinal de nivel descriptivo: no se aplican pruebas de hipótesis ni modelos
            predictivos. El análisis se realiza sobre 108.639 registros jugador-temporada, correspondientes a
            2.227 clubes y 300 ligas en las temporadas 2022/23 a 2025/26. En la base de datos, las temporadas
            2022/23 a 2024/25 están marcadas como fabricadas y solo 2025/26 corresponde a registros originales,
            por lo que las conclusiones sobre tendencias entre temporadas deben leerse con cautela.

            ## Estructura del Dashboard
            - **Marco Teórico:** conceptos que sustentan el estudio (epidemiología de lesiones, concentración de
              talento, dinámicas posicionales) y glosario de términos.
            - **Marco Metodológico:** técnicas y herramientas estadísticas utilizadas para cada objetivo.
            - **Análisis de Lesiones:** responde al objetivo 1.
            - **Concentración de Talento:** responde al objetivo 2.
            - **Análisis Posicional:** responde al objetivo 3.
            - **Simulador de Plantilla:** permite armar un once titular y ver sus métricas colectivas.
            """)

            if connected or supabase:        
                UI.render_sidebar()
            
            

if __name__ == "__main__":
    Main.run()