
/*
==============================================
Tablas de Dimensiones (Contexto)
==============================================
dim_player: Agrupa la información estática y demográfica del jugador (Nombre, Nacionalidad, Altura, Peso, Categoría posicional principal, etc.).

dim_club: Agrupa los datos del club y su división (Nombre del club, Nombre de la división, Fuerza de la división).

dim_season: Contiene las temporadas (Etiqueta, Orden, etc.)



===============================================
Tablas de Hechos (Métricas y Medidas Numéricas)
===============================================

Hechos de Jugador por Temporada (fact_player_season_performance):
Granularidad: cada registro representa el rendimiento de un jugador en una temporada específica.
Columnas desnormalizadas: Combina en una sola tabla física las métricas de player_seasons, player_stats_general, player_stats_attacking, player_stats_defending y el consolidado de lesiones (total_injuries, total_days_lost). Así evitamos hacer 5 JOINs cada vez que queramos relacionar la altura/peso o los minutos jugados con las lesiones o el rating promedio.

Hechos de Club por Temporada (fact_club_season_summary):
Granularidad: cada registro representa el resumen de rendimiento de un club en una temporada específica.
Columnas desnormalizadas: Consolida el tamaño de la plantilla, el promedio de edad, el puntaje de habilidad promedio (ability_score), la concentración de jugadores de alto rendimiento (conteo y porcentaje de jugadores con rating  7.0), goles totales, xG total, puntos por partido (PPG) y el impacto global de lesiones del club.

Hechos de Línea Posicional por Club y Temporada (fact_club_position_summary):
Granularidad: cada club representa una linea posicional de un club en una temporada específica.
Columnas desnormalizadas: esta tabla agrupa el tamaño de la línea, minutos jugados, rating de la línea, goles, xG, entradas exitosas e intercepciones para evaluar el peso de cada línea en el rendimiento del equipo.

*/
DROP TABLE IF EXISTS fact_player_season_performance CASCADE;
DROP TABLE IF EXISTS fact_club_season_summary CASCADE;
DROP TABLE IF EXISTS fact_club_position_summary CASCADE;
DROP TABLE IF EXISTS dim_player CASCADE;
DROP TABLE IF EXISTS dim_club CASCADE;
DROP TABLE IF EXISTS dim_season CASCADE;


--TABLAS DE DIMENSIONES-- Dimensión Jugador
CREATE TABLE dim_player (
    player_id         INTEGER PRIMARY KEY,
    name              VARCHAR(150) NOT NULL,
    nation_code       VARCHAR(10),
    height_cm         SMALLINT NOT NULL,
    weight_kg         SMALLINT NOT NULL,
    primary_category  VARCHAR(12)
);

-- Dimensión Club
CREATE TABLE dim_club (
    club_id           INTEGER PRIMARY KEY,
    club_name         VARCHAR(150) NOT NULL,
    division_name     VARCHAR(150),
    division_strength NUMERIC(6,2)
);

-- Dimensión Temporada
CREATE TABLE dim_season (
    season_id         INTEGER PRIMARY KEY,
    season_label      VARCHAR(10) NOT NULL,
    season_order      SMALLINT NOT NULL
);


-- TABLAS DE HECHOS

-- Rendimiento y Lesiones por Jugador y Temporada
CREATE TABLE fact_player_season_performance (
    player_season_id              INTEGER PRIMARY KEY,
    player_id                     INTEGER NOT NULL REFERENCES dim_player(player_id),
    season_id                     INTEGER NOT NULL REFERENCES dim_season(season_id),
    age                           SMALLINT NOT NULL,
    mins                          INTEGER NOT NULL,
    starts                        SMALLINT NOT NULL,
    sub_appearances               SMALLINT NOT NULL,
    distance_covered_per_90       NUMERIC(5,2),
    high_intensity_sprints_per_90 NUMERIC(6,3),
    total_injuries                INTEGER NOT NULL DEFAULT 0,
    total_days_lost               INTEGER NOT NULL DEFAULT 0,
    average_rating                NUMERIC(3,2),
    points_per_game               NUMERIC(4,3),
    goals_per_90                  NUMERIC(5,3),
    xg_per_90                     NUMERIC(5,3)
);

-- Resumen de Club por Temporada y Concentración de Talento
CREATE TABLE fact_club_season_summary (
    club_id                        INTEGER NOT NULL REFERENCES dim_club(club_id),
    season_id                      INTEGER NOT NULL REFERENCES dim_season(season_id),
    squad_size                     INTEGER NOT NULL,
    avg_squad_age                  NUMERIC(4,1),
    avg_mins_per_player            NUMERIC(6,1),
    avg_ability_score              NUMERIC(7,2),
    avg_player_rating              NUMERIC(3,2),
    high_performance_players_count INTEGER NOT NULL,
    pct_high_performance_players   NUMERIC(5,2),
    total_goals_scored             SMALLINT,
    total_xg                       NUMERIC(6,2),
    avg_ppg                        NUMERIC(4,3),
    squad_total_injuries           INTEGER NOT NULL,
    squad_total_days_lost          INTEGER NOT NULL,
    PRIMARY KEY (club_id, season_id)
);

-- Rendimiento por Línea Posicional del Club
CREATE TABLE fact_club_position_summary (
    club_id                    INTEGER NOT NULL REFERENCES dim_club(club_id),
    season_id                  INTEGER NOT NULL REFERENCES dim_season(season_id),
    primary_category           VARCHAR(12) NOT NULL,
    players_in_position_count  INTEGER NOT NULL,
    avg_mins_played            NUMERIC(6,1),
    line_avg_rating            NUMERIC(3,2),
    line_total_goals           SMALLINT,
    line_total_xg              NUMERIC(6,2),
    line_total_tackles         SMALLINT,
    line_total_interceptions   SMALLINT,
    club_avg_ppg               NUMERIC(4,3),
    PRIMARY KEY (club_id, season_id, primary_category)
);



--SCRIPTS DE POBLACIÓN 

INSERT INTO 
    dim_player (
            player_id, 
            name, 
            nation_code, 
            height_cm, 
            weight_kg, 
            primary_category
        )
SELECT 
    p.player_id, 
    p.name, 
    n.nation_code, 
    p.height_cm, 
    p.weight_kg, 
    p.primary_category
FROM players p
LEFT JOIN nations n 
ON p.nation_id = n.nation_id;

INSERT INTO dim_club (
            club_id, 
            club_name, 
            division_name, 
            division_strength
        )
SELECT 
    c.club_id, 
    c.club_name, 
    d.division_name, 
    d.division_strength
FROM clubs c
LEFT JOIN divisions d 
ON c.division_id = d.division_id;

INSERT INTO dim_season (
        season_id, 
        season_label, 
        season_order
    )
SELECT 
    season_id, 
    season_label, 
    season_order
FROM seasons;


INSERT INTO fact_player_season_performance
SELECT 
    ps.player_season_id,
    ps.player_id,
    ps.season_id,
    ps.age,
    ps.mins,
    ps.starts,
    ps.sub_appearances,
    psg.distance_covered_per_90,
    psg.high_intensity_sprints_per_90,
    COALESCE(si.total_injuries, 0),
    COALESCE(si.total_days_lost, 0),
    psg.average_rating,
    psg.points_per_game,
    psa.goals_per_90,
    psa.xg_per_90
FROM player_seasons ps
INNER JOIN player_stats_general psg ON ps.player_season_id = psg.player_season_id
INNER JOIN player_stats_attacking psa ON ps.player_season_id = psa.player_season_id
LEFT JOIN (
    SELECT 
        player_id, 
        season_id, 
        COUNT(injury_id) AS total_injuries, 
        SUM(DATEDIFF('day', CAST(start_date AS DATE), CAST(end_date AS DATE))) AS total_days_lost
    FROM injuries
    GROUP BY player_id, season_id
) si ON ps.player_id = si.player_id AND ps.season_id = si.season_id;



INSERT INTO fact_club_season_summary
SELECT 
    c.club_id,
    s.season_id,
    COUNT(ps.player_id),
    ROUND(AVG(ps.age), 1),
    ROUND(AVG(ps.mins), 1),
    ROUND(AVG(ps.ability_score), 2),
    ROUND(AVG(psg.average_rating), 2),
    COUNT(CASE WHEN psg.average_rating >= 7.0 THEN 1 END),
    ROUND(100.0 * COUNT(CASE WHEN psg.average_rating >= 7.0 THEN 1 END) / COUNT(ps.player_id), 2),
    SUM(psa.goals),
    ROUND(SUM(psa.xg), 2),
    ROUND(AVG(psg.points_per_game), 3),
    SUM(COALESCE(inj.total_injuries, 0)),
    SUM(COALESCE(inj.total_days_lost, 0))
FROM player_seasons ps
INNER JOIN clubs c ON ps.club_id = c.club_id
INNER JOIN seasons s ON ps.season_id = s.season_id
INNER JOIN player_stats_general psg ON ps.player_season_id = psg.player_season_id
INNER JOIN player_stats_attacking psa ON ps.player_season_id = psa.player_season_id
LEFT JOIN (
    SELECT 
        player_id, 
        season_id, 
        COUNT(injury_id) AS total_injuries, 
        SUM(DATEDIFF('day', CAST(start_date AS DATE), CAST(end_date AS DATE))) AS total_days_lost
    FROM injuries
    GROUP BY player_id, season_id
) inj ON ps.player_id = inj.player_id AND ps.season_id = inj.season_id
GROUP BY c.club_id, s.season_id;



INSERT INTO fact_club_position_summary
SELECT 
    c.club_id,
    s.season_id,
    p.primary_category,
    COUNT(ps.player_id),
    ROUND(AVG(ps.mins), 1),
    ROUND(AVG(psg.average_rating), 2),
    SUM(psa.goals),
    ROUND(SUM(psa.xg), 2),
    SUM(psd.tackles_completed),
    SUM(psd.interceptions),
    MAX(psg.points_per_game)
FROM player_seasons ps
INNER JOIN players p ON ps.player_id = p.player_id
INNER JOIN clubs c ON ps.club_id = c.club_id
INNER JOIN seasons s ON ps.season_id = s.season_id
INNER JOIN player_stats_general psg ON ps.player_season_id = psg.player_season_id
LEFT JOIN player_stats_attacking psa ON ps.player_season_id = psa.player_season_id
LEFT JOIN player_stats_defending psd ON ps.player_season_id = psd.player_season_id
GROUP BY c.club_id, s.season_id, p.primary_category;