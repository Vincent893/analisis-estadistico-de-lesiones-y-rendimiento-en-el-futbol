import streamlit as st
from models.UI import UI
from utils.estilos import cargar_estilos
from database.DB import DB
from database.Query import get_injury_analysis, get_base_sql
from utils.helper import mostrar_caja_mensaje
from components.lesiones_ui import (
    renderizar_seccion_panorama_general,
    renderizar_seccion_frecuencia_lesiones,
    renderizar_seccion_duracion_lesiones,
    renderizar_seccion_antropometria,
    renderizar_seccion_carga_minutos,
    renderizar_seccion_variables_control,
    renderizar_seccion_top_jugadores,
    renderizar_seccion_real_vs_sintetico,
    renderizar_seccion_conclusion
)


def configurar_pagina():
    UI.setup_page()
    UI.render_sidebar()
    cargar_estilos()


def obtener_conexion_y_consulta():
    conexion_base_datos = DB.get_connection()

    @st.cache_data(show_spinner="Consultando base de datos...", ttl=3600)
    def ejecutar_consulta(clave_consulta):
        return get_injury_analysis(conexion_base_datos, clave_consulta)
        
    return ejecutar_consulta


def renderizar_encabezado():
    st.title("Lesiones, antropometría y carga de minutos")
    st.caption("Temporadas 2022/23 a 2025/26 · Análisis de estadística descriptiva · Fuente: Base de datos centralizada")

    st.markdown(
        "**Objetivo:** describir la frecuencia, duración y distribución de las lesiones entre 2022 y 2026 "
        "y relacionarlas con la altura, el peso y los minutos jugados."
    )
    mostrar_caja_mensaje(
        "alerta", 
        "Nota sobre los datos",
        "Solo la temporada **2025/26 es real**. Las temporadas 2022/23, 2023/24 y 2024/25 están marcadas como "
        "sintéticas (`is_fabricated = 1`). Se incluyen las cuatro porque el objetivo cubre 2022-2026, y en la "
        "sección 8 se compara el patrón real contra el sintético."
    )

    with st.expander("Metodología y consulta base"):
        st.markdown(
            "- **Unidad de análisis:** jugador-temporada (una fila por jugador y temporada).\n"
            "- **Duración de una lesión:** días entre la fecha de inicio y la fecha de fin.\n"
            "- **IMC:** peso (kg) / altura (m)².\n"
            "- **Cuartiles:** C1 agrupa los valores más bajos y C4 los más altos. Los grupos no son del mismo "
            "tamaño porque muchos jugadores comparten la misma altura o peso.\n"
            "- **Medidas de frecuencia:** % de jugadores lesionados y lesiones por 1.000 minutos jugados.\n"
            "- **Medidas de duración:** media, mediana y días por lesión."
        )
        st.code(get_base_sql(), language="sql")


def main():
    configurar_pagina()
    ejecutar_consulta = obtener_conexion_y_consulta()
    
    renderizar_encabezado()
    
    # Secciones
    metricas_panorama = renderizar_seccion_panorama_general(ejecutar_consulta)
    renderizar_seccion_frecuencia_lesiones(ejecutar_consulta)
    renderizar_seccion_duracion_lesiones(ejecutar_consulta)
    cuartiles_altura, cuartiles_peso, cuartiles_imc = renderizar_seccion_antropometria(ejecutar_consulta)
    datos_carga_minutos = renderizar_seccion_carga_minutos(ejecutar_consulta)
    renderizar_seccion_variables_control(ejecutar_consulta)
    renderizar_seccion_top_jugadores(ejecutar_consulta)
    renderizar_seccion_real_vs_sintetico(ejecutar_consulta)
    
    datos_posicion_lesionados = ejecutar_consulta("q13")
    datos_edad_lesionados = ejecutar_consulta("q14")
    datos_tipos_lesion = ejecutar_consulta("q5")
    datos_lesion_lca = datos_tipos_lesion.loc[datos_tipos_lesion["injury_type"] == "ACL tear"].iloc[0]
    
    renderizar_seccion_conclusion(
        metricas_panorama, 
        cuartiles_altura, 
        cuartiles_peso, 
        cuartiles_imc, 
        datos_carga_minutos, 
        datos_posicion_lesionados, 
        datos_edad_lesionados, 
        datos_lesion_lca
    )


if __name__ == "__main__":
    main()