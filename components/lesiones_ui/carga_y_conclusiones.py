import streamlit as st
import pandas as pd
import plotly.express as px
from utils.graficos import barras, calor, mostrar
from utils.helper import (
    formatear_numero, mostrar_caja_mensaje, mostrar_expansor_sql,
    mostrar_tabla_datos, calcular_rango_serie, MAPEO_COLORES_TIPO_DATO,
    TRADUCCION_POSICIONES
)

def renderizar_seccion_carga_minutos(consulta_func):
    st.header("5. Carga de minutos jugados")
    df_carga_minutos = consulta_func("q10")
    df_carga_minutos["banda_min"] = df_carga_minutos["banda_min"].str[3:]
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_carga_minutos, "banda_min", "pct_lesionados", "% de jugadores lesionados por minutos jugados", y_max=40)
    with columna_derecha:
        barras(df_carga_minutos, "banda_min", "les_por_1000min", "Lesiones por 1.000 minutos jugados", fmt_txt=".3f")
    mostrar_tabla_datos(df_carga_minutos)
    mostrar_expansor_sql("q10")

    st.subheader("5.1 IMC y minutos jugados combinados")
    df_imc_minutos = consulta_func("q12")
    matriz_imc_minutos = df_imc_minutos.pivot(index="q_bmi", columns="banda_min", values="pct_lesionados")
    matriz_imc_minutos.index = [f"IMC C{i}" for i in matriz_imc_minutos.index]
    matriz_imc_minutos.columns = [columna[3:] for columna in matriz_imc_minutos.columns]
    calor(matriz_imc_minutos, "% de jugadores lesionados: IMC (cuartil) × minutos jugados", zmax=40)
    mostrar_expansor_sql("q12")
    return df_carga_minutos

def renderizar_seccion_variables_control(consulta_func):
    st.header("6. Posición, edad y perfil de los lesionados")
    df_posicion_lesionados = consulta_func("q13")
    df_posicion_lesionados["primary_category"] = df_posicion_lesionados["primary_category"].map(TRADUCCION_POSICIONES).fillna(df_posicion_lesionados["primary_category"])
    df_edad_lesionados = consulta_func("q14")
    df_edad_lesionados["banda_edad"] = df_edad_lesionados["banda_edad"].str[3:]
    
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_posicion_lesionados, "primary_category", "pct_lesionados", "% lesionados por posición", y_max=40)
        mostrar_tabla_datos(df_posicion_lesionados)
    with columna_derecha:
        barras(df_edad_lesionados, "banda_edad", "pct_lesionados", "% lesionados por edad", y_max=40)
        mostrar_tabla_datos(df_edad_lesionados)
    mostrar_expansor_sql("q13")
    mostrar_expansor_sql("q14")

    st.subheader("6.1 Perfil de jugadores con y sin lesión")
    df_perfil_lesion = consulta_func("q15")
    tabla_perfil_transpuesta = df_perfil_lesion.set_index("grupo").T
    tabla_perfil_transpuesta["Diferencia"] = tabla_perfil_transpuesta["Con lesión"] - tabla_perfil_transpuesta["Sin lesión"]
    st.dataframe(tabla_perfil_transpuesta.round(2).reset_index().rename(columns={"index": "Variable"}), hide_index=True)
    mostrar_expansor_sql("q15")

def renderizar_seccion_top_jugadores(consulta_func):
    st.header("7. Jugadores con más días perdidos")
    df_top_jugadores = consulta_func("q17")
    df_top_jugadores["primary_category"] = df_top_jugadores["primary_category"].map(TRADUCCION_POSICIONES).fillna(df_top_jugadores["primary_category"])
    columna_izquierda, columna_derecha = st.columns([3, 2])
    with columna_izquierda:
        mostrar_tabla_datos(df_top_jugadores)
    with columna_derecha:
        barras(df_top_jugadores.sort_values("dias_perdidos"), "dias_perdidos", "name", "Días perdidos en 4 temporadas (top 15)", fmt_txt=",.0f", alto=470, orientation="h")
    mostrar_expansor_sql("q17")

def renderizar_seccion_real_vs_sintetico(consulta_func):
    st.header("8. ¿El patrón cambia entre la temporada real y las sintéticas?")
    df_real_vs_sintetico = consulta_func("q18")
    df_real_vs_sintetico["variable"] = df_real_vs_sintetico["variable"].map({"altura": "Altura", "peso": "Peso", "imc": "IMC"})
    figura_comparativa = px.bar(df_real_vs_sintetico, x="cuartil", y="pct_lesionados", color="tipo_dato", barmode="group", facet_col="variable", color_discrete_map=MAPEO_COLORES_TIPO_DATO, text_auto=".1f", title="% de lesionados por cuartil: real vs. sintética")
    figura_comparativa.update_traces(textposition="outside", cliponaxis=False)
    mostrar(figura_comparativa, 380)
    mostrar_expansor_sql("q18")

def renderizar_seccion_conclusion(metricas_panorama, df_cuartiles_altura, df_cuartiles_peso, df_cuartiles_imc, df_carga_minutos, df_posicion_lesionados, df_edad_lesionados, datos_lesion_lca):
    st.header("9. Conclusión")
    df_resumen_conclusion = pd.DataFrame({
        "Variable": ["Altura (cuartiles)", "Peso (cuartiles)", "IMC (cuartiles)", "Minutos jugados (bandas)", "Edad (bandas)", "Posición"],
        "Diferencia (p.p.)": [
            calcular_rango_serie(df_cuartiles_altura["pct_lesionados"]), 
            calcular_rango_serie(df_cuartiles_peso["pct_lesionados"]), 
            calcular_rango_serie(df_cuartiles_imc["pct_lesionados"]), 
            calcular_rango_serie(df_carga_minutos["pct_lesionados"]), 
            calcular_rango_serie(df_edad_lesionados["pct_lesionados"]), 
            calcular_rango_serie(df_posicion_lesionados["pct_lesionados"])
        ],
    }).round(1).sort_values("Diferencia (p.p.)")
    
    figura_resumen = px.bar(df_resumen_conclusion, x="Diferencia (p.p.)", y="Variable", orientation="h", text_auto=".1f", title=f"Diferencia entre el grupo con más y menos % de lesionados (promedio general: {formatear_numero(metricas_panorama['pct_con_lesion'], 1)} %)")
    mostrar(figura_resumen, 340)

    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        mostrar_caja_mensaje("ok", "Frecuencia y distribución", f"Se registraron {formatear_numero(metricas_panorama['total_lesiones'])} lesiones en cuatro temporadas.")
        mostrar_caja_mensaje("ok", "Antropometría", "La altura, el peso y el IMC no se relacionan con la frecuencia de lesiones.")
    with columna_derecha:
        mostrar_caja_mensaje("ok", "Duración", f"La duración es muy desigual: mediana de {formatear_numero(metricas_panorama['dias_mediana'])} días.")
        mostrar_caja_mensaje("ok", "Carga de minutos", "El % de lesionados es prácticamente el mismo en todas las bandas.")

    st.markdown("**Respuesta al objetivo:** en estas cuatro temporadas, las lesiones son frecuentes y de duración desigual.")