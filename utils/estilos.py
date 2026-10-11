import streamlit as st

def cargar_estilos():
    """ Funcion para importar el estilo global de la app en cualquier pagina"""
    st.markdown("""
        <style>
        /* Fondo general de la aplicación  */
        .stApp {
            background-color: #070F18;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 229, 255, 0.04) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 168, 204, 0.04) 0%, transparent 40%),
                linear-gradient(rgba(7, 15, 24, 0.95), rgba(7, 15, 24, 0.95)),
                repeating-linear-gradient(0deg, transparent, transparent 50px, rgba(0, 229, 255, 0.01) 50px, rgba(0, 229, 255, 0.01) 51px);
        }

        /* Personalización del Sidebar*/
        [data-testid="stSidebar"] {
            background-color: #0B132B !important;
            border-right: 1px solid rgba(0, 229, 255, 0.15);
        }
        [data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }

        /* Cabecera Principal */
        .hero-header {
            background: linear-gradient(135deg, #0B132B 0%, #1C2541 60%, #00A8CC 100%);
            border: 1px solid rgba(0, 229, 255, 0.3);
            padding: 35px;
            border-radius: 16px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 229, 255, 0.15);
            position: relative;
            overflow: hidden;
        }
        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #FFFFFF !important;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .hero-badge {
            background: linear-gradient(90deg, #00A8CC, #00E5FF);
            color: #070F18;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
            margin-bottom: 12px;
        }

        /* Tarjetas KPI Futuristas con efecto Glassmorphism */
        .kpi-card {
            background: rgba(11, 19, 43, 0.7);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-top: 3px solid #00E5FF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .kpi-card:hover {
            border-color: #00E5FF;
            box-shadow: 0 6px 25px rgba(0, 229, 255, 0.25);
            transform: translateY(-3px);
        }
        .kpi-title {
            color: #94A3B8;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }
        .kpi-value {
            color: #FFFFFF;
            font-size: 1.8rem;
            font-weight: 800;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        }
        .kpi-footer {
            color: #00E5FF;
            font-size: 0.75rem;
            margin-top: 8px;
            font-weight: 500;
        }

        /* Contenedores de secciones */
        .section-container {
            background: rgba(11, 19, 43, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 25px;
            margin-top: 25px;
            backdrop-filter: blur(10px);
        }
        
        h3 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

