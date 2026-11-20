import pandas as pd
import streamlit as st
from models.UI import UI
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme
from database.DB import DB

UI.setup_page()
UI.render_sidebar()
cargar_estilos()

st.markdown("""
    <div class="hero-header">
        <span class="hero-badge">Queries </span>
        <div class="hero-title">Cuestionario SQL</div>
        <p style="color:#94A3B8; margin:0; font-size:1.05rem; line-height:1.5;">
            Seis consultas sobre la base de datos original de Kaggle, alojada en Supabase. Cada una responde a una
            pregunta del cuestionario combinando CTEs, funciones de ventana y agregaciones. Selecciona una consulta
            para ver su enunciado, el código SQL y ejecutarla en vivo.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

supabase = DB.connect_supabase()

query_seleccionado = st.selectbox(
        "**Selecciona una consulta:**",
        [
            "Query 1: Rotación de Planteles en las Ligas Principales",
            "Query 2: ¿La Masa Salarial Compra Resultados?", 
            "Query 3: Lesiones Recurrentes",
            "Query 4: Cartera de las Agencias de Representación",
            "Query 5: Peso de los Jugadores Extranjeros en las Ligas Principales",
            "Query 6: Persistencia de la Sobreperformance Goleadora"
        ]
    )
if query_seleccionado == "Query 1: Rotación de Planteles en las Ligas Principales": 
    st.subheader("**Rotación de Planteles en las Ligas Principales**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
    Se quiere medir cuánto cambian los planteles de una temporada a otra y quién juega los minutos.

    Para cada club y temporada (salvo la primera cronológica) calculá la tasa de retención: proporción de los jugadores del plantel 
    de la temporada anterior que siguen en el club. Calculá también qué parte de los minutos del club la jugaron los recién llegados. 
    Considerá solo los clubes con al menos 8 jugadores en la temporada anterior.

    Trabajá con las 15 divisiones más fuertes entre las que tienen al menos 10 clubes que cumplan esa condición en todas las temporadas 
    evaluadas. Para cada temporada y división mostrá la cantidad de clubes, la retención media, la participación media de los recién llegados en los minutos, 
    el club con menor retención (desempate: mayor participación de recién llegados) y su tasa, la variación de la retención media respecto de la temporada anterior 
    de esa división y el puesto de la división dentro de la temporada, de mayor a menor rotación.
    """)
    with st.expander("**Ver Query**"):
        query = """
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_1").select("*").execute()
                    # query_1 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")

if query_seleccionado == "Query 2: ¿La Masa Salarial Compra Resultados?": 
    st.subheader("**¿La Masa Salarial Compra Resultados?**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
    En la temporada más reciente, identificá para cada jugador el contrato vigente con su club al inicio de la temporada. Tomá como fecha 
    de inicio el 1 de julio del primer año de la etiqueta de la temporada, derivándola del texto y no escribiéndola a mano.

    Para cada club con al menos 8 jugadores con contrato vigente calculá la masa salarial semanal y el porcentaje de partidos ganados
    ponderado por minutos jugados. Dentro de cada división, ordená los clubes por masa salarial y por rendimiento, y calculá el coeficiente
    de correlación de rangos de Spearman con la fórmula 1 − 6·Σd² / (n·(n² − 1)).

    Para las divisiones con al menos 10 clubes mostrá la fuerza, la cantidad de clubes, el coeficiente, el club que más puestos gana en 
    rendimiento respecto de su puesto en masa salarial, esa cantidad de puestos y el cociente entre la masa salarial más alta y la más baja 
    de la división. Ordená por coeficiente descendente.
    """)
        
    with st.expander("**Ver Query**"):
        query = """WITH club AS (
    SELECT c.division_id, c.club_name,
           SUM(ct.weekly_wage_eur) AS masa_salarial,
           RANK() OVER (PARTITION BY c.division_id ORDER BY SUM(ct.weekly_wage_eur) DESC) AS r_masa,
           RANK() OVER (PARTITION BY c.division_id ORDER BY SUM(g.game_win_ratio * ps.mins) / SUM(ps.mins) DESC) AS r_rend
    FROM seasons s
    JOIN player_seasons ps ON ps.season_id = s.season_id
    JOIN contracts ct ON ct.player_id = ps.player_id AND ct.club_id = ps.club_id
                     AND CAST(SUBSTR(s.season_label, 1, 4) || '-07-01' AS DATE) BETWEEN ct.start_date AND ct.end_date
    JOIN player_stats_general g ON g.player_season_id = ps.player_season_id
    JOIN clubs c ON c.club_id = ps.club_id
    WHERE s.season_order = 0
    GROUP BY c.club_id, c.division_id, c.club_name
    HAVING COUNT(*) >= 8
),
ordenados AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY division_id ORDER BY r_masa - r_rend DESC, r_rend) AS pos
    FROM club
)
SELECT d.division_name AS division,
       d.division_strength AS fuerza,
       COUNT(*) AS cantidad_clubes,
       ROUND(1 - 6.0 * SUM((o.r_masa - o.r_rend) * (o.r_masa - o.r_rend)) / (COUNT(*) * (COUNT(*) * COUNT(*) - 1)), 4) AS coeficiente_spearman,
       MAX(CASE WHEN o.pos = 1 THEN o.club_name END) AS club_que_mas_puestos_gana,
       MAX(o.r_masa - o.r_rend) AS puestos_ganados,
       ROUND(MAX(o.masa_salarial) / MIN(o.masa_salarial), 2) AS cociente_masa_salarial
FROM ordenados o
JOIN divisions d ON d.division_id = o.division_id
GROUP BY d.division_id, d.division_name, d.division_strength
HAVING COUNT(*) >= 10
ORDER BY coeficiente_spearman DESC
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_2").select("*").execute()
                    # query_2 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")

if query_seleccionado == "Query 3: Lesiones Recurrentes": 
    st.subheader("**Lesiones Recurrentes**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
    Un jugador es recurrente si registra al menos tres lesiones en el período. Clasificá cada lesión como muscular (distensiones, espasmos y fatiga 
    muscular), enfermedad o traumática (el resto).

    Para cada jugador recurrente calculá el intervalo en días entre el fin de una lesión y el inicio de la siguiente, en orden cronológico. Algunas 
    lesiones empiezan antes de que termine la anterior: no las descartes, contalas como solapamientos. Marcá al jugador con patrón de acortamiento si
    cada intervalo es estrictamente menor que el anterior.

    Para cada categoría principal mostrá el total de jugadores de la categoría, la cantidad de recurrentes y la tasa de recurrencia, la proporción de 
    recurrentes con dos o más lesiones musculares, los días de baja promedio, el intervalo medio, la proporción con patrón de acortamiento, la cantidad 
    de recurrentes con al menos un solapamiento y el jugador recurrente con más días de baja acumulados junto con ese total. Ordená por tasa de recurrencia descendente.
        """)
        
    with st.expander("**Ver Query**"):
        query = """ WITH lesion AS (    
        SELECT player_id, start_date,
            end_date - start_date AS dias,
            CASE WHEN injury_type LIKE '%strain' OR injury_type LIKE '%spasm' OR injury_type = 'Muscle fatigue' THEN 'Muscular'
                WHEN injury_type = 'Illness' THEN 'Enfermedad'
                ELSE 'Traumática' END AS clase,
            start_date - LAG(end_date) OVER (PARTITION BY player_id ORDER BY start_date) AS intervalo,
            COUNT(*) OVER (PARTITION BY player_id) AS lesiones
        FROM injuries
    ),
    recurrente AS (
    SELECT *, LAG(intervalo) OVER (PARTITION BY player_id ORDER BY start_date) AS intervalo_anterior
        FROM lesion
        WHERE lesiones >= 3
    ),
    jugador AS (
        SELECT p.player_id, p.name, p.primary_category,
            COUNT(*) AS lesiones,
            SUM(CASE WHEN r.clase = 'Muscular' THEN 1 ELSE 0 END) AS musculares,
            SUM(r.dias) AS dias_baja,
            SUM(r.intervalo) AS suma_intervalos,
            COUNT(r.intervalo) AS intervalos,
            1 - MAX(CASE WHEN r.intervalo >= r.intervalo_anterior THEN 1 ELSE 0 END) AS acorta,
            MAX(CASE WHEN r.intervalo < 0 THEN 1 ELSE 0 END) AS solapa,
            ROW_NUMBER() OVER (PARTITION BY p.primary_category ORDER BY SUM(r.dias) DESC) AS pos
        FROM recurrente r
        JOIN players p ON p.player_id = r.player_id
        GROUP BY p.player_id, p.name, p.primary_category
    )
    SELECT t.primary_category AS categoria,
        t.total AS total_jugadores,
        COUNT(*) AS recurrentes,
        ROUND(COUNT(*) * 1.0 / t.total, 4) AS tasa_recurrencia,
        ROUND(AVG(CASE WHEN j.musculares >= 2 THEN 1.0 ELSE 0 END), 4) AS proporcion_dos_o_mas_musculares,
        ROUND(SUM(j.dias_baja) * 1.0 / SUM(j.lesiones), 1) AS dias_baja_promedio,
        ROUND(SUM(j.suma_intervalos) * 1.0 / SUM(j.intervalos), 1) AS intervalo_medio_dias,
        ROUND(AVG(j.acorta * 1.0), 4) AS proporcion_patron_acortamiento,
        SUM(j.solapa) AS recurrentes_con_solapamiento,
        MAX(CASE WHEN j.pos = 1 THEN j.name END) AS jugador_con_mas_dias_baja,
        MAX(j.dias_baja) AS dias_baja_acumulados
    FROM jugador j
    JOIN (SELECT primary_category, COUNT(*) AS total FROM players GROUP BY primary_category) t
    ON t.primary_category = j.primary_category
    GROUP BY t.primary_category, t.total
    ORDER BY tasa_recurrencia DESC
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_3").select("*").execute()
                    # query_3 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")

if query_seleccionado == "Query 4: Cartera de las Agencias de Representación": 
    st.subheader("**Cartera de las Agencias de Representación**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
Los agentes trabajan para agencias, y una agencia reúne a varios agentes cuyos nombres pueden repetirse en otras agencias. Se quiere un ranking de 
agencias según el valor de su cartera de clientes.

Valorizá a cada jugador representado con el monto total de su contrato más reciente. Para cada agencia calculá la cantidad de clientes, la cantidad 
de agentes, la cantidad de nacionalidades distintas, la proporción de clientes extracomunitarios, el valor total de la cartera en millones, la 
valoración media de sus clientes en la temporada más reciente y un índice de concentración de Herfindahl: la suma de los cuadrados de la participación 
de cada cliente en el valor de la agencia.

Identificá al cliente de mayor valor de cada agencia, la división en la que juega en la temporada más reciente y su peso en la cartera. Mostrá las quince 
agencias de mayor valor con su puesto y la cuota acumulada que representan sobre el valor total de todas las agencias.
    """)
    with st.expander("**Ver Query**"):
        query = """ WITH ultimo_contrato AS (
    SELECT player_id, contract_value_eur AS valor,
           ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY start_date DESC) AS rn
    FROM contracts
    ),
    cliente AS (
        SELECT a.agency_name, p.player_id, p.name, p.nation_id, p.is_eu_national,
           u.valor, g.average_rating, d.division_name,
           u.valor / SUM(u.valor) OVER (PARTITION BY a.agency_name) AS peso,
           ROW_NUMBER() OVER (PARTITION BY a.agency_name ORDER BY u.valor DESC) AS pos
        FROM players p
        JOIN agents a ON a.agent_id = p.agent_id
        JOIN ultimo_contrato u ON u.player_id = p.player_id AND u.rn = 1
        JOIN player_seasons ps ON ps.player_id = p.player_id
        JOIN seasons s ON s.season_id = ps.season_id AND s.season_order = 0
        JOIN player_stats_general g ON g.player_season_id = ps.player_season_id
        JOIN clubs c ON c.club_id = ps.club_id
        LEFT JOIN divisions d ON d.division_id = c.division_id
    )
    SELECT RANK() OVER (ORDER BY SUM(cl.valor) DESC) AS puesto,
       cl.agency_name AS agencia,
       COUNT(*) AS clientes,
       ag.agentes,
       COUNT(DISTINCT cl.nation_id) AS nacionalidades,
       ROUND(AVG(CASE WHEN cl.is_eu_national THEN 0 ELSE 1.0 END), 4) AS proporcion_extracomunitarios,
       ROUND(SUM(cl.valor) / 1000000, 2) AS valor_cartera_millones,
       ROUND(AVG(cl.average_rating), 2) AS valoracion_media,
       ROUND(SUM(cl.peso * cl.peso), 4) AS indice_herfindahl,
       MAX(CASE WHEN cl.pos = 1 THEN cl.name END) AS cliente_mayor_valor,
       MAX(CASE WHEN cl.pos = 1 THEN cl.division_name END) AS division_cliente,
       ROUND(MAX(cl.peso), 4) AS peso_cliente,
       ROUND(SUM(SUM(cl.valor)) OVER (ORDER BY SUM(cl.valor) DESC) / SUM(SUM(cl.valor)) OVER (), 4) AS cuota_acumulada
    FROM cliente cl
    JOIN (SELECT agency_name, COUNT(*) AS agentes FROM agents GROUP BY agency_name) ag
      ON ag.agency_name = cl.agency_name
    GROUP BY cl.agency_name, ag.agentes
    ORDER BY puesto
    LIMIT 15
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_4").select("*").execute()
                    # query_4 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")

if query_seleccionado == "Query 5: Peso de los Jugadores Extranjeros en las Ligas Principales": 
    st.subheader("**Peso de los Jugadores Extranjeros en las Ligas Principales**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
La base no indica a qué país pertenece cada división, así que debe inferirse de los datos: el país de una liga es la nacionalidad que acumula más minutos 
en ella en la temporada más reciente. Un jugador es extranjero en una liga si su nacionalidad difiere del país de la liga.

Trabajá con las 15 divisiones de mayor fuerza, incluidas las que empaten en el último puesto. Para cada una calculá la proporción de minutos jugados por 
extranjeros en la primera y en la última temporada cronológica, la variación entre ambas y el puesto de la división en el ranking de crecimiento.

Para la temporada más reciente agregá la nacionalidad extranjera con más minutos en la liga, su peso dentro de los minutos de extranjeros y qué proporción 
de los minutos de extranjeros corresponde a jugadores extracomunitarios. 
    """)
    with st.expander("**Ver Query**"):
        query = """WITH top_divisiones AS (
    SELECT division_id, division_name
    FROM (SELECT d.*, RANK() OVER (ORDER BY division_strength DESC) AS puesto FROM divisions d) x
    WHERE puesto <= 15
),
minutos AS (
    SELECT t.division_id, t.division_name, s.season_order, n.nation_code,
           MAX(s.season_order) OVER () AS primera,
           SUM(ps.mins) AS mins,
           SUM(CASE WHEN p.is_eu_national THEN 0 ELSE ps.mins END) AS mins_extracom,
           ROW_NUMBER() OVER (PARTITION BY t.division_id, s.season_order ORDER BY SUM(ps.mins) DESC) AS pos
    FROM player_seasons ps
    JOIN seasons s ON s.season_id = ps.season_id
    JOIN clubs c ON c.club_id = ps.club_id
    JOIN top_divisiones t ON t.division_id = c.division_id
    JOIN players p ON p.player_id = ps.player_id
    JOIN nations n ON n.nation_id = p.nation_id
    GROUP BY t.division_id, t.division_name, s.season_order, n.nation_code
),
extranjeros AS (
    SELECT m.*,
           CASE WHEN m.nation_code <> pais.nation_code THEN 1 ELSE 0 END AS es_ext,
           ROW_NUMBER() OVER (PARTITION BY m.division_id, m.season_order
                              ORDER BY CASE WHEN m.nation_code <> pais.nation_code THEN m.mins ELSE 0 END DESC) AS pos_ext
    FROM minutos m
    JOIN minutos pais ON pais.division_id = m.division_id AND pais.season_order = 0 AND pais.pos = 1
),
division AS (
    SELECT division_name,
           MAX(nation_code) FILTER (WHERE season_order = 0 AND es_ext = 0) AS pais,
           SUM(es_ext * mins) FILTER (WHERE season_order = primera) * 1.0
             / SUM(mins) FILTER (WHERE season_order = primera) AS prop_primera,
           SUM(es_ext * mins) FILTER (WHERE season_order = 0) * 1.0
             / SUM(mins) FILTER (WHERE season_order = 0) AS prop_ultima,
           MAX(nation_code) FILTER (WHERE season_order = 0 AND pos_ext = 1 AND es_ext = 1) AS nacion_ext,
           MAX(mins) FILTER (WHERE season_order = 0 AND pos_ext = 1 AND es_ext = 1) * 1.0
             / NULLIF(SUM(es_ext * mins) FILTER (WHERE season_order = 0), 0) AS peso_nacion_ext,
           SUM(es_ext * mins_extracom) FILTER (WHERE season_order = 0) * 1.0
             / NULLIF(SUM(es_ext * mins) FILTER (WHERE season_order = 0), 0) AS prop_extracom
    FROM extranjeros
    GROUP BY division_id, division_name
)
SELECT division_name AS division,
       pais AS pais_inferido,
       ROUND(prop_primera, 4) AS proporcion_extranjeros_primera_temporada,
       ROUND(prop_ultima, 4) AS proporcion_extranjeros_ultima_temporada,
       ROUND(prop_ultima - prop_primera, 4) AS variacion,
       RANK() OVER (ORDER BY prop_ultima - prop_primera DESC) AS puesto_crecimiento,
       nacion_ext AS nacionalidad_extranjera_principal,
       ROUND(peso_nacion_ext, 4) AS peso_nacionalidad_principal,
       ROUND(prop_extracom, 4) AS proporcion_extracomunitarios
FROM division
ORDER BY puesto_crecimiento
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_5").select("*").execute()
                    # query_5 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")

if query_seleccionado == "Query 6: Persistencia de la Sobreperformance Goleadora": 
    st.subheader("**Persistencia de la Sobreperformance Goleadora**")

    with st.expander("**Ver Pregunta**"):
        st.text("""
Marcar más goles que los esperados (xG) puede ser talento o suerte. Si es talento, debería repetirse.

Considerá las temporadas con al menos 900 minutos y 30 remates. Normalizá la sobreperformance (goles menos xG) por 90 minutos y, dentro de cada temporada, 
asigná a cada jugador un quintil (1 = peor, 5 = mejor). Emparejá cada temporada de un jugador con su temporada cronológicamente siguiente cuando ambas 
cumplan el filtro.

Construí la matriz de transición entre el quintil de origen y el de destino, acumulando todos los pares de temporadas. Para cada celda mostrá la cantidad 
de jugadores, la proporción sobre el total de su fila, el lift (proporción de fila dividida por la proporción que el quintil de destino representa sobre 
el total), la sobreperformance media en destino, la proporción de jugadores de la celda que cambió de club y una columna que indique si el jugador persiste,
 mejora o empeora de quintil.
""")
    with st.expander("**Ver Query**"):
        query = """WITH temporada AS (
    SELECT ps.player_id, ps.club_id, s.season_order,
           (a.goals - a.xg) * 90.0 / ps.mins AS sobre_90,
           NTILE(5) OVER (PARTITION BY s.season_order ORDER BY (a.goals - a.xg) * 90.0 / ps.mins) AS quintil
    FROM player_seasons ps
    JOIN seasons s ON s.season_id = ps.season_id
    JOIN player_stats_attacking a ON a.player_season_id = ps.player_season_id
    WHERE ps.mins >= 900 AND a.shots >= 30
)
SELECT o.quintil AS quintil_origen,
       d.quintil AS quintil_destino,
       COUNT(*) AS jugadores,
       ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY o.quintil), 4) AS proporcion_fila,
       ROUND((COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY o.quintil))
             / (SUM(COUNT(*)) OVER (PARTITION BY d.quintil) * 1.0 / SUM(COUNT(*)) OVER ()), 4) AS lift,
       ROUND(AVG(d.sobre_90), 4) AS sobreperformance_media_destino,
       ROUND(AVG(CASE WHEN d.club_id <> o.club_id THEN 1.0 ELSE 0 END), 4) AS proporcion_cambio_club,
       CASE WHEN d.quintil = o.quintil THEN 'Persiste'
            WHEN d.quintil > o.quintil THEN 'Mejora'
            ELSE 'Empeora' END AS evolucion
FROM temporada o
JOIN temporada d ON d.player_id = o.player_id AND d.season_order = o.season_order - 1
GROUP BY o.quintil, d.quintil
ORDER BY o.quintil, d.quintil
        """
        st.code(query, language="sql")

        if st.button("Ejecutar Query"):
            with st.spinner("Ejecutando consulta..."):
                try: 
                    result = supabase.table("query_6").select("*").execute()
                    # query_6 es una vista en la database de Supabase creada con el mismo query mostrado en "query"
                    df = pd.DataFrame(result.data)
                    st.success("Consulta ejecutada con éxito.")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al ejecutar la consulta: {str(e)}")