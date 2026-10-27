import streamlit as st
import plotly.express as px
from utils.graficos import barras, mostrar
from utils.helper import (
    formatear_numero, mostrar_caja_mensaje, mostrar_expansor_sql,
    mostrar_tabla_datos, MAPEO_COLORES_TIPO_DATO, ETIQUETAS_MESES
)

def renderizar_seccion_panorama_general(consulta_func):
    st.header("1. Panorama general")
    metricas_panorama = consulta_func("q1").iloc[0]
    
    columnas_kpi_superior = st.columns(4)
    columnas_kpi_superior[0].metric("Lesiones registradas", formatear_numero(metricas_panorama["total_lesiones"]))
    columnas_kpi_superior[1].metric("Jugadores distintos lesionados", formatear_numero(metricas_panorama["jugadores_lesionados"]))
    columnas_kpi_superior[2].metric("Jugador-temporadas analizadas", formatear_numero(metricas_panorama["jugadores_temporada"]))
    columnas_kpi_superior[3].metric("% con al menos una lesión", f"{formatear_numero(metricas_panorama['pct_con_lesion'], 1)} %")

    columnas_kpi_inferior = st.columns(4)
    columnas_kpi_inferior[0].metric("Días perdidos (total)", formatear_numero(metricas_panorama["dias_totales"]))
    columnas_kpi_inferior[1].metric("Duración promedio", f"{formatear_numero(metricas_panorama['dias_promedio'], 1)} días")
    columnas_kpi_inferior[2].metric("Duración mediana", f"{formatear_numero(metricas_panorama['dias_mediana'])} días")
    columnas_kpi_inferior[3].metric("Duración máxima", f"{formatear_numero(metricas_panorama['dias_max'])} días")
    
    mostrar_caja_mensaje("info", "Lectura rápida", f"La media ({formatear_numero(metricas_panorama['dias_promedio'], 1)} días) es más del doble de la mediana ({formatear_numero(metricas_panorama['dias_mediana'])} días).")
    mostrar_expansor_sql("q1")
    return metricas_panorama

def renderizar_seccion_frecuencia_lesiones(consulta_func):
    st.header("2. Frecuencia de las lesiones")
    
    st.subheader("2.1 Por temporada")
    df_lesiones_por_temporada = consulta_func("q2").sort_values("season_label")
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_lesiones_por_temporada, "season_label", "lesiones", "Lesiones por temporada", fmt_txt=",.0f", color="tipo_dato", color_discrete_map=MAPEO_COLORES_TIPO_DATO)
    with columna_derecha:
        barras(df_lesiones_por_temporada, "season_label", "pct_lesionados", "% de jugadores lesionados por temporada", y_max=40, color="tipo_dato", color_discrete_map=MAPEO_COLORES_TIPO_DATO)
    mostrar_tabla_datos(df_lesiones_por_temporada)
    mostrar_caja_mensaje("ok", "Hallazgo", f"La frecuencia es estable: entre {formatear_numero(df_lesiones_por_temporada['pct_lesionados'].min(), 1)} % y {formatear_numero(df_lesiones_por_temporada['pct_lesionados'].max(), 1)} % de los jugadores se lesiona cada temporada.")
    mostrar_expansor_sql("q2")

    st.subheader("2.2 Distribución de lesiones por jugador")
    df_distribucion_lesiones = consulta_func("q3")
    df_distribucion_lesiones["grupo"] = df_distribucion_lesiones["n_lesiones"].apply(lambda numero_lesiones: "Sin lesión" if numero_lesiones == 0 else f"{numero_lesiones} lesión")
    columna_izquierda, columna_derecha = st.columns([1, 1])
    with columna_izquierda:
        figura_pastel_lesiones = px.pie(df_distribucion_lesiones, names="grupo", values="jugadores_temporada", hole=0.5, title="Jugador-temporadas según número de lesiones")
        mostrar(figura_pastel_lesiones, 340)
    with columna_derecha:
        mostrar_tabla_datos(df_distribucion_lesiones[["n_lesiones", "jugadores_temporada", "pct"]])
    mostrar_caja_mensaje("info", "Dato a tener en cuenta", f"Ningún jugador registra más de **{int(df_distribucion_lesiones['n_lesiones'].max())} lesión por temporada**.")
    mostrar_expansor_sql("q3")

    st.subheader("2.3 Estacionalidad (mes de inicio de la lesión)")
    df_estacionalidad_meses = consulta_func("q6")
    df_estacionalidad_meses["mes_txt"] = df_estacionalidad_meses["mes"].apply(lambda numero_mes: ETIQUETAS_MESES[int(numero_mes) - 1])
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_estacionalidad_meses, "mes_txt", "lesiones", "Lesiones por mes de inicio", fmt_txt=",.0f")
    with columna_derecha:
        barras(df_estacionalidad_meses, "mes_txt", "dias_promedio", "Duración promedio (días) por mes de inicio", y_max=50)
    mostrar_expansor_sql("q6")