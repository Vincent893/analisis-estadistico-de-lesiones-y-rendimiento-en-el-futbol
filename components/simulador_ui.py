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

def _crear_selector(etiqueta, lista_opciones):
    """Función auxiliar privada para evitar repetir la validación de listas vacías."""
    return st.selectbox(etiqueta, lista_opciones if lista_opciones else [""])

def renderizar_panel_seleccion_jugadores(formacion_tactica, lista_arqueros, lista_defensas, lista_mediocampistas, lista_delanteros):
    st.subheader("🔍 Selección de Jugadores")
    
    with st.expander("🛡️ Portería y Línea Defensiva", expanded=True):
        arquero = _crear_selector("Arquero (GK)", lista_arqueros)
        lateral_derecho = _crear_selector("Lateral Derecho (RB)", lista_defensas)
        defensa_central_uno = _crear_selector("Defensa Central 1 (CB)", lista_defensas)
        defensa_central_dos = _crear_selector("Defensa Central 2 (CB)", lista_defensas)
        lateral_izquierdo = _crear_selector("Lateral Izquierdo (LB)", lista_defensas)

    with st.expander("⚡ Zona de Mediocampo", expanded=True):
        if formacion_tactica == "4-3-3":
            mediocampista_uno = _crear_selector("Mediocampista Defensivo (DM)", lista_mediocampistas)
            mediocampista_dos = _crear_selector("Mediocampista Central 1 (CM)", lista_mediocampistas)
            mediocampista_tres = _crear_selector("Mediocampista Central 2 (CM)", lista_mediocampistas)
        else:
            mediocampista_uno = _crear_selector("Pivote Defensivo 1 (DM)", lista_mediocampistas)
            mediocampista_dos = _crear_selector("Pivote Defensivo 2 (DM)", lista_mediocampistas)
            mediocampista_tres = _crear_selector("Mediapunta (AM)", lista_mediocampistas)

    with st.expander("🎯 Frente de Ataque", expanded=True):
        extremo_derecho = _crear_selector("Extremo / Delantero Derecho (RW)", lista_delanteros)
        extremo_izquierdo = _crear_selector("Extremo / Delantero Izquierdo (LW)", lista_delanteros)
        delantero_centro = _crear_selector("Delantero Centro (ST)", lista_delanteros)

    return [
        arquero, lateral_derecho, defensa_central_uno, defensa_central_dos, lateral_izquierdo,
        mediocampista_uno, mediocampista_dos, mediocampista_tres,
        extremo_derecho, extremo_izquierdo, delantero_centro
    ]

def renderizar_tarjetas_kpi(metricas):
    kpi_rating, kpi_xg, kpi_edad, kpi_lesiones = st.columns(4)
    
    with kpi_rating:
        st.metric("⭐ Rating Promedio", f"{metricas['avg_rating']:.2f}")
    with kpi_xg:
        st.metric("⚽ xG Total (90')", f"{metricas['total_xg']:.2f}")
    with kpi_edad:
        st.metric("👤 Edad Promedio", f"{metricas['avg_age']:.1f} años")
    with kpi_lesiones:
        st.metric("🏥 Días de Baja", f"{int(metricas['total_days_lost'])}")

def renderizar_tabla_titulares(datos_alineacion):
    
    st.subheader("📋 Detalle de Jugadores en el Once Titular")
    columnas_mostrar = ['name', 'primary_category', 'age', 'average_rating', 'xg_per_90', 'total_injuries']
    st.dataframe(datos_alineacion[columnas_mostrar], use_container_width=True)