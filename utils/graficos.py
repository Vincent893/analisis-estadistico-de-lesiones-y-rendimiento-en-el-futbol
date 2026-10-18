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