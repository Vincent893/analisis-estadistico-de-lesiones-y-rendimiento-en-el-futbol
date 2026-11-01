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
        
        st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

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
            st.page_link("pages/Marco_Teórico.py", label="Marco Teórico")
            st.page_link("pages/Analisis_de_lesiones.py", label="Análisis de Lesiones")
            st.page_link("pages/Simulador_de_plantilla.py", label="Simulador de Plantilla")
            
            st.divider()