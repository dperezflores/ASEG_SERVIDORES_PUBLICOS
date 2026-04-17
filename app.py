import streamlit as st
import os
from data_manager import buscar_datos, df

st.set_page_config(page_title="Consulta Servidores Públicos", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .orange-bar {
        background-color: #FF5E12;
        height: 70px;
        border-radius: 5px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0 20px;
        margin-bottom: 20px;
    }
    h1 { color: #00304F; text-align: center; }
    .stButton>button { background-color: #00304F !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Encabezado con Logo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, 'static', 'Logo.png')

st.markdown('<div class="orange-bar">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    # Colocamos el logo dentro de la franja naranja usando columnas de Streamlit para el flujo
    col_vacia, col_logo = st.columns([4, 1])
    with col_logo:
        st.image(LOGO_PATH, width=100)
st.markdown('</div>', unsafe_allow_html=True)

st.title("🔍 Consulta de Servidores Públicos")

# Buscador
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Buscador", placeholder="RFC o Nombre", label_visibility="collapsed").strip().upper()
with col2:
    buscar = st.button("Buscar")

if buscar or query:
    if df is not None:
        mensaje, resultados = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.markdown(f"### 👤 {resultados['Nombre'].iloc[0]}")
            st.table(resultados)
        else:
            st.error(mensaje)
    else:
        st.error("Error al cargar la base de datos.")
