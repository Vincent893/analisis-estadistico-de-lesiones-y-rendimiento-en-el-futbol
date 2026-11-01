import streamlit as st

def renderizar_encabezado():
    st.title("⚽ Constructor y Simulador de Alineaciones")
    st.markdown("""
    Selecciona tu esquema táctico y los 11 jugadores titulares para simular las métricas colectivas 
    de rendimiento, goles esperados (xG), carga física y riesgo de lesiones.
    """)

def renderizar_filtros_laterales(lista_temporadas):
    st.sidebar.header("⚙️ Opciones de Configuración")
    temporada_seleccionada = st.sidebar.selectbox("Seleccionar Temporada", lista_temporadas)
    formacion_tactica = st.sidebar.selectbox("Formación Táctica", ["4-3-3", "4-2-3-1"])
    return temporada_seleccionada, formacion_tactica


def renderizar_panel_seleccion_jugadores(formacion_tactica, lista_arqueros, lista_defensas, lista_mediocampistas, lista_delanteros):
  
    st.markdown("""
        <style>
        /* Contenedor del formulario con estilo de tarjeta táctica */
        div[data-testid="stForm"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        /* Encabezados de líneas dentro del panel */
        .linea-tactica {
            font-size: 13px;
            font-weight: 700;
            color: #58a6ff;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 15px;
            margin-bottom: 5px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 3px;
        }
        /* Botón de Aplicar Alineación estilizado */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            border: 1px solid #2ea043 !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%) !important;
            border-color: #3fb950 !important;
            box-shadow: 0 0 10px rgba(46, 160, 67, 0.5) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📋 Selección de Titulares")
    
    with st.form(key="form_simulador_plantilla"):
        
        st.markdown('<p class="linea-tactica">🛡️ Portería</p>', unsafe_allow_html=True)
        arquero = st.selectbox("Arquero (GK)", lista_arqueros, label_visibility="collapsed")
        
        st.markdown('<p class="linea-tactica">🧱 Defensas</p>', unsafe_allow_html=True)
        defensa_1 = st.selectbox("Defensa Central 1", lista_defensas, key="def_1")
        defensa_2 = st.selectbox("Defensa Central 2", lista_defensas, key="def_2")
        lateral_izq = st.selectbox("Lateral Izquierdo", lista_defensas, key="lat_i")
        lateral_der = st.selectbox("Lateral Derecho", lista_defensas, key="lat_d")
        
        st.markdown('<p class="linea-tactica">⚙️ Mediocampistas</p>', unsafe_allow_html=True)
        medio_1 = st.selectbox("Mediocampista 1", lista_mediocampistas, key="med_1")
        medio_2 = st.selectbox("Mediocampista 2", lista_mediocampistas, key="med_2")
        medio_3 = st.selectbox("Mediocampista 3", lista_mediocampistas, key="med_3")
        
        st.markdown('<p class="linea-tactica">⚡ Delanteros</p>', unsafe_allow_html=True)
        delantero_1 = st.selectbox("Extremo Izquierdo", lista_delanteros, key="del_1")
        delantero_centro = st.selectbox("Delantero Centro", lista_delanteros, key="del_c")
        delantero_2 = st.selectbox("Extremo Derecho", lista_delanteros, key="del_2")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        boton_aplicar = st.form_submit_button(label="⚡ Aplicar Alineación", use_container_width=True)
    
    jugadores_seleccionados = [
        arquero, defensa_1, defensa_2, lateral_izq, lateral_der,
        medio_1, medio_2, medio_3, delantero_1, delantero_centro, delantero_2
    ]
    
    return jugadores_seleccionados, boton_aplicar


def renderizar_tarjetas_kpi(metricas):
    kpi_rating, kpi_xg, kpi_edad = st.columns(3)
    
    st.markdown("""
        <style>
        .kpi-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .kpi-title {
            font-size: 13px;
            color: #8b949e;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: 700;
            color: #f0f6fc;
        }
        .icon-star { color: #e3b341; }
        .icon-ball { color: #58a6ff; }
        .icon-user { color: #bc8cff; }
        .icon-med  { color: #f85149; }
        </style>
    """, unsafe_allow_html=True)
    
    with kpi_rating:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title"><i class="fa-solid fa-star icon-star"></i> Rating Promedio</div>
                <div class="kpi-value">{metricas['avg_rating']:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_xg:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title"><i class="fa-solid fa-futbol icon-ball"></i> xG Total (90')</div>
                <div class="kpi-value">{metricas['total_xg']:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_edad:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title"><i class="fa-solid fa-user-group icon-user"></i> Edad Promedio</div>
                <div class="kpi-value">{metricas['avg_age']:.1f} <span style="font-size: 14px; font-weight: normal; color: #8b949e;">años</span></div>
            </div>
        """, unsafe_allow_html=True)
    

def renderizar_tabla_titulares(datos_alineacion):
    
    st.subheader("📋 Detalle de Jugadores en el Once Titular")
    columnas_mostrar = ['name', 'primary_category', 'age', 'average_rating', 'xg_per_90', 'total_injuries']
    st.dataframe(datos_alineacion[columnas_mostrar], use_container_width=True)
    
