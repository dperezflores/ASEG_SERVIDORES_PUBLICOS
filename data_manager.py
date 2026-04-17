import pandas as pd
import re
import unicodedata
import os
import streamlit as st

# --- CONFIGURACIÓN DE RUTAS DINÁMICAS ---
# Esto obtiene la carpeta actual donde está data_manager.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construimos las rutas uniendo la base con la carpeta 'data'
DATA_PART1 = os.path.join(BASE_DIR, 'data', 'data_Fede_P1.parquet')
DATA_PART2 = os.path.join(BASE_DIR, 'data', 'data_Fede_P2.parquet')
DATA_PART3 = os.path.join(BASE_DIR, 'data', 'data_Fede_P3.parquet')
MUNICIPIOS_FILE = os.path.join(BASE_DIR, 'data', 'TABLA_MUNICIPIOS.parquet')

@st.cache_data
def cargar_todo():
    df_final = None
    df_muni = None

    # 1. Cargar Tabla de Municipios (Lookup)
    if os.path.exists(MUNICIPIOS_FILE):
        try:
            temp_muni = pd.read_parquet(MUNICIPIOS_FILE)
            
            # Tu lógica original decía que usabas la columna A y C (índices 0 y 2)
            # Vamos a extraer solo esas dos sin importar cuántas tenga el archivo
            df_muni = temp_muni.iloc[:, [0, 2]].copy() 
            df_muni.columns = ['Clave_Original', 'Entidad_Corregida']
            
            df_muni['Clave_Original'] = df_muni['Clave_Original'].astype(str).str.strip().str.upper()
            print("Tabla de municipios cargada correctamente.")
        except Exception as e:
            st.error(f"Error al procesar columnas de municipios: {e}")

    # 2. Cargar y Unificar Base de Datos Principal
    try:
        if all(os.path.exists(f) for f in [DATA_PART1, DATA_PART2, DATA_PART3]):
            p1 = pd.read_parquet(DATA_PART1)
            p2 = pd.read_parquet(DATA_PART2)
            p3 = pd.read_parquet(DATA_PART3)
            
            df_final = pd.concat([p1, p2, p3], ignore_index=True)
            
            # Procesamiento de fechas
            df_final['Fecha'] = pd.to_datetime(df_final['Fecha'], errors='coerce')
            df_final.dropna(subset=['Fecha'], inplace=True)

            # Enriquecimiento (Merge)
            if df_muni is not None:
                # Nos aseguramos de que Sjto300 sea string para comparar
                df_final['Sjto300_Merge'] = df_final['Sjto300'].astype(str).str.strip().str.upper()
                
                df_merged = df_final.merge(df_muni, left_on='Sjto300_Merge', right_on='Clave_Original', how='left')
                
                # Reemplazamos y limpiamos
                df_final['Sjto300'] = df_merged['Entidad_Corregida'].combine_first(df_final['Sjto300'])
                df_final.drop(columns=['Sjto300_Merge'], inplace=True, errors='ignore')

            # Normalización para búsqueda
            df_final['nombreReceptor_normalizado'] = df_final['nombreReceptor'].apply(normalizar_nombre)
            return df_final
        else:
            return None
    except Exception as e:
        st.error(f"Error crítico en la unión de datos: {e}")
        return None

# --- 2. FUNCIONES DE APOYO ---

def normalizar_nombre(nombre):
    """Convierte texto a mayúsculas y elimina acentos para una búsqueda flexible."""
    if pd.isna(nombre) or nombre is None:
        return ""
    nombre = str(nombre).strip().upper()
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = "".join(c for c in nombre if unicodedata.category(c) != "Mn")
    return nombre

def fecha_formato_largo(fecha):
    """Convierte un objeto datetime a un formato de texto largo en español."""
    if pd.isna(fecha):
        return "FECHA NO DISPONIBLE"
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return f"{fecha.day} DE {meses[fecha.month - 1].upper()} DE {fecha.year}"

# --- 3. CARGA DE DATOS CON CACHÉ ---

@st.cache_data
def cargar_todo():
    """Carga las 3 partes del archivo principal y la tabla de municipios."""
    df_final = None
    df_muni = None

    # A. Cargar Tabla de Municipios (Lookup)
    if os.path.exists(MUNICIPIOS_FILE):
        try:
            df_muni = pd.read_parquet(MUNICIPIOS_FILE)
            # Forzamos nombres de columnas para que coincidan con la lógica de búsqueda
            df_muni.columns = ['Clave_Original', 'Entidad_Corregida']
            df_muni['Clave_Original'] = df_muni['Clave_Original'].astype(str).str.strip().str.upper()
        except Exception as e:
            st.error(f"Error al cargar tabla de municipios: {e}")

    # B. Cargar y Unificar Base de Datos Principal
    try:
        # Verificamos que existan las 3 partes
        if all(os.path.exists(f) for f in [DATA_PART1, DATA_PART2, DATA_PART3]):
            p1 = pd.read_parquet(DATA_PART1)
            p2 = pd.read_parquet(DATA_PART2)
            p3 = pd.read_parquet(DATA_PART3)
            
            df_final = pd.concat([p1, p2, p3], ignore_index=True)
            
            # Procesamiento de fechas
            df_final['Fecha'] = pd.to_datetime(df_final['Fecha'], errors='coerce')
            df_final.dropna(subset=['Fecha'], inplace=True)

            # Enriquecimiento (Merge con municipios)
            if df_muni is not None:
                df_final['Sjto300_Merge'] = df_final['Sjto300'].astype(str).str.strip().str.upper()
                df_merged = df_final.merge(df_muni, left_on='Sjto300_Merge', right_on='Clave_Original', how='left')
                
                # Reemplazar Sjto300 con el nombre corregido si existe
                df_final['Sjto300'] = df_merged['Entidad_Corregida'].combine_first(df_final['Sjto300'])
                df_final.drop(columns=['Sjto300_Merge'], inplace=True, errors='ignore')

            # Pre-normalizar nombres para que la búsqueda sea instantánea
            df_final['nombreReceptor_normalizado'] = df_final['nombreReceptor'].apply(normalizar_nombre)
            
            return df_final
        else:
            st.error("Error: No se encontraron las 3 partes (.parquet) en la carpeta 'data'.")
            return None
    except Exception as e:
        st.error(f"Error crítico cargando datos: {e}")
        return None

# Cargamos el DataFrame global
df = cargar_todo()

# --- 4. LÓGICA DE NEGOCIO Y BÚSQUEDA ---

def validar_rfc(rfc):
    """Valida formato de RFC (Física/Moral)."""
    rfc = rfc.strip().upper()
    persona_fisica = r'^[A-ZÑ&]{4}[0-9]{6}[A-Z0-9]{3}$'
    persona_moral = r'^[A-ZÑ&]{3}[0-9]{6}[A-Z0-9]{3}$'
    return bool(re.match(persona_fisica, rfc) or re.match(persona_moral, rfc))

def procesar_registros(filtrado):
    """Agrupa registros por departamento para consolidar periodos."""
    nombre_completo = filtrado['nombreReceptor'].iloc[0]
    grupos = filtrado.groupby('departamento') 
    registros = []

    for dept, datos in grupos:
        entidad = datos['Sjto300'].iloc[0]
        puesto = datos['puesto'].iloc[0] 
        
        fecha_inicial = datos['fechaInicialPago'].min()
        fecha_final = datos['fechaFinalPago'].max()

        periodo = (f"{fecha_formato_largo(fecha_inicial)} A {fecha_formato_largo(fecha_final)}")

        registros.append({
            "Nombre": nombre_completo,
            "Entidad": entidad,
            "Dependencia": dept,
            "Puesto": puesto,
            "Periodo": periodo
        })

    return "Consulta realizada con éxito.", pd.DataFrame(registros)

def buscar_datos(query):
    """Función principal llamada desde app.py."""
    if df is None:
        return "Error interno: Base de datos no disponible.", None
    
    query = query.strip().upper()
    
    # Búsqueda por RFC
    if validar_rfc(query):
        filtrado = df[df['ReceptorRFC'] == query]
    # Búsqueda por Nombre (Exacta)
    else:
        nombre_busqueda = normalizar_nombre(query)
        filtrado = df[df['nombreReceptor_normalizado'] == nombre_busqueda]
    
    if filtrado.empty:
        return "No se encontraron datos para la búsqueda.", None
    
    return procesar_registros(filtrado)
