import pandas as pd
import re
import unicodedata
import os
import streamlit as st

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Obtenemos la ruta absoluta para evitar errores en el servidor
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

def fecha_formato_largo(fecha):
    """Formato de fecha largo para los resultados."""
    if pd.isna(fecha):
        return "FECHA NO DISPONIBLE"
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{fecha.day} DE {meses[fecha.month - 1].upper()} DE {fecha.year}"

@st.cache_data
def cargar_dataframe():
    """Carga los Excel y realiza la unión de datos."""
    # 1. Cargar Municipios
    df_muni = None
    if os.path.exists(MUNICIPIOS_FILE):
        try:
            # Leemos columnas A y C (0 y 2) como en tu Flask original
            df_muni = pd.read_excel(MUNICIPIOS_FILE, usecols=[0, 2], header=None)
            df_muni.columns = ['Clave_Original', 'Entidad_Corregida']
            df_muni['Clave_Original'] = df_muni['Clave_Original'].astype(str).str.strip().str.upper()
        except Exception as e:
            print(f"Error municipios: {e}")

    # 2. Cargar Base Principal
    if not os.path.exists(DATA_FILE):
        return None

    try:
        df = pd.read_excel(DATA_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df.dropna(subset=['Fecha'], inplace=True)

        # Merge con municipios
        if df_muni is not None:
            df['Sjto300_Merge'] = df['Sjto300'].astype(str).str.strip().str.upper()
            df_merged = df.merge(df_muni, left_on='Sjto300_Merge', right_on='Clave_Original', how='left')
            df['Sjto300'] = df_merged['Entidad_Corregida'].combine_first(df['Sjto300'])
            df.drop(columns=['Sjto300_Merge'], inplace=True, errors='ignore')

        # Pre-normalizar para búsqueda
        df['nombreReceptor_normalizado'] = df['nombreReceptor'].apply(normalizar_nombre)
        return df
    except Exception as e:
        st.error(f"Error al cargar Excel: {e}")
        return None

# Carga inicial
df = cargar_dataframe()

def validar_rfc(rfc):
    rfc = rfc.strip().upper()
    pf = r'^[A-ZÑ&]{4}[0-9]{6}[A-Z0-9]{3}$'
    pm = r'^[A-ZÑ&]{3}[0-9]{6}[A-Z0-9]{3}$'
    return bool(re.match(pf, rfc) or re.match(pm, rfc))

def buscar_datos(query):
    if df is None: return "Base de datos no cargada.", None
    query = query.strip().upper()
    
    if validar_rfc(query):
        filtrado = df[df['ReceptorRFC'] == query]
    else:
        filtrado = df[df['nombreReceptor_normalizado'] == normalizar_nombre(query)]
    
    if filtrado.empty: return "No se encontraron datos.", None

    # Procesar registros (Consolidar periodos)
    nombre = filtrado['nombreReceptor'].iloc[0]
    grupos = filtrado.groupby('departamento')
    registros = []
    for dept, datos in grupos:
        entidad = datos['Sjto300'].iloc[0]
        puesto = datos['puesto'].iloc[0]
        periodo = f"{fecha_formato_largo(datos['fechaInicialPago'].min())} A {fecha_formato_largo(datos['fechaFinalPago'].max())}"
        registros.append({"Nombre": nombre, "Entidad": entidad, "Dependencia": dept, "Puesto": puesto, "Periodo": periodo})
    
    return "Consulta realizada con éxito.", pd.DataFrame(registros)
