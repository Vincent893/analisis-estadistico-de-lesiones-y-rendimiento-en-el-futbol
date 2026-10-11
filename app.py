from database.DB import DB
from models.UI import UI
from models.Graphics import Graphics
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.estilos import cargar_estilos

class Main:

    @staticmethod
    def run():
        
        # setup db connection
        connected = DB.connect()
        
        supabase = DB.connect_supabase()

        UI.setup_page()
        cargar_estilos()

        st.markdown("""
        <div class="hero-header">
            <span class="hero-badge">Temporadas 2022 - 2026</span>
            <div class="hero-title">Analisis Estadistico de Lesiones y Rendimiento Individual y Colectivo en Clubes de Futbol Profesional</div>
            <p style="color: #94A3B8; margin: 0;">Investigación sobre el impacto en clubes de fútbol profesional</p>
         </div>
        """, unsafe_allow_html=True)

        if connected or supabase:        
            UI.render_sidebar()
            
            

if __name__ == "__main__":
    Main.run()