import folium
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pandas as pd

# Cargar datos
df_residuos = pd.read_csv("BD_residuos_sólidos.csv", encoding='latin1', sep=';')
df_ubicaciones = pd.read_csv("BD_ubicacion.csv", encoding='utf-8-sig', sep=';')

# Unir DataFrames por 'DISTRITO'
def preparar_datos(df_residuos, df_ubicaciones):
    df_residuos.columns = df_residuos.columns.str.strip()
    df_ubicaciones.columns = df_ubicaciones.columns.str.strip()
    df = pd.merge(df_residuos, df_ubicaciones, on="DISTRITO", how="inner")
    return df

df = preparar_datos(df_residuos, df_ubicaciones)

# Configuración de Streamlit
st.title("Mapa de Calor: Producción de Residuos Sólidos en el Perú")

# Selección de tipo de residuo
residuo = ["QRESIDUOS_ALIMENTOS", "QRESIDUOS_MALEZA",
        	"QRESIDUOS_OTROS_ORGANICOS", "QRESIDUOS_PAPEL_BLANCO",
            "QRESIDUOS_PAPEL_PERIODICO", "QRESIDUOS_PAPEL_MIXTO",
            "QRESIDUOS_CARTON_BLANCO", "QRESIDUOS_CARTON_MARRON",
            "QRESIDUOS_CARTON_MIXTO", "QRESIDUOS_VIDRIO_TRANSPARENTE",
            "QRESIDUOS_VIDRIO_OTROS_COLORES", "QRESIDUOS_VIDRIOS_OTROS",
            "QRESIDUOS_TEREFLATO_POLIETILENO", "QRESIDUOS_POLIETILENO_ALTA_DENSIDAD",
            "QRESIDUOS_POLIETILENO_BAJA_DENSIDAD", "QRESIDUOS_POLIPROPILENO",
            "QRESIDUOS_POLIESTIRENO", "QRESIDUOS_POLICLORURO_VINILO", "QRESIDUOS_TETRABRICK",
            "QRESIDUOS_LATA", "QRESIDUOS_METALES_FERROSOS",	
            "QRESIDUOS_ALUMINIO","QRESIDUOS_OTROS_METALES",
            "QRESIDUOS_BOLSAS_PLASTICAS", "QRESIDUOS_SANITARIOS",
            "QRESIDUOS_PILAS", "QRESIDUOS_TECNOPOR", 
            "QRESIDUOS_INERTES", "QRESIDUOS_TEXTILES",
            "QRESIDUOS_CAUCHO_CUERO", "QRESIDUOS_MEDICAMENTOS", 
            "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS", "QRESIDUOS_OTROS_NO_CATEGORIZADOS"
]

residuo_sel = st.selectbox("Selecciona un tipo de residuo", sorted(residuo))

# Seleccion de año
año = df['PERIODO'].unique()
año_sel = st.selectbox("Selecciona un año", sorted(año))

# Crear el mapa de calor
def crear_mapa(df):
    m = folium.Map(location=[-9.189967, -75.015152], zoom_start=5)

    # Filtrar el DataFrame por el año seleccionado
    df_filtrado = df[df['PERIODO'] == año_sel]

    # Convertir columnas a numéricas
    df_filtrado['latitud'] = pd.to_numeric(df_filtrado['latitud'], errors='coerce')
    df_filtrado['longitud'] = pd.to_numeric(df_filtrado['longitud'], errors='coerce')
    df_filtrado[residuo_sel] = pd.to_numeric(df_filtrado[residuo_sel], errors='coerce')

    # Eliminar filas con NaN
    df_filtrado = df_filtrado.dropna(subset=['latitud', 'longitud', residuo_sel])

    # Preparar datos para HeatMap: [latitud, longitud, peso]
    heat_data = df_filtrado[['latitud', 'longitud', residuo_sel]].values.tolist()

    HeatMap(heat_data, radius=15).add_to(m)
    return m


# Mostrar el mapa en Streamlit solo si selecciona un residuo y un año
mapa = crear_mapa(df)
st_folium(mapa, width=700, height=500)
