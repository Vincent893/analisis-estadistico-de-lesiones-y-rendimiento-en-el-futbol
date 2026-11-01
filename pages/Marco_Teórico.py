from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos

def render_marco_teorico():
    UI.setup_page()
    cargar_estilos()
    UI.render_sidebar()

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
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 229, 255, 0.15);
        }
        .concept-title {
            color: #00E5FF;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 10px;
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
        .formula-container {
            background: rgba(2, 6, 23, 0.75);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 10px;
            padding: 16px 20px;
            margin: 14px 0;
            text-align: center;
            color: #38BDF8;
        }
        .nav-card {
            background: rgba(11, 19, 43, 0.6);
            border: 1px solid rgba(0, 229, 255, 0.18);
            border-radius: 12px;
            padding: 18px 16px;
            height: 100%;
            transition: all 0.25s ease;
        }
        .nav-card:hover {
            border-color: #00E5FF;
            background: rgba(15, 23, 42, 0.85);
            transform: translateY(-2px);
        }
        .glossary-term {
            color: #00E5FF;
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: 4px;
        }
        .glossary-desc {
            color: #CBD5E1;
            font-size: 0.93rem;
            line-height: 1.55;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-header">
            <span class="hero-badge">Marco Teórico Académico y Metodológico</span>
            <div class="hero-title">Marco Teórico</div>
            <p style="color: #94A3B8; margin: 0; font-size: 1.05rem; line-height: 1.6;">
                El análisis del rendimiento individual y colectivo en el fútbol profesional requiere un sustento conceptual
                que permita definir, clasificar y cuantificar las variables del estudio.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Universo Empírico y Estructura del Estudio")
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
                <div class="kpi-footer">Temporadas 2022 – 2026</div>
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

    tab_intro, tab_sec1, tab_sec2, tab_sec3, tab_sec4, tab_glosario, tab_refs = st.tabs([
        "Introducción",
        "1. Epidemiología y Carga Física",
        "2. Valor Posicional y Concentración",
        "3. Dinámicas Posicionales y Rendimiento",
        "4. Arquitectura y Ecosistema Analítico",
        "Glosario de Términos",
        "Referencias Bibliográficas",
    ])

    with tab_intro:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Introducción</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 12px;">Fundamentación Conceptual de la Investigación</h3>
            <p style="color: #E2E8F0; font-size: 1.02rem; line-height: 1.7; margin-bottom: 12px;">
                El análisis del rendimiento individual y colectivo en el fútbol profesional requiere un sustento conceptual
                que permita definir, clasificar y cuantificar las variables del estudio. El desarrollo teórico se articula
                en cuatro secciones fundamentales.
            </p>
            <p style="color: #CBD5E1; font-size: 1.0rem; line-height: 1.7; margin-bottom: 12px;">
                La primera sección aborda la epidemiología de lesiones y la carga física, que contextualiza el desgaste biológico del jugador.
                La segunda sección profundiza en el valor posicional y la concentración de talento, aportando las métricas matemáticas y estadísticas
                necesarias para medir la distribución del rendimiento. La tercera sección define las dinámicas posicionales y el rendimiento individual,
                estableciendo las métricas de consistencia y eficiencia. Finalmente, la cuarta sección describe la arquitectura de datos y el ecosistema
                analítico, explicando cómo se organiza la información (modelo relacional) y cuáles son las herramientas de procesamiento y visualización utilizadas.
            </p>
            <p style="color: #CBD5E1; font-size: 1.0rem; line-height: 1.7; margin-bottom: 0;">
                El desarrollo de estas secciones proporciona el rigor conceptual necesario para abordar las variables históricas del fútbol profesional
                (2022–2026). El documento se complementa con un glosario de términos que unifica el lenguaje técnico empleado a lo largo de la investigación.
            </p>
        </div>
        """, unsafe_allow_html=True)

        eje1, eje2 = st.columns(2)
        with eje1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">1. Epidemiología de Lesiones y Carga Física</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Contextualiza el desgaste biológico del futbolista mediante estándares internacionales (Consenso BioFORM)
                    y el criterio <i>time-loss</i>, vinculando las características antropométricas (altura, peso, IMC y edad)
                    y los minutos jugados como estimador del estrés fisiológico.
                </p>
                <span class="tag-pill">Consenso BioFORM</span>
                <span class="tag-pill">Criterio Time-Loss</span>
                <span class="tag-pill">Antropometría</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">3. Dinámicas Posicionales y Rendimiento Individual</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Evalúa la consistencia inter-temporada mediante el Coeficiente de Variación (CV = σ / μ) y la dependencia
                    del talento a través de la concentración del rendimiento en el quintil superior (Top 20%) de la plantilla.
                </p>
                <span class="tag-pill">Coeficiente de Variación (CV)</span>
                <span class="tag-pill">Dependencia Top 20%</span>
                <span class="tag-pill">Consistencia Inter-temporada</span>
            </div>
            """, unsafe_allow_html=True)

        with eje2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">2. Valor Posicional y Concentración de Talento</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Estructura las demarcaciones tácticas en cuatro líneas (POR, DEF, MED, DEL), aborda métricas ofensivas
                    avanzadas (xG, SOE) y cuantifica la desigualdad competitiva mediante los índices de Gini, Herfindahl-Hirschman (HHI)
                    y la Curva de Lorenz.
                </p>
                <span class="tag-pill">Estratificación Táctica</span>
                <span class="tag-pill">Goles Esperados (xG)</span>
                <span class="tag-pill">Curva de Lorenz & Gini</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">4. Arquitectura de Datos y Ecosistema Analítico</div>
                <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                    Detalla el modelo relacional normalizado en Tercera Forma Normal (3FN) con 17 tablas y más de 855,000 registros,
                    el motor columnar OLAP local DuckDB, la conexión en la nube con Supabase, y el entorno de procesamiento con Python, Pandas,
                    NumPy, Plotly Express y Streamlit.
                </p>
                <span class="tag-pill">Modelo 3FN (17 Tablas)</span>
                <span class="tag-pill">Motor DuckDB OLAP</span>
                <span class="tag-pill">Python & Streamlit</span>
            </div>
            """, unsafe_allow_html=True)

    with tab_sec1:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Sección 1</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">1. Epidemiología de Lesiones y Carga Física</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Estándares de registro, factores antropométricos y volumen de exposición competitiva.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.1. El Consenso Internacional y el Criterio Time-Loss")
        st.write("""
        La epidemiología de lesiones en el fútbol se rige por estándares internacionales para garantizar la comparabilidad de los datos.
        El **consenso BioFORM** (y sus predecesores) establece que una lesión debe ser registrada bajo el criterio de **time-loss** (pérdida de tiempo).
        Esto significa que solo se considera lesión aquella que impide al jugador participar en entrenamientos o partidos por al menos 24 horas.
        Este criterio permite cuantificar objetivamente la gravedad a través de los **días de baja médica**, evitando sesgos subjetivos.
        """)

        st.markdown("""
        <div class="quote-box">
            <b>Criterio BioFORM / COI:</b><br>
            "Solo se considera lesión aquella que impide al jugador participar en entrenamientos o partidos por al menos 24 horas,
            permitiendo cuantificar de forma objetiva la severidad en días de baja médica."
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 1.2. Antropometría y Biomecánica")
        st.write("""
        La literatura deportiva vincula las características antropométricas (altura, peso, Índice de Masa Corporal —IMC— y edad) con la incidencia
        y el tipo de lesión. El exceso de masa corporal o las variaciones de edad influyen en la carga biomecánica durante los esfuerzos de alta intensidad.
        El análisis de estas variables permite describir perfiles de riesgo de manera poblacional.
        """)

        st.markdown(r"""
        <div class="formula-container">
            <b style="color: #F8FAFC; font-size: 1.05rem;">Índice de Masa Corporal (IMC):</b><br>
            $$\text{IMC} = \frac{\text{Peso (kg)}}{[\text{Altura (m)}]^2}$$
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        - **Masa Corporal e Inercia:** Jugadores de mayor altura y masa corporal concentran mayores fuerzas de desaceleración e impacto articular, modulando la susceptibilidad a sobrecargas y lesiones tendinosas.
        - **Factor Edad:** Los cambios biológicos propios de la edad condicionan la tolerancia tisular y el tiempo de recuperación, siendo una variable fundamental para la estratificación demográfica de las plantillas.
        """)

        st.markdown("#### 1.3. La Carga Física (Minutos Jugados)")
        st.write("""
        La acumulación de minutos de juego es utilizada en la literatura como un **proxy (aproximación) del estrés fisiológico y biomecánico acumulado**.
        La saturación del calendario en el fútbol moderno hace que el volumen de exposición competitiva sea un factor crítico a describir cuando se analizan
        las bajas médicas de una plantilla.
        """)

    with tab_sec2:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Sección 2</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">2. Valor Posicional y Concentración de Talento</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Estratificación táctica, métricas de rendimiento ofensivo y cuantificación de la desigualdad competitiva.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.1. Estratificación Táctica y Demarcaciones")
        st.write("""
        El fútbol se estructura funcionalmente en cuatro líneas o bloques: **Arqueros (POR)**, **Defensas (DEF)**, **Mediocampistas (MED)** y **Delanteros (DEL)**.
        La teoría táctica moderna reconoce una asimetría de responsabilidades: especialización extrema en los extremos del campo
        (la defensa busca neutralizar, la delantera busca resolver) y una polivalencia bidireccional en la zona media.
        El análisis del aporte porcentual por bloque permite describir el equilibrio estructural de un equipo.
        """)

        pos_c1, pos_c2, pos_c3, pos_c4 = st.columns(4)
        with pos_c1:
            st.markdown("""
            <div class="concept-card" style="text-align: center;">
                <b style="color: #00E5FF;">Arqueros (POR)</b>
                <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 6px;">
                    Demarcación altamente especializada orientada a la contención directa de remates y protección del arco.
                </p>
            </div>""", unsafe_allow_html=True)
        with pos_c2:
            st.markdown("""
            <div class="concept-card" style="text-align: center;">
                <b style="color: #10B981;">Defensas (DEF)</b>
                <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 6px;">
                    Especialización en neutralización, cortes de juego, intercepciones y protección del área propia.
                </p>
            </div>""", unsafe_allow_html=True)
        with pos_c3:
            st.markdown("""
            <div class="concept-card" style="text-align: center;">
                <b style="color: #3B82F6;">Mediocampistas (MED)</b>
                <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 6px;">
                    Eje híbrido y bidireccional; combina generación de juego, distribución y contención territorial.
                </p>
            </div>""", unsafe_allow_html=True)
        with pos_c4:
            st.markdown("""
            <div class="concept-card" style="text-align: center;">
                <b style="color: #F59E0B;">Delanteros (DEL)</b>
                <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 6px;">
                    Especialización ofensiva en definición, remates a portería y capitalización de ocasiones de gol.
                </p>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 2.2. Métricas Ofensivas Avanzadas")
        st.write("""
        El análisis descriptivo moderno supera los conteos básicos (goles, asistencias) mediante métricas que contextualizan el rendimiento.
        Los **Goles Esperados (xG)** cuantifican la calidad de las ocasiones generadas, permitiendo evaluar si un jugador o equipo rinde por encima o por debajo
        de lo esperado según la probabilidad de gol de sus disparos. Complementariamente, las métricas de **creación de disparos (SOE)** permiten describir
        la participación de un jugador en la generación de peligro.
        """)

        st.markdown("#### 2.3. Métricas de Concentración: Gini y HHI")
        st.write("""
        Para medir cómo se distribuye el talento o el rendimiento en una liga, la analítica deportiva emplea métricas matemáticas adaptadas del campo
        de la estadística y la economía:
        """)

        st.write("""
        - **Índice de Gini:** Es una medida de desigualdad que se calcula a partir de la Curva de Lorenz; su valor oscila entre 0 (igualdad perfecta) y 1 (concentración total).
          En el contexto deportivo, un Gini cercano a 0 indica que el rendimiento ofensivo está repartido equitativamente, mientras que un valor alto indica que pocos clubes acaparan la producción.
        - **Índice Herfindahl-Hirschman (HHI):** Se calcula sumando los cuadrados de las cuotas de participación. Se utiliza para evaluar la concentración del mercado:
          un HHI bajo indica una estructura competitiva equilibrada, mientras que un HHI alto describe una estructura oligopólica donde unos pocos clubes dominan el talento.
        """)

        st.markdown(r"""
        <div class="formula-container">
            <b style="color: #F8FAFC; font-size: 1.05rem;">Fórmula del Índice Herfindahl-Hirschman (HHI):</b><br>
            $$\text{HHI} = \sum_{i=1}^{N} s_i^2 \quad \text{donde } s_i \text{ representa la cuota porcentual de participación del club } i$$
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.4. La Curva de Lorenz")
        st.write("""
        Es la representación gráfica del Índice de Gini. Mide el **porcentaje acumulado de rendimiento (goles, asistencias)** frente al
        **porcentaje acumulado de jugadores o clubes**. Cuanto más se aleje la curva de la diagonal de 45 grados (línea de igualdad perfecta),
        mayor será la concentración del talento o del gol en pocos actores.
        """)

    with tab_sec3:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Sección 3</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">3. Dinámicas Posicionales y Rendimiento Individual</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Consistencia temporal, dispersión relativa y centralización de la producción en la plantilla.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 3.1. La Consistencia y el Coeficiente de Variación (CV)")
        st.write("""
        La consistencia de un jugador o una demarcación se evalúa mediante la dispersión de sus datos a lo largo del tiempo.
        El **Coeficiente de Variación (CV)** es una medida estadística que expresa la desviación estándar como un porcentaje de la media aritmética:
        """)

        st.markdown(r"""
        <div class="formula-container">
            <b style="color: #F8FAFC; font-size: 1.05rem;">Fórmula del Coeficiente de Variación (CV):</b><br>
            $$CV = \frac{\sigma}{\mu} = \frac{\text{Desviación Estándar}}{\text{Media}}$$
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        Su fórmula permite comparar la volatilidad de datos con diferentes escalas.
        Un **CV bajo** describe un rendimiento estable y homogéneo; un **CV alto** describe un rendimiento volátil, sujeto a altibajos temporada tras temporada.
        En el análisis posicional, las posiciones defensivas y de contención exhiben habitualmente los CV más bajos, mientras que los atacantes exteriores
        y delanteros presentan un CV superior derivado de rachas anotadoras y variabilidad táctica.
        """)

        st.markdown("#### 3.2. La Dependencia del Talento (Top 20%)")
        st.write("""
        La distribución interna del rendimiento en una plantilla es un indicador clave. En la literatura de análisis deportivo, se evalúa
        qué porcentaje del rendimiento total del equipo recae sobre el **20% más productivo de sus jugadores (el quintil superior)**.
        """)

        st.markdown("""
        <div class="quote-box">
            <b>Criterio de Dependencia:</b><br>
            Una concentración superior al <b>65%</b> describe una alta dependencia de un grupo muy reducido de futbolistas, caracterizando plantillas
            cuya producción ofensiva está fuertemente centralizada en sus figuras principales. Por el contrario, registros inferiores al <b>50%</b>
            reflejan un modelo de producción coral y distribuido.
        </div>
        """, unsafe_allow_html=True)

    with tab_sec4:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Sección 4</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">4. Arquitectura de Datos y Ecosistema Analítico</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Principios de ingeniería de datos, almacenamiento relacional, motores analíticos y stack de visualización.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        Para garantizar el rigor y la escalabilidad del análisis, el estudio se sustenta en principios de ingeniería de datos.
        La correcta comprensión de estos conceptos es fundamental para entender cómo se organiza la información del proyecto y qué herramientas permiten su procesamiento.
        """)

        st.markdown("#### 4.1. Modelo Relacional y Normalización (3FN)")
        st.write("""
        El universo de datos del proyecto se organiza bajo un modelo relacional normalizado.
        La **Tercera Forma Normal (3FN)** es un principio de diseño de bases de datos que elimina la redundancia y garantiza la integridad referencial.
        En lugar de tener una única tabla con datos repetidos, la información se divide en **17 tablas especializadas (entidades)** que se relacionan entre sí
        mediante claves primarias y foráneas.
        Esto permite que un jugador, una temporada y una lesión estén vinculados lógicamente sin duplicar información, asegurando la trazabilidad
        de los más de **855,000 registros** del estudio.
        """)

        st.markdown("#### 4.2. Procesamiento Analítico (OLAP) y DuckDB")
        st.write("""
        Para el análisis de grandes volúmenes de datos, se utiliza un enfoque **OLAP (Online Analytical Processing)**.
        A diferencia de las bases de datos transaccionales (**OLTP**) diseñadas para registrar operaciones diarias, las bases de datos OLAP están optimizadas
        para consultas complejas y agregaciones rápidas.

        El motor columnar **DuckDB** es una base de datos analítica local que permite procesar estos datos de manera ultrarrápida,
        mientras que **Supabase** proporciona una capa de conexión remota en la nube para el despliegue del ecosistema.
        """)

        st.markdown("#### 4.3. Procesamiento y Visualización: Python, Pandas y Plotly")
        st.write("""
        El procesamiento de los datos se realiza mediante **Python**, un lenguaje de programación de propósito general ampliamente utilizado en ciencia de datos.
        Las librerías **Pandas** y **NumPy** permiten la manipulación, limpieza y cálculo numérico de los registros.

        Para la representación gráfica, se emplea **Plotly Express**, una librería que permite construir visualizaciones interactivas y dinámicas,
        facilitando la exploración de los datos por parte del usuario.
        """)

        st.markdown("#### 4.4. Interfaz de Usuario: Streamlit")
        st.write("""
        La interfaz de usuario se desarrolla en **Streamlit**, un framework de código abierto que permite desplegar aplicaciones web de datos de forma ágil.
        Streamlit transforma los scripts de Python en dashboards interactivos, permitiendo que el usuario final navegue por las métricas y visualizaciones
        sin necesidad de conocimientos técnicos en programación.
        """)

        st.markdown("<br>", unsafe_allow_html=True)

        col_stk1, col_stk2, col_stk3, col_stk4 = st.columns(4)
        with col_stk1:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <b style="color: #00E5FF; font-size: 1.05rem;">Python & Pandas</b>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 8px; margin-bottom: 0;">
                    Procesamiento, limpieza y cálculo numérico descriptivo de datos tabulares.
                </p>
            </div>""", unsafe_allow_html=True)
        with col_stk2:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <b style="color: #00E5FF; font-size: 1.05rem;">DuckDB OLAP</b>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 8px; margin-bottom: 0;">
                    Motor analítico columnar local para agregaciones y consultas masivas inmediatas.
                </p>
            </div>""", unsafe_allow_html=True)
        with col_stk3:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <b style="color: #00E5FF; font-size: 1.05rem;">Plotly Express</b>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 8px; margin-bottom: 0;">
                    Construcción de gráficos interactivos descriptivos con control dinámico de datos.
                </p>
            </div>""", unsafe_allow_html=True)
        with col_stk4:
            st.markdown("""
            <div class="nav-card" style="text-align: center;">
                <b style="color: #00E5FF; font-size: 1.05rem;">Streamlit Web</b>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-top: 8px; margin-bottom: 0;">
                    Despliegue de paneles web reactivos y navegación modular para el usuario.
                </p>
            </div>""", unsafe_allow_html=True)

    with tab_glosario:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Glosario</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">Glosario de Términos y Métricas</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Definición formal y operativa de los términos técnicos y métricas analíticas de la investigación.
            </p>
        </div>
        """, unsafe_allow_html=True)

        g_items = [
            ("BioFORM", "Consenso internacional para el registro estandarizado de lesiones deportivas."),
            ("Time-Loss", "Criterio epidemiológico que define una lesión por la incapacidad de participar en entrenamientos o partidos."),
            ("P90 (Percentil 90)", "Umbral estadístico que identifica al 10% superior de los jugadores en una métrica determinada (jugadores de élite)."),
            ("Coeficiente de Variación (CV)", "Medida estadística que expresa la desviación estándar como porcentaje de la media (CV = σ / μ)."),
            ("Gini", "Medida económica que cuantifica la desigualdad en una distribución (0 = igualdad, 1 = concentración total)."),
            ("HHI (Herfindahl-Hirschman)", "Medida de concentración de mercado que suma los cuadrados de las cuotas de participación."),
            ("xG (Goles Esperados)", "Métrica probabilística que mide la calidad de un disparo."),
            ("Top 20%", "El quintil superior de una plantilla (el 20% más productivo)."),
            ("3FN (Tercera Forma Normal)", "Estándar de diseño de bases de datos relacionales que elimina la redundancia."),
            ("OLAP", "Procesamiento Analítico en Línea; arquitectura de bases de datos optimizada para consultas multidimensionales y agregación de grandes volúmenes de datos."),
            ("OLTP", "Procesamiento de Transacciones en Línea; arquitectura de bases de datos optimizada para el registro rápido de operaciones diarias."),
        ]

        col_g1, col_g2 = st.columns(2)
        for i, (term, desc) in enumerate(g_items):
            target_col = col_g1 if i % 2 == 0 else col_g2
            with target_col:
                st.markdown(f"""
                <div class="concept-card">
                    <div class="glossary-term">{term}</div>
                    <p class="glossary-desc">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab_refs:
        st.markdown("""
        <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 22px 26px; margin-bottom: 22px;">
            <span class="theory-badge">Bibliografía</span>
            <h3 style="color: #F8FAFC; margin-top: 5px; margin-bottom: 8px;">Referencias Bibliográficas (Formato APA 7ma Edición)</h3>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                Literatura científica especializada en epidemiología de lesiones, modelos de carga física, valoración posicional y analítica deportiva.
            </p>
        </div>
        """, unsafe_allow_html=True)

        referencias = [
            ("Bahr, R., Clarsen, B., Derman, W., Dvorak, J., Emery, C. A., Finch, C. F., ... & Khan, K. M. (2020)", "International Olympic Committee consensus statement: Methods for recording and reporting of epidemiological data on injury and illness in sport 2020 (including the STROBE Extension for Sport Injury and Illness Surveillance (STROBE-SIIS)). British Journal of Sports Medicine, 54(7), 372–389."),
            ("Frick, B., Quansah, T. K., & Lang, M. (2023)", "Talent concentration and competitive imbalance in European soccer. Frontiers in Sports and Active Living, 5, 1148122. https://doi.org/10.3389/fspor.2023.1148122"),
            ("Fuller, C. W., Ekstrand, J., Junge, A., Andersen, T. E., Bahr, R., Dvorak, J., ... & Meeuwisse, W. H. (2006)", "Consensus statement on injury definitions and data collection procedures in studies of football (soccer) injuries. British Journal of Sports Medicine, 40(3), 193–201."),
            ("Gabbett, T. J., Hulin, B. T., Blanch, P., & Whiteley, R. (2016)", "High chronic training loads and exposure to bouts of maximal velocity running reduce injury risk in elite rugby league players. Journal of Science and Medicine in Sport, 19(3), 234–238."),
            ("Harlow, C. K., Drummond, J. E., & Voos, J. E. (2021)", "The effect of COVID-19 lockdown on injury rates in the Bundesliga. Frontiers in Sports and Active Living, 3, 630576."),
            ("Impellizzeri, F. M., Tenan, M. S., Kempton, T., Novak, A., & Coutts, A. J. (2020)", "Acute:Chronic Workload Ratio: Conceptual issues and fundamental pitfalls. International Journal of Sports Physiology and Performance, 15(6), 907–913."),
            ("Krutsch, W., Zeman, F., Zellner, J., Pfeifer, C., Nerlich, M., & Angele, P. (2016)", "Injury patterns among elite football players: A media-based analysis over 6 seasons with emphasis on playing position. International Journal of Sports Medicine, 37(11), 898–908."),
            ("Lucey, P., Bialkowski, A., Monfort, M., Carr, P., & Matthews, I. (2015)", "Quality vs quantity: Improved shot prediction in soccer using strategic features from spatiotemporal data. MIT Sloan Sports Analytics Conference."),
            ("Pappalardo, L., Cintia, P., Ferragina, P., Massucco, E., Pedreschi, D., & Giannotti, F. (2019)", "PlayerRank: Data-driven performance evaluation and player ranking in soccer via a machine learning approach. ACM Transactions on Intelligent Systems and Technology, 10(5), 1–27."),
            ("Pelechrinis, K., & Winston, W. (2021)", "Positional value in soccer: Expected league points added above replacement. Journal of Quantitative Analysis in Sports, 17(3), 187–201."),
        ]

        for autor, obra in referencias:
            st.markdown(f"""
            <div class="bib-item">
                <b style="color: #00E5FF;">{autor}</b>. {obra}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Conclusiones del Marco Teórico")

    st.markdown("""
    <div class="section-container" style="border-left: 4px solid #00E5FF; padding: 25px 30px; margin-top: 15px; margin-bottom: 25px;">
        <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Síntesis Conceptual y Metodológica de la Investigación</h4>
        <ul style="color: #E2E8F0; line-height: 1.8; margin-bottom: 0; font-size: 1.0rem;">
            <li><b>Estandarización Epidemiológica y Cuantificación de Carga:</b> La adopción del consenso internacional BioFORM bajo el criterio de pérdida de tiempo (<i>time-loss</i>) proporciona una delimitación médica objetiva. A su vez, los minutos acumulados se consolidan como un estimador (<i>proxy</i>) reproducible del estrés mecánico y fisiológico en el ciclo 2022–2026.</li>
            <li><b>Estratificación Táctica y Valor Posicional:</b> La estructuración del juego en cuatro bloques funcionales (Arqueros, Defensas, Mediocampistas y Delanteros) sustenta la asimetría de responsabilidades: especialización extrema en finalización y neutralización en los extremos del campo frente a la polivalencia bidireccional en la zona media.</li>
            <li><b>Cuantificación de la Desigualdad y Concentración Competitiva:</b> La traslación de métricas económicas como el Coeficiente de Gini, las Curvas de Lorenz y el Índice Herfindahl-Hirschman (HHI) permite diagnosticar con precisión matemática si el rendimiento y el talento de élite (P90) se distribuyen de forma paritaria o se concentran en oligopolios deportivos.</li>
            <li><b>Solidez del Ecosistema Relacional y Enfoque Descriptivo:</b> La arquitectura normalizada en Tercera Forma Normal (3FN) con 17 entidades y más de 855,000 registros, procesada a través del motor columnar local DuckDB y visualizada en Streamlit y Plotly, asegura la trazabilidad íntegra del estudio bajo una perspectiva estrictamente descriptiva.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_marco_teorico()
