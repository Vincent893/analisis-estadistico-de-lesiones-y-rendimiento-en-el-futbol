import streamlit as st
from utils.graficos import barras, calor
from utils.helper import (
    formatear_numero, mostrar_caja_mensaje, mostrar_expansor_sql,
    mostrar_tabla_datos, calcular_rango_serie, renderizar_bloque_cuartiles,
    TRADUCCION_TIPOS_LESION
)

def renderizar_seccion_duracion_lesiones(consulta_func):
    st.header("3. Duración de las lesiones")
    
    st.subheader("3.1 Distribución por rangos de días")
    df_duracion_lesiones = consulta_func("q4")
    df_totales_duracion = df_duracion_lesiones.groupby("rango_duracion", as_index=False)["lesiones"].sum()
    df_totales_duracion["pct"] = (100 * df_totales_duracion["lesiones"] / df_totales_duracion["lesiones"].sum()).round(1)
    df_totales_duracion["rango"] = df_totales_duracion["rango_duracion"].str[3:]
    df_duracion_lesiones["rango"] = df_duracion_lesiones["rango_duracion"].str[3:]
    
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_totales_duracion, "rango", "pct", "% de lesiones según duración (4 temporadas)", y_max=40)
    with columna_derecha:
        barras(df_duracion_lesiones, "rango", "lesiones", "Lesiones por rango de duración y temporada", fmt_txt=False, color="season_label", barmode="group")
        
    df_pivote_duracion = df_duracion_lesiones.pivot_table(index="rango_duracion", columns="season_label", values="lesiones").reset_index()
    df_pivote_duracion["rango"] = df_pivote_duracion.pop("rango_duracion").str[3:]
    mostrar_tabla_datos(df_pivote_duracion[["rango"] + [columna for columna in df_pivote_duracion.columns if columna != "rango"]])
    mostrar_expansor_sql("q4")

    st.subheader("3.2 Tipos de lesión: frecuencia vs. gravedad")
    df_tipos_lesion = consulta_func("q5")
    df_tipos_lesion["tipo"] = df_tipos_lesion["injury_type"].map(TRADUCCION_TIPOS_LESION).fillna(df_tipos_lesion["injury_type"])
    df_tipos_lesion["pct_dias"] = (100 * df_tipos_lesion["dias_totales"] / df_tipos_lesion["dias_totales"].sum()).round(1)
    
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_tipos_lesion.sort_values("dias_promedio"), "dias_promedio", "tipo", "Días promedio por tipo de lesión", alto=470, orientation="h")
    with columna_derecha:
        df_comparacion_casos_dias = df_tipos_lesion.sort_values("pct_dias").melt(id_vars="tipo", value_vars=["pct", "pct_dias"], var_name="medida", value_name="valor")
        df_comparacion_casos_dias["medida"] = df_comparacion_casos_dias["medida"].map({"pct": "% de las lesiones", "pct_dias": "% de los días perdidos"})
        barras(df_comparacion_casos_dias, "valor", "tipo", "Peso de cada tipo: casos vs. días perdidos (%)", alto=470, orientation="h", barmode="group", color="medida")
        
    mostrar_tabla_datos(df_tipos_lesion[["tipo", "lesiones", "pct", "jugadores", "dias_promedio", "dias_mediana", "dias_totales", "pct_dias"]].rename(columns={"tipo": "injury_type", "pct_dias": "% de los días"}))
    mostrar_expansor_sql("q5")

def renderizar_seccion_antropometria(consulta_func):
    st.header("4. Antropometría: altura, peso e IMC")
    mostrar_caja_mensaje("info", "Cómo leer esta sección", "Cada gráfico compara los cuartiles de la variable.")
    
    df_cuartiles_altura = renderizar_bloque_cuartiles(consulta_func, "q7", "altura", "min_cm", "max_cm", "cm")
    df_cuartiles_peso = renderizar_bloque_cuartiles(consulta_func, "q8", "peso", "min_kg", "max_kg", "kg")
    df_cuartiles_imc = renderizar_bloque_cuartiles(consulta_func, "q9", "IMC", "min_imc", "max_imc", "")

    st.subheader("4.4 Altura y peso combinados")
    df_altura_peso_combinados = consulta_func("q11")
    df_altura_peso_combinados["pct"] = 100 * df_altura_peso_combinados["lesiones"] / df_altura_peso_combinados["jugadores"]
    matriz_jugadores_combinados = df_altura_peso_combinados.pivot(index="q_altura", columns="q_peso", values="jugadores")
    matriz_porcentaje_lesionados = df_altura_peso_combinados.pivot(index="q_altura", columns="q_peso", values="pct").where(matriz_jugadores_combinados >= 500)
    
    for matriz_actual in (matriz_jugadores_combinados, matriz_porcentaje_lesionados):
        matriz_actual.index = [f"Altura C{i}" for i in matriz_actual.index]
        matriz_actual.columns = [f"Peso C{i}" for i in matriz_actual.columns]
        
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        calor(matriz_jugadores_combinados, "Jugador-temporadas por combinación", fmt_txt=",.0f")
    with columna_derecha:
        calor(matriz_porcentaje_lesionados, "% lesionados (celdas con 500+ jugadores)", zmax=40)
        
    mostrar_expansor_sql("q11")
    return df_cuartiles_altura, df_cuartiles_peso, df_cuartiles_imc