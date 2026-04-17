# data_manager.py
import pandas as pd
import re
import unicodedata
import os
import numpy as np

# --- 1. CONFIGURACIÓN Y CARGA DE DATOS ---

# Nota: Asegúrate que estos archivos están en la carpeta 'data/'
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'data_Fede.xlsx')
MUNICIPIOS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'TABLA_MUNICIPIOS.xlsx')

df = None
df_municipios = None

def normalizar_nombre(nombre):
    """Convierte texto a mayúsculas y elimina acentos para una búsqueda flexible."""
    if pd.isna(nombre) or nombre is None:
        return ""
    nombre = str(nombre).strip().upper()
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = "".join(c for c in nombre if unicodedata.category(c) != "Mn")
    return nombre

def cargar_dataframe():
    """Carga, enriquece con la tabla de municipios y pre-normaliza el DataFrame principal."""
    global df_municipios
    
    # 1. Cargar la Tabla de Municipios (Lookup Table)
    if os.path.exists(MUNICIPIOS_FILE):
        try:
            # Asumimos Columnas A (Clave) y C (Nombre Corregido)
            df_municipios = pd.read_excel(MUNICIPIOS_FILE, 
                                          usecols="A,C", 
                                          header=None, # Asumir que no hay encabezado en la primera fila
                                          names=['Clave_Original', 'Entidad_Corregida'])
            
            # Normalizar la clave de búsqueda
            df_municipios['Clave_Original'] = df_municipios['Clave_Original'].astype(str).str.strip().str.upper()
            df_municipios['Entidad_Corregida'] = df_municipios['Entidad_Corregida'].astype(str).str.strip().str.upper()
            print("Tabla de municipios cargada.")
        except Exception as e:
             print(f"Error al cargar la tabla de municipios: {e}")
             df_municipios = None
    
    # 2. Cargar la Tabla Principal
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: Archivo no encontrado en: {DATA_FILE}")
        return None
        
    try:
        df = pd.read_excel(DATA_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df.dropna(subset=['Fecha'], inplace=True)
        
        # 3. REALIZAR EL MERGE (UNIÓN)
        if df_municipios is not None:
            # Crear columna auxiliar para la unión con la clave de la tabla principal
            df['Sjto300_Merge'] = df['Sjto300'].astype(str).str.strip().str.upper()
            
            # Realizar el Left Join
            df_merged = df.merge(df_municipios, 
                                 left_on='Sjto300_Merge', 
                                 right_on='Clave_Original', 
                                 how='left')
            
            # Reemplazar 'Sjto300' (Entidad) con el valor corregido. 
            # Si el merge no encontró coincidencia (NaN), mantiene el valor original de 'Sjto300'.
            df['Sjto300'] = df_merged['Entidad_Corregida'].combine_first(df['Sjto300'])
            
            df.drop(columns=['Sjto300_Merge'], inplace=True, errors='ignore')
            print("Datos principales enriquecidos con nombres de municipios.")
        
        # 4. Normalización del Nombre del Receptor (para búsqueda)
        df['nombreReceptor_normalizado'] = df['nombreReceptor'].apply(normalizar_nombre)
        print("Base de datos de servidores cargada y lista.")
        return df
        
    except Exception as e:
        print(f"Error al cargar o procesar el Excel: {e}")
        return None

# Cargar el DataFrame una sola vez al inicio
df = cargar_dataframe()

# --- 2. VALIDACIÓN ---
def validar_rfc(rfc):
    """Valida si el formato de la cadena corresponde a un RFC (Física o Moral)."""
    rfc = rfc.strip().upper()
    persona_fisica = r'^[A-ZÑ&]{4}[0-9]{6}[A-Z0-9]{3}$'
    persona_moral = r'^[A-ZÑ&]{3}[0-9]{6}[A-Z0-9]{3}$'
    return bool(re.match(persona_fisica, rfc) or re.match(persona_moral, rfc))

def fecha_formato_largo(fecha):
    """Convierte un objeto datetime a un formato de texto largo."""
    if pd.isna(fecha):
        return "Fecha no disponible"
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"

# --- 3. PROCESAMIENTO DE REGISTROS ---
def procesar_registros(filtrado):
    """Agrupa los registros del servidor público por departamento para consolidar periodos."""
    
    nombre = filtrado['nombreReceptor'].iloc[0]

    grupos = filtrado.groupby('departamento') 
    registros = []

    for dept, datos in grupos:
        entidad = datos['Sjto300'].iloc[0] # Contiene el valor corregido/original
        puesto = datos['puesto'].iloc[0] 
        
        fecha_inicial = datos['fechaInicialPago'].min()
        fecha_final = datos['fechaFinalPago'].max()

        periodo = (
            f"{fecha_formato_largo(fecha_inicial)} a "
            f"{fecha_formato_largo(fecha_final)}"
        ).upper()

        registros.append({
            "Nombre": nombre,
            "Entidad": entidad,
            "Dependencia": dept,
            "Puesto": puesto,
            "Periodo": periodo
        })

    return "Consulta realizada con éxito.", pd.DataFrame(registros)

# --- 4. FUNCIÓN DE BÚSQUEDA PRINCIPAL ---
def buscar_datos(query):
    """Determina si buscar por RFC o Nombre y ejecuta la consulta."""
    
    if df is None:
        return "Error interno: Base de datos no cargada.", None
    
    query = query.strip().upper()
    
    # 1. Búsqueda por RFC (Coincidencia Exacta)
    if validar_rfc(query):
        filtrado = df[df['ReceptorRFC'] == query]
    
    # 2. Búsqueda por Nombre (Coincidencia Exacta)
    else:
        nombre_normalizado = normalizar_nombre(query)
        
        # Coincidencia Exacta solicitada por el usuario
        filtrado = df[df['nombreReceptor_normalizado'] == nombre_normalizado]
    
    if filtrado.empty:
        return "No se encontraron datos para la búsqueda.", None
    
    return procesar_registros(filtrado)
