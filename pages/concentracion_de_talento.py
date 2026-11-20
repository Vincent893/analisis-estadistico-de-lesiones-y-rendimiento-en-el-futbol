from database.DB import DB
from models.UI import UI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme

UI.setup_page()
UI.render_sidebar()
cargar_estilos()

conn = DB.get_connection()

def calcular_gini(valores):
    arr = np.sort(np.array(valores, dtype=float))
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * arr) / (n * arr.sum())) - (n + 1) / n

def calcular_hhi(valores):
    total = sum(valores)
    if total == 0:
        return 0.0
    participaciones = [v / total * 100 for v in valores]
    return sum(p ** 2 for p in participaciones)

POSICIONES_ES = {"GOALKEEPER": "Arquero", "DEFENDER": "Defensa", "MIDFIELDER": "Mediocampista", "ATTACKER": "Delantero"}

# Una fila por jugador-temporada, con la división del club como "liga"
SQL_JUGADOR_TEMPORADA = """
SELECT COALESCE(d.division_name, 'Sin división') AS liga,
       c.club_name          AS club,
       s.season_label       AS season,
       p.primary_category   AS position,
       ps.mins              AS minutes_played,
       psa.goals,
       psa.assists,
       ps.ability_score,
       psa.xg_per_90        AS xg_90
FROM player_seasons ps
JOIN players p                 USING (player_id)
JOIN clubs c                   USING (club_id)
LEFT JOIN divisions d          USING (division_id)
JOIN seasons s                 USING (season_id)
JOIN player_stats_attacking psa USING (player_season_id)
"""

@st.cache_data
def cargar_datos(_conn):
    df = _conn.execute(SQL_JUGADOR_TEMPORADA).df()
    df["position"] = df["position"].map(POSICIONES_ES).fillna(df["position"])
    return df

if conn is None:
    st.error("No se pudo conectar a la base de datos. Revisa las variables de entorno.")
    st.stop()

try:
    df_raw = cargar_datos(conn)
except Exception as e:
    st.error(f"Error al consultar los datos del Objetivo 2: {e}")
    st.stop()

umbral_col = "ability_score"
liga_col   = "liga"

df = df_raw.copy()
df["elite"] = df.groupby([liga_col, "season"])[umbral_col].transform(
    lambda x: x >= x.quantile(0.90)
)
df["goles_asistencias"] = df["goals"] + df["assists"]

st.markdown("""
    <div class="hero-header">
        <span class="hero-badge">Objetivo 2 · Temporadas 2022 – 2026</span>
        <div class="hero-title">Concentración de Talento</div>
        <p style="color:#94A3B8; margin:0; font-size:1.05rem; line-height:1.5;">
            Cuantificar la distribución y concentración de jugadores de alto rendimiento dentro de las plantillas de los clubes,
            evaluando su comportamiento ofensivo y consistencia competitiva a lo largo de las temporadas 2022-2026.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Indicadores Clave")

total_clubs = df.groupby([liga_col, "club"]).ngroups
total_ligas = df.loc[df[liga_col] != "Sin división", liga_col].nunique()
pct_elite = df["elite"].mean() * 100
total_jugadores = len(df)

gini_vals = []
hhi_vals = []
for liga, grp in df.groupby(liga_col):
    vals_jugadores = grp["goles_asistencias"].values
    if vals_jugadores.sum() > 0:
        gini_vals.append(calcular_gini(vals_jugadores))
    aporte_club = grp.groupby("club")["goles_asistencias"].sum().values
    if aporte_club.sum() > 0:
        hhi_vals.append(calcular_hhi(aporte_club))

gini_prom = np.mean(gini_vals) if gini_vals else 0
hhi_prom = np.mean(hhi_vals) if hhi_vals else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Clubes Analizados</div>
        <div class="kpi-value">{total_clubs:,}</div>
        <div class="kpi-footer">{total_ligas} ligas</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Jugadores Élite (P90)</div>
        <div class="kpi-value">{pct_elite:.1f}%</div>
        <div class="kpi-footer">sobre {total_jugadores:,} registros</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Gini Promedio / Liga</div>
        <div class="kpi-value">{gini_prom:.3f}</div>
        <div class="kpi-footer">0 = equidad · 1 = máx. concentración</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">HHI Promedio / Liga</div>
        <div class="kpi-value">{hhi_prom:,.0f}</div>
        <div class="kpi-footer">Índice Herfindahl-Hirschman</div>
    </div>""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 1: Distribución de Jugadores de Alto Rendimiento por Liga, Club y Temporada")
st.caption("Con «Todas»: jugadores élite por liga, usando un umbral común (P90 del Ability Score de cada temporada sobre todas las ligas); se muestran las 20 ligas con más élite. Con una liga seleccionada: jugadores élite por club, usando el P90 de esa liga y temporada.")

ligas_disponibles = sorted(df[liga_col].unique())
liga_sel = st.selectbox("Filtrar por liga:", ["Todas"] + ligas_disponibles, key="g1_liga")

if liga_sel == "Todas":
    eje_x, etiqueta_y, modo = liga_col, "Jugadores Élite (P90 global)", "stack"
    df_glob = df[df[umbral_col] >= df.groupby("season")[umbral_col].transform(lambda x: x.quantile(0.90))]
    df_g1_agg = df_glob.groupby([liga_col, "season"]).size().reset_index(name="jugadores_elite")
    orden_x = df_glob.groupby(liga_col).size().nlargest(20).index.tolist()
    df_g1_agg = df_g1_agg[df_g1_agg[liga_col].isin(orden_x)]
else:
    eje_x, etiqueta_y, modo = "club", "Jugadores Élite", "stack"
    df_g1 = df[(df["elite"] == True) & (df[liga_col] == liga_sel)]
    orden_x = df_g1.groupby("club").size().sort_values(ascending=False).index.tolist()
    df_g1_agg = df_g1.groupby(["club", "season"]).size().reset_index(name="jugadores_elite")

fig1 = px.bar(
    df_g1_agg,
    x=eje_x,
    y="jugadores_elite",
    color="season",
    barmode=modo,
    text_auto=True,
    category_orders={eje_x: orden_x},
    labels={"jugadores_elite": etiqueta_y, "club": "Club", liga_col: "Liga", "season": "Temporada"},
    color_discrete_sequence=["#00E5FF", "#3B82F6", "#8B5CF6", "#EC4899"],
)
fig1.update_layout(height=430, xaxis_tickangle=-35)
fig1 = apply_theme(fig1)
st.plotly_chart(fig1, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Al aplicar un umbral común a todas las competiciones (percentil 90 del Ability Score de cada temporada), los 10,866 registros de élite se distribuyen de forma muy desigual entre ligas: solo 114 de las 299 ligas cuentan con al menos un jugador élite. Las cinco ligas con mayor volumen (English Premier Division con 1,024, Spanish First Division con 881, Italian Serie A con 813, Sky Bet Championship con 809 y Bundesliga con 768) reúnen el 39.5 % del total; las diez primeras, el 64.2 %, y las veinte primeras, el 81.9 %.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        La concentración también se observa en términos relativos: en la English Premier Division el 80.6 % de los registros jugador-temporada supera el umbral global, y en la Serie A, la Bundesliga, la Spanish First Division y la Ligue 1 la proporción se sitúa entre el 64 % y el 66 %. Destaca la Sky Bet Championship (segunda división inglesa), que en volumen absoluto supera a la Bundesliga, aunque con una proporción menor (44.8 %) por su mayor número de jugadores registrados.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        En la evolución por temporada, las barras de 2025/26 prácticamente duplican a las de años anteriores en las ligas principales (por ejemplo, la English Premier Division pasa de 182, 216 y 245 élite a 381). Este salto coincide con un umbral P90 más bajo en 2025/26 (570.3 puntos frente a 604–609 en las temporadas previas) y con que es la única temporada no marcada como fabricada en la base de datos, por lo que debe leerse como un efecto del registro y no como un aumento real del talento.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Al seleccionar una liga concreta, el umbral se calcula dentro de esa competición y el gráfico describe el reparto entre sus clubes. En la English Premier Division, por ejemplo, los tres clubes con más registros élite (Newcastle con 26, Crystal Palace con 20 y Wolves y Man UFC con 18) reúnen apenas el 22.5 % de los élite de la liga, lo que describe un reparto interno relativamente amplio.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración entre ligas:</b> El talento de élite se concentra en un grupo reducido de competiciones, principalmente las cinco grandes ligas europeas y la segunda división inglesa, mientras que 185 de las 299 ligas no registran ningún jugador élite.</li>
        <li><b>Concentración entre clubes:</b> A nivel global, 1,130 de los 2,773 clubes (40.8 %) tienen al menos un registro élite y el coeficiente de Gini del número de élite por club es 0.84. Dentro de una misma liga de primer nivel, en cambio, el talento se reparte entre un número mayor de clubes.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 2: Curva de Lorenz (Concentración del Rendimiento Ofensivo)")
st.caption("Curva de Lorenz con diagonal de igualdad perfecta · X = % acumulado de jugadores · Y = % acumulado del rendimiento ofensivo (goles + asistencias)")

liga_lorenz = st.multiselect(
    "Selecciona ligas:", ligas_disponibles,
    default=df[liga_col].value_counts().index[:3].tolist(), key="g2_ligas"
)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1],
    mode="lines", name="Igualdad perfecta",
    line=dict(color="rgba(255,255,255,0.45)", dash="dash", width=1.5),
))

colores_lorenz = ["#00E5FF", "#10B981", "#F59E0B", "#EC4899", "#3B82F6"]
for i, liga in enumerate(liga_lorenz):
    vals = np.sort(df[df[liga_col] == liga]["goles_asistencias"].values)
    if len(vals) == 0 or vals.sum() == 0:
        continue
    vals_cum = np.cumsum(vals) / vals.sum()
    x_lorenz = np.linspace(0, 1, len(vals_cum) + 1)
    y_lorenz = np.insert(vals_cum, 0, 0.0)
    gini_i = calcular_gini(vals)

    fig2.add_trace(go.Scatter(
        x=x_lorenz, y=y_lorenz,
        mode="lines",
        name=f"{liga} (Gini={gini_i:.3f})",
        line=dict(color=colores_lorenz[i % len(colores_lorenz)], width=2.5),
    ))

fig2.update_layout(
    height=430,
    xaxis_title="% acumulado de jugadores",
    yaxis_title="% acumulado del rendimiento ofensivo (goles + asistencias)",
    xaxis=dict(tickformat=".0%", range=[0, 1]),
    yaxis=dict(tickformat=".0%", range=[0, 1]),
)
fig2 = apply_theme(fig2)
st.plotly_chart(fig2, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Las Curvas de Lorenz se alejan de forma pronunciada de la diagonal de igualdad perfecta en todas las ligas. Para el conjunto de la muestra, el coeficiente de Gini de goles + asistencias es 0.618; el promedio de los Gini calculados liga por liga es 0.563, y en las ligas con mayor número de registros los valores oscilan entre 0.578 (English Premier Division) y 0.673 (Brazilian National Lower Division).
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        La curvatura se explica en buena parte por la elevada proporción de registros sin aporte ofensivo: el 26.5 % de los jugadores-temporada no registra goles ni asistencias (entre el 19.5 % y el 35.1 % según la liga). Como resultado, el 50 % de los jugadores con menor aporte genera solo el 7.7 % de la producción ofensiva total, mientras que el 20 % superior concentra el 62.2 % y el 10 % superior, el 40.5 %.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Esta desigualdad es prácticamente constante en el tiempo: el Gini global por temporada se mantiene entre 0.615 y 0.619 a lo largo del ciclo 2022–2026.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> Con coeficientes de Gini cercanos a 0.6, la producción ofensiva está fuertemente centralizada en una minoría de futbolistas: uno de cada cinco jugadores genera más de seis de cada diez goles + asistencias.</li>
        <li><b>Comparación entre ligas:</b> Las diferencias entre ligas son moderadas (Gini entre 0.58 y 0.67 en las ligas de mayor tamaño) y no siguen un patrón claro según el nivel competitivo; la desigualdad en el aporte ofensivo es un rasgo común a todas las competiciones.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 3: Relación entre Minutos Jugados y Rendimiento Ofensivo")
st.caption("Cada punto representa un jugador en una temporada (muestra aleatoria de hasta 800 registros). Las estrellas indican jugadores élite (P90 del Ability Score de su liga y temporada).")

col_g3a, col_g3b = st.columns([2, 1])
with col_g3a:
    temp_sel = st.multiselect(
        "Temporadas:", sorted(df["season"].unique()),
        default=sorted(df["season"].unique()), key="g3_temp"
    )
with col_g3b:
    liga_g3 = st.selectbox("Liga:", ["Todas"] + ligas_disponibles, key="g3_liga")

df_g3 = df.copy()
if temp_sel:
    df_g3 = df_g3[df_g3["season"].isin(temp_sel)]
if liga_g3 != "Todas":
    df_g3 = df_g3[df_g3[liga_col] == liga_g3]

if len(df_g3) > 800:
    df_g3 = df_g3.sample(800, random_state=42)

fig3 = px.scatter(
    df_g3,
    x="minutes_played",
    y="goles_asistencias",
    color="season",
    size="goals",
    size_max=20,
    symbol="elite",
    symbol_map={True: "star", False: "circle"},
    hover_data=["club", "position", "ability_score"],
    labels={
        "minutes_played": "Minutos Jugados",
        "goles_asistencias": "Goles + Asistencias",
        "season": "Temporada",
        "elite": "Jugador Élite",
    },
    opacity=0.75,
    color_discrete_sequence=["#00E5FF", "#3B82F6", "#8B5CF6", "#EC4899"],
)
fig3.update_layout(height=460)
fig3 = apply_theme(fig3)
st.plotly_chart(fig3, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        La nube de puntos describe una relación positiva y moderada entre los minutos jugados y la producción ofensiva (correlación de Spearman de 0.53; Pearson de 0.49). El aporte medio crece con la exposición: 0.85 goles + asistencias con 500 minutos o menos, 3.36 entre 1,001 y 1,500 minutos y 7.09 entre 2,501 y 3,000 minutos. Por encima de los 3,000 minutos el crecimiento se estanca (media de 7.51 y mediana de 5), ya que en ese tramo aumenta el peso de defensas y arqueros, con mucha continuidad pero poco aporte ofensivo (59.3 % de los registros, frente al 48.5 % en el total de la muestra). La densa nube de la zona inferior izquierda corresponde a futbolistas de rotación: el 23 % de los registros no supera los 500 minutos.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Los jugadores élite (estrellas) juegan más y producen más que el resto: su mediana es de 1,978 minutos frente a 1,299, y de 4 goles + asistencias frente a 2. También son más eficientes, con una mediana de 0.26 goles + asistencias por cada 90 minutos frente a 0.15. Sin embargo, la élite se define por el Ability Score, que está muy débilmente asociado a la producción ofensiva (Spearman de 0.10): el 14.3 % de los élite no registra goles ni asistencias, porque la categoría incluye defensas y arqueros, y el 25.7 % disputa menos de 800 minutos.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Se identifican además valores atípicos de alta eficiencia en la zona superior izquierda: 1,523 registros (1.4 % del total) alcanzan 5 o más goles + asistencias con menos de 800 minutos jugados.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Exposición y producción:</b> El volumen de minutos está asociado de forma moderada con el aporte ofensivo, aunque con rendimientos decrecientes a partir de los 3,000 minutos; no es el único factor que lo explica.</li>
        <li><b>Élite y aporte ofensivo:</b> Ser élite según el Ability Score implica más minutos y mayor producción por partido, pero no garantiza aporte ofensivo, ya que el puntaje refleja una habilidad general que incluye funciones defensivas.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 4: Volatilidad del Rendimiento por Posición")
st.caption("El Coeficiente de Variación (CV = desviación estándar / media) mide la dispersión relativa de goles + asistencias entre los jugadores de cada línea posicional, considerando las cuatro temporadas. Un CV más alto indica mayor dispersión.")

# CV = desviación estándar / media de goles + asistencias por línea posicional
df_cv = df.groupby("position")["goles_asistencias"].agg(["std", "mean", "count"]).reset_index()
df_cv["cv"] = df_cv["std"] / df_cv["mean"]
df_cv = df_cv.sort_values("cv", ascending=True)

fig4 = px.bar(
    df_cv,
    x="cv",
    y="position",
    orientation="h",
    text=df_cv["cv"].apply(lambda v: f"{v:.3f} ({v*100:.1f}%)"),
    color="cv",
    labels={"cv": "Coeficiente de Variación (CV)", "position": "Posición / Demarcación"},
)
fig4.update_layout(
    height=420,
    yaxis=dict(autorange="reversed"),
    coloraxis_showscale=False,
    xaxis=dict(tickformat=".0%"),
)
fig4.update_traces(textposition="outside", cliponaxis=False)
fig4 = apply_theme(fig4)
st.plotly_chart(fig4, width="stretch")

st.markdown("<p style='color:#94A3B8; font-weight:600; margin-bottom:8px;'>Tabla Descriptiva de Dispersión Relativa (CV por Posición)</p>", unsafe_allow_html=True)
tabla_cv_resumen = df_cv[["position", "count", "mean", "std", "cv"]].copy()
tabla_cv_resumen.columns = ["Línea", "N", "Media G+A", "Desv. estándar", "Coeficiente de Variación (CV)"]
tabla_cv_resumen[["Media G+A", "Desv. estándar"]] = tabla_cv_resumen[["Media G+A", "Desv. estándar"]].round(3)
tabla_cv_resumen["Coeficiente de Variación (CV)"] = tabla_cv_resumen["Coeficiente de Variación (CV)"].apply(lambda x: f"{x:.3f} ({x*100:.1f}%)")
st.dataframe(tabla_cv_resumen, width="stretch", hide_index=True)

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Entre las líneas de campo, los delanteros presentan la menor dispersión relativa (CV de 0.88), seguidos por los mediocampistas (1.00) y los defensas (1.27). Aunque los delanteros tienen la mayor desviación estándar en términos absolutos (7.24), también tienen la media más alta (8.21 goles + asistencias), y solo el 7.1 % de ellos no registra aporte ofensivo. En los defensas, la media es baja (2.27) y el 31.1 % no registra goles ni asistencias, lo que eleva su dispersión relativa: unos pocos defensas con aporte ofensivo se alejan mucho de una mayoría con aporte nulo o mínimo.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        El CV de los arqueros (29.27) no es interpretable en la práctica: su media es de 0.003 goles + asistencias y el 99.8 % no registra aporte ofensivo, de modo que cualquier caso aislado dispara el cociente.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Al calcular el CV por separado en cada temporada, los valores son casi idénticos (delanteros entre 0.87 y 0.89; mediocampistas entre 0.99 y 1.01; defensas entre 1.26 y 1.27), y la media de cada línea varía menos de un 1 % entre temporadas. La estructura de dispersión por línea es, por tanto, estable a lo largo del ciclo.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Homogeneidad relativa (CV bajo):</b> Los delanteros, cuya función principal es la producción ofensiva, muestran el aporte más homogéneo en relación con su media.</li>
        <li><b>Heterogeneidad relativa (CV alto):</b> En defensas, y sobre todo en arqueros, el aporte ofensivo es ocasional, por lo que su dispersión relativa es mayor. Un CV alto refleja aquí diferencias entre jugadores dentro de la línea, no inestabilidad entre temporadas.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 5: Dependencia del Rendimiento en el Top 20% de la Plantilla")
st.caption("Porcentaje del rendimiento ofensivo del club generado por su 20% más productivo. Tonos oscuros = mayor concentración (dependencia de pocos jugadores); tonos claros = menor concentración (rendimiento más distribuido)")

liga_hm = st.selectbox("Liga para el mapa de calor:", ligas_disponibles, key="g5_liga")

df_hm = df[df[liga_col] == liga_hm].copy()
top_clubes_hm = df_hm.groupby("club")["goles_asistencias"].sum().nlargest(20).index
df_hm = df_hm[df_hm["club"].isin(top_clubes_hm)]
pct_top20_rows = []
for (club_h, season_h), grp in df_hm.groupby(["club", "season"]):
    total_ren = grp["goles_asistencias"].sum()
    if total_ren == 0:
        pct = 0.0
    else:
        umbral_20 = grp["goles_asistencias"].quantile(0.80)
        top20_ren = grp[grp["goles_asistencias"] >= umbral_20]["goles_asistencias"].sum()
        pct = top20_ren / total_ren * 100
    pct_top20_rows.append({"club": club_h, "season": season_h, "pct_top20": round(pct, 1)})

df_hm_agg = pd.DataFrame(pct_top20_rows)
pivot_hm = df_hm_agg.pivot(index="club", columns="season", values="pct_top20")

textos_heatmap = []
for row in pivot_hm.values:
    fila_t = []
    for v in row:
        if pd.isna(v):  
            fila_t.append("")
            continue
        color_texto = "#FFFFFF" if v >= 62.0 else "#082F49"
        fila_t.append(f"<b style='color:{color_texto}; font-size:13px;'>{v:.1f}%</b>")
    textos_heatmap.append(fila_t)

fig5 = go.Figure(go.Heatmap(
    z=pivot_hm.values,
    x=pivot_hm.columns.tolist(),
    y=pivot_hm.index.tolist(),
    colorscale=[
        [0.0,  "#E0F2FE"],
        [0.35, "#7DD3FC"],
        [0.65, "#0284C7"],
        [1.0,  "#082F49"],
    ],
    text=textos_heatmap,
    texttemplate="%{text}",
    hovertemplate="Club: %{y}<br>Temporada: %{x}<br>Top 20%%: %{z:.1f}%%<extra></extra>",
    showscale=True,
    colorbar=dict(
        title=dict(text="% Rendimiento", font=dict(color="#E2E8F0")),
        tickfont=dict(color="#E2E8F0"),
    ),
))
fig5.update_layout(
    height=max(320, len(pivot_hm) * 55 + 80),
    xaxis_title="Temporada",
    yaxis_title="Club",
)
fig5 = apply_theme(fig5)
st.plotly_chart(fig5, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        En el conjunto de las 11,053 combinaciones club-temporada, el 20 % más productivo de cada plantilla genera en promedio el 68.2 % de sus goles + asistencias (mediana del 66.7 %). En el 54.0 % de los casos esa cuota supera el 65 %, y solo en el 10.3 % queda por debajo del 50 %. El promedio es estable entre temporadas (entre el 67.9 % y el 68.7 %).
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Hay diferencias entre ligas: en la English Premier Division la dependencia media es del 57.5 %, frente al 65.2 % de la Spanish First Division y el 65.6 % de la 3. Liga, lo que describe una producción ofensiva algo más repartida en los clubes de la liga inglesa.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Estos valores deben leerse con cautela, porque la base de datos no contiene plantillas completas: la mediana es de 10 jugadores registrados por club y temporada, y el 25.8 % de los casos tiene 5 o menos. Además, en el 35.4 % de los casos los empates en el percentil 80 hacen que el «top 20 %» incluya a más del 30 % de la plantilla. Las celdas con 100 % corresponden sobre todo a plantillas muy pequeñas (mediana de 3 jugadores registrados) o con un único jugador con aporte (61.1 % de esos casos), y las celdas con 0 % a clubes sin goles ni asistencias registrados en esa temporada (2.7 % de los casos).
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Dependencia:</b> En la mayoría de los clubes, la producción ofensiva depende de un grupo reducido de jugadores: más de la mitad de los casos supera el 65 % de concentración en su quintil más productivo.</li>
        <li><b>Distribución:</b> Los clubes con cuotas inferiores al 50 % son minoría (10.3 %) y describen un aporte ofensivo más repartido entre la plantilla.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Conclusiones del Análisis")

st.markdown("""
<div class="section-container" style="border-left: 4px solid #00E5FF; padding: 25px 30px; margin-top: 15px; margin-bottom: 25px;">
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        El análisis de las 108,639 observaciones jugador-temporada, que abarcan 2,773 clubes y 299 ligas, describe una distribución marcadamente desigual del talento de alto rendimiento. Con un umbral común para todas las competiciones, solo 114 ligas tienen jugadores élite, y las cinco con mayor volumen (English Premier Division, Spanish First Division, Italian Serie A, Sky Bet Championship y Bundesliga) reúnen el 39.5 % del total, mientras que las veinte primeras alcanzan el 81.9 %. Entre clubes, menos de la mitad (40.8 %) cuenta con algún jugador élite. Dentro de una misma liga de primer nivel, en cambio, el talento se reparte entre más clubes: en la English Premier Division los tres clubes con más élite reúnen solo el 22.5 %.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        La producción ofensiva también está muy concentrada en pocos jugadores. El coeficiente de Gini de goles + asistencias es 0.618 para el conjunto de la muestra y se mantiene entre 0.615 y 0.619 en todas las temporadas: el 20 % más productivo genera el 62.2 % del aporte ofensivo y el 50 % menos productivo, solo el 7.7 %. Esa misma concentración aparece dentro de cada club, donde el quintil más productivo de la plantilla aporta en promedio el 68.2 % de los goles y asistencias.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        La exposición en minutos se asocia de forma moderada con el aporte ofensivo (Spearman de 0.53), con rendimientos decrecientes por encima de los 3,000 minutos. Los jugadores élite juegan más y producen más por partido que el resto, pero el Ability Score que los define está muy débilmente relacionado con la producción ofensiva (Spearman de 0.10), por lo que la élite incluye perfiles defensivos sin aporte goleador.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 0; font-size: 1.02rem;">
        En cuanto a la consistencia por línea, los delanteros presentan el aporte ofensivo más homogéneo en relación con su media (CV de 0.88), seguidos por mediocampistas (1.00) y defensas (1.27), mientras que en los arqueros el aporte ofensivo es prácticamente nulo. Estas estructuras se mantienen casi idénticas a lo largo de las cuatro temporadas. En conjunto, el ciclo 2022–2026 describe un talento de élite concentrado en pocas ligas y una producción ofensiva dependiente de una minoría de jugadores, con patrones muy estables en el tiempo.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Nota Metodológica")

st.markdown("""
<div class="section-container" style="border-left: 3px solid rgba(255, 255, 255, 0.25); padding: 20px 25px; margin-top: 15px;">
    <p style="color: #94A3B8; line-height: 1.7; margin-bottom: 0; font-size: 0.98rem;">
        El análisis se abordó desde una perspectiva estrictamente descriptiva, sobre 108,639 registros jugador-temporada de las temporadas 2022/23 a 2025/26, tomando como «liga» la división del club. Se definió como jugador élite a quien alcanza o supera el percentil 90 (P90) del Ability Score: dentro de su liga y temporada para los indicadores, el detalle por club y la dispersión, y sobre todas las ligas de cada temporada para la comparación entre ligas del Gráfico 1. El rendimiento ofensivo se midió como la suma de goles y asistencias. Se utilizaron medidas de tendencia central, de dispersión (Coeficiente de Variación) y de concentración (Curvas de Lorenz, coeficiente de Gini e índice HHI), además de mapas de calor. Por legibilidad, el Gráfico 1 muestra las 20 ligas con más élite y el Gráfico 5, los 20 clubes con mayor aporte de la liga seleccionada. En la base de datos, las temporadas 2022/23 a 2024/25 están marcadas como fabricadas; solo 2025/26 corresponde a registros originales.
    </p>
</div>
""", unsafe_allow_html=True)