# Análisis Estadístico de Lesiones y Rendimiento Individual y Colectivo en Clubes de Fútbol Profesional en las Temporadas Comprendidas Entre los Años 2022 y 2026

**Aplicación desplegada:** https://proyectogrupo12.streamlit.app/

## Planteamiento del problema
El fútbol profesional contemporáneo es un deporte donde la exigencia es máxima, por lo que la intuición ya no puede ser la única medida para la toma de decisiones en el campo. Sin embargo, a pesar de la gran cantidad de registros sobre los partidos los directores técnicos y analistas luchan para unificar en una misma herramienta dimensiones como la salud y disponibilidad de los jugadores, la eficiencia del rendimiento individual frente a la concentración de talento en plantillas colectivas y el aporte real de cada línea posicional. No tener esta información entorpece la optimización y la rotación de plantillas, la prevención de lesiones y el rendimiento colectivo. 

## Justificación
Este dashboard estadístico interactivo busca responder la necesidad de una herramienta cuantitativa que permita el análisis diagnóstico preciso para la mejora del rendimiento colectivo y la prevención de lesiones tomando en cuenta las características antropométricas, como lo son la altura y el peso; y la edad de los jugadores. Este trabajo además, contribuye a la línea de investigación estadística aplicada al deporte de la UCV, por lo que sienta un precedente metodológico aplicable para el estudio del rendimiento en el fútbol profesional

## Objetivo General
Describir y visualizar el comportamiento de las métricas físicas, de lesiones y de rendimiento individual y colectivo en el fútbol profesional durante el período comprendido entre el año 2022 y el año 2026, con el fin de caracterizar los patrones de rendimiento de los jugadores y la concentración de talento en los clubes.

## Objetivos Específicos
Para dar respuesta al objetivo general, el dashboard aborda y desglosa los siguientes ejes analíticos:

1. Describir la frecuencia, duración y distribución de las lesiones en los jugadores entre las temporadas comprendidas entre los años 2022 y 2026, relacionándolas con sus características antropométricas (altura y peso) y su carga de minutos jugados.

2. Cuantificar la distribución y concentración de jugadores de alto rendimiento dentro de las plantillas de los clubes, evaluando su comportamiento ofensivo y consistencia competitiva a lo largo de las temporadas entre el 2022-2026.

3. Examinar el aporte porcentual y el promedio de rendimiento de las diferentes líneas posicionales (arqueros, defensas, mediocampistas y delanteros) dentro de la estructura de los equipos durante el ciclo 2022-2026.

## Preguntas de investigación
1. ¿Cuál ha sido la frecuencia, duración y distribución de las lesiones en los jugadores de fútbol profesional entre las temporadas comprendidas entre los años 2022-2026, y qué relación guardan con sus características antropométricas (altura y peso) y su carga de minutos jugados?

2. ¿Cómo se distribuyen y concentran los jugadores de alto rendimiento dentro de las plantillas de los clubes, y cuál ha sido su comportamiento ofensivo y consistencia competitiva a lo largo de las temporadas del ciclo 2022-2026?

3. ¿Cuál es el aporte porcentual y el promedio de rendimiento de las diferentes líneas posicionales (arqueros, defensas, mediocampistas y delanteros) dentro de la estructura colectiva de los equipos durante el período 2022-2026?

## Fuente de los datos

Los datos provienen del conjunto público de Kaggle [SQL Practice: Football Players](https://www.kaggle.com/datasets/tomersolo/sql-practice-football-players): una base relacional normalizada de 17 tablas y 855.439 registros, con 27.343 jugadores, 108.639 registros jugador-temporada y 26.949 lesiones entre las temporadas 2022/23 y 2025/26.

### Limitaciones

- **Temporadas fabricadas:** en la base de datos, las temporadas 2022/23 a 2024/25 están marcadas como fabricadas y solo 2025/26 corresponde a registros originales. La estabilidad observada entre temporadas no debe interpretarse como una tendencia real.
- **Estudio descriptivo:** no se aplicaron pruebas de hipótesis ni modelos predictivos, por lo que los resultados describen asociaciones y no relaciones de causa y efecto.
- **Plantillas incompletas:** la base no contiene plantillas completas (mediana de 10 jugadores registrados por club y temporada).

## Tecnologías y arquitectura

- **Streamlit:** aplicación web de varias páginas.
- **DuckDB / MotherDuck:** base analítica (OLAP) usada para la investigación. Contiene las tablas de origen, 3 vistas analíticas y 6 tablas desnormalizadas de dimensiones y hechos. Se usa DuckDB local en desarrollo y MotherDuck en la aplicación desplegada.
- **Supabase (PostgreSQL):** aloja la base original totalmente normalizada (3FN); se usa únicamente para el Cuestionario SQL.
- **Pandas y NumPy:** filtrado y cálculo de indicadores (Gini, HHI, coeficiente de variación).
- **Plotly:** visualizaciones interactivas.

## Estructura del proyecto

```
.
├── app.py                          # Página de inicio: introducción, objetivos y alcance
├── pages/                          # Una página por apartado de la investigación
│   ├── marco_teorico.py            # Conceptos, antecedentes, glosario y referencias
│   ├── marco_metodologico.py       # Enfoque, población, fórmulas y operacionalización
│   ├── analisis_de_lesiones.py     # Objetivo 1: lesiones, antropometría y minutos
│   ├── concentracion_de_talento.py # Objetivo 2: jugadores élite, Gini, Lorenz y HHI
│   ├── analisis_posicional.py      # Objetivo 3: aporte y rendimiento por línea
│   ├── conclusiones.py             # Respuesta al objetivo general
│   ├── simulador_de_plantilla.py   # Armado de un once titular y sus métricas
│   └── queries.py                  # Cuestionario SQL (6 consultas)
├── components/                     # Piezas de interfaz del simulador
│   ├── simulador_ui.py             # Encabezado, filtros, selección de jugadores y KPIs
│   └── cancha_tactica.py           # Dibujo de la cancha con la alineación
├── database/
│   ├── DB.py                       # Conexión a DuckDB / MotherDuck y a Supabase
│   ├── Query.py                    # Consulta de rendimiento usada por el simulador
│   ├── views.sql                   # Vistas analíticas (analytics_*)
│   └── desnormalizacion-olap.sql   # Tablas de dimensiones y hechos (dim_*, fact_*)
├── models/
│   ├── UI.py                       # Configuración de página y menú lateral
│   └── Graphics.py
├── utils/
│   ├── estilos.py                  # Estilos CSS compartidos
│   └── graficos.py                 # Tema de Plotly y gráficos del simulador
├── powerbi/                        # Proyecto de Power BI (.pbip)
├── .streamlit/config.toml          # Tema visual de la aplicación
├── env-template                    # Plantilla de variables de entorno
├── requirements.txt                # Dependencias de Python
└── evaluacion_sql_futbol_formulario_G12.docx  # Enunciado del cuestionario SQL
```

## Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Vincent893/analisis-estadistico-de-lesiones-y-rendimiento-en-el-futbol.git
   cd analisis-estadistico-de-lesiones-y-rendimiento-en-el-futbol
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:** copiar `env-template` como `.env` y completar los valores.
   ```bash
   cp env-template .env
   ```

   | Variable | Descripción |
   | :--- | :--- |
   | `DEV_MODE` | `true` usa un archivo DuckDB local en `database/database.duckdb`; `false` se conecta a MotherDuck. |
   | `DB_CONNECTION_URL` | Cadena de conexión a MotherDuck (necesaria con `DEV_MODE=false`). |
   | `SUPABASE_URL` | URL del proyecto de Supabase, usado por el Cuestionario SQL. |
   | `SUPABASE_KEY` | Clave de acceso del proyecto de Supabase. |

5. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

## Equipo

**Integrantes (Grupo 12):**

- Vicente Diaz
- Juan Hernandez
- Carlos Nuñez
- Mariangela Laya
- Anyimar Castillo
- Marco Ramirez

**Profesores:** Jesus Ochoa y Oliver Triveño

**Materia:** Computación 2 · Escuela de Estadística y Ciencias Actuariales · Universidad Central de Venezuela
