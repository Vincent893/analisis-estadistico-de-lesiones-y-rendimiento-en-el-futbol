import plotly.express as px

class Graphics:
    
    @staticmethod
    def create_talent_donut_chart(df):
        
        grafico_de_pie = px.pie(df, names="Liga", values="Jugadores", hole=0.4)
        grafico_de_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        return grafico_de_pie

    @staticmethod
    def create_position_performance_bar_chart(df):
        
        grafico_de_barra = px.bar(df, x="Posicion", y="Cantidad", color="Posicion", text_auto=True)
        grafico_de_barra.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, showlegend=False)
        return grafico_de_barra

    @staticmethod
    def create_injury_evolution_line_chart(df):
        
        grafico_de_linea = px.line(df, x="Año", y="Total Lesiones", markers=True, line_shape="spline")
        grafico_de_linea.update_traces(line_color="#FF4B4B", line_width=3)
        grafico_de_linea.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
        return grafico_de_linea

    @staticmethod
    def create_top_players_bar_chart(df):
        
        grafico = px.bar(
            df, 
            x="Rating General", 
            y="Jugador", 
            orientation="h", 
            text="Rating General", 
            color="Jugador"
        )
        grafico.update_layout(
            margin=dict(t=10, b=10, l=10, r=10), 
            height=250, 
            yaxis={'categoryorder':'total ascending'}, 
            showlegend=False
        )
        return grafico