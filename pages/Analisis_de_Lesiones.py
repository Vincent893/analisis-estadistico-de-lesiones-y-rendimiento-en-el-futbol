import os
import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv, find_dotenv
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme

cargar_estilos()
load_dotenv(find_dotenv(), override=True)

MOTHERDUCK_TOKEN = os.getenv("MOTHERDUCK_TOKEN", "").strip()
DB_MOTHERDUCK = f"md:database?motherduck_token={MOTHERDUCK_TOKEN}" if MOTHERDUCK_TOKEN else "md:database"


def run_query(query):
    with duckdb.connect(DB_MOTHERDUCK) as conn:
        return conn.execute(query).df()


def mostrar(fig, alto=360):
    res = apply_theme(fig)
    fig = res if res is not None else fig
    fig.update_layout(height=alto, legend_title_text="")
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})


# El CTE principal para cada consulta, es un filtro con el fin de no copiar el cte en cada consulta
P_CTE = """
WITH temp AS (
    SELECT season_id, season_label, season_order,
           CASE WHEN is_fabricated = 0 THEN 1 ELSE 0 END AS es_real
    FROM seasons
),
les AS (
    SELECT i.injury_id, i.player_id, i.season_id, i.injury_type,
           TRY_CAST(i.start_date AS DATE) AS f_ini,
           TRY_CAST(i.end_date   AS DATE) AS f_fin,
           date_diff('day', TRY_CAST(i.start_date AS DATE), TRY_CAST(i.end_date AS DATE)) AS dias
    FROM injuries i
    JOIN temp t ON t.season_id = i.season_id
),
les_ps AS (
    SELECT player_id, season_id, COUNT(*) AS n_les, SUM(dias) AS dias_perdidos
    FROM les
    GROUP BY player_id, season_id
),
ps_base AS (
    SELECT a.player_id, a.season_id, t.season_label, t.season_order, t.es_real,
           a.age, a.mins, p.primary_category, a.height_cm, a.weight_kg,
           COALESCE(l.n_les, 0) AS n_les,
           COALESCE(l.dias_perdidos, 0) AS dias_perdidos
    FROM analytics_player_seasons a
    JOIN temp t ON t.season_id = a.season_id
    JOIN players p ON p.player_id = a.player_id
    LEFT JOIN les_ps l ON l.player_id = a.player_id AND l.season_id = a.season_id
    WHERE a.height_cm > 0 AND a.weight_kg > 0
),
ps AS (
    SELECT *,
        CEIL(4 * CUME_DIST() OVER (ORDER BY height_cm))::INT AS q_altura,
        CEIL(4 * CUME_DIST() OVER (ORDER BY weight_kg))::INT AS q_peso
    FROM ps_base
)
"""


# Título y presentación
st.title("Estudio Descriptivo de Frecuencia, Duración y Distribución de Lesiones en el Fútbol Profesional (2022-2026)")
st.markdown("##### *Objetivo: Describir la frecuencia, duración y distribución de las lesiones en los jugadores entre las temporadas comprendidas entre los años 2022 y 2026, relacionándolas con sus características antropométricas (altura y peso) y su carga de minutos jugados.*")
st.markdown("""
La presente aplicación tiene como propósito fundamental examinar la incidencia, la distribución temporal y la duración de las lesiones deportivas registradas en el periodo comprendido entre las campañas 2022/23 y 2025/26. A través de un enfoque cuantitativo y riguroso, se busca determinar si factores antropométricos o variables asociadas a la carga competitiva en tiempo tienen relación directa con la ocurrencia de episodios lesivos en los jugadores de campo y porteros.
""")

st.divider()

# Parte 1 con kpis.
st.header("1. Panorama general")

st.markdown("""
El análisis descriptivo inicial abarca un total de 108,639 observaciones de jugador-temporada. Esta exploración preliminar permite cuantificar la dimensión global de las afectaciones físicas, estableciendo los parámetros de frecuencia de los futbolistas que presentan al menos un evento lesivo durante el periodo competitivo, así como la distribución acumulada de los días de inactividad.
""")

sql_q1 = P_CTE + """
SELECT
  (SELECT COUNT(*) FROM les) AS total_lesiones,
  (SELECT COUNT(DISTINCT player_id) FROM les) AS jugadores_lesionados,
  (SELECT COUNT(*) FROM ps) AS jugadores_temporada,
  (SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) FROM ps) AS pct_con_lesion,
  (SELECT ROUND(AVG(dias), 1) FROM les) AS dias_promedio,
  (SELECT MEDIAN(dias) FROM les) AS dias_mediana,
  (SELECT MAX(dias) FROM les) AS dias_max,
  (SELECT SUM(dias) FROM les) AS dias_totales;
"""
k = run_query(sql_q1).iloc[0]

f1 = st.columns(4)
f1[0].metric("Lesiones registradas", f"{k['total_lesiones']:,}")
f1[1].metric("Jugadores distintos lesionados", f"{k['jugadores_lesionados']:,}")
f1[2].metric("Jugador-temporadas analizadas", f"{k['jugadores_temporada']:,}")
f1[3].metric("% con al menos una lesión", f"{k['pct_con_lesion']} %")

f2 = st.columns(4)
f2[0].metric("Días perdidos (total)", f"{k['dias_totales']:,}")
f2[1].metric("Duración promedio", f"{k['dias_promedio']} días")
f2[2].metric("Duración mediana", f"{k['dias_mediana']} días")
f2[3].metric("Duración máxima", f"{k['dias_max']} días")

st.markdown(f"""
Al analizar los estadísticos de posición, se observa que la media aritmética de la duración de las lesiones (38.4 días) es considerablemente mayor que la mediana (15.0 días). Esta diferencia evidencia una asimetría positiva en la distribución, provocada por un subconjunto de lesiones severas de larga duración que desplazan el promedio hacia valores altos. Por esta razón, se emplean conjuntamente ambas medidas de tendencia central para lograr una caracterización adecuada de la severidad sin distorsiones.
""")

st.divider()

# Parte 2 Frecuencias
st.header("2. Frecuencia de las lesiones")

st.subheader("2.1 Evolución y distribución por temporada")
st.markdown("""
Con el propósito de evaluar la estabilidad temporal de la variable lesiva, se analiza la frecuencia absoluta acumulada de lesiones y la proporción de jugadores afectados a lo largo de las cuatro temporadas deportivas evaluadas. Esta distribución permite observar el comportamiento global del fenómeno de estudio en el periodo analizado.
""")

sql_q2 = P_CTE + """
SELECT season_label,
       season_order,
       COUNT(*) AS jugadores,
       SUM(n_les) AS lesiones,
       ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados
FROM ps GROUP BY season_label, season_order ORDER BY season_order;
"""
q2 = run_query(sql_q2).sort_values("season_label")

q2["top_rect"] = q2.apply(
    lambda r: f"{r['lesiones']:,.0f} les. ({r['pct_lesionados']}%)", 
    axis=1
)

fig_q2 = px.bar(q2, x="season_label", y="lesiones", text="top_rect",
                title="Evolución plurianual: Volumen y tasa de afectación por temporada",
                labels={"season_label": "Temporada", "lesiones": "Cantidad de Lesiones"})

fig_q2.update_traces(textposition="outside", cliponaxis=False, width=0.45, marker_color="#1f77b4")
fig_q2.update_xaxes(title_text="")
mostrar(fig_q2, 400)

st.markdown("""
Los resultados reflejan una notable homogeneidad en la tasa de incidencia, manteniéndose en un rango estrecho entre el 24.4% y el 25.0% anual. Dicha estabilidad a lo largo de los periodos indica la ausencia de fluctuaciones atípicas en el comportamiento lesivo global de la población estudiada.
""")


st.subheader("2.2 Distribución de lesiones por jugador en el ciclo anual")
st.markdown("""
Es relevante analizar si los jugadores acumulan múltiples lesiones dentro de un mismo periodo competitivo o si el total de afectados corresponde a eventos únicos por individuo.
""")

sql_q3 = P_CTE + """
SELECT LEAST(n_les, 4) AS n_lesiones,
       COUNT(*) AS jugadores_temporada,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM ps GROUP BY 1 ORDER BY 1;
"""
q3 = run_query(sql_q3)
q3["grupo"] = q3["n_lesiones"].apply(lambda n: "Sin lesión" if n == 0 else f"{n} lesión registrada")

c1, c2 = st.columns([1, 1])
with c1:
    fig_q3 = px.pie(q3, names="grupo", values="jugadores_temporada", hole=0.5,
                     title="Proporción de afectación por jugador-temporada")
    mostrar(fig_q3, 340)
with c2:
    st.markdown("""
    La distribución porcentual muestra que el 75.2% de las observaciones individuales por temporada transcurren sin registrar lesiones, mientras que el 24.8% restante corresponde exactamente a un único evento por individuo. Ningún perfil supera una lesión contabilizada por temporada en la base datos.
    """)


# 2.3 Distribución mensual de las lesiones
st.subheader("2.3 Distribución mensual de las lesiones")
st.markdown("""
La distribución mensual de los inicios de lesiones permite identificar posibles patrones calendario asociados a períodos de alta exigencia competitiva, pretemporadas o fases de descanso reglamentario.
""")

sql_q6 = P_CTE + """
SELECT MONTH(f_ini) AS mes, COUNT(*) AS lesiones, ROUND(AVG(dias), 1) AS dias_promedio
FROM les WHERE f_ini IS NOT NULL GROUP BY 1 ORDER BY 1;
"""
q6 = run_query(sql_q6)
meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
q6["mes_txt"] = q6["mes"].apply(lambda m: meses_nombres[int(m) - 1])

import plotly.graph_objects as go

fig_q6 = go.Figure()

fig_q6.add_trace(go.Bar(
    x=q6["mes_txt"],
    y=q6["lesiones"],
    text=q6["lesiones"].apply(lambda x: f"<b>{x} les.</b>"),
    textposition="outside",
    width=0.5,
    showlegend=False
))

fig_q6.add_trace(go.Bar(
    x=q6["mes_txt"],
    y=q6["lesiones"],
    text=q6["dias_promedio"].apply(lambda x: f"{x}d prom"),
    textposition="inside",
    insidetextanchor="middle",
    textangle=0,  # <--- Esto mantiene el texto horizontal
    width=0.5,
    marker=dict(opacity=0),
    showlegend=False
))

fig_q6.update_layout(
    title="Volumen de lesiones y duración media según mes de inicio",
    barmode="overlay"
)
fig_q6.update_xaxes(title_text="")
mostrar(fig_q6, 380)

st.markdown("""
Se advierte una distribución bastante homogénea a lo largo de los meses activos del año, con una ausencia lógica de registros durante los meses de receso estival. Los valores se mantienen estables sin picos extremos que sugieran un riesgo asociado a un mes en particular, reflejando una carga de stress físico sostenida.
""")

st.divider()

# Parte 3. La duración y gravedad de las lesiones
st.header("3. Duración y gravedad de las lesiones")

st.subheader("3.1 Agrupación por rangos de días de baja")
st.markdown("""
Para comprender las características de las recuperaciones, las lesiones se clasifican en intervalos temporales de días de baja. Esto permite distinguir entre molestias de carácter leve y lesiones de larga duración.
""")

sql_q4 = P_CTE + """
SELECT t.season_label,
       CASE WHEN dias <= 7  THEN '1) 0-7 días'
            WHEN dias <= 14 THEN '2) 8-14'
            WHEN dias <= 30 THEN '3) 15-30'
            WHEN dias <= 60 THEN '4) 31-60'
            WHEN dias <= 90 THEN '5) 61-90'
            WHEN dias <= 180 THEN '6) 91-180'
            ELSE '7) 180+' END AS rango_duracion,
       COUNT(*) AS lesiones
FROM les l
JOIN temp t ON t.season_id = l.season_id
WHERE dias IS NOT NULL AND dias >= 0
GROUP BY ALL ORDER BY t.season_label, rango_duracion;
"""
q4 = run_query(sql_q4)
tot = q4.groupby("rango_duracion", as_index=False)["lesiones"].sum()
tot["pct_del_total"] = (100 * tot["lesiones"] / tot["lesiones"].sum()).round(1)
tot["rango"] = tot["rango_duracion"].str[3:]

fig_q4 = px.bar(
    tot, 
    x="rango", 
    y="pct_del_total", 
    text_auto=".1f",
    title="Distribución porcentual de las lesiones según su duración en días",
    labels={
        "pct_del_total": "Porcentaje Respecto al Total",
        "rango": "Rango de duración"
    }
)
fig_q4.update_traces(textposition="outside", cliponaxis=False, width=0.55)
fig_q4.update_yaxes(title_text="Porcentaje Respecto al Total")
mostrar(fig_q4, 360)

st.markdown("""
El análisis por rangos revela que cerca de la mitad de las incidencias médicas se resuelven en un plazo inferior o igual a 14 días, mientras que un segmento minoritario pero crítico concentra las bajas prolongadas. El intervalo intermedio de 91 a 180 días registra una presencia prácticamente nula.
""")


st.subheader("3.2 Clasificación de lesiones: Frecuencia frente al impacto en días de baja")
st.markdown("""
No todas las patologías poseen el mismo peso operativo en un plantel profesional. A continuación se contrasta la frecuencia de aparición de cada diagnóstico clínico frente al volumen total de jornadas de baja que provocan.
""")

sql_q5 = P_CTE + """
SELECT injury_type,
       COUNT(*) AS lesiones,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct,
       COUNT(DISTINCT player_id) AS jugadores,
       ROUND(AVG(dias), 1) AS dias_promedio,
       MEDIAN(dias) AS dias_mediana,
       SUM(dias) AS dias_totales
FROM les GROUP BY injury_type ORDER BY lesiones DESC LIMIT 20;
"""
q5 = run_query(sql_q5)
tipos_es = {
    "ACL tear": "Rotura de LCA", "Fracture": "Fractura",
    "Knee ligament sprain": "Esguince de ligamento de rodilla",
    "Ankle sprain": "Esguince de tobillo", "Groin strain": "Distensión de ingle",
    "Calf strain": "Distensión de gemelo", "Hamstring strain": "Distensión de isquiotibiales",
    "Back spasm": "Espasmo de espalda", "Concussion": "Conmoción cerebral",
    "Muscle fatigue": "Fatiga muscular", "Illness": "Enfermedad"
}
q5["tipo"] = q5["injury_type"].map(tipos_es).fillna(q5["injury_type"])
q5["pct_dias"] = (100 * q5["dias_totales"] / q5["dias_totales"].sum()).round(1)
q5o = q5.sort_values("dias_promedio")

c1, c2 = st.columns(2)
with c1:
    fig_dur = px.bar(
        q5o, x="dias_promedio", y="tipo", orientation="h", text_auto=".1f",
        title="Duración promedio (días) por patología",
        labels={"dias_promedio": "Días de Baja Promedio por Lesión", "tipo": "Tipo de Lesión"}
    )
    fig_dur.update_layout(yaxis={"categoryorder": "total ascending"})
    mostrar(fig_dur, 420)

with c2:
    comp = q5o.melt(id_vars="tipo", value_vars=["pct", "pct_dias"], var_name="medida", value_name="valor")
    comp["medida"] = comp["medida"].map({"pct": "Frecuencia de casos (%)", "pct_dias": "Días perdidos acumulados (%)"})
    
    fig_comp = px.bar(
        comp, x="valor", y="tipo", orientation="h", barmode="group", color="medida",
        text_auto=".1f",
        title="Comparativa: % de casos vs % de días de baja",
        labels={"valor": "Porcentaje", "tipo": "Tipo de Lesión", "medida": "Métrica"}
    )
    fig_comp.update_traces(textposition="outside")
    mostrar(fig_comp, 420)

st.markdown("""
**Lectura clave para la toma de decisiones:**
* **Duración promedio por lesión:** Mide el costo temporal individual de cada patología. Se observa con claridad que lesiones críticas como la **Rotura de LCA** promedian más de 230 días de baja por cada evento, superando drásticamente a molestias menores como la fatiga muscular o enfermedades comunes, que apenas rondan los 5 o 6 días.
* **Frecuencia de casos (%):** Mide qué porcentaje de los eventos totales representa cada tipo de lesión. Muchos diagnósticos comunes se distribuyen de forma similar en cuanto al número de veces que ocurren.
* **Días perdidos acumulados (%):** Mide el impacto real en tiempo de baja global para el equipo. Aquí se evidencia el contraste absoluto: lesiones graves como la **Rotura de LCA** disparan drásticamente el porcentaje de tiempo acumulado fuera de las canchas a pesar de no ser las más numerosas en cantidad de eventos.

La gravedad clínica de la lesión es el factor crítico que determina la indisponibilidad del plantel, superando con creces a la simple cantidad de veces que se repite una dolencia leve.
""")

st.divider()

# 4. Antropometría (altura y peso)
st.header("4. Características Antropométricas")

st.markdown("""
En este apartado tomaremos los valores antropométricos de altura y peso para comprobar si el riesgo a sufrir lesiones, se segmenta a la población de jugadores. La segmentación se dividirá en cuartiles. Si existiera un riesgo antropométrico vinculado a la estatura o al peso, se observaría una progresión evidente en las tasas de lesionados.
""")

col_alt, col_pes = st.columns(2)

with col_alt:
    st.subheader("4.1 Análisis por cuartiles de altura")
    sql_q7 = P_CTE + """
    SELECT q_altura AS cuartil, MIN(height_cm) AS min_cm, MAX(height_cm) AS max_cm,
           ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados
    FROM ps GROUP BY 1 ORDER BY 1;
    """
    alt = run_query(sql_q7)
    alt["grupo"] = [f"C{c}: {a:g}–{b:g} cm" for c, a, b in zip(alt["cuartil"], alt["min_cm"], alt["max_cm"])]

    fig_alt = px.bar(alt, x="grupo", y="pct_lesionados", text_auto=".1f",
                     title="% de lesionados por cuartil de altura",
                     labels={"grupo": "Cuartil de Altura", "pct_lesionados": "Porcentaje de Lesionados por Cuartil"})
    fig_alt.update_traces(textposition="outside", cliponaxis=False, width=0.45, marker_color="#1f77b4")
    fig_alt.update_yaxes(range=[0, 40])
    fig_alt.update_xaxes(title_text="")
    mostrar(fig_alt, 360)

with col_pes:
    st.subheader("4.2 Análisis por cuartiles de peso")
    sql_q8 = P_CTE + """
    SELECT q_peso AS cuartil, MIN(weight_kg) AS min_kg, MAX(weight_kg) AS max_kg,
           ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados
    FROM ps GROUP BY 1 ORDER BY 1;
    """
    pes = run_query(sql_q8)
    pes["grupo"] = [f"C{c}: {a:g}–{b:g} kg" for c, a, b in zip(pes["cuartil"], pes["min_kg"], pes["max_kg"])]

    fig_pes = px.bar(pes, x="grupo", y="pct_lesionados", text_auto=".1f",
                     title="% de lesionados por cuartil de peso",
                     labels={"grupo": "Cuartil de Peso", "pct_lesionados": "Porcentaje de Lesionados por Cuartil"})
    fig_pes.update_traces(textposition="outside", cliponaxis=False, width=0.45, marker_color="#ff7f0e")
    fig_pes.update_yaxes(range=[0, 40])
    fig_pes.update_xaxes(title_text="")
    mostrar(fig_pes, 360)

st.markdown("""
Los gráficos anteriores evidencian la gran independencia entre las características antropométricas y la probabilidad de lesión. Las variaciones porcentuales entre el cuartil inferior y el superior son pequeñas, dándonos como resultado que un jugador más alto o más pesado no incrementa ni reduce por sí solo el riesgo de sufrir una lesión.
""")


# 4.3 Cruce entre altura y peso
st.subheader("4.3 Relación entre altura y peso")

col1, col2 = st.columns(2, vertical_alignment="center")

with col1:
    st.markdown("""
    Al analizar conjuntamente la altura y el peso de los futbolistas, los datos muestran que los jugadores se agrupan de manera natural en proporciones equilibradas. 
    
    La gran mayoría se concentra en los perfiles físicos más habituales, donde la estatura y la masa corporal guardan una relación más estrecha, mientras que los casos con combinaciones extremas o poco comunes tienen menos presentación en la muestra.
    """)

with col2:
    sql_q11 = P_CTE + """
    SELECT q_altura, q_peso, COUNT(*) AS jugadores
    FROM ps GROUP BY 1, 2 ORDER BY 1, 2;
    """
    q11 = run_query(sql_q11)
    n_mat = q11.pivot(index="q_altura", columns="q_peso", values="jugadores")
    n_mat.index = [f"Altura C{i}" for i in n_mat.index]
    n_mat.columns = [f"Peso C{i}" for i in n_mat.columns]

    fig = px.imshow(
        n_mat, 
        text_auto=",.0f", 
        aspect="auto", 
        title="Concentración de jugador-temporadas por biotipo",
        color_continuous_scale="Blues"
    )
    fig.update_layout(coloraxis_showscale=False)
    mostrar(fig, 340)

st.divider()

# 5. Análisis en la carga de minutos jugados
st.header("5. Carga de minutos jugados")

col_txt_min, col_fig_min = st.columns(2, vertical_alignment="center")

with col_txt_min:
    st.markdown("""
    Una de las hipótesis recurrentes en la medicina deportiva es el desgaste acumulado por exceso de minutos competitivos. Para examinar este factor, la muestra se divide en bandas crecientes de minutos disputados por temporada.
    
    De manera contundente, el porcentaje de futbolistas que experimentan lesiones permanece invariable (aproximadamente 24% a 25%) independientemente de que acumulen pocos o muchos minutos en el terreno de juego. La carga cuantitativa de participación no condiciona la probabilidad de lesionarse.
    """)

with col_fig_min:
    sql_q10 = P_CTE + """
    SELECT 
        CASE WHEN mins <= 500  THEN 'a) <=500'
             WHEN mins <= 1000 THEN 'b) 501-1000'
             WHEN mins <= 1500 THEN 'c) 1001-1500'
             WHEN mins <= 2000 THEN 'd) 1501-2000'
             WHEN mins <= 2500 THEN 'e) 2001-2500'
             WHEN mins <= 3000 THEN 'f) 2501-3000'
             ELSE 'g) 3000+' END AS banda_min,
        ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados
    FROM ps GROUP BY 1 ORDER BY 1;
    """
    q10 = run_query(sql_q10)
    q10["banda_min"] = q10["banda_min"].str[3:]

    fig_mins = px.bar(q10, x="banda_min", y="pct_lesionados", text_auto=".1f",
                      title="Porcentaje de lesionados según minutos jugados",
                      labels={"banda_min": "Banda de Minutos", "pct_lesionados": "% Lesionados"})
    fig_mins.update_traces(textposition="outside", cliponaxis=False, width=0.35, marker_color="#4ba3e3")
    fig_mins.update_yaxes(range=[0, 40])
    fig_mins.update_xaxes(title_text="")
    mostrar(fig_mins, 380)

st.divider()

# 6. Comparativa de jugadores con y sin lesiones
st.header("6. Perfil Comparativo: Jugadores con y sin lesión")

st.markdown("""
Para perfilar de manera definitiva si existen rasgos diferenciales entre quienes sufren lesiones y quienes no, la tabla siguiente contrasta las características promedio de ambos segmentos poblacionales.
""")

sql_q15 = P_CTE + """
SELECT CASE WHEN n_les > 0 THEN 'Con lesión' ELSE 'Sin lesión' END AS grupo,
       COUNT(*) AS jugadores,
       ROUND(AVG(height_cm), 2) AS altura_prom,
       ROUND(AVG(weight_kg), 2) AS peso_prom,
       ROUND(AVG(mins), 0) AS mins_promedio,
       ROUND(AVG(age), 2) AS edad_prom
FROM ps GROUP BY 1;
"""
q15 = run_query(sql_q15)
perfil = q15.set_index("grupo").T
etiq = {"jugadores": "Jugador-temporadas", "altura_prom": "Altura promedio (cm)", "peso_prom": "Peso promedio (kg)",
        "mins_promedio": "Minutos promedio", "edad_prom": "Edad promedio"}
perfil.index = [etiq.get(i, i) for i in perfil.index]
st.dataframe(perfil.round(2).reset_index().rename(columns={"index": "Variable Biométrica / Operativa"}), hide_index=True)

st.markdown("""
Los datos numéricos son concluyentes: los promedios de altura, peso, volumen de minutos y edad son muy idénticos entre los jugadores que completaron la temporada sin lesiones y aquellos que registraron bajas médicas.
""")

st.divider()

# 7. Lista de jugadores con mayor tiempo lesionado
st.header("7. Jugadores con mayor acumulación de días de baja")

st.markdown("""
Identificar los casos extremos de inactividad médica permite analizar la naturaleza de los perfiles más castigados por la enfermería a lo largo de las cuatro temporadas evaluadas.
""")

sql_q17 = P_CTE + """
SELECT p.name, ps.primary_category,
       MAX(ps.height_cm) AS altura_cm, MAX(ps.weight_kg) AS peso_kg,
       SUM(ps.mins) AS minutos, SUM(ps.n_les) AS lesiones, SUM(ps.dias_perdidos) AS dias_perdidos
FROM ps
JOIN players p ON p.player_id = ps.player_id
GROUP BY p.player_id, p.name, ps.primary_category
ORDER BY dias_perdidos DESC LIMIT 15;
"""
q17 = run_query(sql_q17)
pos_es = {"MIDFIELDER": "Mediocampista", "DEFENDER": "Defensa", "GOALKEEPER": "Portero", "ATTACKER": "Delantero"}
q17["primary_category"] = q17["primary_category"].map(pos_es).fillna(q17["primary_category"])
nombres_cols = {
    "name": "Jugador", "primary_category": "Posición", "altura_cm": "Altura (cm)",
    "peso_kg": "Peso (kg)", "minutos": "Minutos", "lesiones": "Lesiones", "dias_perdidos": "Días perdidos"
}

c1, c2 = st.columns([3, 2])
with c1:
    df_renombrado = q17.rename(columns=nombres_cols)
    
    def columna_resalte(val):
        max_val = df_renombrado["Lesiones"].max()
        min_val = df_renombrado["Lesiones"].min()
        rango = max_val - min_val if max_val != min_val else 1
        pct = (val - min_val) / rango

        opacidad = 0.35 + (pct * 0.65)
        return f'background-color: rgba(77, 208, 225, {opacidad:.2f}); color: #000000; font-weight: 500;'

    df_styled = (
        df_renombrado
        .style.map(columna_resalte, subset=["Lesiones"])
        .format({"Altura (cm)": "{:.0f}", "Peso (kg)": "{:.1f}", "Minutos": "{:,.0f}", "Lesiones": "{:.0f}", "Días perdidos": "{:,.0f}"})
    )
    st.dataframe(df_styled, hide_index=True)

with c2:
    fig_top = px.bar(q17.sort_values("dias_perdidos"), x="dias_perdidos", y="name", orientation="h", text_auto=",.0f",
                     title="Top 15 jugadores por días de baja acumulados",
                     labels={"dias_perdidos": "Días Perdidos", "name": "Jugador"})
    fig_top.update_traces(textposition="outside", cliponaxis=False)
    mostrar(fig_top, 460)

st.markdown("""
Los futbolistas que encabezan el registro de días perdidos acumulan cifras muy elevadas de inactividad debido a lesiones de larga duración (como roturas ligamentosas), y no a una alta frecuencia de pequeños incidentes. Sus características físicas se encuentran dentro de la media general de la competición.
""")
st.divider()

# Conclusión general
st.header("Conclusión general")

st.markdown("""
A modo de síntesis global, el análisis desarrollado a lo largo de las cuatro temporadas permite responder con total claridad al objetivo planteado:
""")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    * **Frecuencia constante:** Alrededor de uno de cada cuatro futbolistas sufre al menos una lesión por temporada (~24.8%), siendo lo habitual registrar un único episodio por campaña en cada jugador.
    * **El físico no define el riesgo:** Características corporales como la altura y el peso no tienen relación con las lesiones; los jugadores altos, bajos, delgados o pesados se lesionan exactamente en la misma proporción.
    """)
with c2:
    st.markdown("""
    * **Lo que importa es el tipo de lesión, no el cansancio:** Acumular muchos o pocos minutos en el terreno de juego no hace que un futbolista sea más propenso a lastimarse. El tiempo total de baja depende de la gravedad de cada lesión (como una rotura de ligamentos), no del desgaste por minutos.
    * **Resultados estables:** Los datos se comportan de forma idéntica año tras año, lo que confirma que las tendencias encontradas son sólidas en todo el período estudiado.
    """)

st.markdown("""
Con base en los datos analizados, ni la complexión física ni la cantidad de minutos jugados determinan quién se lesiona o cuánto tiempo pasa fuera de las canchas en el fútbol profesional evaluado.
""")