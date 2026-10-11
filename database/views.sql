/*
Nuestra base de datos ya se encuentra en una tercera forma normal, no obstante, para optimizar el rendimiento de las consultas, se decidió desnormalizar la base de datos. A continuación se presentan las instrucciones SQL para crear las tablas desnormalizadas y sus relaciones.

*/ 


/*
===============================
        INICIO VISTA 
    analytics_player_seasons
===============================
Esta primera vista nos permite tener en una misma tabla datos como caracterisitcas fisicas, que tanto jugo en la temporada y como le fue (goles, calificacion promedio, etc) para poder establecer relaciones, si las hay, entre sus lesiones y las variables anteriormente nombradas.


*/

/*
sqlite no soporta la clausula CREATE OR REPLACE, asi que con el DROP VIEW IF EXISTS "nos cubrimos las espaldas" y nos aseguramos de que la vista se cree sin problemas. 
*/
DROP VIEW IF EXISTS analytics_player_seasons;

CREATE VIEW analytics_player_seasons AS
SELECT 

    /*
        ==================================================
        Estas si son las columnas que se veran en la vista
        ==================================================
    */
    -- Identificadores
    ps.player_season_id,
    p.player_id,
    ps.season_id,
    
     -- datos relacionados a las caracteristicas fisicas del jugador
    p.height_cm, 
    p.weight_kg, 
    ps.age, 
    
    
    -- variables relacionadas a que tanto jugo en la temporada
    ps.mins, 
    ps.starts, 
    ps.sub_appearances, 
    psg.distance_covered_per_90, 
    psg.high_intensity_sprints_per_90,

    -- Métricas de lesiones
    
    COALESCE(si.total_injuries, 0) AS total_injuries, -- El COALESCE es para que si un jugador no tuvo lesiones esa temporada el valor NULL aparezca como 0 porque tuvo 0 lesiones
    COALESCE(si.total_days_lost, 0) AS total_days_lost,

    -- Métricas del rendimiento que tuvo ese jugador en la temporada
    psg.average_rating, 
    psg.points_per_game, 
    psa.goals_per_90, 
    psa.xg_per_90

FROM players p 
INNER JOIN player_seasons ps 
    ON p.player_id = ps.player_id
INNER JOIN player_stats_general psg 
    ON ps.player_season_id = psg.player_season_id
INNER JOIN player_stats_attacking psa 
    ON ps.player_season_id = psa.player_season_id


-- El uso de LEFT JOIN garantiza que se conserven todos los registros de jugadores, independientemente de si sufrieron o no alguna lesión en el año.


LEFT JOIN (
    /*
    un jugador puede tener mas de una lesion en una temporada, por lo que se hace un resumen de las lesiones para cada jugador y temporada en una tabla temporal.
    */
    SELECT 
        player_id,
        season_id,
        COUNT(injury_id) AS total_injuries,
        SUM(DATEDIFF('day', CAST(start_date AS DATE), CAST(end_date AS DATE))) AS total_days_lost
    FROM injuries
    GROUP BY player_id, season_id
) si 
    ON ps.player_id = si.player_id 
   AND ps.season_id = si.season_id;


/*
===============================
            FIN VISTA 
    analytics_player_seasons
===============================

*/


/*
===============================
        INICIO VISTA 
    analytics_club_seasons
===============================

*/

/*
El objetivo de esta vista es poder visualizar informacion que pueda dar una idea sobre la concentracion de talento y rendimiento colectivo de los clubes en cada temporada. Esto permitira identificar patrones y relaciones entre la concentración de talento, el rendimiento colectivo y el impacto de las lesiones en el desempeño del club. Para lograr esto, se han seleccionado variables que relflejan la composición y carga de la plantilla, la concentración de talento, el rendimiento ofensivo y colectivo del club, y el impacto global de las lesiones en el club.
*/


DROP VIEW IF EXISTS analytics_club_seasons;

CREATE VIEW analytics_club_seasons AS
SELECT 
    -- Identificadores de Club, División y Temporada
    c.club_id,
    c.club_name,
    d.division_id,
    d.division_name,
    d.division_strength,
    s.season_id,
    s.season_label,

    -- Composición y Carga de la Plantilla
    COUNT(ps.player_id) AS squad_size,  
    ROUND(AVG(ps.age), 1) AS avg_squad_age,
    ROUND(AVG(ps.mins), 1) AS avg_mins_per_player,

    -- Concentración de Talento (Objetivo 2)
    ROUND(AVG(ps.ability_score), 2) AS avg_ability_score,
    ROUND(AVG(psg.average_rating), 2) AS avg_player_rating,
    COUNT(CASE WHEN psg.average_rating >= 7.0 THEN 1 END) AS high_performance_players_count, --Conteo de Jugadores de Alto Rendimiento
    ROUND(100.0 * COUNT(CASE WHEN psg.average_rating >= 7.0 THEN 1 END) / COUNT(ps.player_id), 2) AS pct_high_performance_players, --orcentaje de Concentración de Talento

    -- Rendimiento Ofensivo y Colectivo del Club
    SUM(psa.goals) AS total_goals_scored,
    ROUND(SUM(psa.xg), 2) AS total_xg,
    ROUND(AVG(psg.points_per_game), 3) AS avg_ppg,

    -- Impacto Global de Lesiones en el Club (Objetivo 1)
    SUM(COALESCE(inj.total_injuries, 0)) AS squad_total_injuries,  -- El COALESCE es para que si un jugador no tuvo lesiones esa temporada el valor NULL aparezca como 0 porque tuvo 0 lesiones
    SUM(COALESCE(inj.total_days_lost, 0)) AS squad_total_days_lost

FROM player_seasons ps
INNER JOIN clubs c 
    ON ps.club_id = c.club_id
LEFT JOIN divisions d 
    ON c.division_id = d.division_id
INNER JOIN seasons s 
    ON ps.season_id = s.season_id
INNER JOIN player_stats_general psg 
    ON ps.player_season_id = psg.player_season_id
INNER JOIN player_stats_attacking psa 
    ON ps.player_season_id = psa.player_season_id
LEFT JOIN (

    /*
    
        En este paso se realiza un resumen de las lesiones para cada jugador y temporada en una tabla temporal, similar a la vista anterior. Esto permite calcular el impacto global de las lesiones en el club al sumar el total de lesiones y días perdidos por todos los jugadores del club en cada temporada en una tabla resumida, esto evita tener que repetir el cálculo en múltiples consultas.
    */

    SELECT 
        player_id,
        season_id,
        COUNT(injury_id) AS total_injuries,
        SUM(DATEDIFF('day', CAST(start_date AS DATE), CAST(end_date AS DATE))) AS total_days_lost
    FROM injuries
    GROUP BY player_id, season_id
) inj 
    ON ps.player_id = inj.player_id 
   AND ps.season_id = inj.season_id
GROUP BY 
    c.club_id,
    c.club_name,
    d.division_id,
    d.division_name,
    d.division_strength,
    s.season_id,
    s.season_label;


/*
===============================
        FIN VISTA 
    analytics_club_seasons
===============================

*/

/*
=====================================
            INICIO VISTA 
    analytics_club_position_seasons
=====================================

*/

/*
esta vista agrupa  las estadísticas de los jugadores no solo por club y temporada, sino también por su categoría posicional principal permitiendo evaluar si el rendimiento de líneas específicas (como la solidez defensiva frente a la eficacia ofensiva) ejerce un peso estadísticamente mayor sobre la obtención de puntos por partido
*/

DROP VIEW IF EXISTS analytics_club_position_seasons;

CREATE VIEW analytics_club_position_seasons AS
SELECT 
    c.club_id,
    c.club_name,
    s.season_id,
    s.season_label,
    p.primary_category, -- 'GOALKEEPER', 'DEFENDER', 'MIDFIELDER', 'ATTACKER'[cite: 1]

    -- Tamaño y carga de esa línea posicional
    COUNT(ps.player_id) AS players_in_position_count,
    ROUND(AVG(ps.mins), 1) AS avg_mins_played,

    -- Rendimiento específico de la línea
    ROUND(AVG(psg.average_rating), 2) AS line_avg_rating,
    SUM(psa.goals) AS line_total_goals,
    ROUND(SUM(psa.xg), 2) AS line_total_xg,
    SUM(psd.tackles_completed) AS line_total_tackles,
    SUM(psd.interceptions) AS line_total_interceptions,

    -- Éxito del club en esa temporada (para correlacionar)
    MAX(psg.points_per_game) AS club_avg_ppg -- O la métrica de puntos del club de la otra vista

FROM player_seasons ps
INNER JOIN players p 
    ON ps.player_id = p.player_id
INNER JOIN clubs c 
    ON ps.club_id = c.club_id
INNER JOIN seasons s 
    ON ps.season_id = s.season_id
INNER JOIN player_stats_general psg 
    ON ps.player_season_id = psg.player_season_id
LEFT JOIN player_stats_attacking psa 
    ON ps.player_season_id = psa.player_season_id
LEFT JOIN player_stats_defending psd 
    ON ps.player_season_id = psd.player_season_id
GROUP BY 
    c.club_id,
    c.club_name,
    s.season_id,
    s.season_label,
    p.primary_category;