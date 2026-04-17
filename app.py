import streamlit as st
import os
from data_manager import buscar_datos, df

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="centered"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    :root {
        --color-principal-oscuro: #00304F;
        --color-acento-fuerte: #FF5E12;
    }
    .orange-bar {
        background-color: var(--color-acento-fuerte);
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 40px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    h1 { color: var(--color-principal-oscuro) !important; text-align: center; }
    .stButton>button {
        background-color: var(--color-principal-oscuro) !important;
        color: white !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA (Logo y Barra) ---
st.markdown('<div class="orange-bar">', unsafe_allow_html=True)
# Intentamos cargar el logo desde la carpeta static
if os.path.exists("static/Logo.png"):
    col_vacia, col_logo = st.columns([4, 1])
    with col_logo:
        st.image("static/Logo.png", width=120)
st.markdown('</div>', unsafe_allow_html=True)

st.title("🔍 Consulta de Servidores Públicos")

# --- FORMULARIO DE BÚSQUEDA ---
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Búsqueda", placeholder="Ingrese RFC o Nombre Completo", label_visibility="collapsed").strip().upper()
    with col2:
        buscar = st.button("Buscar")

# --- LÓGICA DE RESULTADOS ---
if buscar or query:
    if df is None:
        st.error("Error: No se pudo cargar la base de datos de servidores.")
    elif not query:
        st.warning("Por favor, ingrese un término de búsqueda.")
    else:
        mensaje, resultados_df = buscar_datos(query)
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            st.subheader(f"👤 {resultados_df['Nombre'].iloc[0]}")
            st.table(resultados_df)
        else:
            st.error(mensaje)

st.markdown("---")
st.caption("© 2026 Sistema de Consulta Institucional - ASEG")
