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
            </div>
        """, unsafe_allow_html=True)

    with col_nivel_analitico:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Nivel Analítico</div>
                <div class="kpi-value">Descriptivo</div>
            </div>
        """, unsafe_allow_html=True)

    with col_poblacion_muestral:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Población</div>
                <div class="kpi-value">27.343 Jugadores</div>
            </div>
        """, unsafe_allow_html=True)

    with col_herramienta:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Herramientas</div>
                <div class="kpi-value">DuckDB / Supabase</div>
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
            Para cumplir con este objetivo, analizamos los datos de lesiones temporada por temporada (de 2022/23 a 2025/26) usando consultas en SQL sobre DuckDB. No modificamos los datos de los jugadores; los estudiamos tal como están registrados en la base de datos para describir qué relación guardan las lesiones con el físico y con los minutos jugados.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Conteo de lesiones y cálculo de duración:</b> Creamos consultas en SQL agrupando las lesiones por temporada. Contabilizamos cuántos jugadores se lesionaron y cuántos días de baja tuvo cada lesión (fecha de fin menos fecha de inicio).</li>
                <li><b>Segmentación por cuartiles de altura, peso e IMC:</b> Para describir si el tamaño o la masa corporal se relacionan con las lesiones, dividimos a los jugadores en 4 grupos usando funciones de ventana en SQL, y comparamos el porcentaje de lesionados y los días de baja promedio de cada grupo.</li>
                <li><b>Agrupación por minutos jugados:</b> Para describir si una mayor carga de minutos se asocia con más lesiones, dividimos a los jugadores en rangos de 500 minutos, desde 500 o menos hasta más de 3.000, y medimos el porcentaje de lesionados en cada rango.</li>
                <li><b>Análisis de asimetría y gravedad:</b> Calculamos tanto la media aritmética como la mediana de los días de baja. La diferencia entre ambas (38 frente a 15 días) muestra que la mayoría de las lesiones se resuelve pronto, mientras que lesiones graves como la rotura de ligamento cruzado, con más de 200 días de baja por caso, elevan el promedio.</li>
                <li><b>Perfil comparativo:</b> Comparamos los promedios de altura, peso, minutos y edad entre los jugadores con y sin lesión en la temporada.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_obj2:
        st.markdown("### Objetivo 2: Concentración de Talento y Rendimiento")
        st.markdown("""
        <div class="text-block-m">
            En este objetivo queríamos saber si el talento y la producción ofensiva están repartidos de forma equitativa o si se concentran en pocas ligas, pocos clubes y pocos jugadores.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Identificación de jugadores élite (P90):</b> A partir del puntaje de habilidad general (<i>Ability Score</i>) de cada jugador, calculamos el percentil 90 por liga y temporada, y etiquetamos como "jugadores élite" a quienes lo alcanzan o superan. Para comparar ligas entre sí usamos un umbral común: el percentil 90 de cada temporada sobre todas las ligas.</li>
                <li><b>Curva de Lorenz y Coeficiente de Gini:</b> Ordenamos el rendimiento ofensivo (goles + asistencias) de menor a mayor para trazar la Curva de Lorenz. Al medir cuánto se aleja esta curva de la línea de igualdad perfecta obtuvimos el coeficiente de Gini, que describe qué tan concentrada está la producción en pocos jugadores.</li>
                <li><b>Índice Herfindahl-Hirschman (HHI):</b> Dentro de cada liga, sumamos los cuadrados de la participación porcentual de cada club en los goles + asistencias, para describir si la producción ofensiva se concentra en pocos clubes. Se presenta como promedio de las ligas en los indicadores clave.</li>
                <li><b>Coeficiente de Variación (CV):</b> Dividimos la desviación estándar entre la media de los goles + asistencias de cada línea posicional. Mide qué tan parecidos o distintos son entre sí los jugadores de una misma línea, no la variación de un jugador en el tiempo.</li>
                <li><b>Relación entre minutos y producción:</b> Describimos la asociación entre los minutos jugados y los goles + asistencias con un diagrama de dispersión y el coeficiente de correlación de Spearman.</li>
                <li><b>Mapas de calor del Top 20%:</b> Evaluamos qué porcentaje de los goles + asistencias de cada club aporta su quintil más productivo, es decir, el 20% superior de su plantilla.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_obj3:
        st.markdown("### Objetivo 3: Dinámicas y Aporte por Líneas Posicionales")
        st.markdown("""
        <div class="text-block-m">
            Aquí nos enfocamos en describir cómo trabaja cada sector del equipo (Arqueros, Defensas, Mediocampistas y Delanteros) y cuánto aporta cada línea al rendimiento colectivo.
        </div>
        <div class="text-block-m">
            <b>Paso a paso detallado de lo que hicimos:</b>
            <ul>
                <li><b>Cálculo del aporte porcentual por línea:</b> Sumamos los goles, las asistencias y los tackles por temporada y línea, y los dividimos entre el total de la temporada para conocer el peso de cada línea. Por ejemplo, los mediocampistas aportan cerca del 65% de los goles + asistencias y los delanteros, el 19,3% de los goles. Se excluyen los arqueros, cuyo aporte en estas métricas es prácticamente nulo.</li>
                <li><b>Promedio por jugador:</b> Calculamos la media de las mismas métricas por jugador de cada línea, para separar el peso colectivo de una línea (que depende de cuántos jugadores tiene) de su rendimiento individual típico. Las métricas por 90 minutos solo consideran jugadores con 450 minutos o más.</li>
                <li><b>Diagramas de caja (Boxplots):</b> Usamos diagramas de caja para estudiar la mediana, el rango intercuartílico y la asimetría de cada variable por línea. En el <i>Ability Score</i> las cuatro líneas resultan casi idénticas; las diferencias aparecen en las métricas de producción.</li>
                <li><b>Perfiles multidimensionales en gráficos de radar:</b> Normalizamos cinco variables (goles, asistencias, pases clave, tackles y minutos) en una escala común de 0 a 1 para contrastar visualmente el perfil de cada línea.</li>
                <li><b>Balance ofensivo frente a defensivo:</b> Diseñamos barras apiladas al 100% para contrastar el peso de las acciones ofensivas (goles, asistencias y pases clave) frente a las defensivas (tackles) en cada línea.</li>
                <li><b>Métricas propias de los arqueros:</b> Evaluamos a los arqueros con indicadores de portería: porcentaje de paradas, porterías a cero, goles concedidos y goles evitados por 90 minutos.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab_arq:
        st.markdown("### Arquitectura y Herramientas del Proyecto")
        st.markdown("""
        <div class="text-block-m">
            Los datos provienen de un conjunto público de Kaggle sobre fútbol profesional. A partir de él, el proyecto se apoya en dos bases de datos con funciones distintas y en un conjunto de herramientas de análisis y visualización:
            <ul>
                <li><b>Base de datos original en Supabase (PostgreSQL):</b> Aloja la base relacional normalizada en Tercera Forma Normal (3FN): 17 tablas conectadas mediante claves, con 855.439 registros en total. Sobre ella se ejecutan las consultas del Cuestionario SQL.</li>
                <li><b>Base analítica en DuckDB / MotherDuck:</b> Una copia de las mismas tablas alimenta el dashboard. Se usa DuckDB de forma local durante el desarrollo y MotherDuck (DuckDB en la nube) en la aplicación publicada. Sobre esta copia se añadieron 3 vistas analíticas, que resumen los datos por jugador, por club y por línea posicional, y 6 tablas desnormalizadas (dimensiones y hechos) que alimentan el Simulador de Plantilla.</li>
                <li><b>Consultas SQL:</b> Los cálculos se resuelven con expresiones de tabla comunes (CTE), agregaciones y funciones de ventana.</li>
                <li><b>Python, Pandas y NumPy:</b> La lógica de la aplicación corre sobre Python; Pandas y NumPy se emplean para el filtrado y el cálculo de indicadores como el Gini, el HHI y el coeficiente de variación.</li>
                <li><b>Plotly (Express y Graph Objects):</b> Con esta librería se construyeron todas las visualizaciones interactivas del dashboard.</li>
                <li><b>Streamlit:</b> Es el framework web que une la programación en Python con una interfaz de varias páginas, una por cada apartado de la investigación.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Primera parte del cuerpo del .py
    st.markdown("### 1. Enfoque y Tipo de Investigación")
    st.markdown("""
    <div class="text-block-m">
        Este trabajo se desarrolló con un enfoque cuantitativo y un diseño no experimental: no se manipuló ninguna variable, sino que se analizó la información tal como está registrada en la base de datos, temporada por temporada, entre 2022/23 y 2025/26. Al observar a los mismos jugadores a lo largo de varias temporadas, el estudio es de tipo longitudinal, y su nivel es descriptivo: se describen frecuencias, distribuciones y asociaciones, sin aplicar pruebas de hipótesis ni modelos predictivos. La fuente es secundaria, ya que los datos no fueron recolectados por el equipo sino tomados de un conjunto de datos público.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 2. Cómo se conecta el Marco Teórico con los Objetivos")
    st.markdown("""
    <div class="text-block-m">
        Para mantener la coherencia entre el marco teórico y el análisis, establecimos los siguientes nexos prácticos:
        <ul>
            <li>La teoría sobre el criterio de días perdidos (<i>time-loss</i>) se aplicó directamente en el <b>Objetivo 1</b> para medir la duración de las lesiones.</li>
            <li>Los conceptos económicos y estadísticos sobre concentración de talento y desigualdad se usaron en el <b>Objetivo 2</b> mediante la Curva de Lorenz y los índices de Gini y HHI.</li>
            <li>La división clásica de las posiciones en la cancha (arqueros, defensas, mediocampistas y delanteros) sirvió de base en el <b>Objetivo 3</b> para medir el aporte porcentual y el rendimiento de cada línea.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 3. La Población: Trabajamos con el Censo Completo")
    st.markdown("""
    <div class="text-block-m">
        A diferencia de los estudios que trabajan con muestras, en este proyecto analizamos el <b>100% de los registros disponibles</b> en la base de datos, por lo que no se aplicó ninguna técnica de muestreo:
        <ul>
            <li><b>27.343 jugadores</b> registrados en total.</li>
            <li><b>108.639 observaciones</b> jugador-temporada.</li>
            <li><b>26.949 lesiones</b> documentadas con sus respectivos días de baja.</li>
        </ul>
        Antes de generar los cálculos, depuramos la base de datos eliminando registros vacíos (como las 250 filas totalmente nulas detectadas en la fase inicial).
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 4. Limitaciones de los Datos")
    st.markdown("""
    <div class="text-block-m">
        Los resultados deben leerse teniendo en cuenta las siguientes características de la base de datos:
        <ul>
            <li><b>Temporadas fabricadas:</b> Las temporadas 2022/23 a 2024/25 están marcadas como fabricadas en la base de datos; solo 2025/26 corresponde a registros originales. Por eso la estabilidad observada entre temporadas no puede interpretarse como una tendencia real.</li>
            <li><b>Registro de lesiones:</b> Cada jugador registra como máximo una lesión por temporada y los once tipos de lesión aparecen con frecuencias casi idénticas, una uniformidad poco habitual en registros reales.</li>
            <li><b>Plantillas incompletas:</b> La base no contiene plantillas completas (mediana de 10 jugadores registrados por club y temporada), lo que afecta a los indicadores calculados dentro de cada club.</li>
            <li><b>Clasificación posicional:</b> Solo el centrodelantero se clasifica como delantero; extremos y mediapuntas se cuentan como mediocampistas.</li>
            <li><b>Alcance descriptivo:</b> Las asociaciones descritas no permiten afirmar relaciones de causa y efecto.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 5. Fórmulas Matemáticas que usamos en el Análisis")
    st.markdown("""
    <div class="text-block-m">
        Para respaldar los cálculos presentados en el dashboard, organizamos las fórmulas estadísticas en pestañas, detallando en qué parte del estudio se aplicó cada una:
    </div>
    """, unsafe_allow_html=True)

    # Tabas para los fórmulas usadas
    tab_media, tab_cv, tab_gini, tab_hhi, tab_spearman, tab_aporte = st.tabs([
        "Media y Mediana",
        "Desviación y CV",
        "Coeficiente de Gini",
        "Índice HHI",
        "Correlación de Spearman",
        "Aporte Posicional (%)"
    ])

    with tab_media:
        col_formula1, col_texto1 = st.columns([1, 1])
        with col_formula1:
            st.markdown("##### Media Aritmética")
            st.latex(r"\bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i")
            st.markdown("##### Mediana")
            st.markdown("Valor central de los datos ordenados: deja el 50% de las observaciones por debajo y el 50% por encima.")
        with col_texto1:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 1:** Para calcular la media y la mediana de los días de baja por lesión, y los promedios de altura, peso, minutos y edad de los jugadores con y sin lesión.
            * **Objetivo 2:** Para comparar los minutos y la producción ofensiva (goles + asistencias) de los jugadores élite frente al resto.
            * **Objetivo 3:** Para determinar el promedio por jugador de cada métrica en las 4 líneas posicionales.
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
            * **Objetivo 2:** Para medir la dispersión relativa de los goles + asistencias entre los jugadores de cada línea posicional.
            * **Objetivo 3:** Para comparar la homogeneidad de los goles + asistencias por 90 minutos entre defensas, mediocampistas y delanteros.
            """)

    with tab_gini:
        col_formula3, col_texto3 = st.columns([1, 1])
        with col_formula3:
            st.markdown("##### Coeficiente de Gini")
            st.latex(r"G = \frac{2 \sum_{i=1}^{n} i \cdot y_i}{n \sum_{i=1}^{n} y_i} - \frac{n + 1}{n}")
            st.markdown("Donde $y_i$ son los valores ordenados de menor a mayor.")
        with col_texto3:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 2:** Para medir el grado de desigualdad en el reparto de goles y asistencias entre los jugadores, en el conjunto de la muestra y dentro de cada liga.
            * **Objetivo 2:** Como resumen numérico de la Curva de Lorenz, que compara la distribución real del rendimiento frente a una igualdad perfecta.
            """)

    with tab_hhi:
        col_formula4, col_texto4 = st.columns([1, 1])
        with col_formula4:
            st.markdown("##### Índice Herfindahl-Hirschman (HHI)")
            st.latex(r"\text{HHI} = \sum_{i=1}^{n} s_i^2")
            st.markdown("Donde $s_i$ es la participación porcentual del club $i$; el índice va de cerca de 0 a 10.000.")
        with col_texto4:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 2:** Para describir si los goles + asistencias de una liga se concentran en pocos clubes. Se calcula por liga y se presenta su promedio.
            """)

    with tab_spearman:
        col_formula6, col_texto6 = st.columns([1, 1])
        with col_formula6:
            st.markdown("##### Coeficiente de Correlación de Spearman")
            st.latex(r"\rho = \frac{\operatorname{cov}(R_X, R_Y)}{S_{R_X}\, S_{R_Y}}")
            st.markdown("Donde $R_X$ y $R_Y$ son los rangos (posiciones ordenadas) de cada variable. Va de −1 a 1.")
        with col_texto6:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 2:** Para describir la asociación entre los minutos jugados y los goles + asistencias, y entre el *Ability Score* y los goles + asistencias.
            """)

    with tab_aporte:
        col_formula5, col_texto5 = st.columns([1, 1])
        with col_formula5:
            st.markdown("##### Aporte Posicional Relativo")
            st.latex(r"A_L\% = \left( \frac{\sum M_{L}}{\sum M_{Total}} \right) \times 100")
        with col_texto5:
            st.markdown("##### Se aplicó en:")
            st.markdown("""
            * **Objetivo 3:** Para calcular el porcentaje de goles, asistencias y tackles que aporta cada línea de campo (Defensas, Mediocampistas y Delanteros) sobre el total de cada temporada.
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 6. Operacionalización de Variables por Objetivo")
    st.markdown("""
    <div class="text-block-m">
        Para tener claridad sobre qué medimos y de dónde extrajimos cada dato, estructuramos un cuadro de operacionalización para cada objetivo específico:
    </div>
    """, unsafe_allow_html=True)

    op_obj1, op_obj2, op_obj3 = st.tabs(["Objetivo 1", "Objetivo 2", "Objetivo 3"])

    with op_obj1:
        st.markdown("""
        | Variable | Dimensión | Indicador | Escala | Fuente en la base de datos |
        | :--- | :--- | :--- | :--- | :--- |
        | **Lesiones** | Frecuencia | Número de lesiones y porcentaje de jugadores lesionados por temporada | Razón | `injuries` |
        | **Lesiones** | Duración | Días de baja (fecha de fin − fecha de inicio): media, mediana y rangos | Razón | `injuries.start_date`, `end_date` |
        | **Lesiones** | Tipo | Tipo de lesión (11 categorías) | Nominal | `injuries.injury_type` |
        | **Antropometría** | Altura | Centímetros, agrupados en cuartiles | Razón | `players.height_cm` |
        | **Antropometría** | Peso | Kilogramos, agrupados en cuartiles | Razón | `players.weight_kg` |
        | **Antropometría** | IMC | Peso / altura² (kg/m²), agrupado en cuartiles | Razón | Derivada de altura y peso |
        | **Carga de minutos** | Exposición | Minutos jugados en la temporada, en rangos de 500 | Razón | `player_seasons.mins` |
        | **Edad** | — | Años cumplidos en la temporada | Razón | `player_seasons.age` |
        """)

    with op_obj2:
        st.markdown("""
        | Variable | Dimensión | Indicador | Escala | Fuente en la base de datos |
        | :--- | :--- | :--- | :--- | :--- |
        | **Alto rendimiento** | Jugador élite | *Ability Score* igual o superior al percentil 90 (por liga y temporada, o por temporada al comparar ligas) | Nominal (sí / no) | `player_seasons.ability_score` |
        | **Rendimiento ofensivo** | Producción | Goles + asistencias en la temporada | Razón | `player_stats_attacking.goals`, `assists` |
        | **Concentración** | Entre jugadores | Curva de Lorenz y coeficiente de Gini de goles + asistencias | Razón (0 a 1) | Cálculo sobre jugadores |
        | **Concentración** | Entre clubes | Índice HHI de goles + asistencias por club dentro de cada liga | Razón (0 a 10.000) | Cálculo sobre clubes |
        | **Dependencia** | Dentro del club | Porcentaje de goles + asistencias del club aportado por el 20% más productivo de su plantilla | Razón | Cálculo por club y temporada |
        | **Consistencia** | Dispersión relativa | Coeficiente de variación de goles + asistencias por línea posicional | Razón | Cálculo por línea |
        | **Exposición** | Minutos | Minutos jugados y su correlación de Spearman con goles + asistencias | Razón | `player_seasons.mins` |
        | **Liga** | — | División a la que pertenece el club | Nominal | `clubs.division_id`, `divisions.division_name` |
        """)

    with op_obj3:
        st.markdown("""
        | Variable | Dimensión | Indicador | Escala | Fuente en la base de datos |
        | :--- | :--- | :--- | :--- | :--- |
        | **Posición** | Línea | Arquero, Defensa, Mediocampista o Delantero | Nominal | `players.primary_category` |
        | **Posición** | Demarcación | Posición principal del jugador (14 demarcaciones) | Nominal | `player_positions`, `positions` |
        | **Aporte colectivo** | Porcentual | Porcentaje de goles, asistencias y tackles de cada línea sobre el total de la temporada | Razón | `player_stats_attacking`, `player_stats_defending` |
        | **Rendimiento individual** | Promedio | Media por jugador de goles, asistencias y tackles; por 90 minutos con 450 minutos o más | Razón | `player_stats_attacking`, `player_stats_defending`, `player_seasons.mins` |
        | **Creación de juego** | Pases clave | Pases clave en la temporada | Razón | `player_stats_passing.key_passes` |
        | **Habilidad** | Puntaje general | *Ability Score* | Intervalo | `player_seasons.ability_score` |
        | **Rendimiento de arqueros** | Portería | Porcentaje de paradas, porterías a cero, goles concedidos y goles evitados por 90 minutos | Razón | `player_stats_goalkeeping` |
        """)

if __name__ == "__main__":
    render_marco_metodologico()
