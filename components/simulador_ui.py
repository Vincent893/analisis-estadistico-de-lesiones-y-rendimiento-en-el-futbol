import streamlit as st

def renderizar_encabezado():
    st.markdown('<h2 style="color: #f0f6fc; font-size: 24px;"><i class="fa-solid fa-chess-board" style="color: #58a6ff; margin-right: 10px;"></i>Constructor y Simulador de Alineaciones</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #8b949e; font-size: 14px;">Selecciona tu esquema táctico y los 11 jugadores titulares para simular las métricas colectivas de rendimiento, goles esperados (xG), carga física y riesgo de lesiones.</p>', unsafe_allow_html=True)
    st.markdown("---")

def renderizar_filtros_laterales(lista_temporadas):
    st.sidebar.markdown('<p style="color: #f0f6fc; font-weight: bold;"><i class="fa-solid fa-gears" style="margin-right: 6px;"></i>Opciones de Configuración</p>', unsafe_allow_html=True)
    temporada_seleccionada = st.sidebar.selectbox("Seleccionar Temporada", lista_temporadas)
    formacion_tactica = st.sidebar.selectbox("Formación Táctica", ["4-3-3", "4-2-3-1"])
    return temporada_seleccionada, formacion_tactica

def renderizar_tarjetas_kpi(metricas):
    kpi_rating, kpi_xg, kpi_edad, kpi_lesiones = st.columns(4)

    with kpi_rating:
        st.markdown(f'<div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; text-align:center;"><div style="color:#8b949e; font-size:12px; font-weight:600; text-transform:uppercase; margin-bottom:4px;"><i class="fa-solid fa-star" style="color:#e3b341;"></i> Rating Promedio</div><div style="font-size:22px; font-weight:bold; color:#f0f6fc;">{metricas["avg_rating"]:.2f}</div></div>', unsafe_allow_html=True)

    with kpi_xg:
        st.markdown(f'<div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; text-align:center;"><div style="color:#8b949e; font-size:12px; font-weight:600; text-transform:uppercase; margin-bottom:4px;"><i class="fa-solid fa-futbol" style="color:#58a6ff;"></i> xG Total (90\')</div><div style="font-size:22px; font-weight:bold; color:#f0f6fc;">{metricas["total_xg"]:.2f}</div></div>', unsafe_allow_html=True)

    with kpi_edad:
        st.markdown(f'<div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; text-align:center;"><div style="color:#8b949e; font-size:12px; font-weight:600; text-transform:uppercase; margin-bottom:4px;"><i class="fa-solid fa-user-group" style="color:#bc8cff;"></i> Edad Promedio</div><div style="font-size:22px; font-weight:bold; color:#f0f6fc;">{metricas["avg_age"]:.1f} <span style="font-size:12px; color:#8b949e;">yrs</span></div></div>', unsafe_allow_html=True)

    with kpi_lesiones:
        st.markdown(f'<div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; text-align:center;"><div style="color:#8b949e; font-size:12px; font-weight:600; text-transform:uppercase; margin-bottom:4px;"><i class="fa-solid fa-kit-medical" style="color:#f85149;"></i> Días de Baja</div><div style="font-size:22px; font-weight:bold; color:#f0f6fc;">{int(metricas["total_days_lost"])}</div></div>', unsafe_allow_html=True)

def renderizar_panel_seleccion_jugadores(formacion_tactica, lista_arqueros, lista_defensas, lista_mediocampistas, lista_delanteros):
    """
    Panel de selección con st.form congelado para optimizar UX.
    Genera dinámicamente los campos según la formación táctica activa.
    """
    st.markdown('<h3 style="color: #f0f6fc; font-size: 18px;"><i class="fa-solid fa-users" style="color: #58a6ff; margin-right: 8px;"></i>Selección de Titulares</h3>', unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        div[data-testid="stForm"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .linea-tactica {
            font-size: 12px;
            font-weight: 700;
            color: #58a6ff;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 12px;
            margin-bottom: 4px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 2px;
        }
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

    with st.form(key=f"form_alineacion_{formacion_tactica}"):
        # 1. Portería
        st.markdown('<p class="linea-tactica"><i class="fa-solid fa-hand-fist"></i> Portería</p>', unsafe_allow_html=True)
        arquero = st.selectbox("Arquero (GK)", lista_arqueros, index=0, key="f_gk")

        # 2. Defensas (4 Defensores comunes)
        st.markdown('<p class="linea-tactica"><i class="fa-solid fa-shield"></i> Defensas</p>', unsafe_allow_html=True)
        def_1 = st.selectbox("Defensa Central 1", lista_defensas, index=0, key="f_def_1")
        def_2 = st.selectbox("Defensa Central 2", lista_defensas, index=min(1, len(lista_defensas)-1), key="f_def_2")
        lat_izq = st.selectbox("Lateral Izquierdo", lista_defensas, index=min(2, len(lista_defensas)-1), key="f_lat_i")
        lat_der = st.selectbox("Lateral Derecho", lista_defensas, index=min(3, len(lista_defensas)-1), key="f_lat_d")

        mediocampistas_seleccionados = []
        delanteros_seleccionados = []

        # 3. Estructura Adaptativa por Formación Táctica
        if formacion_tactica == "4-3-3":
            st.markdown('<p class="linea-tactica"><i class="fa-solid fa-gears"></i> Mediocampistas (3)</p>', unsafe_allow_html=True)
            med_1 = st.selectbox("Mediocampista 1", lista_mediocampistas, index=0, key="f_med_1")
            med_2 = st.selectbox("Mediocampista 2", lista_mediocampistas, index=min(1, len(lista_mediocampistas)-1), key="f_med_2")
            med_3 = st.selectbox("Mediocampista 3", lista_mediocampistas, index=min(2, len(lista_mediocampistas)-1), key="f_med_3")
            mediocampistas_seleccionados = [med_1, med_2, med_3]

            st.markdown('<p class="linea-tactica"><i class="fa-solid fa-bolt"></i> Delanteros (3)</p>', unsafe_allow_html=True)
            del_1 = st.selectbox("Extremo Izquierdo", lista_delanteros, index=0, key="f_del_1")
            del_c = st.selectbox("Delantero Centro", lista_delanteros, index=min(1, len(lista_delanteros)-1), key="f_del_c")
            del_2 = st.selectbox("Extremo Derecho", lista_delanteros, index=min(2, len(lista_delanteros)-1), key="f_del_2")
            delanteros_seleccionados = [del_1, del_c, del_2]

        elif formacion_tactica == "4-2-3-1":
            st.markdown('<p class="linea-tactica"><i class="fa-solid fa-gears"></i> Mediocampistas (4)</p>', unsafe_allow_html=True)
            med_1 = st.selectbox("Pivote Defensivo 1", lista_mediocampistas, index=0, key="f_dm_1")
            med_2 = st.selectbox("Pivote Defensivo 2", lista_mediocampistas, index=min(1, len(lista_mediocampistas)-1), key="f_dm_2")
            med_3 = st.selectbox("Mediapunta (CAM)", lista_mediocampistas, index=min(2, len(lista_mediocampistas)-1), key="f_am")
            med_4 = st.selectbox("Interior / Extremo Adaptado", lista_mediocampistas, index=min(3, len(lista_mediocampistas)-1), key="f_ext")
            mediocampistas_seleccionados = [med_1, med_2, med_3, med_4]

            st.markdown('<p class="linea-tactica"><i class="fa-solid fa-bolt"></i> Delanteros (1)</p>', unsafe_allow_html=True)
            del_c = st.selectbox("Delantero Centro (ST)", lista_delanteros, index=0, key="f_st")
            delanteros_seleccionados = [del_c]

        st.markdown("<br>", unsafe_allow_html=True)
        boton_aplicar = st.form_submit_button(label="⚡ Aplicar Alineación", use_container_width=True)

    jugadores_seleccionados = [arquero, def_1, def_2, lat_izq, lat_der] + mediocampistas_seleccionados + delanteros_seleccionados
    return jugadores_seleccionados, boton_aplicar