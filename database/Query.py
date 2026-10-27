#Esta funcion obtiene el rendimiento de los jugadores desde la tabla de hechos desnormalizada fact_player_season_performance.
def get_player_season_performance(conn):
    
    
    query = """
        SELECT 
            p.player_id,
            p.name,
            p.primary_category,
            p.height_cm,
            p.weight_kg,
            d.season_label,
            f.age,
            f.mins,
            f.total_injuries,
            f.total_days_lost,
            f.average_rating,
            f.goals_per_90,
            f.xg_per_90
        FROM fact_player_season_performance f
        INNER JOIN dim_player p ON f.player_id = p.player_id
        INNER JOIN dim_season d ON f.season_id = d.season_id
    """
    return conn.execute(query).df()