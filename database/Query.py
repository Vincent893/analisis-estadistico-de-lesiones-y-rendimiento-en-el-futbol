
BASE = """
WITH temp AS (
    SELECT season_id, season_label, season_order,
           CASE WHEN is_fabricated = 0 THEN 1 ELSE 0 END AS es_real
    FROM seasons
),
les AS (
    SELECT i.injury_id, i.player_id, i.season_id, i.injury_type,
           TRY_CAST(i.start_date AS DATE) AS f_ini,
           TRY_CAST(i.end_date   AS DATE) AS f_fin,
           date_diff('day', TRY_CAST(i.start_date AS DATE), TRY_CAST(i.end_date AS DATE)) AS dias
    FROM injuries i
    JOIN temp t ON t.season_id = i.season_id
),
les_ps AS (
    SELECT player_id, season_id, COUNT(*) AS n_les, SUM(dias) AS dias_perdidos
    FROM les
    GROUP BY player_id, season_id
),
ps_base AS (
    SELECT a.player_id, a.season_id, t.season_label, t.season_order, t.es_real,
           a.age, a.mins, p.primary_category, a.height_cm, a.weight_kg,
           ROUND(a.weight_kg / POWER(a.height_cm / 100.0, 2), 1) AS bmi,
           COALESCE(l.n_les, 0) AS n_les,
           COALESCE(l.dias_perdidos, 0) AS dias_perdidos
    FROM analytics_player_seasons a
    JOIN temp t ON t.season_id = a.season_id
    JOIN players p ON p.player_id = a.player_id
    LEFT JOIN les_ps l ON l.player_id = a.player_id AND l.season_id = a.season_id
    WHERE a.height_cm > 0 AND a.weight_kg > 0
),
ps AS (
    SELECT *,
        CEIL(4 * CUME_DIST() OVER (ORDER BY height_cm))::INT AS q_altura,
        CEIL(4 * CUME_DIST() OVER (ORDER BY weight_kg))::INT AS q_peso,
        CEIL(4 * CUME_DIST() OVER (ORDER BY bmi))::INT       AS q_bmi,
        CASE WHEN mins <= 500  THEN 'a) <=500'
             WHEN mins <= 1000 THEN 'b) 501-1000'
             WHEN mins <= 1500 THEN 'c) 1001-1500'
             WHEN mins <= 2000 THEN 'd) 1501-2000'
             WHEN mins <= 2500 THEN 'e) 2001-2500'
             WHEN mins <= 3000 THEN 'f) 2501-3000'
             ELSE 'g) 3000+' END AS banda_min,
        CASE WHEN age <= 21 THEN '1) <=21'
             WHEN age <= 25 THEN '2) 22-25'
             WHEN age <= 29 THEN '3) 26-29'
             ELSE '4) 30+' END AS banda_edad
    FROM ps_base
)
"""

CUARTIL_SQL = """
SELECT q_{v} AS cuartil,
       MIN({c}) AS min_{u}, MAX({c}) AS max_{u},
       COUNT(*) AS jugadores,
       ROUND(AVG(mins), 0) AS mins_promedio,
       SUM(n_les) AS lesiones,
       ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados,
       ROUND(SUM(n_les) * 1.0 / COUNT(*), 2) AS les_por_jugador,
       ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min,
       ROUND(SUM(dias_perdidos) * 1.0 / NULLIF(SUM(n_les), 0), 1) AS dias_por_lesion,
       ROUND(AVG(dias_perdidos), 1) AS dias_perdidos_por_jugador
FROM ps GROUP BY 1 ORDER BY 1;
"""

QUERIES_MAP = {
    "q1": "SELECT (SELECT COUNT(*) FROM les) AS total_lesiones, (SELECT COUNT(DISTINCT player_id) FROM les) AS jugadores_lesionados, (SELECT COUNT(*) FROM ps) AS jugadores_temporada, (SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) FROM ps) AS pct_con_lesion, (SELECT ROUND(AVG(dias), 1) FROM les) AS dias_promedio, (SELECT MEDIAN(dias) FROM les) AS dias_mediana, (SELECT MAX(dias) FROM les) AS dias_max, (SELECT SUM(dias) FROM les) AS dias_totales, (SELECT COUNT(*) FROM les WHERE f_fin IS NULL) AS sin_fecha_fin;",
    "q2": "SELECT season_label, CASE WHEN MAX(es_real) = 1 THEN 'Real' ELSE 'Sintética' END AS tipo_dato, COUNT(*) AS jugadores, SUM(n_les) AS lesiones, COUNT(*) FILTER (WHERE n_les > 0) AS jugadores_lesionados, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(SUM(n_les) * 1.0 / COUNT(*), 2) AS les_por_jugador, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, SUM(dias_perdidos) AS dias_perdidos, ROUND(SUM(dias_perdidos) * 1.0 / NULLIF(SUM(n_les), 0), 1) AS dias_por_lesion FROM ps GROUP BY season_label, season_order ORDER BY season_order;",
    "q3": "SELECT LEAST(n_les, 4) AS n_lesiones, COUNT(*) AS jugadores_temporada, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct FROM ps GROUP BY 1 ORDER BY 1;",
    "q4": "SELECT t.season_label, CASE WHEN dias <= 7 THEN '1) 0-7 días' WHEN dias <= 14 THEN '2) 8-14' WHEN dias <= 30 THEN '3) 15-30' WHEN dias <= 60 THEN '4) 31-60' WHEN dias <= 90 THEN '5) 61-90' WHEN dias <= 180 THEN '6) 91-180' ELSE '7) 180+' END AS rango_duracion, COUNT(*) AS lesiones FROM les l JOIN temp t ON t.season_id = l.season_id WHERE dias IS NOT NULL AND dias >= 0 GROUP BY ALL ORDER BY t.season_label, rango_duracion;",
    "q5": "SELECT injury_type, COUNT(*) AS lesiones, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct, COUNT(DISTINCT player_id) AS jugadores, ROUND(AVG(dias), 1) AS dias_promedio, MEDIAN(dias) AS dias_mediana, SUM(dias) AS dias_totales FROM les GROUP BY injury_type ORDER BY lesiones DESC LIMIT 20;",
    "q6": "SELECT MONTH(f_ini) AS mes, COUNT(*) AS lesiones, ROUND(AVG(dias), 1) AS dias_promedio FROM les WHERE f_ini IS NOT NULL GROUP BY 1 ORDER BY 1;",
    "q7": CUARTIL_SQL.format(v="altura", c="height_cm", u="cm"),
    "q8": CUARTIL_SQL.format(v="peso", c="weight_kg", u="kg"),
    "q9": CUARTIL_SQL.format(v="bmi", c="bmi", u="imc"),
    "q10": "SELECT banda_min, COUNT(*) AS jugadores, SUM(n_les) AS lesiones, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(SUM(n_les) * 1.0 / COUNT(*), 2) AS les_por_jugador, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, ROUND(SUM(dias_perdidos) * 1.0 / NULLIF(SUM(n_les), 0), 1) AS dias_por_lesion, ROUND(AVG(dias_perdidos), 1) AS dias_perdidos_por_jugador, ROUND(AVG(height_cm), 1) AS altura_prom, ROUND(AVG(weight_kg), 1) AS peso_prom FROM ps GROUP BY 1 ORDER BY 1;",
    "q11": "SELECT q_altura, q_peso, COUNT(*) AS jugadores, SUM(n_les) AS lesiones, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, ROUND(AVG(dias_perdidos), 1) AS dias_perdidos_por_jugador FROM ps GROUP BY 1, 2 ORDER BY 1, 2;",
    "q12": "SELECT q_bmi, banda_min, COUNT(*) AS jugadores, SUM(n_les) AS lesiones, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(AVG(dias_perdidos), 1) AS dias_perdidos_por_jugador FROM ps GROUP BY 1, 2 ORDER BY 1, 2;",
    "q13": "SELECT primary_category, COUNT(*) AS jugadores, ROUND(AVG(height_cm), 1) AS altura_prom, ROUND(AVG(weight_kg), 1) AS peso_prom, ROUND(AVG(mins), 0) AS mins_promedio, SUM(n_les) AS lesiones, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, ROUND(SUM(dias_perdidos) * 1.0 / NULLIF(SUM(n_les), 0), 1) AS dias_por_lesion FROM ps GROUP BY 1 ORDER BY lesiones DESC;",
    "q14": "SELECT banda_edad, COUNT(*) AS jugadores, ROUND(AVG(mins), 0) AS mins_promedio, SUM(n_les) AS lesiones, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, ROUND(SUM(dias_perdidos) * 1.0 / NULLIF(SUM(n_les), 0), 1) AS dias_por_lesion FROM ps GROUP BY 1 ORDER BY 1;",
    "q15": "SELECT CASE WHEN n_les > 0 THEN 'Con lesión' ELSE 'Sin lesión' END AS grupo, COUNT(*) AS jugadores, ROUND(AVG(height_cm), 1) AS altura_prom, ROUND(AVG(weight_kg), 1) AS peso_prom, ROUND(AVG(bmi), 2) AS imc_prom, ROUND(AVG(mins), 0) AS mins_promedio, ROUND(AVG(age), 1) AS edad_prom FROM ps GROUP BY 1;",
    "q17": "SELECT p.name, ps.primary_category, MAX(ps.height_cm) AS altura_cm, MAX(ps.weight_kg) AS peso_kg, SUM(ps.mins) AS minutos, SUM(ps.n_les) AS lesiones, SUM(ps.dias_perdidos) AS dias_perdidos FROM ps JOIN players p ON p.player_id = ps.player_id GROUP BY p.player_id, p.name, ps.primary_category ORDER BY dias_perdidos DESC LIMIT 15;",
    "q18": "SELECT 'altura' AS variable, q_altura AS cuartil, CASE WHEN es_real = 1 THEN 'Real' ELSE 'Sintética' END AS tipo_dato, COUNT(*) AS jugadores, ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1) AS pct_lesionados, ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3) AS les_por_1000min, ROUND(AVG(dias_perdidos), 1) AS dias_perdidos_por_jugador FROM ps GROUP BY ALL UNION ALL SELECT 'peso', q_peso, CASE WHEN es_real = 1 THEN 'Real' ELSE 'Sintética' END, COUNT(*), ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1), ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3), ROUND(AVG(dias_perdidos), 1) FROM ps GROUP BY ALL UNION ALL SELECT 'imc', q_bmi, CASE WHEN es_real = 1 THEN 'Real' ELSE 'Sintética' END, COUNT(*), ROUND(100.0 * COUNT(*) FILTER (WHERE n_les > 0) / COUNT(*), 1), ROUND(SUM(n_les) * 1000.0 / NULLIF(SUM(mins), 0), 3), ROUND(AVG(dias_perdidos), 1) FROM ps GROUP BY ALL ORDER BY 1, 2, 3;",
}

def get_injury_analysis(conn, clave):
    if clave not in QUERIES_MAP:
        raise ValueError(f"La clave de consulta '{clave}' no existe.")
    
    full_query = BASE + "\n" + QUERIES_MAP[clave]
    return conn.execute(full_query).df()

def get_raw_query_sql(clave):
    return QUERIES_MAP.get(clave, "").strip()

def get_base_sql():
    return BASE.strip()


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