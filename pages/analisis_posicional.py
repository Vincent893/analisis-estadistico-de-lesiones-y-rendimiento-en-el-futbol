from database.DB import DB
from models.UI import UI
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme, PALETA_APP

UI.setup_page()
UI.render_sidebar()
cargar_estilos()

conn = DB.get_connection()

LINEAS_ES = {"GOALKEEPER": "Arquero", "DEFENDER": "Defensa", "MIDFIELDER": "Mediocampista", "ATTACKER": "Delantero"}
POSICIONES_ES = {
    "GK": "POR", "D-C": "DFC", "D-L": "LI", "D-R": "LD", "WB-L": "CI", "WB-R": "CD",
    "DM": "MCD", "M-C": "MC", "M-L": "MI", "M-R": "MD",
    "AM-C": "MCO", "AM-L": "EI", "AM-R": "ED", "ST-C": "DC",
}

# Una fila por jugador-temporada. Un jugador puede tener varias posiciones con rank 1;
# se toma una sola (menor position_id) para no duplicar filas.
SQL_JUGADOR_TEMPORADA = """
WITH pos_principal AS (
    SELECT pp.player_id, po.role_code || COALESCE('-' || po.side_code, '') AS pos
    FROM player_positions pp
    JOIN positions po USING (position_id)
    WHERE pp.position_rank = 1
    QUALIFY ROW_NUMBER() OVER (PARTITION BY pp.player_id ORDER BY pp.position_id) = 1
)
SELECT COALESCE(d.division_name, 'Sin división') AS liga,
       c.club_name            AS club,
       s.season_label         AS season,
       pp.pos                 AS position,
       p.primary_category     AS linea,
       ps.mins                AS minutes_played,
       psa.goals,
       psa.assists,
       psd.tackles_completed  AS tackles,
       psp.key_passes,
       ps.ability_score,
       psk.save_ratio,
       psk.saves_per_90,
       psk.clean_sheets_per_90,
       psk.conceded_per_90,
       psk.expected_goals_prevented_per_90
FROM player_seasons ps
JOIN players p                   USING (player_id)
JOIN pos_principal pp            USING (player_id)
JOIN clubs c                     USING (club_id)
LEFT JOIN divisions d            USING (division_id)
JOIN seasons s                   USING (season_id)
JOIN player_stats_attacking psa  USING (player_season_id)
JOIN player_stats_defending psd  USING (player_season_id)
JOIN player_stats_passing psp    USING (player_season_id)
LEFT JOIN player_stats_goalkeeping psk USING (player_season_id)
"""

@st.cache_data
def cargar_datos(_conn):
    df = _conn.execute(SQL_JUGADOR_TEMPORADA).df()
    df["linea"] = df["linea"].map(LINEAS_ES).fillna(df["linea"])
    df["position"] = df["position"].map(POSICIONES_ES).fillna(df["position"])
    return df

if conn is None:
    st.error("No se pudo conectar a la base de datos. Revisa las variables de entorno.")
    st.stop()

try:
    df_raw = cargar_datos(conn)
except Exception as e:
    st.error(f"Error al consultar los datos del Objetivo 3: {e}")
    st.stop()

df = df_raw.copy()
df["goles_asistencias"] = df["goals"] + df["assists"]
MIN_MINUTOS_90 = 450
_min_ok = df["minutes_played"].where(df["minutes_played"] >= MIN_MINUTOS_90)
for col in ["goles_asistencias", "goals", "assists"]:
    df[f"{col}_90"] = df[col] * 90 / _min_ok
liga_col = "liga"
# Arqueros con minutos suficientes para que las métricas por 90' y los ratios sean estables
df_arq = df[(df["linea"] == "Arquero") & (df["minutes_played"] >= MIN_MINUTOS_90)].copy()
df_arq["pct_paradas"] = df_arq["save_ratio"] * 100
LINEAS_ORDEN =["Arquero", "Defensa", "Mediocampista", "Delantero"]
colores_kpi = dict(zip(LINEAS_ORDEN, PALETA_APP))

st.markdown("""
    <div class="hero-header">
        <span class="hero-badge">Objetivo 3 · Temporadas 2022 – 2026</span>
        <div class="hero-title">Dinámicas Posicionales</div>
        <p style="color:#94A3B8; margin:0; font-size:1.05rem; line-height:1.5;">
            Examinar el aporte porcentual y el promedio de rendimiento de las líneas posicionales (arqueros, defensas,
            mediocampistas y delanteros) dentro de la estructura de los equipos durante el ciclo 2022-2026.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Indicadores Clave por Línea")

agg_kpi = df.groupby("linea").agg(
    Jugadores=("linea", "count"),
    Goles_prom=("goals", "mean"),
    Asist_prom=("assists", "mean"),
    Mins_prom=("minutes_played", "mean"),
    Tackles_prom=("tackles", "mean"),
).round(2)
total_jug = agg_kpi["Jugadores"].sum()

cols_kpi = st.columns(4)
for i, linea in enumerate(LINEAS_ORDEN):
    if linea not in agg_kpi.index:
        continue
    row = agg_kpi.loc[linea]
    pct = row["Jugadores"] / total_jug * 100
    color = colores_kpi[linea]
    if linea == "Arquero":
        # Métricas de portería
        detalle = (
            f"Paradas: {df_arq['pct_paradas'].mean():.1f}%<br>"
            f"Porterías a cero/90': {df_arq['clean_sheets_per_90'].mean():.2f}<br>"
            f"Goles concedidos/90': {df_arq['conceded_per_90'].mean():.2f}"
        )
    else:
        detalle = (
            f"Goles prom: {row['Goles_prom']:.2f}<br>"
            f"Asist prom: {row['Asist_prom']:.2f} · Tackles prom: {row['Tackles_prom']:.1f}<br>"
            f"Minutos prom: {row['Mins_prom']:.0f}"
        )
    with cols_kpi[i]:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color:{color};">
            <div class="kpi-title">{linea}</div>
            <div class="kpi-value" style="font-size:1.35rem;">{row['Jugadores']:,.0f} jug.</div>
            <div class="kpi-footer" style="font-size:0.85rem; line-height:1.4;">
                {detalle}
            </div>
        </div>""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 1: Aporte Porcentual por Línea y Temporada")
# Gráficos 1 y 2: sin arqueros, su aporte en goles, asistencias y tackles es prácticamente nulo
df_campo = df[df["linea"] != "Arquero"]
st.caption("Porcentaje de goles, asistencias y tackles aportado por cada línea de campo respecto al total de la muestra. Se excluyen los arqueros: su aporte en estas métricas es prácticamente nulo (0.01 % de goles + asistencias y 0.1 % de tackles)."
)

metrica_g1 = st.radio(
    "Métrica de aporte:", ["Goles + Asistencias", "Goles", "Asistencias", "Tackles"],
    horizontal=True, key="g1_metrica"
)
col_metrica = {
    "Goles + Asistencias": "goles_asistencias",
    "Goles":               "goals",
    "Asistencias":         "assists",
    "Tackles":             "tackles",
}[metrica_g1]

total_por_temp = df_campo.groupby("season")[col_metrica].sum().rename("total_temp")
agg_g1 = df_campo.groupby(["season", "linea"])[col_metrica].sum().reset_index(name="suma")
agg_g1 = agg_g1.merge(total_por_temp, on="season")
agg_g1["pct"] = agg_g1["suma"] / agg_g1["total_temp"] * 100
agg_g1["linea"] = pd.Categorical(agg_g1["linea"], categories=LINEAS_ORDEN, ordered=True)
agg_g1 = agg_g1.sort_values(["season", "linea"])

fig1 = px.bar(
    agg_g1, x="season", y="pct", color="linea",
    barmode="group", text_auto=".1f",
    color_discrete_map=colores_kpi,
    category_orders={"linea": LINEAS_ORDEN},
    labels={"season": "Temporada", "pct": "% del Aporte Total", "linea": "Línea"},
)
fig1.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
fig1.update_layout(height=430, yaxis_ticksuffix="%")
fig1 = apply_theme(fig1)
st.plotly_chart(fig1, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Los mediocampistas concentran la mayor parte del aporte total: cerca del 65% de los goles + asistencias, el 65% de los goles y el 65% de las asistencias en todas las temporadas. Esto se explica por el volumen de la línea: en la base de datos la categoría de mediocampista incluye extremos, interiores y mediapuntas, y reúne al 45.3% de los registros. Los defensas aportan el 22.3% de los goles + asistencias, apoyados sobre todo en las asistencias (30.6%), mientras que los delanteros, que solo agrupan a los centrodelanteros (6.2% de la muestra), aportan el 12.5% de los goles + asistencias y el 19.3% de los goles. En la métrica de tackles, el aporte se reparte entre defensas (50.4%) y mediocampistas (46.0%), con una participación residual de los delanteros (3.6%).
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> El aporte colectivo está dominado por la línea más numerosa: los mediocampistas producen alrededor de dos tercios del total ofensivo, y defensas y mediocampistas se reparten casi por igual la carga defensiva.</li>
        <li><b>Estabilidad:</b> Las proporciones varían menos de 0.2 puntos porcentuales entre temporadas, por lo que no hay transferencia de carga entre líneas en el ciclo 2022-2026.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 2: Promedio por Jugador por Línea y Temporada")
st.caption("Promedio por jugador de goles, asistencias y tackles en cada línea posicional. Contrasta con el Gráfico 1: aquel muestra cuánto aporta cada línea al total; este, cuánto aporta un jugador típico de cada línea. Se excluyen los arqueros: su aporte en estas métricas es prácticamente nulo (0.01 % de goles + asistencias y 0.1 % de tackles).")

metrica_prom = st.radio(
    "Métrica promedio:", ["Goles + Asistencias", "Goles", "Asistencias", "Tackles"],
    horizontal=True, key="g2_prom_metrica"
)
col_prom = {
    "Goles + Asistencias": "goles_asistencias",
    "Goles":               "goals",
    "Asistencias":         "assists",
    "Tackles":             "tackles",
}[metrica_prom]

# Promedio por jugador: no depende de cuántos jugadores tenga cada línea
agg_prom = df_campo.groupby(["season", "linea"])[col_prom].mean().reset_index(name="promedio")
agg_prom["linea"] = pd.Categorical(agg_prom["linea"], categories=LINEAS_ORDEN, ordered=True)
agg_prom = agg_prom.sort_values(["season", "linea"])

fig_prom = px.bar(
    agg_prom, x="season", y="promedio", color="linea",
    barmode="group",
    color_discrete_map=colores_kpi,
    category_orders={"linea": LINEAS_ORDEN},
    labels={"season": "Temporada", "promedio": f"{metrica_prom} promedio por jugador", "linea": "Línea"},
)
fig_prom.update_traces(texttemplate="%{y:.2f}", textposition="outside")
fig_prom.update_layout(height=430)
fig_prom = apply_theme(fig_prom)
st.plotly_chart(fig_prom, width="stretch")

with st.expander("Explicación de Lectura"):
    st.markdown("""
    Este gráfico de barras agrupadas muestra, para cada temporada, cuántos goles, asistencias o tackles registró en promedio un jugador de cada línea posicional. A diferencia del aporte porcentual del Gráfico 1, este promedio no depende de cuántos jugadores tenga cada línea: una línea con muchos jugadores puede aportar mucho al total aunque cada jugador produzca poco, y al revés. Comparar ambos gráficos permite distinguir el peso colectivo de una línea de su rendimiento individual típico.
    """)

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Al eliminar el efecto del tamaño de cada línea, el orden se invierte respecto al Gráfico 1. Un delantero típico registra entre 8.1 y 8.3 goles + asistencias por temporada, frente a 5.8–6.0 de un mediocampista y 2.3 de un defensa. En goles la diferencia es mayor: 6.9–7.0 por delantero contra 3.2–3.3 por mediocampista y menos de 0.9 por defensa. Las asistencias, en cambio, son la especialidad del mediocampo (2.6–2.7 por jugador), mientras que defensas y delanteros quedan casi igualados (1.4 y 1.2). En tackles, el defensa típico lidera (35.0–35.9), seguido del mediocampista (28.5–29.2) y del delantero (16.2–16.5).
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Rendimiento individual:</b> El delantero es el jugador con mayor producción goleadora individual, aunque su línea aporte solo el 12.5% del total; el peso colectivo del mediocampo proviene de su número de jugadores, no de un rendimiento individual superior.</li>
        <li><b>Evolución:</b> Los promedios se mantienen casi planos en las cuatro temporadas, con un leve aumento de los tackles por defensa (+2.5% entre 2022/23 y 2025/26).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

NOMBRES_VAR = {
    "ability_score": "Puntuacion de Habilidad",
    "goles_asistencias": "Goles + Asistencias",
    "goals": "Goles",
    "assists": "Asistencias",
    "goles_asistencias_90": "Goles + Asistencias por 90'",
    "goals_90": "Goles por 90'",
    "assists_90": "Asistencias por 90'",
    "minutes_played": "Minutos Jugados",
}

st.subheader("Gráfico 3: Distribución del Rendimiento Individual por Línea")

metrica_box = st.selectbox(
    "Variable analizada:", list(NOMBRES_VAR), format_func=NOMBRES_VAR.get,
    index=list(NOMBRES_VAR).index("goles_asistencias_90"), key="g2_var"
)
st.caption(f"Distribución de {NOMBRES_VAR[metrica_box]} por línea posicional. La caja representa el rango intercuartílico, la línea central la mediana y la línea punteada la media. Los valores atípicos no se dibujan (son miles de registros); sus extremos figuran en la tabla inferior."
           + (f" Las métricas por 90' solo incluyen jugadores con {MIN_MINUTOS_90}+ minutos." if metrica_box.endswith("_90") else ""))

df_g2 = df[df["linea"].isin(LINEAS_ORDEN)].copy()
df_g2["linea"] = pd.Categorical(df_g2["linea"], categories=LINEAS_ORDEN, ordered=True)

fig2 = go.Figure()
for linea in LINEAS_ORDEN:
    sub = df_g2[df_g2["linea"] == linea][metrica_box].dropna()

    hex_color = colores_kpi[linea].lstrip("#")
    r, g, b = (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )
    fill_rgba = f"rgba({r}, {g}, {b}, 0.3)"  

    fig2.add_trace(
        go.Box(
            y=sub,
            name=linea,
            marker_color=colores_kpi[linea],
            boxmean=True,
            boxpoints=False,
            line=dict(width=2),
            fillcolor=fill_rgba,
        )
    )

fig2.update_layout(
    height=430,
    yaxis_title=NOMBRES_VAR[metrica_box],
    showlegend=False,
)
fig2 = apply_theme(fig2)
st.plotly_chart(fig2, width="stretch")

with st.expander("Explicación de Lectura"):
    st.markdown("""
    Este boxplot resume la distribución de la variable seleccionada en cada línea posicional. La línea central de cada caja indica la mediana (percentil 50). La caja representa el rango intercuartílico (Rango IQ), donde se concentra el 50% central de los jugadores (entre el percentil 25 y el 75). La línea punteada marca la media aritmética. Los bigotes (líneas verticales que salen de la caja) llegan hasta 1.5 veces el rango intercuartílico; los valores más allá de ese límite (atípicos) no se dibujan, y el máximo de cada línea se informa en la tabla inferior. La longitud de la caja y de los bigotes describe la dispersión de los datos: cajas más largas indican mayor heterogeneidad, cajas más compactas indican mayor homogeneidad.
    """)

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        En goles + asistencias por 90' (variable por defecto), las medianas separan con claridad las líneas: 0.48 en delanteros, 0.30 en mediocampistas, 0.09 en defensas y 0 en arqueros. Las cajas de delanteros y mediocampistas tienen un ancho similar (rango intercuartílico de 0.29 y 0.28), pero en relación con su media la dispersión crece a medida que la línea se aleja del arco rival: el coeficiente de variación es 0.46 en delanteros, 0.66 en mediocampistas y 1.02 en defensas. En las cuatro líneas la media supera a la mediana, señal de asimetría positiva: pocos jugadores con producción muy alta (máximos cercanos a 1.9 en delanteros y mediocampistas) elevan el promedio.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Asimetría:</b> Todas las líneas presentan asimetría positiva, más marcada en defensas, donde la mediana (0.09) queda muy por debajo de los valores máximos (1.65).</li>
        <li><b>Consistencia relativa:</b> Los delanteros son la línea más homogénea en términos relativos (menor coeficiente de variación); los defensas, la más heterogénea. En el Ability Score, en cambio, las cuatro cajas son casi idénticas (medianas entre 375 y 407).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

desc_table = (
    df_g2.groupby("linea")[metrica_box]
         .describe(percentiles=[0.25, 0.5, 0.75])
         .rename(columns={"count": "N", "mean": "Media", "std": "DE", "min": "Mín.", "25%": "Q1 (P25)", "50%": "Mediana", "75%": "Q3 (P75)", "max": "Máx."})
         .round(3)
)
st.dataframe(desc_table, width="stretch")

st.divider()

st.subheader("Gráfico 4: Promedio de Rendimiento por Línea")

metrica_g3 = st.selectbox(
    "Variable evaluada:", list(NOMBRES_VAR), format_func=NOMBRES_VAR.get,
    index=0, key="g3_var"
)
st.caption(f"Media aritmética de {NOMBRES_VAR[metrica_g3]} por línea posicional."
           + (f" Solo jugadores con {MIN_MINUTOS_90}+ minutos." if metrica_g3.endswith("_90") else ""))

agg_g3 = (
    df.groupby("linea")[metrica_g3]
      .agg(["mean", "count"])
      .reset_index()
      .rename(columns={"mean": "media", "count": "n"})
)
agg_g3["linea"] = pd.Categorical(agg_g3["linea"], categories=LINEAS_ORDEN, ordered=True)
agg_g3 = agg_g3.sort_values("linea")

fig3 = go.Figure()
for _, row in agg_g3.iterrows():
    linea = row["linea"]
    texto = f"{row['media']:.3f}" if row["media"] < 10 else f"{row['media']:,.1f}"
    fig3.add_trace(go.Bar(
        y=[linea], x=[row["media"]],
        orientation="h",
        marker_color=colores_kpi[linea],
        name=linea,
        text=texto,
        textposition="outside",
        cliponaxis=False,
        hovertemplate=f"<b>{linea}</b><br>Media: {texto}<br>N: {row['n']:,}<extra></extra>",
    ))

fig3.update_layout(
    height=340,
    xaxis_title=NOMBRES_VAR[metrica_g3],
    yaxis_title="Línea Posicional",
    showlegend=False,
    bargap=0.35,
)
fig3 = apply_theme(fig3)
st.plotly_chart(fig3, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        En la Puntuación de Habilidad (variable por defecto), los mediocampistas registran la media más alta (416.3), seguidos por defensas (409.8), delanteros (388.9) y arqueros (385.1). La diferencia entre la línea más alta y la más baja es de solo 31 puntos en una escala que va de 116 a 768, es decir, menos del 5% del rango: la habilidad promedio es prácticamente la misma en todas las demarcaciones. Las diferencias reales entre líneas aparecen en las métricas de producción: en goles + asistencias por 90', la media del delantero (0.50) cuadruplica la del defensa (0.11).
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Habilidad:</b> El Ability Score no discrimina entre líneas; las medias se ordenan mediocampistas > defensas > delanteros > arqueros con brechas muy pequeñas.</li>
        <li><b>Producción:</b> Las métricas de goles y asistencias sí separan las líneas, con el delantero a la cabeza en goles y el mediocampista en asistencias.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 5: Distribución Porcentual de Jugadores por Línea Posicional")
st.caption("Proporción de jugadores en la muestra según su demarcación táctica.")

comp_linea = df["linea"].value_counts().reset_index()
comp_linea.columns = ["Línea", "Jugadores"]
comp_linea["Línea"] = pd.Categorical(comp_linea["Línea"], categories=LINEAS_ORDEN, ordered=True)
comp_linea = comp_linea.sort_values("Línea")

fig5 = px.pie(
    comp_linea,
    names="Línea",
    values="Jugadores",
    hole=0.45,
    color="Línea",
    color_discrete_map=colores_kpi,
    category_orders={"Línea": LINEAS_ORDEN},
)
fig5.update_traces(
    textinfo="label+percent",
    textfont_size=13,
    hovertemplate="<b>%{label}</b><br>Jugadores: %{value:,}<br>Proporción: %{percent}<extra></extra>",
)
fig5.update_layout(height=400)
fig5 = apply_theme(fig5)
st.plotly_chart(fig5, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Los mediocampistas son la línea más numerosa (45.3% de los registros jugador-temporada), seguidos por los defensas (40.4%), los arqueros (8.1%) y los delanteros (6.2%). La baja proporción de delanteros se debe a la clasificación de la base de datos: solo el centrodelantero se considera delantero, mientras que extremos y mediapuntas se cuentan como mediocampistas. Esta composición explica los resultados del Gráfico 1: el mediocampo domina el aporte total por volumen, mientras que los delanteros, con el 6.2% de los registros, generan el 12.5% de los goles + asistencias y el 19.3% de los goles.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Composición de la muestra:</b> Mediocampistas y defensas suman el 85.7% de los registros; arqueros y delanteros, el 14.3% restante.</li>
        <li><b>Impacto relativo:</b> Los delanteros aportan aproximadamente el triple de goles que su peso en la muestra (19.3% frente a 6.2%), el mayor impacto relativo por jugador de las cuatro líneas.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Análisis Complementario")

tab1, tab2, tab5 = st.tabs([
    "Perfil Multidimensional",
    "Balance Ofensivo vs. Defensivo",
    "Rendimiento de Arqueros",
])

with tab1:
    st.caption(
        "Perfil promedio por línea · Ejes normalizados (0-1) para evitar distorsión visual · "
        "Variables: Goles, Asistencias, Pases Clave, Acciones Defensivas, Minutos"
    )
    radar_vars = {
        "Goles":            "goals",
        "Asistencias":      "assists",
        "Pases Clave":      "key_passes",
        "Acc. Defensivas":  "tackles",
        "Minutos":          "minutes_played",
    }
    agg_radar = df.groupby("linea")[list(radar_vars.values())].mean()
    agg_radar_norm = (agg_radar - agg_radar.min()) / (agg_radar.max() - agg_radar.min() + 1e-9)

    fig_r = go.Figure()
    theta_labels = list(radar_vars.keys())
    for linea in LINEAS_ORDEN:
      if linea not in agg_radar_norm.index:
        continue
      vals = agg_radar_norm.loc[linea].tolist()
      vals += [vals[0]]

      hex_color = colores_kpi[linea].lstrip("#")
      r, g, b = (
          int(hex_color[0:2], 16),
          int(hex_color[2:4], 16),
          int(hex_color[4:6], 16),
      )
      fill_rgba = (
          f"rgba({r}, {g}, {b}, 0.3)"  
      )

      fig_r.add_trace(
          go.Scatterpolar(
              r=vals,
              theta=theta_labels + [theta_labels[0]],
              fill="toself",
              name=linea,
              fillcolor=fill_rgba,
              line=dict(color=colores_kpi[linea], width=2),
          )
      )
    fig_r.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=430,
        showlegend=True,
    )
    st.plotly_chart(fig_r, width="stretch")

    st.markdown("""
    <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
        <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
        <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
            Cada eje está normalizado entre la línea con el promedio más bajo (0) y la línea con el promedio más alto (1), por lo que el radar compara la forma de los perfiles y no sus magnitudes. El delantero marca el máximo en goles (6.97 por temporada) y el mínimo en minutos (1,496). El mediocampista lidera en asistencias (2.66) y pases clave (20.9) y es segundo en acciones defensivas (28.8 tackles), lo que le da el perfil más amplio de las cuatro líneas. El defensa lidera en acciones defensivas (35.5 tackles) y en minutos (1,809), con valores intermedios en asistencias y pases clave (1.40 y 13.9). El arquero solo destaca en minutos (1,805); en el resto de los ejes queda en cero porque es la línea con el promedio más bajo.
        </p>
        <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
        <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
            <li><b>Especialización:</b> Delanteros y defensas tienen perfiles concentrados en un extremo (goles y acciones defensivas, respectivamente), mientras que el mediocampista reparte su aporte entre creación y recuperación.</li>
            <li><b>Continuidad:</b> Arqueros y defensas son las líneas con más minutos por temporada (unos 1,800), frente a unos 1,500 de los delanteros, la línea con mayor rotación.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.caption("Barras apiladas al 100% · Aporte ofensivo (Goles + Asistencias + Pases Clave) vs. defensivo (Tackles) por línea")
    df["aporte_ofensivo"] = df["goals"] + df["assists"] + df["key_passes"]
    df["aporte_defensivo"] = df["tackles"]

    agg_ov = df.groupby("linea")[["aporte_ofensivo", "aporte_defensivo"]].sum()
    total_ov = agg_ov.sum(axis=1)
    agg_ov_pct = (agg_ov.div(total_ov, axis=0) * 100).reset_index()
    agg_ov_pct["linea"] = pd.Categorical(agg_ov_pct["linea"], categories=LINEAS_ORDEN, ordered=True)
    agg_ov_pct = agg_ov_pct.sort_values("linea")

    fig_ov = go.Figure()
    fig_ov.add_trace(go.Bar(
        y=agg_ov_pct["linea"], x=agg_ov_pct["aporte_ofensivo"],
        name="Ofensivo", orientation="h",
        marker_color=PALETA_APP[0], text=agg_ov_pct["aporte_ofensivo"].round(1).astype(str) + "%",
        textposition="inside",
    ))
    fig_ov.add_trace(go.Bar(
        y=agg_ov_pct["linea"], x=agg_ov_pct["aporte_defensivo"],
        name="Defensivo", orientation="h",
        marker_color=PALETA_APP[1], text=agg_ov_pct["aporte_defensivo"].round(1).astype(str) + "%",
        textposition="inside",
    ))
    fig_ov.update_layout(
        barmode="stack", height=320,
        xaxis_title="% Acumulado del Aporte", xaxis_ticksuffix="%",
        yaxis_title="Línea Posicional",
    )
    fig_ov = apply_theme(fig_ov)
    st.plotly_chart(fig_ov, width="stretch")

    st.markdown("""
    <div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
        <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
        <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
            En los defensas, el 68.7% de las acciones contabilizadas son defensivas (tackles) y el 31.3% ofensivas (goles, asistencias y pases clave). El mediocampista queda casi en equilibrio (48.2% ofensivo y 51.8% defensivo) y el delantero es la única línea de campo donde predomina lo ofensivo (53.3%). La barra de los arqueros (61.1% ofensivo) no es interpretable: registran en promedio menos de un pase clave y menos de un tackle por temporada, de modo que la proporción se calcula sobre un volumen mínimo.
        </p>
        <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
        <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
            <li><b>Gradiente posicional:</b> El peso de lo ofensivo crece a medida que la línea se acerca al arco rival: 31.3% en defensas, 48.2% en mediocampistas y 53.3% en delanteros.</li>
            <li><b>Alcance de la comparación:</b> El balance suma acciones de distinta naturaleza y solo considera los tackles como acción defensiva, por lo que sirve para comparar líneas entre sí y no como medida absoluta del trabajo de cada una.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.caption(
        f"Métricas propias de la portería · Arqueros con {MIN_MINUTOS_90}+ minutos "
        f"({len(df_arq):,} registros jugador-temporada) · Promedio por arquero"
    )
    k1, k2, k3, k4 = st.columns(4)
    for col_k, titulo, valor, pie in [
        (k1, "% de Paradas", f"{df_arq['pct_paradas'].mean():.1f}%", "Remates a puerta detenidos"),
        (k2, "Paradas por 90'", f"{df_arq['saves_per_90'].mean():.2f}", "Volumen de trabajo"),
        (k3, "Porterías a cero por 90'", f"{df_arq['clean_sheets_per_90'].mean():.2f}", "Partidos sin goles recibidos"),
        (k4, "Goles evitados por 90'", f"{df_arq['expected_goals_prevented_per_90'].mean():+.3f}", "Goles esperados − recibidos"),
    ]:
        with col_k:
            st.markdown(f"""
            <div class="kpi-card" style="border-top-color:{colores_kpi['Arquero']};">
                <div class="kpi-title">{titulo}</div>
                <div class="kpi-value" style="font-size:1.35rem;">{valor}</div>
                <div class="kpi-footer" style="font-size:0.85rem;">{pie}</div>
            </div>""", unsafe_allow_html=True)

    metricas_arq = {
        "% de Paradas":               "pct_paradas",
        "Porterías a cero por 90'":   "clean_sheets_per_90",
        "Goles concedidos por 90'":   "conceded_per_90",
        "Goles evitados por 90'":     "expected_goals_prevented_per_90",
    }
    metrica_arq = st.radio("Métrica:", list(metricas_arq), horizontal=True, key="t5_metrica")
    col_arq = metricas_arq[metrica_arq]

    agg_arq = df_arq.groupby("season")[col_arq].mean().reset_index(name="promedio")
    fig_arq = px.bar(
        agg_arq, x="season", y="promedio",
        labels={"season": "Temporada", "promedio": f"{metrica_arq} (promedio)"},
    )
    fig_arq.update_traces(
        marker_color=colores_kpi["Arquero"],
        texttemplate="%{y:.1f}%" if col_arq == "pct_paradas" else "%{y:.3f}",
        textposition="outside", cliponaxis=False,
    )
    fig_arq.update_layout(height=400)
    fig_arq = apply_theme(fig_arq)
    st.plotly_chart(fig_arq, width="stretch")

st.divider()

st.subheader("Conclusiones del Análisis")

st.markdown("""
<div class="section-container" style="border-left: 4px solid #00E5FF; padding: 25px 30px; margin-top: 15px; margin-bottom: 25px;">
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        El análisis posicional del ciclo 2022-2026 muestra que el aporte colectivo y el rendimiento individual cuentan historias distintas. Por volumen, el mediocampo domina: con el 45.3% de los registros produce cerca del 65% de los goles + asistencias, y comparte con la defensa la carga defensiva (46.0% y 50.4% de los tackles). Por jugador, en cambio, el delantero es el más productivo en ataque (8.2 goles + asistencias por temporada y 0.50 por 90'), el mediocampista lidera en asistencias y pases clave, y el defensa en tackles (35.5 por temporada). El balance ofensivo-defensivo confirma esta especialización: el aporte del defensa es 69% defensivo, el del delantero 53% ofensivo y el del mediocampista queda casi equilibrado (48% / 52%).
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        La distribución del rendimiento individual presenta asimetría positiva en todas las líneas: la mayoría de los jugadores produce poco y unos pocos elevan la media. En términos relativos, los delanteros son la línea más homogénea (coeficiente de variación de 0.46 en goles + asistencias por 90') y los defensas la más heterogénea (1.02). La Puntuación de Habilidad, por su parte, apenas varía entre líneas (medias entre 385 y 416), por lo que las diferencias posicionales se explican por el rol en el campo y no por un nivel de habilidad distinto.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        Los arqueros, analizados con sus métricas propias, detienen en promedio el 70.5% de los remates a puerta, reciben 1.27 goles por 90' y mantienen la portería a cero en 0.32 partidos por 90'. El 59% de ellos evita más goles de los esperados, aunque el promedio (+0.044 por 90') es apenas positivo. En minutaje, arqueros y defensas son las líneas de mayor continuidad (unos 1,800 minutos por temporada), mientras que los delanteros registran el promedio más bajo (unos 1,500), lo que indica mayor rotación en la posición más ofensiva.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 0; font-size: 1.02rem;">
        En cuanto a la evolución temporal, tanto las proporciones como los promedios por línea se mantienen prácticamente constantes en las cuatro temporadas (variaciones menores a 0.2 puntos porcentuales en el aporte). Esta estabilidad debe leerse con cautela: tres de las cuatro temporadas (2022/23 a 2024/25) están marcadas como fabricadas en la base de datos (solo 2025/26 es real), lo que limita las conclusiones sobre tendencias.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Nota Metodológica")

st.markdown("""
<div class="section-container" style="border-left: 3px solid rgba(255, 255, 255, 0.25); padding: 20px 25px; margin-top: 15px;">
    <p style="color: #94A3B8; line-height: 1.7; margin-bottom: 0; font-size: 0.98rem;">
        El análisis posicional se desarrolló sobre 108,639 registros jugador-temporada, clasificando a cada jugador en una de cuatro líneas (Arqueros, Defensas, Mediocampistas y Delanteros) según la categoría principal de la base de datos, y en una demarcación específica según su posición principal. El aporte porcentual (Gráfico 1) y el promedio por jugador (Gráfico 2) se calcularon por temporada, excluyendo a los arqueros, cuyo aporte en goles, asistencias y tackles es prácticamente nulo. Las métricas por 90 minutos solo consideran jugadores con 450 minutos o más, para evitar valores inflados por muestras pequeñas; el mismo filtro se aplicó a las métricas de portería. Se emplearon medidas de tendencia central (media y mediana) y de dispersión (rango intercuartílico y coeficiente de variación). Las temporadas 2022/23 a 2024/25 están marcadas como fabricadas en la base de datos (campo is_fabricated); solo 2025/26 corresponde a datos reales. No se aplicaron pruebas de hipótesis ni modelos predictivos.
    </p>
</div>
""", unsafe_allow_html=True)