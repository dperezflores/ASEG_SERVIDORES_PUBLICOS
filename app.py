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

# Función para logo en base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_b64 = get_base64_image(os.path.join(BASE_DIR, 'static', 'logo.png'))

# --- 2. TODO TU CSS ORIGINAL INYECTADO ---
st.markdown(f"""
    <style>
    /* Reset de Streamlit para permitir diseño 100% */
    .block-container {{ padding: 0rem !important; max-width: 100% !important; }}
    header {{ visibility: hidden; display: none; }}
    footer {{ visibility: hidden; }}
    #root > div:nth-child(1) > div > div > div {{ padding: 0; }}

    /* TUS ESTILOS CSS ORIGINALES */
    :root {{
        --color-principal-oscuro: #00304F;
        --color-acento-fuerte: #FF5E12;
        --color-acento-claro: #FF7D42;
        --color-texto-oscuro: #362D32;
        --color-fondo-claro: #D6D6D6;
        --color-fondo-pagina: #f4f4f9;
        --color-fondo-hover: #57A0D4;
    }}

    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: var(--color-fondo-pagina);
    }}

    #header {{
        background-color: var(--color-acento-fuerte);
        height: 70px;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 40px;
    }}

    #logo-aseg {{ max-height: 50px; width: auto; }}

    .container {{
        max-width: 900px;
        margin: 100px auto;
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }}

    h1 {{ color: var(--color-principal-oscuro); text-align: center; margin-bottom: 30px; font-weight: 600; font-size: 32px; }}

    /* Simulación de tu Formulario con Streamlit */
    .stTextInput > div > div > input {{
        padding: 12px !important;
        border-radius: 6px !important;
        border: 1px solid var(--color-fondo-claro) !important;
        text-transform: uppercase;
    }}

    .stButton > button {{
        background-color: var(--color-principal-oscuro) !important;
        color: white !important;
        padding: 12px 25px !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        height: 48px !important;
        width: 100%;
    }}

    /* Estilos de tus mensajes */
    .message {{ padding: 15px; border-radius: 6px; margin-bottom: 20px; font-weight: bold; text-align: center; border: 1px solid; font-family: sans-serif; }}
    .error-msg {{ background-color: #fce8e6; color: #c5221f; border-color: #f9bdbb; }}
    .success-msg {{ background-color: #e6f4ea; color: #1e8e3e; border-color: #c3e8cd; }}

    /* Tabla de Resultados Original */
    h2 {{ color: var(--color-texto-oscuro); border-bottom: 2px solid var(--color-fondo-claro); padding-bottom: 10px; margin-top: 30px; font-size: 24px; }}
    
    .table-container {{ width: 100%; margin-top: 15px; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }}
    th {{ background-color: var(--color-acento-claro) !important; color: white !important; padding: 12px 15px; text-align: left; text-transform: uppercase; font-size: 14px; }}
    td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid var(--color-fondo-claro); color: #333; }}
    tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>

    <div id="header">
        <img id="logo-aseg" src="data:image/png;base64,{logo_b64}" alt="Logo de ASEG">
    </div>
    """, unsafe_allow_html=True)

# --- 3. ESTRUCTURA HTML DENTRO DEL CONTAINER ---
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1>🔍 Consulta de Servidores Públicos</h1>', unsafe_allow_html=True)

# Recreamos el Formulario (Input + Botón)
col_input, col_btn = st.columns([4, 1])
with col_input:
    query = st.text_input("busqueda", placeholder="Ingrese RFC o Nombre Completo", label_visibility="collapsed").strip().upper()
with col_btn:
    btn_buscar = st.button("Buscar")

# --- LÓGICA DE RESULTADOS ---
if btn_buscar or query:
    if df is not None:
        mensaje, resultados = buscar_datos(query)
        
        # Clase dinámica para el mensaje (Error o Success)
        clase_msg = "error-msg" if ("No se" in mensaje or "Error" in mensaje) else "success-msg"
        st.markdown(f'<p class="message {clase_msg}">{mensaje}</p>', unsafe_allow_html=True)
        
        if resultados is not None:
            # Título con el nombre del servidor (H2)
            st.markdown(f"<h2>{resultados['Nombre'].iloc[0]}</h2>", unsafe_allow_html=True)
            
            # Tabla construida manualmente con HTML para que sea IDÉNTICA
            html_tabla = '<div class="table-container"><table><thead><tr>'
            for col in resultados.columns:
                html_tabla += f'<th>{col}</th>'
            html_tabla += '</tr></thead><tbody>'
            
            for _, row in resultados.iterrows():
                html_tabla += '<tr>'
                for val in row:
                    html_tabla += f'<td>{val}</td>'
                html_tabla += '</tr>'
            html_tabla += '</tbody></table></div>'
            
            st.markdown(html_tabla, unsafe_allow_html=True)
    else:
        st.markdown('<p class="message error-msg">Error: Base de datos no cargada.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Cierre de container
