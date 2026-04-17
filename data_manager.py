import pandas as pd
import re
import unicodedata
import os
import numpy as np
import streamlit as st

# --- 1. CONFIGURACIÓN Y CARGA DE DATOS ---

# Rutas dinámicas para que funcionen en el servidor de GitHub
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'data_Fede.xlsx')
MUNICIPIOS_FILE = os.path.join(BASE_DIR, 'data', 'TABLA_MUNICIPIOS.xlsx')

def normalizar_nombre(nombre):
    """Convierte texto a mayúsculas y elimina acentos."""
    if pd.isna(nombre) or nombre is None:
        return ""
    nombre = str(nombre).strip().upper()
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = "".join(c for c in nombre if unicodedata.category(c) != "Mn")
    return nombre

@st.cache_data
def cargar_dataframe():
    """Carga, enriquece y normaliza el DataFrame principal."""
    df_municipios = None
    
    # 1. Cargar la Tabla de Municipios
    if os.path.exists(MUNICIPIOS_FILE):
        try:
            df_municipios = pd.read_excel(MUNICIPIOS_FILE, 
                                          usecols="A,C", 
                                          header=None, 
                                          names=['Clave_Original', 'Entidad_Corregida'])
            df_municipios['Clave_Original'] = df_municipios['Clave_Original'].astype(str).str.strip().str.upper()
            df_municipios['Entidad_Corregida'] = df_municipios['Entidad_Corregida'].astype(str).str.strip().str.upper()
        except Exception as e:
            st.error(f"Error al cargar municipios: {e}")
    
    # 2. Cargar la Tabla Principal
    if not os.path.exists(DATA_FILE):
        return None
        
    try:
        df = pd.read_excel(DATA_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df.dropna(subset=['Fecha'], inplace=True)
        
        # 3. REALIZAR EL MERGE
        if df_municipios is not None:
            df['Sjto300_Merge'] = df['Sjto300'].astype(str).str.strip().str.upper()
            df_merged = df.merge(df_municipios, left_on='Sjto300_Merge', right_on='Clave_Original', how='left')
            df['Sjto300'] = df_merged['Entidad_Corregida'].combine_first(df['Sjto300'])
            df.drop(columns=['Sjto300_Merge', 'Clave_Original', 'Entidad_Corregida'], inplace=True, errors='ignore')
        
        df['nombreReceptor_normalizado'] = df['nombreReceptor'].apply(normalizar_nombre)
        return df
        
    except Exception as e:
        st.error(f"Error al procesar Excel: {e}")
        return None

# Inicializar la base de datos
df = cargar_dataframe()

# --- 2. VALIDACIÓN Y FORMATO ---
def validar_rfc(rfc):
    rfc = rfc.strip().upper()
    persona_fisica = r'^[A-ZÑ&]{4}[0-9]{6}[A-Z0-9]{3}$'
    persona_moral = r'^[A-ZÑ&]{3}[0-9]{6}[A-Z0-9]{3}$'
    return bool(re.match(persona_fisica, rfc) or re.match(persona_moral, rfc))

def fecha_formato_largo(fecha):
    if pd.isna(fecha): return "Fecha no disponible"
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"

# --- 3. PROCESAMIENTO Y BÚSQUEDA ---
def procesar_registros(filtrado):
    nombre = filtrado['nombreReceptor'].iloc[0]
    grupos = filtrado.groupby('departamento') 
    registros = []

    for dept, datos in grupos:
        entidad = datos['Sjto300'].iloc[0]
        puesto = datos['puesto'].iloc[0] 
        f_inicial = datos['fechaInicialPago'].min()
        f_final = datos['fechaFinalPago'].max()
        periodo = f"{fecha_formato_largo(f_inicial)} a {fecha_formato_largo(f_final)}".upper()

        registros.append({
            "Nombre": nombre, "Entidad": entidad, "Dependencia": dept,
            "Puesto": puesto, "Periodo": periodo
        })

    return "Consulta realizada con éxito.", pd.DataFrame(registros)

def buscar_datos(query):
    if df is None: return "Error interno: Base de datos no cargada.", None
    query = query.strip().upper()
    
    if validar_rfc(query):
        filtrado = df[df['ReceptorRFC'] == query]
    else:
        filtrado = df[df['nombreReceptor_normalizado'] == normalizar_nombre(query)]
    
    if filtrado.empty: return "No se encontraron datos para la búsqueda.", None
    return procesar_registros(filtrado)
