import streamlit.components.v1 as components


def renderizar_cancha_tactica(df_titulares, formacion="4-3-3"):
    """
    Renderiza la cancha táctica interactiva utilizando los jugadores 
    del DataFrame de titulares y la formación seleccionada.
    """
    
   
    coordenadas_formaciones = {
        "4-3-3": {
            "GK": {"top": 88, "left": 50},
            "LB": {"top": 72, "left": 15},
            "CB1": {"top": 75, "left": 38},
            "CB2": {"top": 75, "left": 62},
            "RB": {"top": 72, "left": 85},
            "CM1": {"top": 50, "left": 30},
            "CM2": {"top": 55, "left": 50},
            "CM3": {"top": 50, "left": 70},
            "LW": {"top": 25, "left": 20},
            "ST": {"top": 18, "left": 50},
            "RW": {"top": 25, "left": 80},
        },
        "4-2-3-1": {
            "GK": {"top": 88, "left": 50},
            "LB": {"top": 72, "left": 15},
            "CB1": {"top": 75, "left": 38},
            "CB2": {"top": 75, "left": 62},
            "RB": {"top": 72, "left": 85},
            "DM1": {"top": 62, "left": 38},
            "DM2": {"top": 62, "left": 62},
            "LM": {"top": 38, "left": 20},
            "AM": {"top": 35, "left": 50},
            "RM": {"top": 38, "left": 80},
            "ST": {"top": 18, "left": 50},
        }
    }

    coords = coordenadas_formaciones.get(formacion, coordenadas_formaciones["4-3-3"])

   
    asignacion = {}
    if df_titulares is not None and not df_titulares.empty:
        # Filtrar por categorías o posición principal
        gk = df_titulares[df_titulares['primary_category'] == 'GOALKEEPER']
        defensores = df_titulares[df_titulares['primary_category'] == 'DEFENDER'].reset_index(drop=True)
        mediocampistas = df_titulares[df_titulares['primary_category'] == 'MIDFIELDER'].reset_index(drop=True)
        delanteros = df_titulares[df_titulares['primary_category'] == 'ATTACKER'].reset_index(drop=True)

        if not gk.empty:
            asignacion["GK"] = {
                "nombre": str(gk.iloc[0]['name']), 
                "dorsal": str(gk.iloc[0].get('dorsal', '1'))
            }
        
        def_keys = [k for k in coords.keys() if k.startswith("CB") or k == "LB" or k == "RB"]
        for i, key in enumerate(def_keys):
            if i < len(defensores):
                asignacion[key] = {
                    "nombre": str(defensores.iloc[i]['name']),
                    "dorsal": str(defensores.iloc[i].get('dorsal', i+2))
                }

        mid_keys = [k for k in coords.keys() if k in ["CM1", "CM2", "CM3", "DM1", "DM2", "LM", "AM", "RM"]]
        for i, key in enumerate(mid_keys):
            if i < len(mediocampistas):
                asignacion[key] = {
                    "nombre": str(mediocampistas.iloc[i]['name']),
                    "dorsal": str(mediocampistas.iloc[i].get('dorsal', i+6))
                }

        att_keys = [k for k in coords.keys() if k in ["LW", "ST", "RW"]]
        for i, key in enumerate(att_keys):
            if i < len(delanteros):
                asignacion[key] = {
                    "nombre": str(delanteros.iloc[i]['name']),
                    "dorsal": str(delanteros.iloc[i].get('dorsal', i+9))
                }

    # Este bloque genera dinámicamente el HTML de las fichas de los jugadores según las coordenadas
    html_jugadores = ""
    for pos_key, pos_coords in coords.items():
        jugador = asignacion.get(pos_key, {"nombre": pos_key, "dorsal": "--"})
        nombre = jugador["nombre"]
        # de esta forma acortamos el nombre si es demasiado largo
        nombre_corto = nombre.split(" ")[-1] if len(nombre) > 12 else nombre
        dorsal = jugador["dorsal"]
        
        top = pos_coords["top"]
        left = pos_coords["left"]
        
        html_jugadores += f"""
        <div style="position: absolute; top: {top}%; left: {left}%; transform: translate(-50%, -50%); text-align: center;">
            <div style="width: 38px; height: 38px; background: #111111; border: 2px solid #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 2px auto; color: #ffffff; font-family: sans-serif; font-size: 12px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.4);">{dorsal}</div>
            <div style="background-color: rgba(0, 0, 0, 0.75); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-family: sans-serif; font-size: 10px; font-weight: 600; white-space: nowrap;">{nombre_corto}</div>
        </div>
        """

    # HTML de la estructura de la cancha
    html_total = f"""
    <div style="position: relative; width: 100%; height: 580px; background: linear-gradient(180deg, #2e8b57 0%, #228b22 100%); border-radius: 12px; border: 3px solid #ffffff; overflow: hidden; box-shadow: 0 6px 15px rgba(0,0,0,0.3); margin-bottom: 20px;">
        <!-- Línea central -->
        <div style="position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background-color: rgba(255, 255, 255, 0.7);"></div>
        <!-- Círculo central -->
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100px; height: 100px; border: 2px solid rgba(255, 255, 255, 0.7); border-radius: 50%;"></div>
        <!-- Punto central -->
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 6px; height: 6px; background-color: rgba(255, 255, 255, 0.7); border-radius: 50%;"></div>
        
        {html_jugadores}
    </div>
    """

    components.html(html_total, height=600)