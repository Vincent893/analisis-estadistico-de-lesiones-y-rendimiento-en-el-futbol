import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

PALETA_APP = [
    "#00E5FF",   # cian principal
    "#10B981",   # verde
    "#00A8CC",   # cian oscuro
    "#3B82F6",   # azul
    "#F59E0B",   # ámbar
    "#EC4899",   # rosa
]

COLOR_TEXTO = "#F8FAFC"
COLOR_TEXTO_SUAVE = "#94A3B8"
COLOR_GRID = "rgba(0, 229, 255, 0.1)"
COLOR_LINEA_EJE = "rgba(0, 229, 255, 0.3)"
NOMBRE_TEMA = "futbol_cian"


def registrar_tema():
    """Registra el template de la app y lo asigna como default de Plotly.

    Se llama una sola vez, al importar este módulo, y a partir de ahí
    cualquier figura creada en cualquier página hereda el estilo base.
    """
    pio.templates[NOMBRE_TEMA] = go.layout.Template(
        layout=go.Layout(
            # Paleta: Plotly toma el color de cada categoría aquí por orden
            colorway=PALETA_APP,
            # Fondos transparentes para integrarse al fondo de la app
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            # Tipografía general
            font=dict(color=COLOR_TEXTO, family="sans-serif"),
            # Leyenda flotante sobre el fondo oscuro de la app
            legend=dict(
                font=dict(color="#E2E8F0"),
                bgcolor="rgba(11, 19, 43, 0.7)",
                bordercolor="rgba(0, 229, 255, 0.2)",
                borderwidth=1,
            ),
            # Estilos de ejes (también aplica a eje secundario via bootstrap)
            xaxis=dict(
                gridcolor=COLOR_GRID,
                linecolor=COLOR_LINEA_EJE,
                tickfont=dict(color=COLOR_TEXTO_SUAVE),
                title_font=dict(color="#E2E8F0"),
            ),
            yaxis=dict(
                gridcolor=COLOR_GRID,
                linecolor=COLOR_LINEA_EJE,
                tickfont=dict(color=COLOR_TEXTO_SUAVE),
                title_font=dict(color="#E2E8F0"),
            ),
            margin=dict(l=20, r=20, t=50, b=20),
        )
    )
    # Confirmamos que px y todas las figuras nuevas usen el template,
    # ANTES de que se creen las figuras (por eso es a nivel de módulo).
    px.defaults.template = NOMBRE_TEMA
    pio.templates.default = NOMBRE_TEMA


registrar_tema()


def apply_theme(fig, title=""):
    """Ajusta detalles puntuales de una figura sobre el tema base.
    """
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color="#FFFFFF", size=16, family="sans-serif"),
                x=0.0,
                xanchor="left",
            )
        )
    return fig
