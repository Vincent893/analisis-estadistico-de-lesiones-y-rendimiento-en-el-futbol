from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos

UI.setup_page()
UI.render_sidebar()
cargar_estilos()


P = 'style="color: #E2E8F0; line-height: 1.8; margin-bottom: 16px; font-size: 1.02rem;"'
UL = 'style="color: #E2E8F0; line-height: 1.7; margin-bottom: 0;"'


def caja(titulo, cuerpo, borde="3px solid #00E5FF"):
    st.markdown(f"""
<div class="section-container" style="border-left: {borde}; padding: 22px 28px; margin-top: 15px; margin-bottom: 25px;">
    <h4 style="color: #00E5FF; margin-top: 0; font-size: 1.1rem;">{titulo}</h4>
    {cuerpo.strip()}
</div>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="hero-header">
        <span class="hero-badge">Síntesis · Temporadas 2022 – 2026</span>
        <div class="hero-title">Conclusiones</div>
        <p style="color:#94A3B8; margin:0; font-size:1.05rem; line-height:1.5;">
            Objetivo general: describir y visualizar el comportamiento de las métricas físicas, de lesiones y de
            rendimiento individual y colectivo en el fútbol profesional durante el período 2022-2026, con el fin de
            caracterizar los patrones de rendimiento de los jugadores y la concentración de talento en los clubes.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("Respuesta al Objetivo General")

caja("Conclusión general", f"""
    <p {P}>
        El análisis descriptivo de 108,639 registros jugador-temporada, correspondientes a 27,343 jugadores y 299 ligas
        en las temporadas 2022/23 a 2025/26, permite caracterizar el fútbol profesional del período a partir de tres
        rasgos. Primero, las lesiones se comportan como un fenómeno de frecuencia constante e independiente del perfil
        físico y de la carga de minutos del jugador. Segundo, el talento y la producción ofensiva están fuertemente
        concentrados: en pocas ligas, en pocos clubes y, dentro de cada plantilla, en pocos jugadores. Tercero, el
        rendimiento se explica por el rol posicional más que por el nivel de habilidad: cada línea aporta de una manera
        distinta y estable al funcionamiento colectivo.
    </p>
    <p {P.replace("margin-bottom: 16px", "margin-bottom: 0")}>
        Los tres rasgos comparten una característica: se mantienen prácticamente sin cambios a lo largo de las cuatro
        temporadas. El ciclo 2022-2026 describe, por tanto, una estructura estable más que una evolución, tanto en la
        salud de los jugadores como en la distribución del talento y en el aporte de cada línea.
    </p>
""", borde="4px solid #00E5FF")

st.divider()

st.subheader("Hallazgos por Objetivo Específico")

caja("Objetivo 1 · Lesiones, antropometría y carga de minutos", f"""
    <p {P}>
        Se registraron 26,949 lesiones en 18,552 jugadores distintos. En cada temporada se lesiona aproximadamente uno
        de cada cuatro jugadores (entre el 24.4 % y el 25.0 %), y ningún jugador registra más de una lesión por campaña.
        La duración presenta una marcada asimetría positiva: la media es de 38 días de baja y la mediana de 15, y cerca
        de la mitad de las lesiones (48.8 %) se resuelve en 14 días o menos.
    </p>
    <ul {UL}>
        <li><b>La gravedad pesa más que la frecuencia:</b> la rotura de ligamento cruzado anterior representa el 8.7 % de
            las lesiones, pero con un promedio de 230 días de baja concentra el 52.2 % de todos los días perdidos.</li>
        <li><b>El físico no diferencia el riesgo:</b> el porcentaje de lesionados apenas varía entre cuartiles de altura
            (24.6 % a 25.0 %), de peso (24.7 % a 24.9 %) y de índice de masa corporal (24.4 % a 25.2 %).</li>
        <li><b>La carga de minutos tampoco:</b> entre quienes juegan 500 minutos o menos y quienes superan los 3,000, el
            porcentaje de lesionados se mantiene entre el 24.2 % y el 25.2 %.</li>
        <li><b>La duración es igual de uniforme:</b> los días de baja promedio de los lesionados se sitúan entre 37 y 40
            en todos los grupos de altura, peso, IMC y minutos.</li>
    </ul>
""")

caja("Objetivo 2 · Concentración de talento", f"""
    <p {P}>
        Definiendo como élite a los jugadores que alcanzan el percentil 90 del puntaje de habilidad de cada temporada,
        solo 114 de las 299 ligas cuentan con al menos un jugador élite. Las cinco ligas con mayor volumen (English
        Premier Division, Spanish First Division, Italian Serie A, Sky Bet Championship y Bundesliga) reúnen el 39.5 %
        del total, y las veinte primeras el 81.9 %.
    </p>
    <ul {UL}>
        <li><b>Producción ofensiva desigual:</b> el coeficiente de Gini de goles + asistencias es 0.618 y se mantiene
            entre 0.615 y 0.619 en las cuatro temporadas. El 20 % de jugadores más productivo genera el 62.2 % del aporte
            ofensivo y la mitad menos productiva, solo el 7.7 %; el 26.5 % de los registros no tiene goles ni asistencias.</li>
        <li><b>Dependencia dentro de cada club:</b> el quinto más productivo de cada plantilla aporta en promedio
            alrededor de dos tercios de los goles y asistencias de su club.</li>
        <li><b>Minutos y producción:</b> la exposición se asocia de forma moderada con el aporte ofensivo (correlación de
            Spearman de 0.53).</li>
        <li><b>Habilidad no es producción:</b> el puntaje de habilidad está muy débilmente asociado al aporte ofensivo
            (Spearman de 0.10), porque la élite incluye defensas y arqueros.</li>
    </ul>
""")

caja("Objetivo 3 · Dinámicas posicionales", f"""
    <p {P}>
        Los mediocampistas son la línea más numerosa (45.3 % de los registros), seguidos por los defensas (40.4 %), los
        arqueros (8.1 %) y los delanteros (6.2 %). El peso colectivo de una línea y el rendimiento de sus jugadores
        cuentan historias distintas.
    </p>
    <ul {UL}>
        <li><b>Aporte colectivo:</b> entre los jugadores de campo, el mediocampo produce el 65.2 % de los goles +
            asistencias, la defensa el 22.3 % y la delantera el 12.5 %. La carga defensiva se reparte entre defensas
            (50.4 % de los tackles) y mediocampistas (46.0 %).</li>
        <li><b>Rendimiento por jugador:</b> el orden se invierte. Un delantero promedia 8.2 goles + asistencias por
            temporada, un mediocampista 5.9 y un defensa 2.3; en tackles lidera el defensa (35.5), seguido del
            mediocampista (28.8) y del delantero (16.3).</li>
        <li><b>Consistencia:</b> los delanteros son la línea más homogénea en su aporte ofensivo (coeficiente de
            variación de 0.88), frente a mediocampistas (1.00) y defensas (1.27).</li>
        <li><b>Habilidad similar entre líneas:</b> el puntaje de habilidad promedio va de 385 a 416 según la línea; las
            diferencias de rendimiento responden al rol en el campo y no a un nivel distinto.</li>
        <li><b>Arqueros:</b> evaluados con sus propias métricas, detienen en promedio el 70.5 % de los remates a puerta
            y reciben 1.27 goles por cada 90 minutos.</li>
    </ul>
""")

st.divider()

st.subheader("Alcance y Limitaciones")

caja("Cómo deben leerse estas conclusiones", f"""
    <ul {UL}>
        <li><b>Estudio descriptivo:</b> no se aplicaron pruebas de hipótesis ni modelos predictivos. Los resultados
            describen asociaciones en los datos y no permiten afirmar relaciones de causa y efecto.</li>
        <li><b>Temporadas fabricadas:</b> en la base de datos, las temporadas 2022/23 a 2024/25 están marcadas como
            fabricadas y solo 2025/26 corresponde a registros originales. La estabilidad observada entre temporadas debe
            interpretarse con cautela y no como evidencia de una tendencia real.</li>
        <li><b>Registro de lesiones:</b> los once tipos de lesión aparecen con frecuencias casi idénticas y con un máximo
            de una lesión por jugador y temporada, una uniformidad que limita la generalización de los resultados del
            objetivo 1 a contextos reales.</li>
        <li><b>Plantillas incompletas:</b> la base no contiene plantillas completas (mediana de 10 jugadores registrados
            por club y temporada), lo que afecta a los indicadores calculados dentro de cada club.</li>
        <li><b>Clasificación posicional:</b> solo el centrodelantero se clasifica como delantero; extremos y mediapuntas
            se cuentan como mediocampistas, lo que explica parte del peso del mediocampo.</li>
    </ul>
""", borde="3px solid rgba(255, 255, 255, 0.25)")
