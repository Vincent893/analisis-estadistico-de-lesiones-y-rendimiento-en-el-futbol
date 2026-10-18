from database.DB import DB
from models.UI import UI
import streamlit as st
from utils.estilos import cargar_estilos
from utils.graficos import apply_theme

UI.setup_page()
UI.render_sidebar()
cargar_estilos()

conn = DB.get_connection()

if conn:
    df = conn.execute("SELECT * FROM players").df()
    st.dataframe(df)
