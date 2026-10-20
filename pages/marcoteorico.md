Dashboard Estadístico de Fútbol: Evaluación de Lesiones, Dinámicas Posicionales y Rendimiento de Clubes (2022-2026)

MARCO TEÓRICO

INTRODUCCIÓN
La fundamentación teórica de esta investigación se articula en torno a tres ejes analíticos que corresponden a los objetivos específicos que hemos desarrollado: 
	La epidemiología de lesiones y su relación con características antropométricas y carga de minutos.
	La cuantificación del rendimiento ofensivo y la consistencia competitiva mediante métricas probabilísticas.
	La valoración posicional y la concentración de talento en las plantillas.
Los datos utilizados provienen de la base de datos SQL Practice DB: Football Players (17 Tables), que contiene 27,343 jugadores, 108,639 registros de temporadas y 26,949 lesiones documentadas, estructurados en un esquema relacional normalizado de 17 tablas. Esta base de datos proporciona un entorno realista para la exploración de patrones de rendimiento, lesiones y valor posicional, permitiendo la aplicación de técnicas de consulta SQL, visualización interactiva y análisis estadístico.
El período 2022-2026 tiene una especial relevancia por la intensificación del calendario futbolístico derivada de la expansión de competiciones internacionales, lo que incrementó la necesidad de herramientas analíticas robustas para la gestión de cargas, la prevención de lesiones y la optimización del rendimiento colectivo.
El desarrollo teórico se organiza en cuatro secciones que abordan los fundamentos conceptuales de cada eje analítico, culminando con los principios de la visualización de datos aplicada al deporte como herramienta de apoyo.

SECCIÓN 1.
 EPIDEMIOLOGÍA DE LESIONES, ANTROPOMETRÍA Y CARGA DE MINUTOS
1.1 Definición Operativa y Clasificación de Lesiones en el Fútbol
La investigación epidemiológica en lesiones deportivas enfrenta un desafío fundamental: la ausencia histórica de definiciones estandarizadas que permitan la comparabilidad entre estudios. Las aproximaciones iniciales varían desde definiciones basadas en días perdidos de entrenamiento hasta aquellas que limitaban la participación atlética al menos un día después del inicio de los síntomas.
El consenso ReFORM, derivado de la posición del Comité Olímpico Internacional, establece un marco unificado para la epidemiología de lesiones en fútbol. La definición operativa central adopta el criterio de pérdida de tiempo:
Se registra una lesión cuando un jugador no puede participar plenamente en entrenamientos o partidos posteriores debido a un problema de salud. Este criterio, aunque no exento de limitaciones, proporciona una base cuantificable que permite el cálculo de tasas de incidencia comparables.
La clasificación de severidad según días de baja constituye un componente esencial del marco ReFORM. Las categorías establecidas son: 0 días, 1-3 días, 4-7 días, 8-28 días, 29-90 días, 91-180 días, y más de 180 días. Esta gradación permite estratificar las lesiones según su impacto en la disponibilidad del jugador.
Además de la severidad, el consenso ReFORM enfatiza la necesidad de circunstanciar las especificidades de aparición: 
	Diferenciación entre lesiones relacionadas y no relacionadas con el fútbol. 
	Modo de aparición (súbito o progresivo). 
	Mecanismo específico del fútbol (carrera, cambio de dirección, disparo, cabeceo, entrada). 
	Categorías de contacto (sin contacto, contacto directo o indirecto) (Walden et al., 2025).
En la base de datos utilizada, la tabla injuries contiene 26,949 registros con campos como injury_type (tipo de lesión), days_out (días de baja) e información del jugador y la temporada. Esta estructura permite calcular medidas de tendencia central y dispersión (medias, desviaciones estándar, conteos absolutos y relativos) sobre la duración de las bajas médicas y la frecuencia de las lesiones, tal como se describe en el procedimiento analítico del marco metodológico.
1.2 Características Antropométricas como Factores de Riesgo
La antropometría que es el estudio de las dimensiones y proporciones del cuerpo humano, constituye un factor relevante en la epidemiología de lesiones deportivas. Las variables antropométricas más estudiadas en fútbol incluyen altura, peso, índice de masa corporal (IMC) y composición corporal.
La evidencia empírica sugiere que los jugadores más altos y pesados presentan un mayor riesgo de lesiones musculares, particularmente en la musculatura isquiotibial, debido a la mayor tensión mecánica sobre los tejidos durante acciones explosivas. Un estudio sobre 800 jugadores universitarios de fútbol en China identificó que las características físicas (edad, altura, peso, IMC) junto con métricas específicas de fútbol (posición, horas de entrenamiento, historial de lesiones) constituyen predictores relevantes para lesiones en la temporada siguiente.
La edad constituye otro factor antropométrico relevante: los jugadores mayores de 30 años presentan mayor incidencia de lesiones musculares y tiempos de recuperación más prolongados, mientras que los jugadores jóvenes (menores de 21 años) exhiben mayor riesgo de lesiones por sobrecarga debido a la inmadurez del sistema musculoesquelético.
En la base de datos utilizada, la tabla players contiene los campos height (altura) y weight (peso), lo que permite cruzar estas características con la incidencia y duración de lesiones. Este cruce se realizará mediante análisis de distribución y dispersión, identificando perfiles de riesgo y patrones de fatiga física a lo largo de las temporadas, tal como se establece en el marco metodológico.
La relación entre antropometría y lesión no es lineal ni determinista. Los factores antropométricos interactúan con la carga de entrenamiento, la posición de juego, el historial de lesiones previas y factores contextuales. El dashboard propuesto permitirá explorar estas relaciones de forma visual y exploratoria, sin pretender establecer causalidad.
1.3 Carga de Minutos como Proxy de Carga Externa
El modelo de carga aguda: crónica relación de carga aguda (ACWR) postula que el riesgo de lesión depende de la relación entre la carga reciente (aguda) y la carga de adaptación acumulada demostraron en futbolistas profesionales que una relación de carga aguda entre 1.00 y 1.25 tiene un efecto protector (OR = 0.68, p = 0.006), mientras que cargas de pretemporada ≥1500 AU incrementan el riesgo (OR = 1.95, p = 0.006).
Ajuste metodológico: Dado que el marco metodológico establece el uso de carga acumulada de minutos jugados como variable operativa, y no el cálculo completo del ACWR (que requeriría datos semanales de carga que la base de datos no proporciona), en esta sección ajustamos para utilizar los minutos jugados como proxy de la carga externa. La tabla player_seasons contiene el campo minutes_played (minutos jugados) y appearances (apariciones) , permitiendo calcular la carga acumulada por jugador y la temporada.
La lógica subyacente es fisiológica: a mayor carga acumulada de minutos, mayor estrés mecánico sobre los tejidos, y por tanto mayor vulnerabilidad a la lesión. Esta relación, aunque simplificada respecto al modelo ACWR completo, es consistente con la literatura que identifica la carga de minutos como un factor de riesgo relevante.
1.4 Limitaciones del Enfoque de Carga de Minutos
La evidencia es observacional, lo que impide establecer relaciones causales definitivas. La asociación entre carga de minutos y lesiones puede estar confundida por variables no medidas como calidad del sueño, estado nutricional o factores psicológicos. Además, los minutos jugados no capturan completamente la carga interna (respuesta fisiológica) ni la naturaleza intermitente de las demandas del fútbol.
Un estudio retrospectivo sobre la Bundesliga durante el período COVID-19 encontró que la tasa de lesiones aumentó más de 3 veces después del confinamiento (0.84 lesiones por partido vs. 0.27 lesiones por partido). Este hallazgo sugiere que la preparación física posterior a períodos de inactividad constituye un factor de riesgo significativo, independientemente de la carga de minutos.
1.5 Diferencias Posicionales en Patrones de Lesión
La evidencia epidemiológica documenta diferencias posicionales significativas. Krutsch et al. (2016) analizaron 6 temporadas de la Bundesliga y encontraron que los extremos presentaron la mayor incidencia y carga de lesiones en partidos, los defensas centrales la mayor incidencia en entrenamientos, y los centrocampistas la mayor tasa de no disponibilidad tanto en partidos como en entrenamientos.
En la base de datos utilizada, la tabla positions contiene 14 posiciones diferentes (D, M, ST, etc.), y la tabla player_positions (62,349 registros) establece una relación muchos-a-muchos que permite que un jugador tenga múltiples posiciones elegibles. Esta estructura permite estratificar el análisis de lesiones por posición específica, tal como se establece en el procedimiento analítico de segmentación.

SECCIÓN 2.
RENDIMIENTO OFENSIVO, CONSISTENCIA COMPETITIVA Y GOLES ESPERADOS (xG)
2.1 Fundamentos Teóricos del xG
Los goles esperados (xG) constituye la métrica más influyente en el análisis moderno del rendimiento ofensivo. Su fundamento teórico radica en la modelización probabilística de las oportunidades de gol: cada disparo se caracteriza por una probabilidad de conversión en gol, estimada a partir de las circunstancias objetivas del disparo.
La lógica del xG responde a una limitación fundamental de las métricas tradicionales basadas en resultados. Los goles y asistencias son eventos discretos y relativamente infrecuentes que, en muestras pequeñas, están dominados por la varianza aleatoria. Un equipo puede generar oportunidades de alta calidad y no marcar debido a actuaciones excepcionales del portero rival o simple mala suerte.
El xG separa el proceso del resultado, evaluando la calidad de las oportunidades generadas independientemente de si estas se convirtieron en gol. Esta distinción es crucial para la evaluación del rendimiento: una caída en los goles sin una caída correspondiente en xG sugiere un problema de finalización o mala fortuna, mientras que una caída en xG indica un deterioro estructural en la generación de oportunidades.
Los modelos de xG incorporan múltiples factores predictivos: posición del jugador, ubicación del disparo, ángulo hacia el arco, distancia, parte del cuerpo utilizada, preparación del disparo, número de toques previos, número de jugadores en la trayectoria y posición del portero.
La base de datos utilizada contiene en la tabla player_stats_attacking los campos goals (goles), Xg (expected goals – goles esperados), shots (disparos), assists (asistencias) y dribbles (regates) Esto permite calcular rangos de rendimiento ofensivo y métricas de eficiencia relativa, como la diferencia entre goles reales y xG acumulado (GOE, Goals Over Expected), tal como se establece en el marco metodológico para el análisis de distribución y concentración de talento.
2.2 Limitaciones del xG Tradicional
El xG tradicional presenta limitaciones metodológicas identificadas en la literatura reciente:
	Primera limitación: sesgo de selección de disparo. Los modelos de xG se entrenan exclusivamente con disparos que efectivamente ocurrieron, ignorando los momentos de peligro que no llegaron a materializarse en disparo. Un ejemplo ilustrativo proviene de un partido entre Real Madrid y Manchester City en febrero de 2025: un centro raso al área pequeña que tres jugadores estuvieron cerca de conectar pero que finalmente fue despejado no genera contribución alguna al xG, a pesar de representar un momento de peligro inminente. En contraste, un disparo especulativo desde 35 metros genera un xG bajo pero no nulo.
	Segunda limitación: independencia de eventos. El xG trata cada disparo como un evento independiente, lo que genera valores acumulados inflados en posesiones con múltiples disparos rápidos. Si una posesión incluye tres disparos con xG de 0.3 cada uno, la suma de xG es 0.9, cuando en realidad solo puede resultar un gol por posesión.
	Tercera limitación: homogeneidad de jugadores. Los modelos de xG asignan la misma probabilidad a un disparo dado independientemente de quién lo ejecute. Un disparo de larga distancia ejecutado por un especialista tiene una probabilidad de gol diferente que un disparo idéntico ejecutado por un defensor, pero el xG estándar no captura esta diferencia.
2.3 Desarrollos Metodológicos: xG+ y Modelización Dinámica
El marco xG+ representa un avance significativo al modelar no solo la probabilidad de gol condicionada al disparo, sino también la probabilidad de que ocurra un disparo. El componente xS (probabilidad de disparo en el siguiente segundo) captura momentos de peligro que no se materializan en disparos, abordando directamente el sesgo de selección del xG tradicional.
La combinación de xG y xS produce xG+, definido como la probabilidad de gol en el siguiente segundo, ocurra o no un disparo. Esta métrica refleja de manera más completa la peligrosidad de cada momento del juego.
Hallazgo clave: La capacidad de creación de disparos (shot creation) es mucho más estable entre temporadas que la capacidad de finalización. Los jugadores con altos valores de SOE (Shots Over Expected) aquellos que consistentemente generan más disparos de lo esperado mantienen esta habilidad a lo largo del tiempo, mientras que el rendimiento en finalización exhibe mayor variabilidad. El análisis de datos de la Premier League (2022-2025) confirma que xG+ es más predictivo de goles reales que el xG tradicional, y que las métricas que enfatizan la creación sostenida de oportunidades proporcionan una base más estable para la valoración que las métricas centradas en la finalización. Este hallazgo es directamente relevante para el análisis de consistencia competitiva inter-temporada establecido en el marco metodológico.
2.4 Consistencia Competitiva: Definición y Operacionalización
La consistencia competitiva se define como la capacidad de un jugador o equipo de mantener un nivel de rendimiento estable a lo largo del tiempo, resistiendo fluctuaciones asociadas a la varianza aleatoria, el estado de forma, las lesiones o los cambios tácticos.
Operacionalización según el marco metodológico: La consistencia competitiva se calculará mediante:
1.	Estabilidad inter-temporada de métricas ofensivas: comparación de xG/90, SOE y GOE/90 entre las 4 temporadas disponibles. La tabla seasons contiene el campo season_order (0 = temporada real, 1-3 = temporadas fabricadas) y season_label.
2.	Coeficiente de variación de métricas de rendimiento dentro de una misma temporada.
3.	Persistencia de la contribución ofensiva: correlación entre el rendimiento ofensivo de un jugador en temporadas sucesivas.
La evidencia de Pipping et al. (2025) indica que las métricas de creación de oportunidades (xG/90, SOE) exhiben mayor estabilidad inter-temporada que las métricas de finalización (GOE), lo que las hace más apropiadas para evaluar la consistencia competitiva.
2.5 Distribución y Concentración de Talento
La concentración de talento se refiere a la distribución desigual de jugadores de alto rendimiento entre equipos. En el contexto del dashboard, se calculará mediante:
1.	Distribución porcentual de jugadores de alto rendimiento por club y división.
2.	Índice de concentración (coeficiente de Gini, HHI) para cada división.
3.	Rangos de rendimiento ofensivo (percentiles de xG/90, SOE, GOE/90).
La tabla clubs contiene 2,773 clubes con club_name y división_id. 
La tabla divisions contiene 299 divisiones con un strength_rating. 
La tabla player_seasons contiene el campo ability_score que fue generado por un modelo de regresión entrenado para predecir el rating general de cada jugador a partir de sus estadísticas. 
El modelo produce cuatro scores: Overall, Offensive, Defensive y Midfield. Esta estructura permite calcular índices de concentración de talento y distribución porcentual, tal como se establece en el procedimiento analítico de análisis de distribución porcentual y rangos de rendimiento ofensivo.
Frick, Quansah y Lang (2023) examinaron la relación entre concentración de talento y equilibrio competitivo en 12 países de Europa Occidental, con 5,299 observaciones club-temporada (2005/06–2020/21). Metodológicamente, utilizaron modelos de regresión con efectos fijos de año, país y división. Su conclusión principal es que, tras controlar por año, país y división, el efecto de la concentración de talento sobre el equilibrio competitivo es solo débilmente significativo o no significativo. Los autores sugieren que el sistema de ascenso y descenso en las ligas europeas es efectivo para mantener un equilibrio competitivo sin necesidad de intervenciones regulatorias adicionales.

SECCIÓN 3.
VALOR POSICIONAL Y APORTES POR LÍNEAS
3.1 Definición y Funciones de las Líneas Posicionales
La estructura organizativa del fútbol se articula en torno a cuatro líneas posicionales con funciones y demandas diferenciadas: arqueros, defensas, mediocampistas y delanteros.
•	Arqueros: posición más especializada. Su función primordial es prevenir goles. Aportan los menores valores de eLPAR para un nivel dado de calificación.
•	Defensas: función principal de proteger el arco y recuperar la posesión. Aportan los mayores valores de eLPAR para una calificación equivalente.
•	Mediocampistas: posición intermedia con responsabilidades duales de creación ofensiva y contención defensiva. Se sitúan cerca de los defensas en eLPAR.
•	Delanteros: especializados en la finalización. Aportan menos eLPAR que defensas y mediocampistas para una calificación dada, debido a la mayor varianza en su contribución.
En la base de datos, la tabla player_seasons contiene el campo ability_score (puntaje de habilidad) que fue generado por un modelo de regresión entrenado para predecir el rating general de cada jugador a partir de sus estadísticas. El modelo produce cuatro scores: Overall, Offensive, Defensive y Midfield. Esta estructura permite calcular el aporte porcentual de cada línea posicional al rendimiento colectivo, utilizando los scores específicos por posición.
3.2 El Modelo eLPAR: Fundamentos y Metodología
El eLPAR (expected League Points Above Replacement) proporciona un marco cuantitativo para evaluar la contribución relativa de jugadores y posiciones al éxito del equipo. Su fundamento teórico proviene del concepto de "replacement player" desarrollado en la sabermetría: un jugador de nivel "de reemplazo" es aquel fácilmente disponible en el mercado.
La metodología de cálculo implica:
1.	Definir el nivel de reemplazo como un porcentaje del promedio posicional (típicamente el percentil 20 o el 80% del promedio).
2.	Utilizar un modelo de regresión de Skellam sobre diferencias de goles para estimar cómo los cambios en el rating promedio de cada línea afectan la probabilidad de victoria, empate y derrota.
3.	Calcular: eLPAR = 3·δPw + 1·δPd, donde δPw y δPd son los cambios en las probabilidades de victoria y empate (Pelechrinis & Winston, 2021).
Pelechrinis y Winston (2021) utilizaron datos de ~20,000 partidos de 11 ligas europeas y calificaciones de jugadores del videojuego FIFA. Su conclusión clave es que el mercado de la Premier League infravalora a los jugadores de la línea defensiva en relación con los porteros.
La investigación original de Pelechrinis y Winston utilizó calificaciones de FIFA como proxy de la capacidad de los jugadores. La base de datos utilizada en este proyecto emplea un enfoque similar pero más robusto: el ability_score fue generado por un modelo de regresión entrenado con estadísticas de rendimiento, con el objetivo explícito de evitar que el modelo aprendiera atajos como "juega para un buen equipo" o "acumuló muchos minutos".
3.3 Aporte Porcentual por Línea Posicional: Operacionalización
El aporte porcentual por línea se refiere a la contribución relativa de cada línea al rendimiento colectivo del equipo, medido a través de métricas ofensivas, defensivas y de contribución general.
El aporte porcentual se calculará mediante:
1.	Segmentación del rendimiento colectivo por líneas posicionales (arqueros, defensas, mediocampistas, delanteros).
2.	Cálculo de aportes porcentuales promedio de cada posición específica que ocupa un jugador dentro del campo de juego (D, M, ST × L/R/C) respecto a los indicadores globales del equipo.
3.	Contraste de la importancia y eficiencia individual de cada línea dentro de la estructura práctica.
Pappalardo et al. (2019) analizaron las diferencias posicionales en el rendimiento técnico y encontraron patrones consistentes: los delanteros dominan en goles; las asistencias se distribuyen entre todas las posiciones; los mediocampistas dominan en pases; los delanteros en regates; y existen diferencias significativas en tackles, despejes y bloqueos, pero no en interceptaciones.
En la base de datos, las tablas player_stats_attacking, player_stats_passing, player_stats_defending y player_stats_goalkeeping contienen métricas específicas para cada dimensión del rendimiento. La tabla de porteros contiene saves, clean sheets y expected goals prevented, que están poblados únicamente para porteros (NULL/0 para jugadores de campo). Esta estructura permite calcular el aporte porcentual de cada línea mediante la agregación de métricas ponderadas, tal como se establece en el procedimiento analítico de segmentación y agregación de datos.
3.4 Implicaciones para la Gestión de Plantillas
El análisis de valor posicional y concentración de talento tiene implicaciones directas para la gestión de plantillas:
•	Dado que los defensas están subvalorados en el mercado, la inversión en defensas de calidad ofrece un retorno esperado superior.
•	La profundidad de plantilla es crítica para el éxito sostenido: la concentración excesiva de talento genera vulnerabilidad a lesiones y sanciones.
•	La dependencia del eLPAR de la formación táctica subraya que el valor de un jugador no es una propiedad intrínseca, sino que depende del contexto táctico (Pelechrinis & Winston, 2021).
En el contexto de la base de datos utilizada, la tabla transfers (41,425 registros) y contracts (41,425 registros) permiten explorar la relación entre el valor de mercado de los jugadores y su contribución al rendimiento, aunque estas tablas deben interpretarse como ejercicios de práctica analítica más que como evidencia empírica real.

SECCIÓN 4.
VISUALIZACIÓN DE DATOS Y ARQUITECTURA DEL DASHBOARD
4.1 Fundamentos de la Visualización de Datos
La visualización de datos es el proceso de representar información cuantitativa y cualitativa mediante elementos gráficos (gráficos, tablas, mapas, diagramas) para facilitar la comprensión de patrones, tendencias y relaciones. En el contexto deportivo, la visualización permite traducir la complejidad estadística en información accionable para cuerpos técnicos y analistas.
Los principios fundamentales de la visualización efectiva incluyen:
•	Claridad: la representación debe ser comprensible sin explicación adicional.
•	Precisión: los datos deben representarse sin distorsión.
•	Relevancia: solo se visualiza la información pertinente para la decisión.
•	Interactividad: el usuario debe poder explorar los datos según sus necesidades.
4.2 Técnicas de Visualización según el Marco Metodológico
El marco metodológico establece tres tipos de visualización que estructuran la representación gráfica del dashboard:
1. Gráficos de Distribución y Dispersión: Sirven para contrastar la relación entre la carga de minutos, las características antropométricas y la incidencia de lesiones entre las temporadas 2022-2023. Se implementarán mediante diagramas de dispersión que permitan visualizar correlaciones entre altura, peso, minutos jugados y días de baja.
2. Gráficos de Tendencia Temporal: Se implementan para seguir la evolución clínica del rendimiento y la concentración de talento a lo largo de las temporadas del período 2022-2026. Se utilizarán gráficos de línea que muestren la evolución de xG/90, SOE, ability_score y lesiones por temporada.
3. Diagramas Comparativos por Líneas Posicionales: Diseñados para contrastar el aporte porcentual y las medias de rendimiento entre defensas, mediocampistas, delanteros y arqueros de manera simultánea. Se implementarán mediante gráficos de barras agrupadas y diagramas de caja (boxplots).
4.3 Arquitectura Técnica del Dashboard
El dashboard está implementado íntegramente en Python, utilizando el siguiente stack tecnológico:
•	Procesamiento y Manipulación de Datos: Pandas, NumPy
•	Interfaz y Visualización Interactiva: streamlit / Plotly
•	(para gráficos dinámicos de dispersión, mapas de calor de correlación y distribuciones estadísticas)
La estructura del proyecto incluye:
Power BI	Archivos de la aplicación en Microsoft Power BI
Assets	Recursos gráficos y logos
 Db	Datasets procesados y en bruto (CSV / Parquet)
src/utils.py	Funciones auxiliares de limpieza y formato
app.py	Punto de partida de la app
requirements.txt	Dependencias del proyecto
README.md 	Documentación del proyecto

Esta arquitectura permite integración de datos, actualización en tiempo real y accesibilidad para usuarios no técnicos, alineándose con el objetivo de ofrecer a cuerpos técnicos y analistas una herramienta robusta de toma de decisiones basada en datos.
4.4 Traducción de Métricas Complejas en Información Accionable
El valor de un dashboard no radica en la complejidad de sus cálculos, sino en su capacidad de traducir métricas complejas (xG, xG+, eLPAR, ACWR) en información comprensible y accionable para entrenadores, analistas y directores deportivos. La visualización efectiva de estas métricas requiere:
•	Contextualización: cada métrica debe acompañarse de su interpretación (ej. xG alto = buena generación de oportunidades).
•	Comparación: permitir comparar jugadores, equipos o temporadas.
•	Tendencias: mostrar la evolución temporal de las métricas.
•	Alertas: identificar valores atípicos o situaciones de riesgo.

SECCIÓN 5. 
FUNDAMENTOS DE BASES DE DATOS RELACIONALES Y SQL
5.1 Modelo Relacional y Estructura del Dataset
El modelo relacional organiza los datos en relaciones (tablas) compuestas por filas (tuplas)
y columnas (atributos), donde cada fila representa una instancia de una entidad y cada columna un atributo de esa entidad 14. Este modelo, propuesto originalmente por E.F. Codd, se sustenta en dos principios operativos: la independencia física de los datos (el usuario no necesita conocer cómo se almacenan) y la manipulación declarativa mediante lenguajes como SQL.
La base de datos SQL Practice DB: Football Players implementa este modelo con 17 tablas normalizadas que totalizan aproximadamente 855,000 filas. La arquitectura sigue una jerarquía clara:
•	Tablas de dimensión: nations (174) registros, divicions (299), Clubs (2773), positions (14), seasons (4).
•	Entidad central: player (27,343), contiene únicamente hechos biográficos (nombre, nación, altura, peso, posición primaria).
•	Tabla puente (hub): player_seasons (108.639) constituye el eje del modelo, donde cada fila representa la participación de un jugador en una temporada específica.
•	Tablas de estadísticas vinculadas 1:1: player_stats_general, player_stats_attacking, player_stats_passing, player_stats_defending, player_stats_goalkeeping.
•	Tabla de unión M:N: player_positions (62,349) permite que un jugador tenga múltiples posiciones elegibles.
•	Tablas complementarias: injuries(26.949), transfers (41.425), contracts (41.425), agents (850).
En esta estructura es donde player_seasons actúa como nexo entre y las cinco tablas de estadísticas, respondiendo al principio de que cada tabla debe almacenar información de una sola entidad. El resultado es un esquema que permite consultas de múltiples saltos (joins) sin redundancia innecesaria.
5.2 Claves Primarias, Claves Foráneas e Integridad Referencial
Una clave primaria (PRIMARY KEY) es una columna o combinación de columnas cuyos valores identifican de forma única cada fila de una tabla. En el dataset, cada tabla posee una clave subrogada (por ejemplo, player_id, player_seasons_id, en player_seasons). El caso de clubs merece mención específica: su clave primaria es subrogada (club_id) pero la unicidad real recae en la combinación (club_name, division_id) ya que los nombres de clubes se repiten entre divisiones.
Una clave foránea (FOREIGN KEY) es una columna cuyos valores deben coincidir con la clave primaria de otra tabla, estableciendo así una relación referencial. El esquema del dataset implementa tres tipos de relaciones:
 
La integridad referencial garantiza que no existan valores de clave foránea que apunten a filas inexistentes. En este dataset, la restricción más didáctica es la nulabilidad de clubs.division_id, (344) jugadores no tienen división asignada. Esto no es un error, sino un escenario realista que requiere el uso de LEFT JOIN para recuperar esas filas sin perderlas en la consulta.
5.3 Álgebra Relacional y Operaciones SQL
El álgebra relacional define un conjunto de operadores que transforman relaciones en nuevas relaciones, siendo las relaciones cerradas bajo estos operadores: el resultado de cualquier operación es a su vez una relación. Las operaciones fundamentales son:
•	Selección: filtra tuplas que cumplen un predicado. En SQL corresponde a WHERE.
•	Proyección: selecciona atributos específicos, eliminando duplicados. En SQL corresponde a la lista SELECT
•	Producto cartesiano: combina todas las tuplas de dos relaciones. En SQL es CROSS JOIN
•	Unión, Intersección, Diferencia: operaciones de conjuntos que en SQL se implementan mediante UNION, INTERSECT, EXCEPT.
•	Reunión (JOIN): combina tuplas de dos relaciones que cumplen una condición, siendo la operación más importante en bases de datos relacionales.
SQL no es una implementación literal del álgebra relacional la cláusula SELECT de SQL, por ejemplo, no corresponde al operador σ sino un lenguaje declarativo que especifica qué se quiere obtener, dejando al motor de base de datos la tarea de decidir cómo obtenerlo. El dataset de 17 tablas está diseñado precisamente para practicar estas operaciones: desde selecciones simples (WHERE height >180) hasta joins de múltiples saltos que atraviesan (players – player_seasons – player_stats_attacking)
5.4 JOINs: Tipos y Aplicación al Dataset
La operación de reunión (JOIN) es el mecanismo central para combinar datos distribuidos entre tablas normalizadas. El dataset ofrece oportunidades de práctica para cada tipo:
INNER JOIN retorna únicamente las filas donde existe coincidencia en ambas tablas. Es el tipo por defecto y se usa cuando se necesita intersección de datos. Ejemplo: obtener todos los jugadores que tienen lesiones registradas.
LEFT JOIN (LEFT OUTER JOIN) retorna todas las filas de la tabla izquierda, con valores NULL en las columnas de la tabla derecha cuando no hay coincidencia. Este es el operador clave para el análisis de disponibilidad: identificar jugadores que no tuvieron lesiones en una temporada, o clubes sin división asignada.
RIGHT JOIN es el espejo de LEFT JOIN: retorna todas las filas de la tabla derecha. Su uso en este dataset es menos frecuente porque el diseño del hub (player_Pseasons) naturalmente orienta las consultas desde player hacia las tablas de estadísticas.
CROSS JOIN genera el producto cartesiano completo. En el contexto del dataset, se puede usar para generar combinaciones teóricas de jugadores × posiciones, útil para explorar la flexibilidad posicional máxima de una plantilla.
La correcta elección del tipo de JOIN determina no solo el resultado, sino también el rendimiento de la consulta: el motor de base de datos debe decidir el orden de las uniones y el algoritmo de acceso (nested loop, hash join, merge join) basándose en las claves foráneas y la cardinalidad estimada.
5.5 Funciones de Agregación, GROUP BY y HAVING
Las funciones de agregación (COUNT, SUM,AVG, MIN, MAX ) realizan cálculos sobre conjuntos de filas, transformando múltiples filas en un único valor resumen. Aplicadas al dataset:
•	COUNT (*) o CONUT(injury_id): Sobre injuries agrupdo por injury_type, permite identificar los tipos de lesión más frecuentes.
•	AVG (days_out): Agrupado por position_id, permite contrastar la severidad media por posición.
•	SUM(goals) y SUM(xg) por player_id, calculan métricas acumuladasde rendimiento ofensivo.
La cláusula GROUP BY particiona las filas en subconjuntos según valores de columnas específicas, sobre los cuales se aplican las funciones de agregación. Sin GROUP BY, una función de agregación colapsa toda la tabla en una sola fila. Con GROUP BY, produce una fila por cada grupo distinto.
La cláusula HAVING filtra los grupos resultantes de GROUP BY basándose en el resultado de funciones de agregación. Es crucial entender la distinción:
•	WHERE filtra filas antes de la agrupación.
•	HAVING filtra grupos después de la agrupación.
5.6 Funciones de Ventana (Window Functions)
Las funciones de ventana realizan cálculos sobre un conjunto de filas relacionadas con la fila actual, sin colapsar el conjunto de resultados. A diferencia de las funciones de agregación tradicionales, las window functions preservan las filas individuales mientras añaden valores calculados.
5.7 Normalización y Diseño Relacional
La normalización es el proceso de aplicar reglas estructurales a las relaciones para eliminar redundancia, prevenir anomalías de inserción/actualización/borrado y garantizar la integridad de los datos. Las formas normales relevantes para este dataset son:
Primera Forma Normal (1FN): Cada atributo contiene un valor atómico. El dataset cumple 1FN: no hay columnas que almacenen listas o grupos repetidos. La tabla player_positions existe precisamente para eliminar el grupo repetitivo de posiciones que, de otro modo, violaría 1FN.
Segunda Forma Normal (2FN): Cada atributo no clave depende funcionalmente de la clave completa, no de una parte de ella. Todas las tablas del dataset que tienen clave simple (surrogate) cumplen 2FN automáticamente. La tabla player_positions con clave compuesta (player_id, position_id) también cumple 2FN porque no tiene atributos adicionales que dependan parcialmente de la clave.
Tercera Forma Normal (3FN): no existen dependencias transitivas entre atributos no clave. El dataset cumple 3FN.
La descomposición normalizada del dataset tiene un costo: para obtener una vista completa de un jugador (nombre + estadísticas + club + división + lesiones), se requieren joins de hasta 5 tablas. Este es el trade-off fundamental de la normalización: menos redundancia y mayor integridad a cambio de consultas más complejas. El dataset está diseñado para que el practicante experimente directamente este trade-off.
5.8 Del SQL al Dashboard: Integración con la Arquitectura Analítica
Los fundamentos de bases de datos presentados en esta sección no constituyen un cuerpo teórico aislado, sino la infraestructura técnica sobre la cual se construye el dashboard estadístico. Cada consulta SQL que alimenta una visualización se apoya en los principios aquí descritos:
•	Las distribuciones y diagramas de dispersión de la Sección 4.2 (altura vs. días de baja, minutos jugados vs. incidencia de lesiones) requieren INNER JOIN entre player, palyer_seasons e injuries más funciones de agregación para calcular promedios y desviaciones por grupo.
•	Los gráficos de tendencia temporal (evolución de xG/90, ability_score y lesiones por temporada) se construyen con window functions que particionan por jugador y ordenan por seasons_order, permitiendo comparar la trayectoria individual a lo largo de las cuatro temporadas.
•	Los diagramas comparativos por líneas posicionales (boxplots de aporte porcentual por posición) dependen de GROUP BY sobre positions y joins múltiples que atraviesan player_positions, player_seasons y las tablas de estadísticas específicas por dimensión.
•	El cálculo de índices de concentración de talento (Gini, HHI) mencionado en la Sección 2.5 requiere agregaciones anidadas y subconsultas que explotan la estructura jerárquica del esquema ( divisions – clubs – player_seasons – ability_score)
•	Esta integración entre SQL y visualización es coherente con el principio de que un dashboard no es una colección de gráficos, sino un sistema de información donde la calidad de las consultas subyacentes determina la validez de las conclusiones. La solidez del modelo relacional claves para la integridad y la normalización se traduce directamente en la confiabilidad de las métricas visualizadas.
Las cinco secciones que hemos desarrollado convergen en un marco conceptual que articula, en primer lugar, los fundamentos de las bases de datos relacionales y SQL y el modelo relacional, claves para la integridad referencial, JOINs, agregaciones, funciones de ventana y normalización; en segundo lugar, la epidemiología de lesiones y su relación con la antropometría y la carga de minutos; en tercer lugar, la evaluación del rendimiento ofensivo mediante métricas probabilísticas como el xG, el xG+ y los indicadores derivados (SOE, GOE); en cuarto lugar, la valoración posicional y la concentración de talento a través del modelo eLPAR; y, finalmente, la visualización de datos y la arquitectura del dashboard como herramienta de apoyo a la decisión.
Esta articulación proporciona el sustento teórico necesario para abordar los tres objetivos específicos de la investigación y para interpretar los datos de la base SQL Practice DB: Football Player de manera coherente. La Sección 5 actúa como infraestructura técnica transversal: los conceptos de bases de datos relacionales no constituyen un cuerpo teórico aislado, sino el soporte sobre el cual se construyen las consultas que alimentan cada uno de los ejes analíticos y las visualizaciones del dashboard.






















REFERENCIAS BIBLIOGRÁFICAS
Frick, B., Quansah, T. K., & Lang, M. (2023). Talent concentration and competitive imbalance in European soccer. Frontiers in Sports and Active Living, 5, 1148122. https://doi.org/10.3389/fspor.2023.1148122
Fuller, C. W., Ekstrand, J., Junge, A., Andersen, T. E., Bahr, R., Dvorak, J., ... & Meeuwisse, W. H. (2006). Consensus statement on injury definitions and data collection procedures in studies of football (soccer) injuries. British Journal of Sports Medicine, 40(3), 193–201.
Gabbett, T. J., Hulin, B. T., Blanch, P., & Whiteley, R. (2016). High chronic training loads and exposure to bouts of maximal velocity running reduce injury risk in elite rugby league players. Journal of Science and Medicine in Sport, 19(3), 234–238.
Harlow, C. K., Drummond, J. E., & Voos, J. E. (2021). The effect of COVID-19 lockdown on injury rates in the Bundesliga. Frontiers in Sports and Active Living, 3, 630576.
Impellizzeri, F. M., Tenan, M. S., Kempton, T., Novak, A., & Coutts, A. J. (2020). Acute:Chronic Workload Ratio: Conceptual issues and fundamental pitfalls. International Journal of Sports Physiology and Performance, 15(6), 907–913.
Krutsch, W., Zeman, F., Zellner, J., Pfeifer, C., Nerlich, M., & Angele, P. (2016). Injury patterns among elite football players: A media-based analysis over 6 seasons with emphasis on playing position. International Journal of Sports Medicine, 37(11), 898–908.
Lucey, P., Bialkowski, A., Monfort, M., Carr, P., & Matthews, I. (2015). Quality vs quantity: Improved shot prediction in soccer using strategic features from spatiotemporal data. MIT Sloan Sports Analytics Conference.
Malone, S., Owen, A., Newton, M., Mendes, B., Collins, K. D., & Gabbett, T. J. (2016). The acute:chronic workload ratio in relation to injury risk in professional soccer. Journal of Science and Medicine in Sport, 20(6), 561–565.
Pappalardo, L., Cintia, P., Ferragina, P., Massucco, E., Pedreschi, D., & Giannotti, F. (2019). PlayerRank: Data-driven performance evaluation and player ranking in soccer via a machine learning approach. ACM Transactions on Intelligent Systems and Technology, 10(5), 1–27.
Pelechrinis, K., & Winston, W. (2021). Positional value in soccer: Expected league points added above replacement. Journal of Quantitative Analysis in Sports, 17(3), 187–201.
Pipping, J., Feng, T., & Sabin
