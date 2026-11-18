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
       psa.goals_per_90 + psa.assists_per_90                    AS offensive_score,
       psd.tackles_completed_per_90 + psd.interceptions_per_90  AS defensive_score
FROM player_seasons ps
JOIN players p                   USING (player_id)
JOIN pos_principal pp            USING (player_id)
JOIN clubs c                     USING (club_id)
LEFT JOIN divisions d            USING (division_id)
JOIN seasons s                   USING (season_id)
JOIN player_stats_attacking psa  USING (player_season_id)
JOIN player_stats_defending psd  USING (player_season_id)
JOIN player_stats_passing psp    USING (player_season_id)
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
LINEAS_ORDEN = ["Arquero", "Defensa", "Mediocampista", "Delantero"]
# Un color fijo por línea en toda la página, tomado de la paleta del tema
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
    with cols_kpi[i]:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color:{color};">
            <div class="kpi-title">{linea}</div>
            <div class="kpi-value" style="font-size:1.35rem;">{row['Jugadores']:,.0f} jug.</div>
            <div class="kpi-footer" style="font-size:0.85rem; line-height:1.4;">
                {pct:.1f}% del censo · Goles prom: {row['Goles_prom']:.2f}<br>
                Asist prom: {row['Asist_prom']:.2f} · Tackles prom: {row['Tackles_prom']:.1f}<br>
                Minutos prom: {row['Mins_prom']:.0f}
            </div>
        </div>""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 1: Aporte Porcentual por Línea y Temporada")
# Gráficos 1 y 2: sin arqueros, su aporte en goles, asistencias y tackles es prácticamente nulo
df_campo = df[df["linea"] != "Arquero"]
NOTA_ARQUEROS = "Se excluyen los arqueros: su aporte en estas métricas es prácticamente nulo (0,01 % de goles + asistencias y 0,1 % de tackles)."

st.caption("Porcentaje de goles, asistencias y tackles aportado por cada línea de campo respecto al total de la muestra. " + NOTA_ARQUEROS)

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
        El análisis del aporte porcentual por línea muestra una estructura de contribución estable a lo largo del ciclo 2022-2026. Los delanteros concentran la mayor cuota de producción ofensiva, superando el 54% del total en todas las temporadas. Le siguen los mediocampistas, con un aporte que oscila entre el 27% y el 29%, y los defensas, que representan entre el 11% y el 13%. Los arqueros, por su parte, mantienen una participación marginal inferior al 3%. Esta distribución refleja una especialización funcional clara: la finalización recae principalmente en la delantera, mientras que el mediocampo sostiene una cuota significativa de creación y contención.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> La producción ofensiva está altamente concentrada en la línea de delanteros, que aporta más de la mitad del rendimiento total en cada temporada.</li>
        <li><b>Estabilidad:</b> Las proporciones de aporte por línea se mantienen prácticamente constantes a lo largo de las cuatro temporadas, lo que describe una estructura de responsabilidades estable en la muestra analizada.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 2: Promedio por Jugador por Línea y Temporada")
st.caption("Promedio por jugador de goles, asistencias y tackles en cada línea posicional. Contrasta con el Gráfico 1: aquel muestra cuánto aporta cada línea al total; este, cuánto aporta un jugador típico de cada línea. " + NOTA_ARQUEROS)

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
        La composición del aporte por línea se mantiene estable a lo largo del ciclo 2022-2026, sin transferencias significativas de carga entre demarcaciones. Los delanteros conservan la franja más amplia, representando más de la mitad del aporte total en todas las temporadas. Los mediocampistas mantienen una franja estable cercana al 30%, mientras que defensas y arqueros ocupan las franjas inferiores con variaciones mínimas. Esta estabilidad en la composición describe una estructura de responsabilidades funcional que no ha experimentado cambios bruscos en la distribución de la producción entre líneas.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Estabilidad:</b> La estructura de aporte por línea se mantiene constante a lo largo de las cuatro temporadas, sin variaciones significativas en la proporción de cada demarcación.</li>
        <li><b>Dominio Ofensivo:</b> Los delanteros conservan la mayor cuota de participación en el total de la métrica, seguidos por los mediocampistas, mientras que defensas y arqueros mantienen una participación menor y estable.</li>
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
    Este boxplot resume la distribución de la variable seleccionada en cada línea posicional. La línea central de cada caja indica la mediana (percentil 50). La caja representa el rango intercuartílico (Rango IQ), donde se concentra el 50% central de los jugadores (entre el percentil 25 y el 75). La línea punteada marca la media aritmética. Los bigotes (líneas verticales que salen de la caja) llegan hasta 1,5 veces el rango intercuartílico; los valores más allá de ese límite (atípicos) no se dibujan, y el máximo de cada línea se informa en la tabla inferior. La longitud de la caja y de los bigotes describe la dispersión de los datos: cajas más largas indican mayor heterogeneidad, cajas más compactas indican mayor homogeneidad.
    """)

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        El análisis de distribución muestra diferencias claras en la forma de los datos según la demarcación. La línea de delanteros presenta una caja con mayor longitud y una mediana ligeramente superior, acompañada de una mayor cantidad de valores atípicos en la zona alta del gráfico. Esto describe una mayor heterogeneidad en el rendimiento ofensivo, con una presencia significativa de jugadores que se alejan de la media hacia arriba. En contraste, las líneas de arqueros, defensas y mediocampistas muestran cajas más compactas y simétricas, con medianas muy próximas entre sí y una menor cantidad de valores atípicos. Esto describe una mayor homogeneidad y consistencia en el rendimiento de estas posiciones.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Asimetría:</b> La línea de delanteros presenta una distribución con mayor dispersión y asimetría positiva (valores atípicos en la zona alta), lo que describe una mayor variabilidad en el rendimiento individual de esta posición.</li>
        <li><b>Simetría:</b> Las líneas de arqueros, defensas y mediocampistas muestran distribuciones más simétricas y compactas, con una menor dispersión de los datos y una mayor concentración en torno a la mediana.</li>
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
        El análisis de los valores medios muestra que la línea de delanteros presenta el promedio de rendimiento (Ability Score) más alto de la muestra. Le siguen los mediocampistas, luego los defensas y, finalmente, los arqueros, que registran la media más baja. Sin embargo, al observar las líneas de error (que representan la desviación estándar), se aprecia que los delanteros y los mediocampistas poseen una mayor dispersión en sus datos, lo que indica que su rendimiento promedio está acompañado de una mayor variabilidad interna. En contraste, los arqueros y defensas, aunque tienen medias más bajas, presentan una menor longitud en sus líneas de error, describiendo una mayor homogeneidad en sus registros de rendimiento.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Promedio:</b> La línea de delanteros registra la media de rendimiento más alta, seguida por mediocampistas, defensas y arqueros.</li>
        <li><b>Dispersión:</b> Los delanteros y mediocampistas presentan una mayor desviación estándar, lo que describe una mayor heterogeneidad en su rendimiento. Arqueros y defensas muestran una menor dispersión, indicando registros más homogéneos.</li>
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
        El gráfico de anillo muestra la composición de la muestra de jugadores según su línea posicional. Los defensas representan la mayor proporción de la muestra (36.8%), seguidos por los mediocampistas (31%) y los delanteros (26.1%). Los arqueros constituyen el grupo más reducido (6.1%). Esta distribución describe el volumen demográfico de cada demarcación en la base de datos analizada. Al contrastar estos porcentajes con los datos de producción ofensiva del Gráfico 1, se observa que los delanteros, a pesar de representar aproximadamente una cuarta parte de la muestra, concentran más del 54% del aporte ofensivo total, lo que describe un alto impacto relativo por jugador en esa posición.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Composición de la muestra:</b> Los defensas y mediocampistas constituyen la mayor parte de la muestra (67.8% combinado), mientras que los delanteros representan el 26.1% y los arqueros el 6.1%.</li>
        <li><b>Impacto relativo:</b> Los delanteros presentan una producción ofensiva desproporcionada en relación con su volumen demográfico, concentrando más de la mitad del aporte total con apenas una cuarta parte de los jugadores de la muestra.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Análisis Complementario")

tab1, tab2, tab3, tab4 = st.tabs([
    "Perfil Multidimensional",
    "Balance Ofensivo vs. Defensivo",
    "Dispersión Ofensiva vs. Defensiva",
    "Minutos y Rotación por Rol",
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

with tab3:
    st.caption("Dispersión · X = Goles + Asistencias por 90' · Y = Tackles + Intercepciones por 90' · Color = línea posicional · Jugadores con 450+ minutos")
    if "offensive_score" in df.columns and "defensive_score" in df.columns:
        # Con pocos minutos las métricas por 90' se disparan
        df_sc = df[df["minutes_played"] >= 450]
        df_sc = df_sc.sample(min(800, len(df_sc)), random_state=1)
        fig_sc = px.scatter(
            df_sc, x="offensive_score", y="defensive_score",
            color="linea", color_discrete_map=colores_kpi,
            opacity=0.65,
            hover_data=["club", "position", "season"],
            labels={
                "offensive_score": "Goles + Asistencias por 90'",
                "defensive_score": "Tackles + Intercepciones por 90'",
                "linea": "Línea",
            },
        )
        fig_sc.update_layout(height=430)
        fig_sc = apply_theme(fig_sc)
        st.plotly_chart(fig_sc, width="stretch")

with tab4:
    st.caption("Box-plot · Minutos jugados por demarcación específica · Ilustra la regularidad y rotación por rol")
    df_t4 = df[df["linea"].isin(LINEAS_ORDEN)].copy()
    linea_fil = st.selectbox("Filtrar línea:", ["Todas"] + LINEAS_ORDEN, key="t4_linea")
    if linea_fil != "Todas":
        df_t4 = df_t4[df_t4["linea"] == linea_fil]

    fig_t4 = px.box(
        df_t4, x="position", y="minutes_played",
        color="linea", color_discrete_map=colores_kpi,
        points="outliers",
        labels={"position": "Posición", "minutes_played": "Minutos Jugados", "linea": "Línea"},
        category_orders={"linea": LINEAS_ORDEN},
    )
    fig_t4.update_layout(height=430, xaxis_tickangle=-25, showlegend=True)
    fig_t4 = apply_theme(fig_t4)
    st.plotly_chart(fig_t4, width="stretch")

st.divider()

st.subheader("Conclusiones del Análisis")

st.markdown("""
<div class="section-container" style="border-left: 4px solid #00E5FF; padding: 25px 30px; margin-top: 15px; margin-bottom: 25px;">
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        El análisis posicional del ciclo 2022-2026 describe una estructura de rendimiento con una clara especialización funcional. Los delanteros, que representan aproximadamente una cuarta parte de la muestra (26.1%), concentran más del 54% de la producción de goles y asistencias. En contraste, los mediocampistas constituyen el eje híbrido y bidireccional del juego: las comparativas multidimensionales confirman que esta zona combina cuotas significativas de creación ofensiva (asistencias y pases clave) con labores de contención territorial (tackles y presión media).
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        La distribución del rendimiento individual muestra una asimetría clara según la demarcación. Los diagramas de caja evidencian que el rendimiento en la delantera presenta una mayor dispersión y una asimetría positiva, con valores atípicos sobresalientes (jugadores con una producción ofensiva excepcionalmente alta). Por su parte, el rendimiento en defensas y arqueros muestra distribuciones más simétricas y agrupadas alrededor de la mediana, lo que describe una mayor homogeneidad en sus registros.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 0; font-size: 1.02rem;">
        En cuanto a la evolución temporal, la composición del aporte por línea se mantiene estable a lo largo de las cuatro temporadas, sin transferencias significativas de carga entre demarcaciones. Los delanteros conservan la mayor cuota de participación ofensiva, mientras que el mediocampo mantiene su rol de equilibrio. Finalmente, el análisis de minutaje por rol revela una marcada rigidez en arqueros y defensas centrales (con distribuciones compactas en el límite superior y menor rotación), frente a una mayor alternancia y dosificación física en extremos y carrileros, posiciones que presentan una mayor variabilidad en su participación.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Nota Metodológica")

st.markdown("""
<div class="section-container" style="border-left: 3px solid rgba(255, 255, 255, 0.25); padding: 20px 25px; margin-top: 15px;">
    <p style="color: #94A3B8; line-height: 1.7; margin-bottom: 0; font-size: 0.98rem;">
        El análisis posicional se desarrolló a partir de la clasificación de los jugadores en cuatro líneas funcionales (Arqueros, Defensas, Mediocampistas y Delanteros). Las métricas de rendimiento individual se estandarizaron mediante el Ability Score, lo que permitió comparar el desempeño entre demarcaciones en una escala común. Para el análisis de dispersión y consistencia se emplearon medidas de tendencia central (media y mediana) y de dispersión (desviación estándar y rango intercuartílico), representadas mediante diagramas de caja y gráficos de barras con líneas de error. El aporte porcentual por línea se calculó sobre el total de la métrica seleccionada (goles, asistencias) en cada temporada. Todas las visualizaciones y cálculos se realizaron sobre la muestra de 108,639 registros de temporadas, sin aplicar pruebas de hipótesis ni modelos predictivos.
    </p>
</div>
""", unsafe_allow_html=True)