import pandas as pd
import os
import unicodedata
import re

# Rutas de tus archivos Excel
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'data_Fede.xlsx')
MUNICIPIOS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'TABLA_MUNICIPIOS.xlsx')

df = None

def normalizar_nombre(nombre):
    if pd.isna(nombre) or nombre is None: return ""
    nombre = str(nombre).strip().upper()
    nombre = unicodedata.normalize("NFD", nombre)
    return "".join(c for c in nombre if unicodedata.category(c) != "Mn")

def cargar_dataframe():
    global df
    try:
        # 1. Cargar Municipios (Columna A y C)
        df_muni = pd.read_excel(MUNICIPIOS_FILE, usecols="A,C", header=None, names=['Clave', 'Nombre_Muni'])
        df_muni['Clave'] = df_muni['Clave'].astype(str).str.strip().str.upper()
        df_muni['Nombre_Muni'] = df_muni['Nombre_Muni'].astype(str).str.upper()

        # 2. Cargar Data Principal
        df = pd.read_excel(DATA_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        
        # 3. Unir (Merge) para corregir Entidad
        df['Sjto300_Key'] = df['Sjto300'].astype(str).str.strip().str.upper()
        df = df.merge(df_muni, left_on='Sjto300_Key', right_on='Clave', how='left')
        
        # Reemplazar y limpiar
        df['Sjto300'] = df['Nombre_Muni'].combine_first(df['Sjto300']).str.upper()
        df['nombreReceptor_norm'] = df['nombreReceptor'].apply(normalizar_nombre)
        
        print("✅ Datos cargados correctamente.")
        return df
    except Exception as e:
        print(f"❌ Error al cargar Excel: {e}")
        return None

df = cargar_dataframe()

def buscar_datos(query):
    if df is None: return "Error: Base de datos no lista.", None
    q = query.strip().upper()
    
    # Búsqueda simple (RFC o Nombre)
    filtrado = df[(df['ReceptorRFC'] == q) | (df['nombreReceptor_norm'] == normalizar_nombre(q))]
    
    if filtrado.empty: return "No se encontraron resultados.", None
    
    # Agrupar resultados
    res = []
    for dept, datos in filtrado.groupby('departamento'):
        res.append({
            "Nombre": filtrado['nombreReceptor'].iloc[0],
            "Entidad": datos['Sjto300'].iloc[0],
            "Dependencia": dept,
            "Puesto": datos['puesto'].iloc[0],
            "Periodo": f"{datos['Fecha'].min().strftime('%d/%m/%Y')} A {datos['Fecha'].max().strftime('%d/%m/%Y')}".upper()
        })
    return "Éxito", pd.DataFrame(res)
    
    if filtrado.empty:
        return "No se encontraron datos para la búsqueda.", None
    
    return procesar_registros(filtrado)
