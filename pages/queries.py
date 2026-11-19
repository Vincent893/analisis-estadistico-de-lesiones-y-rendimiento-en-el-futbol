import pandas as pd
import streamlit as st
from models.UI import UI
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme
from database.DB import DB

UI.setup_page()
UI.render_sidebar()
cargar_estilos()


supabase = DB.connect_supabase()

query_seleccionado = st.selectbox(
        "**Selecciona una consulta:**",
        [
            "Query 1: Rotación de Planteles en las Ligas Principales",
            "Query 2: ¿La Masa Salarial Compra Resultados?", 
            "Query 3: Lesiones Recurrentes",
            "Query 4",
            "Query 5",
            "Query 6"
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
        query = """
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