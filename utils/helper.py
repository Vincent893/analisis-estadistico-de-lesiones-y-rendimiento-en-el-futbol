# utils/helper.py
import streamlit as st
from database.Query import get_raw_query_sql
from utils.graficos import barras

# ==========================================
# DICCIONARIOS Y CONSTANTES
# ==========================================

MAPEO_COLORES_TIPO_DATO = {"Real": "#1f77b4", "Sintética": "#b0b0b0"}
ETIQUETAS_MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TRADUCCION_POSICIONES = {"MIDFIELDER": "Mediocampista", "DEFENDER": "Defensa", "GOALKEEPER": "Portero", "ATTACKER": "Delantero"}

TRADUCCION_TIPOS_LESION = {
    "ACL tear": "Rotura de LCA", "Fracture": "Fractura", "Knee ligament sprain": "Esguince de ligamento de rodilla",
    "Ankle sprain": "Esguince de tobillo", "Groin strain": "Distensión de ingle", "Calf strain": "Distensión de gemelo",
    "Hamstring strain": "Distensión de isquiotibiales", "Back spasm": "Espasmo de espalda", "Concussion": "Conmoción cerebral",
    "Muscle fatigue": "Fatiga muscular", "Illness": "Enfermedad"
}

DICCIONARIO_NOMBRES_COLUMNAS = {
    "season_label": "Temporada", "tipo_dato": "Tipo de dato", "jugadores": "Jugadores", "lesiones": "Lesiones",
    "jugadores_lesionados": "Jugadores lesionados", "pct_lesionados": "% lesionados", "les_por_jugador": "Lesiones por jugador",
    "les_por_1000min": "Lesiones por 1.000 min", "dias_perdidos": "Días perdidos", "dias_por_lesion": "Días por lesión",
    "dias_promedio": "Días promedio", "dias_mediana": "Días mediana", "dias_totales": "Días totales", "pct": "%",
    "injury_type": "Tipo de lesión", "mins_promedio": "Minutos promedio", "dias_perdidos_por_jugador": "Días perdidos por jugador",
    "cuartil": "Cuartil", "min_cm": "Mín (cm)", "max_cm": "Máx (cm)", "min_kg": "Mín (kg)", "max_kg": "Máx (kg)",
    "min_imc": "Mín IMC", "max_imc": "Máx IMC", "banda_min": "Minutos jugados", "banda_edad": "Edad",
    "primary_category": "Posición", "altura_prom": "Altura prom (cm)", "peso_prom": "Peso prom (kg)",
    "name": "Jugador", "altura_cm": "Altura (cm)", "peso_kg": "Peso (kg)", "minutos": "Minutos", "mes": "Mes",
    "rango": "Rango de duración", "variable": "Variable", "jugadores_temporada": "Jugador-temporadas", "n_lesiones": "N° de lesiones",
}

# ==========================================
# FUNCIONES AUXILIARES DE FORMATO E INTERFAZ
# ==========================================

def formatear_numero(valor, decimales=0):
    texto_formateado = f"{valor:,.{decimales}f}"
    return texto_formateado.replace(",", "X").replace(".", ",").replace("X", ".")

def mostrar_caja_mensaje(tipo_mensaje, titulo, texto):
    funcion_streamlit = {"info": st.info, "ok": st.success, "alerta": st.warning}[tipo_mensaje]
    funcion_streamlit(f"**{titulo}**\n\n{texto}")

def mostrar_expansor_sql(clave_consulta):
    with st.expander("Ver consulta SQL (se ejecuta después de la consulta base)"):
        st.code(get_raw_query_sql(clave_consulta), language="sql")

def mostrar_tabla_datos(dataframe):
    st.dataframe(dataframe.rename(columns=DICCIONARIO_NOMBRES_COLUMNAS), hide_index=True)

def calcular_rango_serie(serie_numerica):
    return float(serie_numerica.max() - serie_numerica.min())

def renderizar_bloque_cuartiles(consulta_func, clave_consulta, nombre_variable, columna_min, columna_max, unidad_medida):
    df_cuartiles = consulta_func(clave_consulta)
    df_cuartiles["grupo"] = [
        f"C{cuartil}: {min_val:g}–{max_val:g} {unidad_medida}" 
        for cuartil, min_val, max_val in zip(df_cuartiles["cuartil"], df_cuartiles[columna_min], df_cuartiles[columna_max])
    ]
    
    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        barras(df_cuartiles, "grupo", "pct_lesionados", f"% de jugadores lesionados por cuartil de {nombre_variable}", y_max=40)
    with columna_derecha:
        barras(df_cuartiles, "grupo", "dias_por_lesion", f"Días por lesión por cuartil de {nombre_variable}", y_max=50)
        
    mostrar_tabla_datos(df_cuartiles.drop(columns=["grupo"]))
    mostrar_expansor_sql(clave_consulta)
    return df_cuartiles