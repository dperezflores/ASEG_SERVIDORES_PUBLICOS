import streamlit as st
import pandas as pd
import os
from data_manager import buscar_datos, df

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="centered"
)

# --- 2. CSS PARA FORZAR EL DISEÑO ---
st.markdown("""
    <style>
    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor Principal */
    .main {
        background-color: #f4f4f9;
    }

    /* Franja Naranja Superior */
    .orange-bar {
        background-color: #FF5E12;
        height: 80px;
        width: 100%;
        border-radius: 0px 0px 10px 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding-right: 20px;
    }

    /* Estilo del Título */
    .titulo-principal {
        color: #00304F;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
        font-size: 40px;
        margin-top: 20px;
    }

    /* Botón de Búsqueda */
    .stButton>button {
        background-color: #00304F !important;
        color: white !important;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO Y ENCABEZADO ---
BASE_DIR_APP = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR_APP, 'static', 'Logo.png')

st.markdown('<div class="orange-bar">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=120)
else:
    # Esto te ayudará a saber si Streamlit NO encuentra el logo
    st.write(f"Logo no encontrado en: {LOGO_PATH}") 
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 class="titulo-principal">🔍 Consulta de Servidores Públicos</h1>', unsafe_allow_html=True)

# --- 4. INTERFAZ DE BÚSQUEDA ---
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Buscador", placeholder="Ingrese RFC o Nombre Completo", label_visibility="collapsed").strip().upper()
    with col2:
        boton = st.button("Buscar")

# --- 5. LÓGICA DE DATOS ---
if boton or query:
    if df is None:
        # Si df es None, intentamos ver por qué
        st.error("⚠️ Error: No se encontraron los archivos en la carpeta 'data/'. Verifica que los archivos .parquet estén en GitHub.")
    elif not query:
        st.warning("Por favor, ingresa un dato para buscar.")
    else:
        mensaje, resultados_df = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.markdown(f"### 👤 {resultados_df['Nombre'].iloc[0]}")
            st.table(resultados_df)
        else:
            st.error(mensaje)

# Pie de página
st.markdown("<br><hr><center>© 2026 Sistema de Consulta Institucional - ASEG</center>", unsafe_allow_html=True)
