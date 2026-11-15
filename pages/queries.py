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
            "Query 2", 
            "Query 3",
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
                df = pd.DataFrame(result)
                st.success("Consulta ejecutada con éxito.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {str(e)}")