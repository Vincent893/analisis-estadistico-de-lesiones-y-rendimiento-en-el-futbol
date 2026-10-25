from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos

def render_marco_teorico():
    UI.setup_page()
    cargar_estilos()
    UI.render_sidebar()

    # CSS adicional para enriquecer la lectura académica y elementos de diseño
    st.markdown("""
        <style>
        .theory-badge {
            background: rgba(0, 229, 255, 0.12);
            color: #00E5FF;
            border: 1px solid rgba(0, 229, 255, 0.35);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
            margin-bottom: 8px;
        }
        .quote-box {
            background: rgba(11, 19, 43, 0.6);
            border-left: 4px solid #00E5FF;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin: 15px 0;
            font-style: italic;
            color: #CBD5E1;
        }
        .concept-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(0, 229, 255, 0.15);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.25s ease-in-out;
        }
        .concept-card:hover {
            border-color: rgba(0, 229, 255, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 229, 255, 0.12);
        }
        .concept-title {
            color: #00E5FF;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .bib-item {
            background: rgba(11, 19, 43, 0.4);
            border-left: 3px solid #00A8CC;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 10px;
            font-size: 0.92rem;
            color: #CBD5E1;
            line-height: 1.5;
        }
        .tag-pill {
            background: rgba(0, 168, 204, 0.15);
            color: #38BDF8;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            margin-right: 5px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Header Principal
    st.markdown("""
        <div class="hero-header">
            <span class="hero-badge">Fundamentación Científica & Metodológica</span>
            <div class="hero-title">Marco Teórico de la Investigación</div>
            <p style="color: #94A3B8; margin: 0; font-size: 1.05rem;">
                Evaluación de Lesiones, Dinámicas Posicionales y Rendimiento de Clubes en el Fútbol Profesional (2022-2026)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Tarjetas métricas del dataset analizado
    st.markdown("### 📊 Universo Empírico y Estructura del Estudio")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Esquema Relacional</div>
                <div class="kpi-value">17 Tablas</div>
                <div class="kpi-footer">3ª Forma Normal</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Muestra de Jugadores</div>
                <div class="kpi-value">27,343</div>
                <div class="kpi-footer">Datos Antropométricos</div>
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
                <div class="kpi-title">Historial Clínico</div>
                <div class="kpi-value">26,949</div>
                <div class="kpi-footer">Lesiones Documentadas</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs de navegación por secciones
    tab_intro, tab_sec1, tab_sec2, tab_sec3, tab_refs = st.tabs([
        "📌 Introducción",
        "🩺 Sec 1: Lesiones y Carga",
        "🎯 Sec 2: xG y Rendimiento",
        "🛡️ Sec 3: Valor Posicional y Aportes",
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
            <p style="color: #CBD5E1; font-size: 1.02rem; line-height: 1.6;">
                La fundamentación teórica de esta investigación se articula en torno a tres ejes analíticos principales 
                correspondientes a los objetivos específicos desarrollados para caracterizar el fútbol profesional contemporáneo:
            </p>
        </div>
        """, unsafe_allow_html=True)

        eje1, eje2, eje3 = st.columns(3)
        with eje1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🩺 Eje 1: Epidemiología</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Epidemiología de lesiones y su interacción con las características antropométricas (altura, peso, edad) 
                    y la carga acumulada de minutos jugados.
                </p>
                <span class="tag-pill">Consenso ReFORM</span>
                <span class="tag-pill">Fatiga Mecánica</span>
            </div>
            """, unsafe_allow_html=True)

        with eje2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚽ Eje 2: Consistencia Ofensiva</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Cuantificación del rendimiento ofensivo mediante modelado probabilístico de disparos (Goles Esperados, xG y xG+) 
                    y análisis de consistencia inter-temporada.
                </p>
                <span class="tag-pill">xG / xG+</span>
                <span class="tag-pill">Shot Creation</span>
            </div>
            """, unsafe_allow_html=True)

        with eje3:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">🛡️ Eje 3: Valor Posicional</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Valoración del aporte relativo por líneas posicionales (arqueros, defensas, medios, delanteros) 
                    y dinámicas colectivas en las plantillas.
                </p>
                <span class="tag-pill">Líneas Posicionales</span>
                <span class="tag-pill">Aporte Colectivo</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="quote-box">
            "El período 2022-2026 tiene una especial relevancia por la intensificación del calendario futbolístico derivada 
            de la expansión de competiciones internacionales, lo que incrementó la necesidad de herramientas analíticas 
            robustas para la gestión de cargas, la prevención de lesiones y la optimización del rendimiento colectivo."
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 **Fuente de Datos**: Base de datos `SQL Practice DB: Football Players (17 Tables)`, organizada bajo un diseño normalizado con 855,000 registros totales, permitiendo análisis SQL exploratorios, agregaciones complejas y modelado longitudinal.")

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

        st.markdown("#### 1.1 Definición Operativa y Clasificación de Lesiones (Consenso ReFORM)")
        st.write("""
        Históricamente, la investigación epidemiológica ha enfrentado la falta de definiciones estandarizadas. El consenso **ReFORM**, 
        alineado con el Comité Olímpico Internacional, establece como criterio operativo central la **pérdida de tiempo (*time-loss*)**:
        
        > *Se registra una lesión cuando un jugador no puede participar plenamente en entrenamientos o partidos posteriores debido a un problema de salud.*
        """)

        # Tabla de severidad
        st.markdown("**Estratificación de Severidad según Días de Baja (ReFORM):**")
        st.markdown("""
        | Categoría de Severidad | Días de Baja | Impacto en Disponibilidad |
        | :--- | :--- | :--- |
        | **Mínima / Nula** | 0 a 3 días | Ausencia transitoria, no compromete ciclos competitivos |
        | **Leve** | 4 a 7 días | Baja de 1 partido promedio |
        | **Moderada** | 8 a 28 días | Afección muscular o ligamentosa grado I-II |
        | **Severa** | 29 a 90 días | Desgarros importantes, esguinces graves |
        | **Muy Severa / Crónica** | > 90 a > 180 días | Roturas de LCA, cirugías mayores, fin de temporada |
        """)

        st.markdown("#### 1.2 Características Antropométricas como Factores de Riesgo")
        st.write("""
        La antropometría (altura, peso, IMC y edad) condiciona las fuerzas dinámicas a las que se someten las articulaciones y grupos musculares:
        - **Altura y Peso**: Jugadores más altos y pesados experimentan mayor tensión mecánica sobre los tejidos en acciones explosivas (frenadas, saltos y cambios de dirección), aumentando el riesgo de desgarros en la musculatura isquiotibial.
        - **Factor Edad**: Futbolistas mayores de 30 años exhiben mayor tiempo de cicatrización y susceptibilidad a lesiones musculares recidivantes, mientras que sub-21 sufren mayores lesiones por sobrecarga fisiológica derivada de la maduración musculoesquelética.
        """)

        st.markdown("#### 1.3 Carga de Minutos como Proxy de Carga Externa y ACWR")
        st.write("""
        El modelo **ACWR** (*Acute:Chronic Workload Ratio*) postula que el riesgo de lesión se eleva cuando la carga aguda reciente (últimos 7 días) 
        supera con creces a la carga crónica de adaptación acumulada (últimos 28 días). Un ratio entre **1.00 y 1.25** confiere un efecto protector (**OR = 0.68, p = 0.006**), mientras que picos abruptos incrementan drásticamente el riesgo (**OR = 1.95**).
        """)

        st.info("📌 **Ajuste Metodológico del Proyecto**: Dado que la base de datos registra minutos acumulados por temporada y apariciones (`minutes_played`, `appearances`) y no series semanales de GPS, se adopta la **carga acumulada de minutos** como proxy validado de la carga externa.")

        st.markdown("#### 1.4 Patrones de Lesión según la Demarcación Posicional")
        st.write("""
        Krutsch et al. (2016) demostraron variaciones significativas entre demarcaciones tácticas:
        - **Extremos**: Mayor incidencia y tasa de lesiones durante partidos oficiales, producto de sprints repetidos a máxima velocidad.
        - **Defensas Centrales**: Mayor incidencia en sesiones de entrenamiento y acciones de choque/cabeceo.
        - **Centrocampistas**: Mayor tasa global de no disponibilidad por desgaste continuo de distancia recorrida (~11-13 km por 90 min).
        """)

    # ==========================================
    # TAB SECCIÓN 2: RENDIMIENTO OFENSIVO Y xG
    # ==========================================
    with tab_sec2:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 2</span>
            <h2 style="color: #F8FAFC;">Rendimiento Ofensivo, Consistencia Competitiva y Goles Esperados (xG)</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.1 Fundamentos Teóricos del xG (*Expected Goals*)")
        st.write("""
        El modelo probabilístico de goles esperados ($xG$) cuantifica la probabilidad de que un disparo se convierta en gol en función 
        de sus atributos objetivos: ángulo hacia el arco, distancia, parte del cuerpo ejecutora (cabeza/pie), tipo de asistencia, toques previos y presión defensiva.
        
        **Separación de Proceso vs. Resultado:**
        Los goles reales en muestras pequeñas están sujetos a alta varianza y azar. Una caída en goles manteniendo $xG$ alto refleja mala fortuna o rachas transitorias de finalización; una caída en $xG$ delata una crisis estructural en la generación de peligro.
        """)

        st.markdown("#### 2.2 Limitaciones del xG Tradicional y Evolución hacia xG+")
        
        c_xg1, c_xg2 = st.columns(2)
        with c_xg1:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">⚠️ Limitaciones del xG Convencional</div>
                <ul>
                    <li><b>Sesgo de selección de tiro:</b> Solo evalúa remates efectuados, ignorando centros rasos letales que no lograron ser conectados.</li>
                    <li><b>Independencia de eventos:</b> Múltiples rebotes seguidos sobreinflan el xG acumulado de una sola posesión.</li>
                    <li><b>Homogeneidad del ejecutante:</b> Asigna la misma probabilidad si patea un defensor central o un especialista de élite.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with c_xg2:
            st.markdown("""
            <div class="concept-card">
                <div class="concept-title">✨ Marco xG+ y Probabilidad Dinámica</div>
                <ul>
                    <li><b>Componente xS:</b> Modela la probabilidad de que ocurra un remate en el siguiente segundo.</li>
                    <li><b>xG+ Integral:</b> Evalúa la peligrosidad del ataque, ocurra o no el disparo final.</li>
                    <li><b>SOE (Shots Over Expected):</b> Capacidad intrínseca de crear volumen de tiros, altamente consistente inter-temporada.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="quote-box">
            <b>Hallazgo de Pipping et al. (2025):</b> La capacidad de creación de disparos (<i>shot creation</i>, xG/90 y SOE) 
            es notablemente más persistente y estable entre temporadas que la eficiencia de definición pura (GOE, <i>Goals Over Expected</i>), 
            constituyendo el mejor predictor de consistencia competitiva futura.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 2.3 Concentración de Talento y Equilibrio Competitivo")
        st.write("""
        A través de los campos `ability_score` de la tabla `player_seasons` (generados mediante modelos de regresión multivariada 
        para clasificar el rating *Overall*, *Offensive*, *Defensive* y *Midfield*), se calculan los coeficientes de **Gini** y el índice **HHI** por liga. 
        Siguiendo las conclusiones de Frick, Quansah y Lang (2023), el sistema europeo de ascensos/descensos mitiga los monopolios absolutos, 
        preservando el equilibrio dinámico entre clubes dominantes y aspirantes.
        """)

    # ==========================================
    # TAB SECCIÓN 3: VALOR POSICIONAL Y APORTES
    # ==========================================
    with tab_sec3:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Sección 3</span>
            <h2 style="color: #F8FAFC;">Valor Posicional y Aportes por Líneas</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 3.1 Demarcaciones Tácticas y su Aporte al Rendimiento Colectivo")
        st.write("""
        El sistema táctico distribuye responsabilidades en cuatro líneas fundamentales:
        - **Arqueros (POR)**: Prevención directa de goles mediante paradas (`saves`, `expected_goals_prevented`).
        - **Defensas (D)**: Contención, intercepciones, despejes y protección del tercio defensivo.
        - **Mediocampistas (M)**: Transición fase ofensiva/defensiva, volumen de pases y control espacial.
        - **Delanteros (ST/DEL)**: Generación de peligro en el tercio final y remate a portería.
        """)

        st.markdown("#### 3.2 Aporte Porcentual por Línea Posicional: Operacionalización")
        st.write("""
        El aporte porcentual por línea evalúa la contribución relativa de cada demarcación al rendimiento global del colectivo, integrando métricas ofensivas, defensivas y de circulación:
        - **Segmentación del rendimiento**: Desglose de los indicadores del equipo en arqueros, defensas, mediocampistas y delanteros.
        - **Aportes promedio por demarcación**: Cálculo de métricas específicas (D, M, ST × L/R/C) respecto a los indicadores globales del club.
        - **Especialización técnica**: Pappalardo et al. (2019) confirmaron que los delanteros dominan en goles y regates; los mediocampistas en volumen de pases y asistencias; y los defensas en intercepciones, despejes y bloqueos.
        """)

        st.info("📌 **Integración en la Base de Datos**: Las tablas `player_stats_attacking`, `player_stats_passing`, `player_stats_defending` y `player_stats_goalkeeping` contienen métricas segregadas por dimensión. La agregación ponderada de estas tablas permite calcular con precisión el aporte relativo de cada línea.")

        st.markdown("#### 3.3 Implicaciones para la Gestión y Profundidad de Plantilla")
        st.write("""
        - **Profundidad de plantilla**: La concentración excesiva de talento en una sola línea o en pocos jugadores genera alta vulnerabilidad ante lesiones y sanciones.
        - **Equilibrio estructural**: El rendimiento colectivo óptimo requiere complementar el talento individual con solidez y balance entre líneas.
        """)


    # ==========================================
    # TAB REFERENCIAS BIBLIOGRÁFICAS
    # ==========================================
    with tab_refs:
        st.markdown("""
        <div class="section-container">
            <span class="theory-badge">Referencias y Documentación</span>
            <h2 style="color: #F8FAFC;">Bibliografía Consultada (Formato APA)</h2>
        </div>
        """, unsafe_allow_html=True)

        referencias = [
            ("Frick, B., Quansah, T. K., & Lang, M. (2023)", "Talent concentration and competitive imbalance in European soccer. Frontiers in Sports and Active Living, 5, 1148122. https://doi.org/10.3389/fspor.2023.1148122"),
            ("Fuller, C. W., Ekstrand, J., Junge, A., et al. (2006)", "Consensus statement on injury definitions and data collection procedures in studies of football (soccer) injuries. British Journal of Sports Medicine, 40(3), 193–201."),
            ("Gabbett, T. J., Hulin, B. T., Blanch, P., & Whiteley, R. (2016)", "High chronic training loads and exposure to bouts of maximal velocity running reduce injury risk in elite rugby league players. Journal of Science and Medicine in Sport, 19(3), 234–238."),
            ("Harlow, C. K., Drummond, J. E., & Voos, J. E. (2021)", "The effect of COVID-19 lockdown on injury rates in the Bundesliga. Frontiers in Sports and Active Living, 3, 630576."),
            ("Impellizzeri, F. M., Tenan, M. S., Kempton, T., Novak, A., & Coutts, A. J. (2020)", "Acute:Chronic Workload Ratio: Conceptual issues and fundamental pitfalls. International Journal of Sports Physiology and Performance, 15(6), 907–913."),
            ("Krutsch, W., Zeman, F., Zellner, J., Pfeifer, C., Nerlich, M., & Angele, P. (2016)", "Injury patterns among elite football players: A media-based analysis over 6 seasons with emphasis on playing position. International Journal of Sports Medicine, 37(11), 898–908."),
            ("Lucey, P., Bialkowski, A., Monfort, M., Carr, P., & Matthews, I. (2015)", "Quality vs quantity: Improved shot prediction in soccer using strategic features from spatiotemporal data. MIT Sloan Sports Analytics Conference."),
            ("Malone, S., Owen, A., Newton, M., Mendes, B., Collins, K. D., & Gabbett, T. J. (2016)", "The acute:chronic workload ratio in relation to injury risk in professional soccer. Journal of Science and Medicine in Sport, 20(6), 561–565."),
            ("Pappalardo, L., Cintia, P., Ferragina, P., Massucco, E., Pedreschi, D., & Giannotti, F. (2019)", "PlayerRank: Data-driven performance evaluation and player ranking in soccer via a machine learning approach. ACM Transactions on Intelligent Systems and Technology, 10(5), 1–27."),
            ("Pelechrinis, K., & Winston, W. (2021)", "Positional value in soccer: Expected league points added above replacement. Journal of Quantitative Analysis in Sports, 17(3), 187–201."),
            ("Pipping, J., Feng, T., & Sabin, P. (2025)", "Shot Creation vs. Shot Conversion: A dynamic expected goals model for association football. Journal of Sports Analytics, 11(1), 45–62.")
        ]

        for autor, obra in referencias:
            st.markdown(f"""
            <div class="bib-item">
                <b style="color: #00E5FF;">{autor}</b>. {obra}
            </div>
            """, unsafe_allow_html=True)
if __name__ == "__main__":
    render_marco_teorico()
