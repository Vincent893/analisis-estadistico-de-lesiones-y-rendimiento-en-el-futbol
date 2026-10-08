import streamlit as st


class UI:

    @staticmethod
    def setup_page():
        st.set_page_config(
            page_title="Influencia de Jugadores y Rendimiento de Clubes - UCV",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(
            """
            <style>
                .block-container { padding-top: 1rem; }
                [data-testid="stMetricValue"] { font-size: 1.8rem; color: #1f77b4; }
            </style>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_sidebar():
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] {
                    display: none;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.sidebar:
            
            st.title("Navegación")
            st.divider()

            
            st.page_link("app.py", label="Inicio")
            st.page_link("pages/01_Lesiones_y_Carga_Física.py", label="Lesiones y Carga Física")
            st.page_link("pages/02_Concentración_de_Talento.py", label="Concentración de Talento")
            st.page_link("pages/03_Análisis_Posicional.py", label="Análisis Posicional")
            
            st.divider()