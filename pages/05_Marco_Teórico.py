from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos

def render_marco_teorico():
    UI.setup_page()
    cargar_estilos()
    UI.render_sidebar()

    # CSS adicional adaptado a la estética Dark Cyber y lectura académica de alta gama
    st.markdown("""
        <style>
        .theory-badge {
            background: rgba(0, 229, 255, 0.12);
            color: #00E5FF;
            border: 1px solid rgba(0, 229, 255, 0.35);
            padding: 4px 14px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            display: inline-block;
            margin-bottom: 12px;
        }
        .quote-box {
            background: rgba(11, 19, 43, 0.7);
            border-left: 4px solid #00E5FF;
            padding: 18px 22px;
            border-radius: 0 12px 12px 0;
            margin: 18px 0;
            font-style: italic;
            color: #E2E8F0;
            line-height: 1.6;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        .concept-card {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(0, 229, 255, 0.16);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.25s ease-in-out;
            backdrop-filter: blur(10px);
        }
        .concept-card:hover {
            border-color: rgba(0, 229, 255, 0.45);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 229, 255, 0.15);
        }
        .concept-title {
            color: #00E5FF;
            font-size: 1.18rem;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .bib-item {
            background: rgba(11, 19, 43, 0.55);
            border: 1px solid rgba(0, 229, 255, 0.12);
            border-left: 4px solid #00A8CC;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 14px;
            font-size: 0.95rem;
            color: #CBD5E1;
            line-height: 1.6;
            transition: all 0.2s ease;
        }
        .bib-item:hover {
            border-left-color: #00E5FF;
            background: rgba(15, 23, 42, 0.75);
            transform: translateX(4px);
        }
        .tag-pill {
            background: rgba(0, 168, 204, 0.16);
            color: #38BDF8;
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 6px;
            display: inline-block;
            margin-top: 6px;
            border: 1px solid rgba(56, 189, 248, 0.25);
        }
        .db-badge {
            background: rgba(139, 92, 246, 0.15);
            color: #C084FC;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(192, 132, 252, 0.3);
            font-family: monospace;
            display: inline-block;
        }
        .formula-container {
            background: rgba(2, 6, 23, 0.75);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 10px;
            padding: 14px 18px;
            margin: 12px 0;
            text-align: center;
            color: #38BDF8;
        }
        .nav-card {
            background: rgba(11, 19, 43, 0.6);
            border: 1px solid rgba(0, 229, 255, 0.18);
            border-radius: 12px;
            padding: 16px;
            height: 100%;
            transition: all 0.25s ease;
        }
        .nav-card:hover {
            border-color: #00E5FF;
            background: rgba(15, 23, 42, 0.85);
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Header Principal
    st.markdown("""
        <div class="hero-header">
            <span class="hero-badge">Marco Teórico Académico & Metodológico</span>
            <div class="hero-title">DASHBOARD ESTADÍSTICO DE FÚTBOL: EVALUACIÓN DE LESIONES Y DINÁMICAS POSICIONALES (2022-2026)</div>
            <p style="color: #94A3B8; margin: 0; font-size: 1.05rem;">
                Fundamentación conceptual, epidemiológica, arquitectural y analítica del rendimiento individual y colectivo
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Tarjetas métricas del dataset analizado (KPIs)
    st.markdown("### 📊 Universo Empírico y Estructura del Estudio")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Esquema Relacional</div>
                <div class="kpi-value">17 Tablas</div>
                <div class="kpi-footer">Tercera Forma Normal (3FN)</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Población de Jugadores</div>
                <div class="kpi-value">27,343</div>
                <div class="kpi-footer">Perfiles Antropométricos</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Registros Longitudinales</div>
                <div class="kpi-value">108,639</div>
                <div class="kpi-footer">Temporadas 2022 - 2026</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Eventos Médicos</div>
                <div class="kpi-value">26,949</div>
                <div class="kpi-footer">Lesiones Documentadas</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pestañas estructuradas según las 4 secciones + glosario + bibliografía del documento oficial
    tab_intro, tab_sec1, tab_sec2, tab_sec3, tab_sec4, tab_refs = st.tabs([
        "📌 Introducción",
        "🩺 Sec 1: Epidemiología & Carga",
        "🛡️ Sec 2: Valor Posicional & Talento",
        "🏛️ Sec 3: Universo de Datos & Arquitectura",
        "📖 Sec 4: Glosario de Métricas",
        "📚 Referencias Bibliográficas"
    ])

    # ==========================================
    # TAB INTRODUCCIÓN
    # ==========================================
    with tab_intro:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Introducción y Planteamiento</span>
            <h2 style="color: #F8FAFC; margin-top: 5px;">Fundamentación Teórica de la Investigación</h2>
            <p style="color: #CBD5E1; font-size: 1.05rem; line-height: 1.7;">
                La fundamentación teórica de esta investigación se articula en torno a los <b>objetivos específicos</b> del proyecto, 
                empleando exclusivamente fundamentos de la <b>estadística descriptiva</b> y la <b>analítica de datos deportivos</b>. 
                El sustento conceptual se divide en cuatro secciones principales:
            </p>
        </div>
        """, unsafe_allow_html=True)

        eje1, eje2 = st.columns(2)
        with eje1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🩺 Sección 1: Epidemiología, Antropometría y Carga</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Aborda los conceptos fundamentales de la epidemiología de lesiones bajo el consenso internacional ReFORM, 
                    el criterio de pérdida de tiempo (<i>time-loss</i>), y su cruce teórico con las características antropométricas 
                    (altura, peso, IMC, edad) y la carga acumulada de minutos como proxy del estrés biomecánico.
                </p>
                <span class="tag-pill">Consenso ReFORM</span>
                <span class="tag-pill">Modelo ACWR Proxy</span>
                <span class="tag-pill">Demarcación Táctica</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🏛️ Sección 3: Universo de Datos y Arquitectura Analítica</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Describe el universo empírico de aproximadamente 855,000 registros organizados en 17 tablas normalizadas (3FN), 
                    el stack de procesamiento analítico (Python 3, DuckDB OLAP, Supabase/MotherDuck, Pandas, NumPy, Plotly Express) 
                    y la estructura interactiva de navegación de la aplicación web Streamlit.
                </p>
                <span class="tag-pill">DuckDB OLAP</span>
                <span class="tag-pill">Vistas SQL Desnormalizadas</span>
                <span class="tag-pill">Dark Cyber UI</span>
            </div>
            """, unsafe_allow_html=True)

        with eje2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🛡️ Sección 2: Valor Posicional, Aportes y Talento</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Define la estructura funcional de las cuatro líneas posicionales (POR, DEF, MED, DEL), el cálculo del aporte porcentual 
                    por bloque táctico al rendimiento colectivo, y la teoría económica y sociológica de la concentración de talento 
                    mediante los índices de Gini y Herfindahl-Hirschman (HHI).
                </p>
                <span class="tag-pill">Líneas Posicionales</span>
                <span class="tag-pill">Índice de Gini & HHI</span>
                <span class="tag-pill">Profundidad de Plantilla</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📖 Sección 4: Glosario de Conceptos y Métricas</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Presenta un catálogo exhaustivo y operativo de los términos de investigación: conceptos epidemiológicos y antropométricos, 
                    métricas ofensivas avanzadas (Goles Esperados xG, xG/90, SOE, consistencia inter-temporada), defensivas y de portería 
                    (xGP, clean sheets) y valor posicional (Ability Scores).
                </p>
                <span class="tag-pill">Goles Esperados (xG)</span>
                <span class="tag-pill">Shot Creation (SOE)</span>
                <span class="tag-pill">Ability Score</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="quote-box">
            <b>Relevancia del Período 2022-2026:</b><br>
            Los datos que contextualizan esta investigación provienen de una base relacional normalizada (<i>SQL Practice DB: Football Players</i>), 
            la cual alberga 27,343 jugadores, 108,639 registros de temporadas y 26,949 lesiones documentadas. El período 2022-2026 tiene una especial 
            relevancia teórica por la intensificación del calendario futbolístico internacional, lo que subraya la necesidad de sistemas de información 
            que resuman, cuantifiquen y visualicen la gestión de cargas y el rendimiento deportivo.
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # TAB SECCIÓN 1: LESIONES Y CARGA
    # ==========================================
    with tab_sec1:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 1</span>
            <h2 style="color: #F8FAFC;">Epidemiología de Lesiones, Antropometría y Carga de Minutos</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.1 Definición Operativa y Clasificación de Lesiones en el Fútbol")
        st.write("""
        La epidemiología de lesiones deportivas requiere definiciones estandarizadas para garantizar la coherencia conceptual. 
        El **consenso ReFORM** (derivado de la posición del Comité Olímpico Internacional) establece el marco unificado adoptado en este proyecto. 
        La definición operativa central adopta el criterio de **pérdida de tiempo (*time-loss*)**:
        """)

        st.markdown("""
        <div class="quote-box">
            "Se considera una lesión cuando un jugador no puede participar plenamente en entrenamientos o partidos posteriores debido a un problema de salud."
            <br><small style="color: #00E5FF;">— Criterio de Pérdida de Tiempo (Consenso ReFORM / COI)</small>
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        La severidad de una lesión se conceptualiza a través de los **días de baja médica (*days_out*)**, estructurados formalmente en siete rangos estandarizados:
        """)

        # Tabla de severidad
        st.markdown("""
        | Categoría de Severidad | Rango de Días de Baja | Impacto en la Disponibilidad Competitiva | Contexto Clínico Habitual |
        | :--- | :--- | :--- | :--- |
        | **Inmediata / Nula** | `0 días` | Sin pérdida de sesiones formales | Golpes leves, contusiones sin baja |
        | **Mínima** | `1 a 3 días` | Ausencia transitoria breve | Sobrecargas musculares leves |
        | **Leve** | `4 a 7 días` | Baja promedio de 1 encuentro | Contracturas, microdistensiones grado I |
        | **Moderada** | `8 a 28 días` | Compromete entre 2 y 4 semanas de competición | Afecciones musculares grado II, esguinces |
        | **Severa** | `29 a 90 días` | Baja de 1 a 3 meses de calendario | Desgarros importantes, esguinces grado III |
        | **Muy Severa** | `91 a 180 días` | Baja prolongada de 3 a 6 meses | Fracturas óseas, cirugías articulares |
        | **Crónica / Fin de Temporada** | `> 180 días` | Pérdida de la temporada completa | Roturas de ligamento cruzado anterior (LCA), tendón de Aquiles |
        """)

        st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 20px;">
            <span class="db-badge">Tabla BD: injuries</span> &nbsp;
            <span class="tag-pill">injury_type</span>
            <span class="tag-pill">days_out</span>
            <span style="color: #94A3B8; font-size: 0.9rem;">Estas variables representan la frecuencia y duración de los eventos médicos en el universo de estudio.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.2 Características Antropométricas en el Fútbol")
        st.write("""
        La antropometría es la ciencia que estudia las dimensiones y proporciones del cuerpo humano. En el ámbito deportivo, 
        las variables antropométricas fundamentales incluyen la **altura (*height*)**, el **peso (*weight*)** y el **índice de masa corporal (IMC)**:
        """)

        st.markdown(r"""
        <div class="formula-container">
            <span style="font-size: 1.1rem; font-weight: 600;">Índice de Masa Corporal (IMC):</span><br>
            $$\text{IMC} = \frac{\text{Peso (kg)}}{[\text{Altura (m)}]^2}$$
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        - **Biomecánica y Somatotipo:** Teóricamente, el somatotipo y las dimensiones físicas de los futbolistas condicionan su desempeño biomecánico. 
        Jugadores de mayor altura y masa corporal concentran mayores inercias y fuerzas de frenado en cambios de aceleración excéntrica, lo que incrementa 
        su exposición a tensiones en la musculatura isquiotibial y estructuras articulares de rodilla y tobillo.
        - **Factor Edad:** La literatura científica destaca la edad como factor modulador crítico, distinguiendo perfiles entre:
          - *Veteranos (> 30 años):* Mayor susceptibilidad a lesiones musculares recidivantes por desgaste acumulado y menor velocidad de cicatrización tisular.
          - *Jóvenes en desarrollo (< 21 años):* Mayor vulnerabilidad a sobrecargas por adaptación musculoesquelética y maduración de cargas de alta competencia.
        """)

        st.markdown("""
        <div style="margin-top: 5px; margin-bottom: 20px;">
            <span class="db-badge">Tabla BD: players</span> &nbsp;
            <span class="tag-pill">height</span>
            <span class="tag-pill">weight</span>
            <span class="tag-pill">date_of_birth (edad)</span>
            <span style="color: #94A3B8; font-size: 0.9rem;">Permiten vincular conceptual y estadísticamente las dimensiones corporales con el registro médico de lesiones.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.3 Carga de Minutos como Proxy de Carga Externa")
        st.write("""
        El modelo teórico de la relación entre carga aguda y carga crónica (**ACWR – *Acute:Chronic Workload Ratio***, propuesto por Gabbett et al., 2016) 
        sostiene que la respuesta biológica del organismo depende del equilibrio dinámico entre la carga reciente de entrenamiento y partidos frente 
        a la capacidad adaptativa crónica acumulada.
        
        En los estudios observacionales de fútbol a gran escala donde no se dispone de telemetría microelectrónica GPS individualizada, 
        **los minutos jugados se utilizan como una aproximación (*proxy*) válida y estandarizada de la carga externa acumulada**.
        
        Conceptualmente, a mayor acumulación de minutos jugados (`minutes_played`) y apariciones (`appearances`), mayor es la exposición 
        del tejido musculoesquelético al estrés mecánico y a la fatiga neuromuscular. Esta teoría proporciona la base para analizar 
        la distribución empírica de los minutos en función de los rangos de severidad de días de baja médica.
        """)

        st.markdown("""
        <div style="margin-top: 5px; margin-bottom: 20px;">
            <span class="db-badge">Tabla BD: player_seasons</span> &nbsp;
            <span class="tag-pill">minutes_played</span>
            <span class="tag-pill">appearances</span>
            <span class="tag-pill">season</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.4 Limitaciones del Enfoque de Carga de Minutos")
        st.write("""
        El enfoque analítico fundamentado en minutos es estrictamente **observacional y descriptivo**. Desde el punto de vista fisiológico, 
        la carga externa acumulada no captura en su totalidad:
        - **La Carga Interna:** Respuesta fisiológica intrínseca individual (frecuencia cardíaca, percepción subjetiva del esfuerzo RPE, niveles de lactato en sangre).
        - **Factores Contextuales:** Calidad del sueño, higiene nutricional, factores de recuperación biomecánica o estrés psicosocial del deportista.
        """)

        st.markdown("""
        <div class="quote-box">
            <b>Evidencia de Harlow et al. (2021) en la Bundesliga:</b><br>
            La literatura científica ha documentado variaciones abruptas en las tasas de incidencia lesional ante modificaciones radicales en los 
            patrones de preparación física. En su análisis de la reanudación tras el confinamiento sanitario, la tasa de lesiones por partido 
            aumentó dramáticamente de <b>0.27 a 0.84 lesiones por encuentro</b>, demostrando la sensibilidad del tejido conectivo a interrupciones 
            y desbalances bruscos de carga.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.5 Diferencias Posicionales en Patrones de Lesión")
        st.write("""
        La teoría táctica moderna establece que las demandas bioenergéticas varían drásticamente según la función desempeñada en el terreno de juego:
        - **Extremos y Carrileros:** Presentan la mayor incidencia de lesiones musculares agudas durante partidos oficiales, producto de sprints repetidos a velocidad submáxima y máxima (>25 km/h).
        - **Defensas Centrales:** Evidencian mayor exposición a traumatismos, impactos articulares y contusiones en disputas aéreas y tackles.
        - **Centrocampistas:** Experimentan mayor tasa de desgaste por sobreuso articular y fatiga por volumen kilométrico total sostenido (~11 a 13 km por 90 minutos).
        """)

        st.markdown("""
        <div style="margin-top: 5px;">
            <span class="db-badge">Tabla BD: positions (14 posiciones)</span> &nbsp;
            <span class="db-badge">Tabla BD: player_positions (62,349 registros)</span> &nbsp;
            <span style="color: #94A3B8; font-size: 0.9rem;">Estructuran el cruce entre rol táctico, exigencia de juego y vulnerabilidad médica.</span>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # TAB SECCIÓN 2: VALOR POSICIONAL & TALENTO
    # ==========================================
    with tab_sec2:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 2</span>
            <h2 style="color: #F8FAFC;">Valor Posicional, Aportes por Líneas y Concentración de Talento</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.1 Definición y Funciones de las Líneas Posicionales")
        st.write("""
        La estructura organizativa del fútbol contemporáneo se articula en torno a cuatro líneas posicionales con demandas tácticas diferenciadas:
        """)

        lp1, lp2, lp3, lp4 = st.columns(4)
        with lp1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🧤 Arqueros (POR)</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Posición más especializada; su función primordial es prevenir goles mediante paradas, atajadas clave y control de centros aéreos.
                </p>
                <span class="tag-pill">Saves</span>
                <span class="tag-pill">Clean Sheets</span>
                <span class="tag-pill">xGP</span>
            </div>
            """, unsafe_allow_html=True)

        with lp2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🛡️ Defensas (DEF)</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Función primordial de proteger el tercio defensivo, cortar líneas de pase, despejar y recuperar la posesión del balón.
                </p>
                <span class="tag-pill">Tackles</span>
                <span class="tag-pill">Intercepciones</span>
                <span class="tag-pill">Bloqueos</span>
            </div>
            """, unsafe_allow_html=True)

        with lp3:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚙️ Mediocampistas (MED)</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Responsabilidades duales: creación y progresión ofensiva, volumen de pases y filtro de contención defensiva en el tercio medio.
                </p>
                <span class="tag-pill">Pases Clave</span>
                <span class="tag-pill">Circulación</span>
                <span class="tag-pill">Presión</span>
            </div>
            """, unsafe_allow_html=True)

        with lp4:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚡ Delanteros (DEL)</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Especializados en la finalización de jugadas, desmarques en profundidad y generación de peligro en el tercio final del campo.
                </p>
                <span class="tag-pill">Goles</span>
                <span class="tag-pill">xG</span>
                <span class="tag-pill">Disparos SOE</span>
            </div>
            """, unsafe_allow_html=True)

        st.write("""
        **Evaluación Multidimensional de Habilidad (`ability_score`):**
        La tabla hub `player_seasons` sintetiza el nivel competitivo del jugador a través del concepto de **`ability_score`**, 
        estructurado en cuatro dimensiones de rendimiento: **Overall**, **Offensive**, **Defensive** y **Midfield**. 
        Estas puntuaciones continuas fundamentan teóricamente el cálculo del aporte relativo y balance cualitativo de la plantilla.
        """)

        st.markdown("#### 2.2 Aporte Porcentual por Línea Posicional")
        st.write("""
        El **aporte porcentual** es un concepto analítico que cuantifica la contribución relativa de cada bloque táctico 
        al rendimiento colectivo total del equipo. Teóricamente se fundamenta en contrastar los indicadores globales del club 
        con las métricas agregadas por línea y demarcación espacial ($D, M, ST \times L/R/C$):
        """)

        st.markdown("""
        <div class="quote-box">
            <b>Hallazgo de Pappalardo et al. (2019):</b><br>
            A través de análisis de grafos y minería de eventos (<i>PlayerRank</i>), se corrobora la especialización técnica por líneas: 
            los delanteros dominan en goles y finalización; los mediocampistas monopolizan el volumen de circulación y pases de conexión; 
            mientras que los defensores sostienen el aporte en quites (*tackles*), intercepciones y despejes aéreos.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 5px; margin-bottom: 20px;">
            <span class="db-badge">player_stats_attacking</span> &nbsp;
            <span class="db-badge">player_stats_passing</span> &nbsp;
            <span class="db-badge">player_stats_defending</span> &nbsp;
            <span class="db-badge">player_stats_goalkeeping</span> &nbsp;
            <span style="color: #94A3B8; font-size: 0.9rem;">Tablas especializadas que sustentan la agregación del aporte porcentual por línea.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.3 Distribución y Concentración de Talento")
        st.write("""
        La concentración de talento es un concepto derivado de la sociología y la economía aplicada al deporte profesional, 
        que describe la distribución asimétrica y desigual de los futbolistas de élite entre los distintos clubes y divisiones competitivas. 
        En este proyecto, se operacionaliza a través de tres pilares cuantitativos:
        """)

        c_g1, c_g2, c_g3 = st.columns(3)
        with c_g1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📈 Distribución Porcentual</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Frecuencias relativas de futbolistas con alta calificación (<i>Tier Elite / Top Quartile</i>) según club y división competitiva.
                </p>
                <span class="tag-pill">Cuotas de Mercado</span>
                <span class="tag-pill">Concentración Top 10%</span>
            </div>
            """, unsafe_allow_html=True)

        with c_g2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚖️ Índices de Concentración</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    <b>Índice de Gini:</b> Desigualdad distributiva (0 = equidad perfecta, 1 = monopolio de talento).<br>
                    <b>Índice HHI:</b> Suma de cuotas al cuadrado.
                </p>
                <span class="tag-pill">Gini Coefficient</span>
                <span class="tag-pill">HHI Index</span>
            </div>
            """, unsafe_allow_html=True)

        with c_g3:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📊 Rangos de Rendimiento</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Estratificación estadística en percentiles y cuartiles sobre los <i>ability_scores</i> para caracterizar asimetrías de calidad.
                </p>
                <span class="tag-pill">Percentiles P25-P75</span>
                <span class="tag-pill">Dispersión Intercuartil</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(r"""
        <div class="formula-container">
            <span style="font-size: 1.05rem; font-weight: 600;">Índice Herfindahl-Hirschman de Talento (HHI):</span><br>
            $$\text{HHI} = \sum_{i=1}^{N} s_i^2 \quad \text{donde } s_i \text{ representa la cuota porcentual de talento del club } i$$
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 5px; margin-bottom: 20px;">
            <span class="db-badge">Tabla BD: clubs (2,773 clubes)</span> &nbsp;
            <span class="db-badge">Tabla BD: divisions (299 divisiones)</span> &nbsp;
            <span style="color: #94A3B8; font-size: 0.9rem;">Proporcionan el marco estructural para cuantificar la dispersión del talento entre ligas.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.4 Implicaciones para la Gestión de Plantillas")
        st.write("""
        Desde la teoría de la gestión deportiva profesional, el **valor posicional** y la **profundidad de plantilla** son factores determinantes del éxito competitivo sostenido:
        - **Profundidad de Plantilla (*Squad Depth*):** Se define como la cantidad y calidad de recambios disponibles por posición sin experimentar caídas drásticas de rendimiento.
        - **Vulnerabilidad por Lesiones:** Una excesiva concentración de minutos o talento en una sola figura convierte al equipo en altamente dependiente y frágil frente a bajas médicas imprevistas.
        - **Valor Económico vs. Rendimiento:** El análisis se complementa conceptualmente con la información de mercado de fichajes y estatus contractual para contrastar costo salarial con aporte deportivo.
        """)

        st.markdown("""
        <div style="margin-top: 5px;">
            <span class="db-badge">Tabla BD: transfers (41,425 registros)</span> &nbsp;
            <span class="db-badge">Tabla BD: contracts (41,425 registros)</span> &nbsp;
            <span style="color: #94A3B8; font-size: 0.9rem;">Aportan el contexto contractual para estudiar la relación entre valor de mercado y rendimiento.</span>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # TAB SECCIÓN 3: UNIVERSO DE DATOS & ARQUITECTURA
    # ==========================================
    with tab_sec3:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 3</span>
            <h2 style="color: #F8FAFC;">El Universo de Datos y Arquitectura Analítica</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 3.1 Sustento Empírico y Esquema Relacional Normalizado")
        st.write("""
        El sustento empírico de esta investigación se basa en una base de datos relacional normalizada en **Tercera Forma Normal (3FN)**, 
        la cual totaliza aproximadamente **855,000 registros** distribuidos armónicamente en 17 tablas:
        """)

        u1, u2 = st.columns(2)
        with u1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">👥 Población y Participación</div>
                <ul>
                    <li><b>27,343 futbolistas registrados:</b> Datos biográficos, fecha de nacimiento, nacionalidad y métricas antropométricas completas (altura, peso).</li>
                    <li><b>108,639 registros de temporadas (<code>player_seasons</code>):</b> Funciona como la tabla hub central longitudinal que une al jugador con su club, liga, minutos y puntuaciones.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with u2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🩺 Registro Clínico y Rendimiento</div>
                <ul>
                    <li><b>26,949 lesiones documentadas:</b> Eventos médicos catalogados por tipo de afección anatómica y severidad en días de baja (<code>days_out</code>).</li>
                    <li><b>Tablas especializadas de juego:</b> Subconjuntos analíticos dedicados a ataque, pases, defensa y portería.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="quote-box">
            <b>Vistas SQL Desnormalizadas:</b><br>
            Para garantizar que la aplicación web responda de manera fluida y en tiempo real, se implementó un concepto de diseño de bases de datos 
            orientado a la aceleración analítica mediante <b>vistas SQL precalculadas y desnormalizadas</b>. Estas vistas consolidan uniones complejas 
            entre jugadores, clubes, lesiones y estadísticas, permitiendo consultas instantáneas en el motor analítico.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 3.2 Stack Tecnológico de la Aplicación")
        st.write("""
        Para el procesamiento y presentación del universo de datos, la arquitectura se fundamenta en un stack moderno de ciencia de datos:
        """)

        st1, st2, st3, st4, st5 = st.columns(5)
        with st1:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <div style="font-size: 2rem;">🐍</div>
                <b style="color: #00E5FF;">Python 3</b>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 6px;">Lenguaje núcleo de procesamiento estadístico.</p>
            </div>
            """, unsafe_allow_html=True)

        with st2:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <div style="font-size: 2rem;">🦆</div>
                <b style="color: #00E5FF;">DuckDB OLAP</b>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 6px;">Motor analítico columnar local de ultra alta velocidad.</p>
            </div>
            """, unsafe_allow_html=True)

        with st3:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <div style="font-size: 2rem;">☁️</div>
                <b style="color: #00E5FF;">Supabase Cloud</b>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 6px;">Conexión remota escalable en la nube (PostgreSQL / MotherDuck).</p>
            </div>
            """, unsafe_allow_html=True)

        with st4:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <b style="color: #00E5FF;">Plotly Express</b>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 6px;">Visualización interactiva con paleta oscura y cian neón.</p>
            </div>
            """, unsafe_allow_html=True)

        with st5:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <div style="font-size: 2rem;">⚡</div>
                <b style="color: #00E5FF;">Streamlit UI</b>
                <p style="color: #94A3B8; font-size: 0.82rem; margin-top: 6px;">Interfaz web reactiva con estética Dark Cyber.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 3.3 Estructura Conceptual y Navegación de la Aplicación")
        st.write("""
        El dashboard operacionaliza la teoría mediante una arquitectura de navegación interactiva estructurada en seis módulos complementarios:
        """)

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🏠 1. Inicio (<code>app.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Portada institucional de la investigación, presentación del problema y acceso a los módulos analíticos.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📖 2. Marco Teórico (<code>05_Marco_Teórico.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Fundamentación académica completa, definiciones epidemiológicas, arquitectura analítica y glosario en pestañas interactivas.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📊 3. Dashboard General (<code>01_dashboard.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Resumen ejecutivo con tarjetas KPI (máximos goleadores, minutos), gráficos de concentración de talento por liga, rendimiento por posición y evolución histórica de lesiones.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🏆 4. Concentración de Talento (<code>02_Concentración_de_Talento.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Módulo de análisis de la distribución de jugadores clave por club, curvas de desigualdad y cálculo de índices de concentración.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚽ 5. Análisis Posicional (<code>03_Análisis_Posicional.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Comparación de estadísticas técnicas, contribución ofensiva/defensiva y cálculo del aporte porcentual por cada línea de juego.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🩺 6. Lesiones y Carga Física (<code>04_Lesiones_y_Carga_Física.py</code>)</div>
                <p style="color: #94A3B8; font-size: 0.92rem;">
                    Exploración visual mediante diagramas de dispersión y correlaciones entre minutos jugados, peso, altura y tiempo de baja médica.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB SECCIÓN 4: GLOSARIO DE CONCEPTOS Y MÉTRICAS
    # ==========================================
    with tab_sec4:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 4</span>
            <h2 style="color: #F8FAFC;">Glosario Integral de Conceptos y Métricas de la Investigación</h2>
            <p style="color: #CBD5E1; font-size: 1rem;">
                Catálogo formal y operativo de variables, definiciones estadísticas y métricas analíticas empleadas en el proyecto:
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 4.1 Conceptos Epidemiológicos y Antropométricos")
        ge1, ge2 = st.columns(2)
        with ge1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🩺 Lesión Deportiva</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Cualquier problema físico que impide al jugador participar plenamente en entrenamientos o partidos posteriores, 
                    conforme al criterio internacional de <b>pérdida de tiempo (time-loss)</b> del consenso ReFORM.
                </p>
                <span class="tag-pill">Time-Loss</span>
                <span class="tag-pill">Consenso ReFORM</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⏱️ Días de Baja (days_out)</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Tiempo cronológico total de inactividad médica deportiva del jugador, clasificado en rangos estandarizados de severidad 
                    (0, 1-3, 4-7, 8-28, 29-90, 91-180 y >180 días).
                </p>
                <span class="tag-pill">days_out</span>
                <span class="tag-pill">Severidad Clínica</span>
            </div>
            """, unsafe_allow_html=True)

        with ge2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">📐 Antropometría e IMC</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Dimensiones corporales de altura (<code>height</code>), peso (<code>weight</code>) e Índice de Masa Corporal 
                    ($\text{Peso} / \text{Altura}^2$) utilizados para tipificar somatotipos y evaluar factores de susceptibilidad física.
                </p>
                <span class="tag-pill">IMC (kg/m²)</span>
                <span class="tag-pill">Somatotipo</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🏃 Carga Física Externa (Proxy)</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Acumulación total de minutos oficiales disputados (<code>minutes_played</code>) y apariciones (<code>appearances</code>) 
                    utilizados como indicador cuantitativo de exposición al desgaste mecánico.
                </p>
                <span class="tag-pill">minutes_played</span>
                <span class="tag-pill">appearances</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 4.2 Métricas de Rendimiento Ofensivo")
        go1, go2 = st.columns(2)
        with go1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚽ Goles y Asistencias</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Eventos discretos tradicionales que representan la conversión directa de remates y el último pase previo al gol, 
                    reflejando el impacto directo en el marcador.
                </p>
                <span class="tag-pill">goals</span>
                <span class="tag-pill">assists</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🎯 Goles Esperados (xG) y xG/90</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    <b>xG:</b> Métrica probabilística que cuantifica la calidad objetiva de una ocasión de remate en función de su distancia, ángulo y situación.<br>
                    <b>xG/90:</b> Estandarización de los goles esperados generados por cada 90 minutos reglamentarios en cancha.
                </p>
                <span class="tag-pill">Expected Goals</span>
                <span class="tag-pill">xG por 90 min</span>
            </div>
            """, unsafe_allow_html=True)

        with go2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">💥 Creación de Disparos (SOE)</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Acciones de juego que derivan en un remate a portería (<i>Shots Over Expected</i>), cuantificando la capacidad intrínseca 
                    del futbolista para generar peligro de ataque.
                </p>
                <span class="tag-pill">SOE</span>
                <span class="tag-pill">Shot Creation</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🔄 Consistencia Inter-temporada</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Grado de estabilidad y persistencia que exhiben las métricas clave (xG/90, SOE) de un futbolista a lo largo 
                    del ciclo longitudinal de cuatro temporadas (2022-2026).
                </p>
                <span class="tag-pill">Persistencia Estadística</span>
                <span class="tag-pill">Ciclo 2022-2026</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 4.3 Métricas Defensivas y de Portería")
        gd1, gd2 = st.columns(2)
        with gd1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🛡️ Acciones Defensivas</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Frecuencia cuantificada de intervenciones para recuperar el balón: entradas exitosas (<i>tackles</i>), 
                    intercepciones de pases rivales, balones divididos ganados y despejes de área.
                </p>
                <span class="tag-pill">tackles</span>
                <span class="tag-pill">interceptions</span>
                <span class="tag-pill">clearances</span>
            </div>
            """, unsafe_allow_html=True)

        with gd2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🧤 Atajadas, Vallas Invictas y Goles Prevenidos (xGP)</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    <b>saves:</b> Paradas realizadas por el guardameta.<br>
                    <b>clean_sheets:</b> Partidos completos sin recibir goles.<br>
                    <b>xGP (Expected Goals Prevented):</b> Medida avanzada que resta los goles recibidos a la dificultad esperada de los tiros recibidos.
                </p>
                <span class="tag-pill">saves</span>
                <span class="tag-pill">clean_sheets</span>
                <span class="tag-pill">xGP</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 4.4 Métricas de Distribución y Valor Posicional")
        gp1, gp2 = st.columns(2)
        with gp1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">👥 Líneas Posicionales y Aporte Porcentual</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    <b>Líneas Posicionales:</b> Clasificación táctica en Arqueros (POR), Defensas (DEF), Mediocampistas (MED) y Delanteros (DEL).<br>
                    <b>Aporte Porcentual:</b> Fracción relativa (%) con la que cada línea contribuye al total de una métrica colectiva del club.
                </p>
                <span class="tag-pill">Líneas Tácticas</span>
                <span class="tag-pill">Aporte Relativo (%)</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⭐ Ability Score</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Puntuación sintética multivariada que resume el nivel de aptitud competitiva del futbolista en cuatro dimensiones 
                    (Overall, Offensive, Defensive, Midfield).
                </p>
                <span class="tag-pill">Overall Ability</span>
                <span class="tag-pill">Rating Multivariado</span>
            </div>
            """, unsafe_allow_html=True)

        with gp2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚖️ Índice de Gini e Índice HHI</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Coeficientes matemáticos para evaluar la asimetría y desigualdad competitiva: Gini mide la distribución de talento 
                    y HHI calcula la suma de participaciones al cuadrado para identificar monopolios deportivos.
                </p>
                <span class="tag-pill">Coeficiente de Gini</span>
                <span class="tag-pill">HHI de Talento</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🔄 Profundidad de Plantilla (Squad Depth)</div>
                <p style="color: #CBD5E1; font-size: 0.93rem;">
                    Distribución conceptual de minutos y calidad entre titulares y suplentes, indicando la resiliencia de la plantilla 
                    para mantener su rendimiento ante lesiones o suspensiones.
                </p>
                <span class="tag-pill">Rotación de Plantilla</span>
                <span class="tag-pill">Resiliencia Deportiva</span>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB REFERENCIAS BIBLIOGRÁFICAS
    # ==========================================
    with tab_refs:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Referencias y Documentación</span>
            <h2 style="color: #F8FAFC;">Bibliografía Consultada (Formato APA 7ma Edición)</h2>
            <p style="color: #CBD5E1; font-size: 0.95rem;">
                Literatura científica especializada en epidemiología de lesiones, modelos de carga física, valoración posicional y analítica deportiva:
            </p>
        </div>
        """, unsafe_allow_html=True)

        referencias = [
            ("Frick, B., Quansah, T. K., & Lang, M. (2023)", "Talent concentration and competitive imbalance in European soccer. Frontiers in Sports and Active Living, 5, 1148122. https://doi.org/10.3389/fspor.2023.1148122"),
            ("Fuller, C. W., Ekstrand, J., Junge, A., Andersen, T. E., Bahr, R., Dvorak, J., ... & Meeuwisse, W. H. (2006)", "Consensus statement on injury definitions and data collection procedures in studies of football (soccer) injuries. British Journal of Sports Medicine, 40(3), 193–201."),
            ("Gabbett, T. J., Hulin, B. T., Blanch, P., & Whiteley, R. (2016)", "High chronic training loads and exposure to bouts of maximal velocity running reduce injury risk in elite rugby league players. Journal of Science and Medicine in Sport, 19(3), 234–238."),
            ("Harlow, C. K., Drummond, J. E., & Voos, J. E. (2021)", "The effect of COVID-19 lockdown on injury rates in the Bundesliga. Frontiers in Sports and Active Living, 3, 630576."),
            ("Impellizzeri, F. M., Tenan, M. S., Kempton, T., Novak, A., & Coutts, A. J. (2020)", "Acute:Chronic Workload Ratio: Conceptual issues and fundamental pitfalls. International Journal of Sports Physiology and Performance, 15(6), 907–913."),
            ("Krutsch, W., Zeman, F., Zellner, J., Pfeifer, C., Nerlich, M., & Angele, P. (2016)", "Injury patterns among elite football players: A media-based analysis over 6 seasons with emphasis on playing position. International Journal of Sports Medicine, 37(11), 898–908."),
            ("Lucey, P., Bialkowski, A., Monfort, M., Carr, P., & Matthews, I. (2015)", "Quality vs quantity: Improved shot prediction in soccer using strategic features from spatiotemporal data. MIT Sloan Sports Analytics Conference."),
            ("Malone, S., Owen, A., Newton, M., Mendes, B., Collins, K. D., & Gabbett, T. J. (2016)", "The acute:chronic workload ratio in relation to injury risk in professional soccer. Journal of Science and Medicine in Sport, 20(6), 561–565."),
            ("Pappalardo, L., Cintia, P., Ferragina, P., Massucco, E., Pedreschi, D., & Giannotti, F. (2019)", "PlayerRank: Data-driven performance evaluation and player ranking in soccer via a machine learning approach. ACM Transactions on Intelligent Systems and Technology, 10(5), 1–27."),
            ("Pelechrinis, K., & Winston, W. (2021)", "Positional value in soccer: Expected league points added above replacement. Journal of Quantitative Analysis in Sports, 17(3), 187–201."),
            ("Walden, M., et al. (2025)", "ReFORM consensus on injury and illness definitions in football. British Journal of Sports Medicine.")
        ]

        for autor, obra in referencias:
            st.markdown(f"""
            <div class="bib-item">
                <b style="color: #00E5FF;">{autor}</b>. {obra}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_marco_teorico()
