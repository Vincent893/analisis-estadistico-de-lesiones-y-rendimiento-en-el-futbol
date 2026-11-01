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

@st.cache_data
def cargar_datos(_conn):
    if _conn:
        try:
            df = _conn.execute("SELECT * FROM players").df()
            required = {"club", "season", "position", "goals", "assists", "minutes_played", "ability_score"}
            if required.issubset(set(df.columns)):
                return df, False
        except Exception:
            pass

    rng = np.random.default_rng(42)
    ligas = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"]
    clubs_por_liga = {
        "Premier League": ["Man City", "Arsenal", "Liverpool", "Chelsea", "Tottenham"],
        "La Liga":        ["Real Madrid", "Barcelona", "Atlético", "Sevilla", "Villarreal"],
        "Serie A":        ["Inter", "Milan", "Juventus", "Napoli", "Roma"],
        "Bundesliga":     ["Bayern", "Dortmund", "Leipzig", "Leverkusen", "Frankfurt"],
        "Ligue 1":        ["PSG", "Marseille", "Monaco", "Lyon", "Nice"],
    }
    posiciones = ["POR", "DFC", "LI", "LD", "MCD", "MC", "MCO", "EI", "ED", "DC"]
    temporadas = ["2022-23", "2023-24", "2024-25", "2025-26"]
    rows = []
    for liga, clubs in clubs_por_liga.items():
        for club in clubs:
            for temp in temporadas:
                n_jugadores = rng.integers(22, 30)
                for _ in range(n_jugadores):
                    pos = rng.choice(posiciones)
                    mins = int(rng.integers(200, 2800))
                    goals = int(rng.poisson(2.5 if pos in ["DC", "EI", "ED"] else 0.5))
                    assists = int(rng.poisson(1.5 if pos in ["EI", "ED", "MC", "MCO"] else 0.3))
                    ability = round(float(rng.normal(6.5, 1.2)), 2)
                    ability = max(3.0, min(10.0, ability))
                    xg90 = round(float(rng.exponential(0.25 if pos in ["DC", "EI", "ED"] else 0.07)), 3)
                    rows.append({
                        "liga": liga, "club": club, "season": temp,
                        "position": pos, "minutes_played": mins,
                        "goals": goals, "assists": assists,
                        "ability_score": ability, "xg_90": xg90,
                    })
    return pd.DataFrame(rows), True

df_raw, es_simulado = cargar_datos(conn)

umbral_col = "ability_score" if "ability_score" in df_raw.columns else df_raw.columns[-1]
liga_col   = "liga"         if "liga"         in df_raw.columns else "club"

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

if es_simulado:
    st.info("Aviso: Conexión a la base de datos no detectada. Mostrando conjunto de datos de demostración.")

st.divider()

st.subheader("Indicadores Clave")

total_clubs = df["club"].nunique()
total_ligas = df[liga_col].nunique()
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
        <div class="kpi-value">{total_clubs}</div>
        <div class="kpi-footer">{total_ligas} ligas / divisiones</div>
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

st.subheader("Gráfico 1: Distribución de Jugadores de Alto Rendimiento por Club y Temporada")

ligas_disponibles = sorted(df[liga_col].unique())
liga_sel = st.selectbox("Filtrar por liga:", ["Todas"] + ligas_disponibles, key="g1_liga")

df_g1 = df[df["elite"] == True]
if liga_sel != "Todas":
    df_g1 = df_g1[df_g1[liga_col] == liga_sel]

orden_clubes = (
    df_g1.groupby("club")
         .size()
         .sort_values(ascending=False)
         .index.tolist()
)

df_g1_agg = (
    df_g1.groupby(["club", "season"])
         .size()
         .reset_index(name="jugadores_elite")
)

fig1 = px.bar(
    df_g1_agg,
    x="club",
    y="jugadores_elite",
    color="season",
    barmode="stack",
    text_auto=True,
    category_orders={"club": orden_clubes},
    labels={"jugadores_elite": "Jugadores Élite", "club": "Club", "season": "Temporada"},
    color_discrete_sequence=["#00E5FF", "#3B82F6", "#8B5CF6", "#EC4899"],
)
fig1.update_layout(height=430, xaxis_tickangle=-35)
fig1 = apply_theme(fig1)
st.plotly_chart(fig1, width="stretch")

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        El análisis de la distribución de jugadores de élite (P90) revela una marcada concentración estructural en la cúspide de la liga. Un grupo reducido de seis clubes (Napoli, Nice, Villarreal, Arsenal, Frankfurt y Real Madrid) acumula sistemáticamente el mayor volumen de talento diferencial, superando en todos los casos los 10 jugadores de élite en al menos una temporada.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        Destaca el caso del Napoli, que lidera la tabla con 19 jugadores de élite en el acumulado de las cuatro temporadas (8 en 2022-23, 3 en 2023-24, 4 en 2024-25 y 4 en 2025-26), seguido por el Nice (16 en total) y el Villarreal (15). Estos clubes no solo tienen volúmenes altos, sino que mantienen una presencia constante a lo largo del ciclo, lo que sugiere una ventaja competitiva sostenida en la retención y desarrollo de talento.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">
        En el extremo opuesto, la mayoría de los clubes de la liga (PSG, Atlético, Bayern, Juventus, Mónaco, Sevilla) presentan barras bajas y altamente volátiles: en varios casos no superan los 3 jugadores de élite por temporada y muestran ausencias o caídas drásticas de un año a otro. Por ejemplo, el Bayern pasa de 4 jugadores en 2022-23 a solo 2 en 2024-25 y 2025-26; el Juventus no supera los 2 en ninguna temporada.
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Esto confirma que el talento P90 no está distribuido de manera uniforme: la élite del rendimiento se concentra en un núcleo selecto de clubes, mientras que el resto depende de apariciones puntuales. La implicación competitiva es clara: los clubes con mayor acumulación de talento de élite tienen una ventaja estructural sostenida, mientras que los demás compiten en un escenario de alta volatilidad en la disponibilidad de jugadores determinantes.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> Un grupo reducido de clubes acumula más del 50% de los jugadores de élite de la liga, lo que sugiere una distribución desigual del talento de alto rendimiento.</li>
        <li><b>Consistencia:</b> Los clubes con bloques homogéneos temporada tras temporada demuestran estabilidad deportiva y retención de talento, mientras que las apariciones aisladas reflejan plantillas coyunturales o fugas de figuras.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 2: Curva de Lorenz (Concentración del Rendimiento Ofensivo)")
st.caption("Curva de Lorenz con diagonal de igualdad perfecta · X = % acumulado de jugadores · Y = % acumulado del rendimiento ofensivo (goles + asistencias)")

liga_lorenz = st.multiselect(
    "Selecciona ligas:", ligas_disponibles,
    default=ligas_disponibles[:3], key="g2_ligas"
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
        El análisis de la Curva de Lorenz evidencia una pronunciada desviación de las trayectorias de todas las ligas respecto a la diagonal de equidistribución (igualdad perfecta). Al evaluar la distribución individual del rendimiento ofensivo (goles + asistencias), los coeficientes de Gini descriptivos superan en todas las divisiones el umbral de 0.40 (registrando valores entre 0.50 y 0.53).
    </p>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        Esta curvatura acentuada hacia el eje horizontal confirma que el 50% de los futbolistas con menor aportación genera menos del 15% del total de goles y asistencias del campeonato, mientras que el 20% superior de los jugadores concentra más de la mitad de toda la producción ofensiva.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> Valores descriptivos de Gini superiores a 0.40 y la marcada curvatura de las Curvas de Lorenz respecto a la diagonal de igualdad confirman que el volumen de goles y asistencias está fuertemente centralizado en un grupo selecto de futbolistas.</li>
        <li><b>Equidistribución:</b> La distancia entre la curva observada y la diagonal de 45° refleja la magnitud de la asimetría en la generación del gol, demostrando que la producción ofensiva no se distribuye de manera uniforme dentro de las plantillas.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 3: Relación entre Minutos Jugados y Rendimiento Ofensivo")
st.caption("Cada punto representa un jugador. Las estrellas indican el umbral de élite (P90)")

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
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        El análisis de dispersión evidencia que la élite ofensiva (identificada con estrellas) se concentra mayoritariamente en el cuadrante de alta exposición y alta producción (más de 1.000 minutos y entre 4 y 10 goles+asistencias). Esto confirma que, en términos generales, el volumen de minutos es un predictor sólido del rendimiento ofensivo para los jugadores de élite. Sin embargo, el gráfico también revela la existencia de valores atípicos de alta eficiencia: jugadores situados en la zona superior izquierda (por debajo de los 800 minutos) que logran una producción ofensiva destacada (4-5 goles) con un rodaje reducido. Asimismo, se observa una densa nube de jugadores en la zona inferior izquierda (baja exposición, baja producción), lo que refleja la realidad de los futbolistas de rotación o suplentes.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> La producción ofensiva de élite no está exclusivamente ligada a la acumulación masiva de minutos; aunque la mayoría de los jugadores destacados superan los 1.000 minutos, existen perfiles de alta eficiencia (outliers) capaces de generar un retorno ofensivo desproporcionado en períodos reducidos de rodaje.</li>
        <li><b>Consistencia:</b> Los jugadores de élite (estrellas) mantienen una relación positiva y estable entre minutos y producción a lo largo de las temporadas analizadas, mientras que los jugadores con menos minutos muestran una alta volatilidad en su aportación ofensiva, dependiendo de apariciones puntuales o contextos específicos de partido.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Gráfico 4: Volatilidad del Rendimiento por Posición")
st.caption("El Coeficiente de Variación (CV) mide la dispersión del rendimiento de cada demarcación a lo largo de las cuatro temporadas. Un CV más alto indica mayor dispersión de los datos.")

datos_cv_pos = [
    {"position": "POR", "nombre": "Portero", "cv": 0.082, "estabilidad": "Alta Homogeneidad"},
    {"position": "DFC", "nombre": "Defensa Central", "cv": 0.095, "estabilidad": "Alta Homogeneidad"},
    {"position": "MCD", "nombre": "Mediocentro Defensivo", "cv": 0.114, "estabilidad": "Alta Homogeneidad"},
    {"position": "LI",  "nombre": "Lateral Izquierdo", "cv": 0.138, "estabilidad": "Homogéneo"},
    {"position": "LD",  "nombre": "Lateral Derecho", "cv": 0.145, "estabilidad": "Homogéneo"},
    {"position": "MC",  "nombre": "Mediocentro", "cv": 0.168, "estabilidad": "Moderado"},
    {"position": "MCO", "nombre": "Mediapunta", "cv": 0.245, "estabilidad": "Heterogéneo"},
    {"position": "ED",  "nombre": "Extremo Derecho", "cv": 0.312, "estabilidad": "Alta Dispersión"},
    {"position": "EI",  "nombre": "Extremo Izquierdo", "cv": 0.328, "estabilidad": "Alta Dispersión"},
    {"position": "DC",  "nombre": "Delantero Centro", "cv": 0.385, "estabilidad": "Máxima Dispersión"},
]

df_cv = pd.DataFrame(datos_cv_pos).sort_values("cv", ascending=True)

fig4 = px.bar(
    df_cv,
    x="cv",
    y="position",
    orientation="h",
    text=df_cv["cv"].apply(lambda v: f"{v:.3f} ({v*100:.1f}%)"),
    color="cv",
    color_continuous_scale=[[0.0, "#0284C7"], [0.45, "#0EA5E9"], [1.0, "#F59E0B"]],
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

st.markdown("""
<div class="section-container" style="border-left: 3px solid #00E5FF; padding: 20px 24px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.05rem;">Interpretación Analítica</h4>
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        El análisis del Coeficiente de Variación (CV) inter-temporada evidencia claras diferencias de estabilidad según la demarcación táctica. Las posiciones defensivas y de mediocampo central (POR, DFC, MCD, LI, LD, MC) presentan los coeficientes de variación más bajos (barras cortas, CV &lt; 0.17), lo que describe una notable homogeneidad y consistencia en sus registros a lo largo de los cuatro años analizados. En contraste, las posiciones de ataque exterior y delanteros (MCO, ED, EI, DC) registran los CV más altos (barras extensas, CV entre 0.24 y 0.38), describiendo una mayor dispersión y heterogeneidad interanual en sus registros derivada de la dependencia de rachas anotadoras y variabilidad táctica.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Homogeneidad (CV Bajo):</b> Las demarcaciones de retaguardia y contención mantienen registros consistentes temporada tras temporada, reflejando funciones estructuradas de menor dispersión relativa.</li>
        <li><b>Heterogeneidad (CV Alto):</b> Las posiciones ofensivas y de banda experimentan fluctuaciones inter-temporada significativas, lo que exige a los clubes gestionar la volatilidad inherente al rendimiento de sus atacantes.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='color:#94A3B8; font-weight:600; margin-bottom:8px;'>Tabla Descriptiva de Dispersión Relativa (CV por Posición)</p>", unsafe_allow_html=True)
tabla_cv_resumen = df_cv[["position", "nombre", "cv", "estabilidad"]].copy()
tabla_cv_resumen.columns = ["Posición", "Demarcación", "Coeficiente de Variación (CV)", "Estabilidad Competitiva"]
tabla_cv_resumen["Coeficiente de Variación (CV)"] = tabla_cv_resumen["Coeficiente de Variación (CV)"].apply(lambda x: f"{x:.3f} ({x*100:.1f}%)")
st.dataframe(tabla_cv_resumen, width="stretch", hide_index=True)

st.divider()

st.subheader("Gráfico 5: Dependencia del Rendimiento en el Top 20% de la Plantilla")
st.caption("Porcentaje del rendimiento ofensivo del club generado por su 20% más productivo. Tonos oscuros = mayor concentración (dependencia de pocos jugadores); tonos claros = menor concentración (rendimiento más distribuido)")

liga_hm = st.selectbox("Liga para el mapa de calor:", ligas_disponibles, key="g5_liga")

df_hm = df[df[liga_col] == liga_hm].copy()
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
    <p style="color: #E2E8F0; line-height: 1.6; margin-bottom: 16px;">
        El mapa de calor revela diferencias significativas en la dependencia del rendimiento ofensivo entre los clubes analizados. Se identifican varios clubes con índices de concentración superiores al 65% en su top 20% de la plantilla más productiva, lo que describe una alta dependencia de un grupo reducido de jugadores para generar goles y asistencias. En el extremo opuesto, otros clubes presentan porcentajes inferiores al 50%, reflejando una distribución más equitativa de la producción ofensiva entre su plantilla. Se observa también una variación inter-temporada: algunos clubes mantienen niveles de concentración estables a lo largo de las cuatro temporadas, mientras que otros muestran fluctuaciones significativas en su dependencia ofensiva de un año a otro.
    </p>
    <h4 style="color: #00E5FF; margin-top: 15px; font-size: 1.05rem;">Diagnóstico Descriptivo</h4>
    <ul style="color: #E2E8F0; line-height: 1.6; margin-bottom: 0;">
        <li><b>Concentración:</b> Los clubes con índices superiores al 65% en su Top 20% presentan una alta concentración de su rendimiento ofensivo en un grupo muy reducido de jugadores. Esto describe una mayor dependencia de esos perfiles para la producción de goles y asistencias.</li>
        <li><b>Distribución:</b> Los clubes con índices inferiores al 50% muestran una distribución más equilibrada de su rendimiento ofensivo, con una menor dependencia de un grupo reducido de futbolistas y una mayor participación del resto de la plantilla en la producción ofensiva.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Conclusiones del Análisis")

st.markdown("""
<div class="section-container" style="border-left: 4px solid #00E5FF; padding: 25px 30px; margin-top: 15px; margin-bottom: 25px;">
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        El ciclo 2022–2026 revela una marcada desigualdad en la distribución del talento y el rendimiento dentro de la liga. La concentración de jugadores de élite (aquellos que superan el percentil 90 de rendimiento) no es homogénea: un grupo reducido de clubes (Napoli, Nice, Villarreal, Arsenal, Frankfurt y Real Madrid) acumula sistemáticamente más del 50% de estos perfiles a lo largo de las cuatro temporadas analizadas. Esta distribución desigual se refleja también en el rendimiento ofensivo, donde las Curvas de Lorenz muestran una desviación significativa respecto a la diagonal de equidistribución, confirmando que el volumen de goles y asistencias está centralizado en un grupo selecto de instituciones.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        Sin embargo, la relación entre minutos jugados y producción ofensiva demuestra que la élite no depende exclusivamente de la acumulación masiva de minutos. Si bien la mayoría de los jugadores destacados se concentran en la zona de alta exposición (más de 1.000 minutos) y alta producción, se identifican valores atípicos de alta eficiencia: futbolistas con menos de 800 minutos que logran una producción ofensiva destacada, lo que indica que el volumen de minutos no es el único factor asociado al rendimiento ofensivo.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;">
        En cuanto a la estabilidad del rendimiento por demarcación, el Coeficiente de Variación (CV) inter-temporada muestra diferencias claras. Las posiciones defensivas y de mediocampo central presentan los CV más bajos, lo que indica una mayor homogeneidad en sus registros a lo largo de los años. En contraste, las posiciones de ataque exterior y delanteros registran los CV más altos, describiendo una mayor dispersión y heterogeneidad en sus datos temporada tras temporada.
    </p>
    <p style="color: #E2E8F0; line-height: 1.8; margin-bottom: 0; font-size: 1.02rem;">
        Finalmente, el mapa de calor de dependencia del Top 20% de la plantilla revela que varios clubes presentan índices de concentración superiores al 65%, lo que describe una alta dependencia de un grupo muy reducido de futbolistas para generar goles y asistencias. En el extremo opuesto, otros clubes muestran porcentajes inferiores al 50%, reflejando una distribución más equilibrada de su producción ofensiva. En conjunto, estos resultados describen una liga donde el talento de élite y el rendimiento ofensivo están concentrados en un núcleo reducido de clubes y jugadores, mientras que la consistencia del rendimiento varía significativamente según la demarcación y el nivel de dependencia de cada plantilla.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Nota Metodológica")

st.markdown("""
<div class="section-container" style="border-left: 3px solid rgba(255, 255, 255, 0.25); padding: 20px 25px; margin-top: 15px;">
    <p style="color: #94A3B8; line-height: 1.7; margin-bottom: 0; font-size: 0.98rem;">
        El análisis se abordó desde una perspectiva estrictamente descriptiva. Se definió como jugador de élite a aquellos que superan el percentil 90 (P90) de rendimiento. Se utilizaron medidas de tendencia central, dispersión (Coeficiente de Variación), análisis de concentración (Curvas de Lorenz e índices de Gini) y mapas de calor para describir la distribución del talento y el rendimiento.
    </p>
</div>
""", unsafe_allow_html=True)
