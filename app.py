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

# Función para convertir imagen local a base64 (para que el CSS la vea sí o sí)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_b64 = get_base64_image(os.path.join(BASE_DIR, 'static', 'Logo.png'))

# --- 2. CSS PARA ELIMINAR TODO MARGEN ---
st.markdown(f"""
    <style>
    /* 1. Eliminar márgenes internos de Streamlit */
    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
    }}
    
    /* 2. Eliminar el espacio en blanco superior (Header de Streamlit) */
    header {{
        display: none !important;
    }}

    /* 3. Barra Naranja al 100% real */
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

    /* 4. Contenedor de la búsqueda (Tarjeta blanca centrada) */
    .main-card {{
        max-width: 900px;
        margin: 40px auto;
        padding: 40px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}

    h1 {{
        color: #00304F;
        text-align: center;
        margin-bottom: 30px;
    }}

    .stButton>button {{
        background-color: #00304F !important;
        color: white !important;
        border-radius: 6px;
    }}
    </style>
    
    <div class="header-aseg">
        <img src="data:image/png;base64,{logo_b64}" height="45">
    </div>
    """, unsafe_allow_html=True)

# --- 3. CUERPO DE LA APLICACIÓN ---
# Envolvemos todo en un contenedor centrado
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.title("🔍 Consulta de Servidores Públicos")

with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Buscador", placeholder="Ingrese RFC o Nombre Completo", label_visibility="collapsed").strip().upper()
    with col2:
        buscar = st.button("Buscar")

if buscar or query:
    if df is not None:
        mensaje, resultados_df = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.markdown(f"### 👤 {resultados_df['Nombre'].iloc[0]}")
            st.table(resultados_df)
        else:
            st.error(mensaje)
    else:
        st.error("Error al cargar la base de datos.")

st.markdown('</div>', unsafe_allow_html=True)

# Pie de página
st.markdown("<br><center>© 2026 Sistema de Consulta Institucional - ASEG</center>", unsafe_allow_html=True)
