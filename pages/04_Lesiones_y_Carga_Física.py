from database.DB import DB
from models.UI import UI
import streamlit as st


UI.setup_page()
UI.render_sidebar()

conn = DB.get_connection()

if conn:
    df = conn.execute("SELECT * FROM players").df()
    st.dataframe(df)
