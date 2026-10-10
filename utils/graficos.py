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
