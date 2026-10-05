import duckdb


class DB:
    
    connection = None
    
    @staticmethod
    def connect():
        
        if DB.connection is None:
            DB.connection = duckdb.connect(database='./database.duckdb', read_only=False)
            print("Conexión a la base de datos establecida.")
        return DB.connection
    
DB.connect()