import streamlit as st
import os
import base64
from data_manager import buscar_datos, df

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="wide"
)

# Función para convertir imagen local a base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_b64 = get_base64_image(os.path.join(BASE_DIR, 'static', 'Logo.png'))

# --- 2. CSS PARA CLONAR TU DISEÑO ---
st.markdown(f"""
    <style>
    /* 1. Eliminar márgenes de la app para que la barra naranja toque los bordes */
    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
    }}
    
    header {{
        display: none !important;
    }}

    /* 2. Barra Naranja Superior */
    .header-aseg {{
        background-color: #FF5E12;
        width: 100%;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 50px;
        margin: 0;
    }}

    /* 3. CONTENEDOR DE LA TARJETA (Aquí está el truco del ancho) */
    .main-card {{
        max-width: 900px; /* Ancho máximo igual a tu diseño original */
        margin: 50px auto; /* Centra la tarjeta y le da aire arriba */
        padding: 40px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    h1 {{
        color: #00304F;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 600;
    }}

    /* Estilo del input y botón */
    .stButton>button {{
        background-color: #00304F !important;
        color: white !important;
        height: 3em;
    }}

    /* Ajuste para que la tabla no se desborde */
    .stTable {{
        width: 100%;
    }}
    </style>
    
    <div class="header-aseg">
        <img src="data:image/png;base64,{logo_b64}" height="45">
    </div>
    """, unsafe_allow_html=True)

# --- 3. CUERPO DE LA APP (DENTRO DE LA TARJETA) ---
# Usamos el div 'main-card' para que todo lo que sigue esté centrado y con sombra
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<h1>🔍 Consulta de Servidores Públicos</h1>', unsafe_allow_html=True)

# Contenedor de búsqueda
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Buscador", 
            placeholder="Ingrese RFC o Nombre Completo", 
            label_visibility="collapsed"
        ).strip().upper()
    with col2:
        buscar = st.button("Buscar")

# Lógica de resultados
if buscar or query:
    if df is not None:
        mensaje, resultados_df = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.markdown(f"<h2 style='color:#362D32; border-bottom: 2px solid #D6D6D6; padding-bottom: 10px;'>{resultados_df['Nombre'].iloc[0]}</h2>", unsafe_allow_html=True)
            st.table(resultados_df)
        else:
            st.error(mensaje)
    else:
        st.error("Error al cargar la base de datos.")

st.markdown('</div>', unsafe_allow_html=True) # Cerramos main-card

# Pie de página
st.markdown("<br><center style='color:#666;'>© 2026 Sistema de Consulta Institucional - ASEG</center>", unsafe_allow_html=True)
