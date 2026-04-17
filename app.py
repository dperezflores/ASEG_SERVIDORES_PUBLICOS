import streamlit as st
import os
import base64
from data_manager import buscar_datos, df

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="wide" # Wide para permitir que la franja naranja sea del 100%
)

# Función para convertir imagen local a base64 (Garantiza que el logo aparezca)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_b64 = get_base64_image(os.path.join(BASE_DIR, 'static', 'Logo.png'))

# --- 2. INYECCIÓN DE CSS INSTITUCIONAL ---
st.markdown(f"""
    <style>
    /* VARIABLES Y RESET DE MÁRGENES STREAMLIT */
    :root {{
        --color-principal-oscuro: #00304F;
        --color-acento-fuerte: #FF5E12;
        --color-acento-claro: #FF7D42;
        --color-texto-oscuro: #362D32;
        --color-fondo-claro: #D6D6D6;
        --color-fondo-pagina: #f4f4f9;
        --color-fondo-hover: #57A0D4;
    }}

    /* Eliminar contenedores de Streamlit */
    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
        background-color: var(--color-fondo-pagina);
    }}
    
    header {{ visibility: hidden; height: 0; }}
    footer {{ visibility: hidden; }}

    /* CABECERA (FRANJA NARANJA) AL 100% */
    .custom-header {{
        background-color: var(--color-acento-fuerte);
        height: 70px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 40px;
    }}

    .logo-img {{
        max-height: 50px;
    }}

    /* CONTENEDOR TIPO TARJETA (Tu .container de CSS) */
    .main-container {{
        max-width: 900px;
        margin: 110px auto 40px auto; /* 110px para bajarlo de la franja fixed */
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    h1 {{
        color: var(--color-principal-oscuro);
        text-align: center;
        margin-bottom: 30px;
        font-weight: 600;
        font-size: 2rem;
    }}

    /* Estilo del Formulario (Contenedor de búsqueda) */
    .search-row {{
        display: flex;
        gap: 10px;
        margin-bottom: 30px;
        padding: 15px;
        border: 1px solid var(--color-fondo-claro);
        border-radius: 8px;
        background-color: #f7f9fc;
    }}

    /* Botón */
    .stButton>button {{
        background-color: var(--color-principal-oscuro) !important;
        color: white !important;
        border: none !important;
        padding: 12px 25px !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: background-color 0.3s !important;
    }}
    
    .stButton>button:hover {{
        background-color: var(--color-fondo-hover) !important;
    }}

    /* Estilos de Tabla */
    thead tr th {{
        background-color: var(--color-acento-claro) !important;
        color: white !important;
        text-transform: uppercase !important;
        font-size: 14px !important;
    }}

    h2 {{
        color: var(--color-texto-oscuro);
        border-bottom: 2px solid var(--color-fondo-claro);
        padding-bottom: 10px;
        margin-top: 30px;
    }}
    </style>
    
    <div class="custom-header">
        <img class="logo-img" src="data:image/png;base64,{logo_b64}" alt="Logo">
    </div>
    """, unsafe_allow_html=True)

# --- 3. CUERPO DE LA APP ---
# Todo el contenido va dentro del div 'main-container' para respetar el ancho de 900px
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<h1>🔍 Consulta de Servidores Públicos</h1>', unsafe_allow_html=True)

# Simulamos tu 'form' de HTML usando columnas
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Búsqueda", 
            placeholder="Ingrese RFC o Nombre Completo", 
            label_visibility="collapsed"
        ).strip().upper()
    with col2:
        buscar = st.button("Buscar")

# Resultados
if buscar or query:
    if df is not None:
        mensaje, resultados_df = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.markdown(f"<h2>👤 {resultados_df['Nombre'].iloc[0]}</h2>", unsafe_allow_html=True)
            st.table(resultados_df)
        else:
            st.error(mensaje)
    else:
        st.error("Error: La base de datos no está disponible.")

st.markdown('</div>', unsafe_allow_html=True) # Cerramos main-container

# Pie de página fuera del contenedor
st.markdown("<center style='color:#666; font-size:14px;'>© 2026 Sistema de Consulta Institucional - ASEG</center>", unsafe_allow_html=True)
