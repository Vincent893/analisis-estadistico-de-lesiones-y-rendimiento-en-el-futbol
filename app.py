from database.DB import DB
from models.UI import UI
from models.Graphics import Graphics
import streamlit as st
import pandas as pd
import plotly.express as px

class Main:

    @staticmethod
    def run():
        
        # setup db connection
        connected = DB.connect()
        
        
        UI.setup_page()
        
        if connected:        
            UI.render_sidebar()
            
            

if __name__ == "__main__":
    Main.run()