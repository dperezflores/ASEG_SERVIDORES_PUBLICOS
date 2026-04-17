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

# --- 2. INYECCIÓN DE ESTILO CSS (Tu diseño institucional) ---
st.markdown("""
    <style>
    :root {
        --color-principal-oscuro: #00304F;
        --color-acento-fuerte: #FF5E12;
        --color-fondo-pagina: #f4f4f9;
    }
    
    /* Estilo para el Header / Franja Naranja */
    .custom-header {
        background-color: var(--color-acento-fuerte);
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 40px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* Títulos y textos */
    h1 {
        color: var(--color-principal-oscuro) !important;
        text-align: center;
    }
    
    /* Personalización de botones */
    .stButton>button {
        background-color: var(--color-principal-oscuro) !important;
        color: white !important;
        width: 100%;
        border-radius: 6px;
    }
    </style>
    
    <div class="custom-header">
        </div>
    """, unsafe_allow_html=True)

# --- 3. LOGO Y TÍTULO ---
# Aquí es donde va el logo. Usamos columnas para alinearlo a la derecha como en tu CSS original
col_logo_1, col_logo_2 = st.columns([3, 1])
with col_logo_2:
    if os.path.exists("static/Logo.png"):
        st.image("static/Logo.png", width=150)

st.title("🔍 Consulta de Servidores Públicos")

# --- 4. INTERFAZ DE BÚSQUEDA ---
with st.container():
    # Usamos columnas para que el input y el botón estén en la misma línea
    c1, c2 = st.columns([4, 1])
    with c1:
        query = st.text_input(
            "Buscador", 
            placeholder="Ingrese RFC o Nombre Completo", 
            label_visibility="collapsed"
        ).strip().upper()
    with c2:
        boton_buscar = st.button("Buscar")

# --- 5. LÓGICA DE RESULTADOS ---
if boton_buscar or query:
    if df is None:
        st.error("Error: La base de datos no se cargó correctamente.")
    elif not query:
        st.warning("Por favor, ingrese un RFC o Nombre para buscar.")
    else:
        mensaje, resultados_df = buscar_datos(query)
        
        if "éxito" in mensaje.lower():
            st.success(mensaje)
            
            # Nombre del servidor como encabezado
            nombre_servidor = resultados_df["Nombre"].iloc[0]
            st.markdown(f"### 👤 {nombre_servidor}")
            
            # Tabla de resultados (estilo fijo para que se vea como tu HTML)
            st.table(resultados_df)
        else:
            st.error(mensaje)

# Pie de página
st.markdown("---")
st.caption("© 2026 Sistema de Consulta Institucional - ASEG")
