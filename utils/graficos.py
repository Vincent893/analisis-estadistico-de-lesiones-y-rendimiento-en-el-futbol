import plotly.express as px



def apply_theme(fig, title=""):
    """Funcion que aplica la paleta de colores de la app a cualquier figura de Plotly."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color="#FFFFFF", size=16, family="sans-serif"),
            x=0.0,
            xanchor="left"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="sans-serif"),
        legend=dict(
            font=dict(color="#E2E8F0"),
            bgcolor="rgba(11, 19, 43, 0.7)",
            bordercolor="rgba(0, 229, 255, 0.2)",
            borderwidth=1
        ),
        colorway=[
            "#00E5FF",   
            "#10B981",   
            "#00A8CC",   
            "#3B82F6",   
            "#F59E0B",  
            "#EC4899"   
        ],
        xaxis=dict(
            gridcolor="rgba(0, 229, 255, 0.1)",
            linecolor="rgba(0, 229, 255, 0.3)",
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#E2E8F0")
        ),
        yaxis=dict(
            gridcolor="rgba(0, 229, 255, 0.1)",
            linecolor="rgba(0, 229, 255, 0.3)",
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#E2E8F0")
        ),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig



#Esta funcion genera un grafico para los promedios y sumatorias colectivas de la plantilla seleccionada.
def calcular_metricas_equipo(lineup_df):
    if lineup_df.empty:
        return {
            "avg_rating": 0.0,
            "total_xg": 0.0,
            "avg_age": 0.0,
            "total_days_lost": 0,
            "total_injuries": 0
        }
        
    return {
        "avg_rating": lineup_df['average_rating'].mean(),
        "total_xg": lineup_df['xg_per_90'].sum(),
        "avg_age": lineup_df['age'].mean(),
        "total_days_lost": lineup_df['total_days_lost'].sum(),
        "total_injuries": lineup_df['total_injuries'].sum()
    }



#Esta funcion crea el gráfico de barras del rating individual de los titulares.
def generar_grafico_rating_titulares(lineup_df):
    fig = px.bar(
        lineup_df, 
        x='name', 
        y='average_rating', 
        color='primary_category',
        title="Calificación Individual del XI Titular",
        labels={'name': 'Jugador', 'average_rating': 'Rating Promedio'}
    )
    fig.update_layout(xaxis_title="", yaxis_title="Rating")
    return fig

def generar_grafico_radar_plantilla(df_titulares):
    if df_titulares is None or df_titulares.empty:
        return px.scatter(title="Sin datos para el radar")

   
    # Rating promedio del equipo (escalado a 10 si viene en formato base 10, o ajustado)
    val_rating = df_titulares['average_rating'].mean() if 'average_rating' in df_titulares.columns else 7.0
    
    # Producción ofensiva basada en xG por 90 (lo escalamos para que 0.5+ xG sea una puntuación alta en el radar)
    val_xg = (df_titulares['xg_per_90'].mean() * 15) if 'xg_per_90' in df_titulares.columns else 5.0
    val_xg = min(10.0, max(0.0, val_xg))

    # Actividad / Frecuencia de juego o aportes 
    val_rendimiento = df_titulares['average_rating'].median() if 'average_rating' in df_titulares.columns else 7.0
    
    # Eficiencia / Menor cantidad de lesiones o mayor consistencia
    val_consistencia = 8.0
    if 'total_injuries' in df_titulares.columns:
        # Menos lesiones históricas / de temporada = mayor puntaje de disponibilidad de rendimiento
        prom_lesiones = df_titulares['total_injuries'].mean()
        val_consistencia = max(4.0, 10.0 - (prom_lesiones * 1.5))

    # Control de balón / aporte colectivo (estimado a partir del rating o métricas auxiliares)
    val_colectivo = (val_rating + val_xg) / 2.0

    
    categorias = [
        'Rating Colectivo', 
        'Potencia Ofensiva (xG)', 
        'Consistencia de Juego', 
        'Disponibilidad (Salud)', 
        'Índice Táctico'
    ]
    
    valores = [
        round(float(val_rating), 2),
        round(float(val_xg), 2),
        round(float(val_rendimiento), 2),
        round(float(val_consistencia), 2),
        round(float(val_colectivo), 2)
    ]

    
    fig = px.line_polar(
        r=valores, 
        theta=categorias,
        line_close=True,
        template="plotly_dark"
    )
    
    fig.update_traces(
        fill='toself', 
        line_color='#2ea043', 
        marker=dict(color='#3fb950', size=8),
        hovertemplate='<b>%{theta}</b>: %{r}<extra></extra>'
    )
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(22, 27, 34, 0.8)',
            radialaxis=dict(visible=True, range=[0, 10], color='#8b949e', showticklabels=True),
            angularaxis=dict(color='#f0f6fc', tickfont=dict(size=10))
        ),
        title=dict(text="Radar de Rendimiento Colectivo (XI Titular)", font=dict(size=14, color="#f0f6fc")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=20, l=30, r=30),
        height=320
    )
    
    return fig