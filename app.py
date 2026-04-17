import streamlit as st
import os
from data_manager import buscar_datos, df

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="wide" # Cambiamos a wide para facilitar el uso del ancho total
)

# --- 2. CSS AVANZADO (Para forzar el 100% de ancho) ---
st.markdown("""
    <style>
    /* Eliminar márgenes superiores de Streamlit */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100% !important;
    }
    
    /* Forzar la barra naranja al borde superior y 100% de ancho */
    .orange-bar {
        background-color: #FF5E12;
        width: 100vw;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end; /* Logo a la derecha */
        padding-right: 40px;
        margin-bottom: 50px;
        position: relative;
        left: 0;
    }

    .logo-container {
        max-height: 50px;
    }

    /* Centrar el contenido de búsqueda nuevamente */
    .search-box {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    h1 {
        color: #00304F;
        text-align: center;
        font-family: sans-serif;
    }

    .stButton>button {
        background-color: #00304F !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA NARANJA SUPERIOR AL 100% ---
# Usamos un div con el logo directamente para control total
LOGO_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/static/Logo.png"

st.markdown(f"""
    <div class="orange-bar">
        <img src="{LOGO_URL}" height="45">
    </div>
    """, unsafe_allow_html=True)

# --- 4. CONTENEDOR DE BÚSQUEDA ---
# Abrimos un div para dar efecto de "tarjeta" blanca centrada
st.markdown('<div class="search-box">', unsafe_allow_html=True)

st.title("🔍 Consulta de Servidores Públicos")

col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Búsqueda", placeholder="Ingrese RFC o Nombre Completo", label_visibility="collapsed").strip().upper()
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

st.markdown('</div>', unsafe_allow_html=True) # Cerramos search-box

# Pie de página
st.markdown("<br><br><center>© 2026 Sistema de Consulta Institucional - ASEG</center>", unsafe_allow_html=True)
