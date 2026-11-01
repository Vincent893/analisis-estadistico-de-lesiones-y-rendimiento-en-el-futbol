from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos

def render_marco_metodologico():
    UI.setup_page()
    cargar_estilos()
    UI.render_sidebar()

    st.markdown("""
        <style>
        .method-badge {
            background: rgba(16, 185, 129, 0.12);
            color: #34D399;
            border: 1px solid rgba(52, 211, 153, 0.35);
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            display: inline-block;
            margin-bottom: 12px;
        }
        .quote-box-m {
            background: rgba(11, 19, 43, 0.7);
            border-left: 4px solid #34D399;
            padding: 18px 22px;
            border-radius: 0 12px 12px 0;
            margin: 18px 0;
            color: #E2E8F0;
            line-height: 1.6;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        .concept-card-m {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(52, 211, 153, 0.16);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.25s ease-in-out;
            backdrop-filter: blur(10px);
        }
        .concept-card-m:hover {
            border-color: rgba(52, 211, 153, 0.45);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(52, 211, 153, 0.15);
        }
        .concept-title-m {
            color: #34D399;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .tag-pill-m {
            background: rgba(16, 185, 129, 0.16);
            color: #34D399;
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 6px;
            display: inline-block;
            margin-top: 6px;
            border: 1px solid rgba(52, 211, 153, 0.25);
        }
        .text-block-m {
            color: #CBD5E1;
            font-size: 1.02rem;
            line-height: 1.75;
            text-align: justify;
            margin-bottom: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-header">
            <span class="method-badge">Marco Metodológico</span>
            <div class="hero-title">Marco Metodológico</div>
            <p style="color: #94A3B8; margin: 0; font-size: 1.05rem; line-height: 1.6;">
                Cómo hicimos la investigación, qué pasos seguimos, las técnicas y herramientas estadísticas que usamos para resolver los objetivos del estudio (2022–2026).
            </p>
        </div>
    """, unsafe_allow_html=True)

    # kpis principales
    st.markdown("### Resumen General del Estudio")
    col_tipo_estudio, col_nivel_analitico, col_poblacion_muestral, col_herramienta = st.columns(4)

    with col_tipo_estudio:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Tipo de Estudio</div>
                <div class="kpi-value">Longitudinal</div>
                <div class="kpi-footer">Panel 2022 – 2026</div>
            </div>
        """, unsafe_allow_html=True)

    with col_nivel_analitico:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Nivel Analítico</div>
                <div class="kpi-value">Descriptivo</div>
                <div class="kpi-footer">Relacional</div>
            </div>
        """, unsafe_allow_html=True)

    with col_poblacion_muestral:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Población Muestral</div>
                <div class="kpi-value">Jugadores Total</div>
                <div class="kpi-footer">27,343 Jugadores</div>
            </div>
        """, unsafe_allow_html=True)

    with col_herramienta:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Herramienta</div>
                <div class="kpi-value">DuckDB / SQL</div>
                <div class="kpi-footer">Consultas y Tablas</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

        # Tabs parte 1 para los objetivos y arquitectura
    tab_obj1, tab_obj2, tab_obj3, tab_arq = st.tabs([
        "Obj. 1: Lesiones y Carga",
        "Obj. 2: Concentración de Talento",
        "Obj. 3: Aporte Posicional",
        "Arquitectura y Herramientas"
    ])

    with tab_obj1:
        st.markdown("### Objetivo 1: Lesiones, Carga y Antropometría")
        st.markdown("""
        <div class="text-block-m">
            Para cumplir con este objetivo, analizamos los datos de lesiones temporada por temporada (del 2022 al 2026) usando consultas en SQL y DuckDB. No tocamos ni modificamos los datos de los jugadores; solo los estudiamos tal cual como ocurrieron en la base de datos para ver qué tanto se relacionan con su físico o sus minutos jugados.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Filtro de lesiones reales y cálculo de duración:</b> Creamos consultas en SQL agrupando los eventos médicos por temporada. Contabilizamos cuántas veces se lesionó cada jugador y cuántos días de baja estuvo.
                <li><b>Segmentación por cuartiles de altura y peso:</b> Para comprobar si el tamaño o la masa corporal influyen en las lesiones, dividimos a todo el censo de jugadores en 4 grupos iguales usando funciones de ventana en SQL, comparando luego el porcentaje de lesionados en cada grupo.</li>
                <li><b>Agrupación por minutos jugados:</b> Para descartar o confirmar si el exceso de horas jugados genera más lesiones, dividimos a los jugadores en rangos de minutos, desde menos de 500 minutos hasta más de 3000 minutos, y medimos la tasa de afectación en cada banda.</li>
                <li><b>Análisis de asimetría y severidad:</b> Calculamos tanto la media aritmética como la mediana de los días de baja. Esto nos permitió descubrir que, aunque la mayoría de las lesiones sanan rápido, existen lesiones graves como la rotura de ligamento cruzado que elevan drásticamente el promedio debido a sus más de 200 días de baja por caso.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_obj2:
        st.markdown("### Objetivo 2: Concentración de Talento y Rendimiento")
        st.markdown("""
        <div class="text-block-m">
            En este objetivo queríamos saber si el talento y los goles están repartidos de forma equitativa entre todos los equipos o si se concentran únicamente en unos pocos clubes "gigantes" de la liga.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Identificación de jugadores élite (P90):</b> A partir del puntaje de habilidad general "ability score" de cada jugador, calculamos el percentil 90 por liga y temporada. Esto nos permitió etiquetar como "jugadores de élite" al 10% más destacado de cada campeonato.</li>
                <li><b>Curva de Lorenz y Coeficiente de Gini:</b> Ordenamos el rendimiento ofensivo de goles y asistencias de menor a mayor para trazar la Curva de Lorenz. Al medir qué tanto se aleja esta curva de la línea de igualdad perfecta, obtuvimos el índice de Gini, demostrando que pocos jugadores generan la mayor parte de los goles.</li>
                <li><b>Índice Herfindahl-Hirschman (HHI):</b> Sumamos los porcentajes al cuadrado de participación de los clubes para evaluar si existe un dominio o concentración del talento en pocas instituciones a lo largo del quinquenio.</li>
                <li><b>Coeficiente de Variación (CV):</b> Analizamos qué tan estables o irregulares son las distintas posiciones en el tiempo dividiendo la desviación estándar entre la media.</li>
                <li><b>Mapas de calor del Top 20%:</b> Evaluamos qué porcentaje de la producción ofensiva total de cada club dependía exclusivamente de su quintil más productivo: el 20% superior de su plantilla.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_obj3:
        st.markdown("### Objetivo 3: Dinámicas y Aporte por Líneas Posicionales")
        st.markdown("""
        <div class="text-block-m">
            Aquí nos enfocamos en ver cómo trabaja cada sector del equipo (Arqueros, Defensas, Mediocampistas y Delanteros) y qué tanto aporta cada línea al rendimiento colectivo del club.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Cálculo del aporte porcentual por línea:</b> Sumamos las métricas colectivas (goles, asistencias, tackles y pases clave) agrupadas por temporada y línea táctica, dividiéndolas entre el total general para conocer el peso exacto de cada demarcación. (Ejemplo: como comprobar que los delanteros superan el 54% del total de goles).</li>
                <li><b>Perfiles multidimensionales en gráficos de radar:</b> Normalizamos cinco variables clave: goles, asistencias, pases clave, tackles y minutos, en una escala común de 0 a 1 para contrastar de forma visual las fortalezas de cada bloque.</li>
                <li><b>Diagramas de caja (Boxplots):</b> Usamos diagramas de caja para estudiar la mediana, el rango intercuartílico y los valores atípicos del "ability score", descubriendo que la delantera tiene una dispersión mucho mayor con casos excepcionales en la zona alta.</li>
                <li><b>Balance ofensivo frente a defensivo:</b> Diseñamos barras apiladas al 100% para contrastar el peso de las acciones ofensivas frente a la labor de recuperación en cada línea.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_arq:
        st.markdown("### Arquitectura y Herramientas del Proyecto")
        st.markdown("""
        <div class="text-block-m">
            Para construir esta aplicación y procesar los datos de forma rápida sin ralentizaciones, utilizamos un conjunto moderno de herramientas tecnológicas:
            <ul>
                <li><b>Base de Datos Relacional Normalizada (3FN):</b> Toda la información está organizada en 17 tablas conectadas entre sí mediante claves, lo que evita duplicar datos y garantiza la integridad de más de 855,000 registros históricos.</li>
                <li><b>DuckDB y Consultas SQL:</b> Usamos DuckDB como el motor analítico local en memoria. Nos permitió ejecutar consultas complejas, funciones de ventana y vistas temporales (CTE) en milisegundos.</li>
                <li><b>Python y Pandas:</b> Toda la lógica de la aplicación corre sobre Python, empleando las librerías Pandas y NumPy para la limpieza, filtrado y cálculo numérico de las tablas.</li>
                <li><b>Plotly (Express y Graph Objects):</b> Diseñamos todas las visualizaciones interactivas del dashboard para facilitar la exploración visual.</li>
                <li><b>Streamlit:</b> Es el framework web que utilizamos para unir la programación en Python con una interfaz visual limpia, interactiva y organizada en pestañas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Primera parte del cuerpo del .py
    st.markdown("### 1. Enfoque y Tipo de Investigación")
    st.markdown("""
    <div class="text-block-m">
        Este trabajo se desarrolló utilizando un enfoque cuantitativo con el apoyo de herramientas estadísticas. No modificamos ni alteramos los datos de los partidos; al contrario, analizamos la información tal como ocurrió temporada por temporada entre 2022 y 2026. Al estudiar los registros de todo el periodo de forma corrida, realizamos un estudio de tipo longitudinal y descriptivo, permitiéndonos ver la realidad del fútbol profesional a partir de datos reales.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 2. Cómo se conecta el Marco Teórico con los Objetivos")
    st.markdown("""
    <div class="text-block-m">
        Para mantener una relación coherente en todo el trabajo junto al marco teórico elaborado por nuestro compañero, establecimos los siguientes nexos prácticos:
        <ul>
            <li>La teoría sobre el criterio de días perdidos (<i>time-loss</i>) se aplicó directamente en el <b>Objetivo 1</b> para clasificar y medir las lesiones.</li>
            <li>Los conceptos económicos y estadísticos sobre concentración de talento y desigualdad se usaron en el <b>Objetivo 2</b> mediante el cálculo de Gini y HHI.</li>
            <li>La división clásica de las posiciones en la cancha (arqueros, defensas, mediocampistas y delanteros) sirvió de base en el <b>Objetivo 3</b> para medir el aporte porcentual y el rendimiento de cada bloque.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 3. La Población: Trabajamos con el Censo Completo")
    st.markdown("""
    <div class="text-block-m">
        A diferencia de estudios que trabajan con muestras pequeñas o encuestas, en este proyecto analizamos el <b>100% de la población disponible</b> en la base de datos:
        <ul>
            <li><b>27,343 jugadores</b> registrados en total.</li>
            <li><b>108,639 observaciones</b> de temporada por jugador.</li>
            <li><b>26,949 lesiones</b> documentadas con sus respectivos días de baja.</li>
        </ul>
        Antes de generar los cálculos, depuramos la base de datos eliminando registros vacíos (como las 250 filas totalmente nulas detectadas en la fase inicial) para garantizar que los resultados fuesen 100% confiables.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 4. Fórmulas Matemáticas que usamos en el Análisis")
    st.markdown("""
    <div class="text-block-m">
        Para respaldar los cálculos presentados en el dashboard, organizamos las fórmulas estadísticas y econométricas en pestañas interactivas para detallar exactamente en qué parte del estudio se aplicó cada una:
    </div>
    """, unsafe_allow_html=True)

    # Tabas para los fórmulas usadas
    tab_media, tab_cv, tab_gini, tab_hhi, tab_aporte = st.tabs([
        "Media y Mediana",
        "Desviación y CV",
        "Coeficiente de Gini",
        "Índice HHI",
        "Aporte Posicional (%)"
    ])

    with tab_media:
        col_formula1, col_texto1 = st.columns([1, 1])
        with col_formula1:
            st.markdown("##### Media Aritmética")
            st.latex(r"\bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i")
        with col_texto1:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 1:** Para calcular el promedio de días de baja por lesión y la altura/peso promedio por jugador.
            * **Objetivo 2:** Para obtener la producción ofensiva media (goles + asistencias) por liga y temporada.
            * **Objetivo 3:** Para determinar el *Ability Score* promedio en cada una de las 4 líneas posicionales.
            """)

    with tab_cv:
        col_formula2, col_texto2 = st.columns([1, 1])
        with col_formula2:
            st.markdown("##### Desviación Estándar y Coeficiente de Variación")
            st.latex(r"S = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(X_i - \bar{X})^2}")
            st.latex(r"CV = \frac{S}{\bar{X}}")
        with col_texto2:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 1:** Para medir la dispersión y variación en la duración de los días perdidos según el tipo de lesión.
            * **Objetivo 2:** Para evaluar la estabilidad o irregularidad en el rendimiento de los jugadores a lo largo de las 4 temporadas.
            * **Objetivo 3:** Para comparar la consistencia interna y variabilidad del *Ability Score* entre defensas, medios y delanteros.
            """)

    with tab_gini:
        col_formula3, col_texto3 = st.columns([1, 1])
        with col_formula3:
            st.markdown("##### Coeficiente de Gini")
            st.latex(r"G = \frac{2 \sum_{i=1}^{n} i \cdot y_i}{n \sum_{i=1}^{n} y_i} - \frac{n + 1}{n}")
        with col_texto3:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 2:** Para medir el grado de desigualdad en el reparto de goles y asistencias dentro de cada liga.
            * **Objetivo 2:** Para trazar la Curva de Lorenz comparando la distribución real del rendimiento frente a una igualdad perfecta.
            """)

    with tab_hhi:
        col_formula4, col_texto4 = st.columns([1, 1])
        with col_formula4:
            st.markdown("##### Índice Herfindahl-Hirschman (HHI)")
            st.latex(r"\text{HHI} = \sum_{i=1}^{n} s_i^2")
        with col_texto4:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 2:** Para determinar si existe una alta concentración o monopolio del talento y de los jugadores de élite (P90) en pocos clubes de la liga.
            """)

    with tab_aporte:
        col_formula5, col_texto5 = st.columns([1, 1])
        with col_formula5:
            st.markdown("##### Aporte Posicional Relativo")
            st.latex(r"A_L\% = \left( \frac{\sum M_{L}}{\sum M_{Total}} \right) \times 100")
        with col_texto5:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 3:** Para calcular el porcentaje exacto de goles, asistencias, tackles y pases clave que aporta cada línea táctica (Arqueros, Defensas, Mediocampistas y Delanteros) al club.
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 5. Resumen de Variables (Matriz de Operacionalización)")
    st.markdown("""
    <div class="text-block-m">
        Para tener claridad sobre qué medimos y de dónde extrajimos cada dato, estructuramos la siguiente tabla de operacionalización:
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    | Qué queremos medir | Variable | Cómo la medimos | De dónde sale en la Base de Datos |
    | :--- | :--- | :--- | :--- |
    | **Carga física** | Minutos jugados | Suma total de minutos en la temporada | `analytics_player_seasons.mins` |
    | **Lesiones** | Días de baja | Conteo de días perdidos por lesión | `injuries` (Fecha fin - Fecha inicio) |
    | **Físico** | Altura y Peso | Valores en centímetros y kilogramos | `analytics_player_seasons.height_cm`, `weight_kg` |
    | **Desigualdad** | Gini y HHI | Concentración de goles y talentos | Cálculos sobre clubes y jugadores |
    | **Posición** | Línea táctica | POR, DEF, MED, DEL | `players.primary_category` |
    | **Rendimiento** | Ability Score | Puntaje general de habilidad | `analytics_player_seasons.ability_score` |
    """)

if __name__ == "__main__":
    render_marco_metodologico()