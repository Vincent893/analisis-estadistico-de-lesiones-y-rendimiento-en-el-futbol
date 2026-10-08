import os
import duckdb
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class DB:
    connection = None

    @staticmethod
    @st.cache_resource
    def _inicializar_conexion():
        
        dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
        
        try:
            if dev_mode:
                conn = duckdb.connect(database='./database/database.duckdb', read_only=False)
                print("Conexión a la base de datos local establecida.")
            else:
                db_url = os.getenv("DB_CONNECTION_URL", "md:")
                conn = duckdb.connect(db_url)
                print("Conexión a MotherDuck establecida.")
            return conn
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    @staticmethod
    def connect():
       
        if DB.connection is None:
            DB.connection = DB._inicializar_conexion()
        
        return DB.connection is not None

    @staticmethod
    def get_connection():
       
        if DB.connection is None:
            DB.connect() 
        
        return DB.connection