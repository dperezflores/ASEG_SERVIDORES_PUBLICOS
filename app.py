import streamlit as st
import pandas as pd
import os
from data_manager import buscar_datos, df, cargar_dataframe

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Consulta de Servidores Públicos",
    page_icon="🔍",
    layout="centered"
)

# --- INYECCIÓN DE ESTILO CSS (Tu diseño original) ---
st.markdown(f"""
    <style>
    :root {{
        --color-principal-oscuro: #00304F;
        --color-acento-fuerte: #FF5E12;
        --color-fondo-pagina: #f4f4f9;
    }}
    
    /* Estilo para el Header / Franja Naranja */
    .custom-header {{
        background-color: var(--color-acento-fuerte);
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 40px;
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    
    .logo-img {{
        max-height: 50px;
    }}

    /* Títulos y textos */
    h1 {{
        color: var(--color-principal-oscuro) !important;
        text-align: center;
    }}
    
    /* Personalización de botones de Streamlit para que parezcan los tuyos */
    .stButton>button {{
        background-color: var(--color-principal-oscuro) !important;
        color: white !important;
        width: 100%;
    }}
    </style>
    
    <div class="custom-header">
        <img class="logo-img" src="https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/static/Logo.png" alt="Logo">
    </div>
    """, unsafe_allow_html=True)

# --- INTERFAZ DE USUARIO ---
st.title("🔍 Consulta de Servidores Públicos")

# Formulario de búsqueda
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

# --- LÓGICA DE BÚSQUEDA ---
if buscar or query:
    if df is None:
        st.error("Error: No se pudo cargar la base de datos de servidores.")
    elif not query:
        st.warning("Por favor, ingrese un término de búsqueda.")
    else:
        mensaje, resultados_df = buscar_datos(query)
        
        # Mostrar mensajes de éxito o error
        if "Éxito" in mensaje or "éxito" in mensaje:
            st.success(mensaje)
            
            # Mostrar el nombre como encabezado (como hacías en el HTML)
            nombre_servidor = resultados_df["Nombre"].iloc[0]
            st.subheader(f"👤 {nombre_servidor}")
            
            # Mostrar la tabla de resultados
            # Usamos st.table para que se vea fija y clásica como tu HTML
            st.table(resultados_df)
        else:
            st.error(mensaje)

# Pie de página o información adicional
st.markdown("---")
st.caption("Sistema de Consulta Institucional - ASEG")
