import os
import duckdb
from dotenv import load_dotenv

load_dotenv()

class DB:
    connection = None
    
    @staticmethod
    def connect():
        if DB.connection is None:
            dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"
            
            if dev_mode:
                DB.connection = duckdb.connect(database='./database.duckdb', read_only=False)
                print("Conexión a la base de datos local establecida.")
            else:
                db_url = os.getenv("DB_CONNECTION_URL", "md:")
                DB.connection = duckdb.connect(db_url)
                print("Conexión a MotherDuck establecida.")
                
        return DB.connection

