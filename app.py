import streamlit as st
import sqlite3
# Importamos tus motores (asegúrate que los nombres coincidan con tus archivos)
from modulos import finanzas 
# de ser necesario, importar biomonitor aquí también

# 1. CONFIGURACIÓN "NIVEL DIOS" (Debe ser la primera línea de código)
st.set_page_config(page_title="Sistema Quevedo", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILO VISUAL (Para que se vea como App profesional en el celular)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .stMetric { background-color: #f8f9fa; border: 1px solid #e0e0e0; padding: 15px; border-radius: 15px; }
    [data-testid="stSidebar"] { background-color: #111827; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Búsqueda y Filtros)
with st.sidebar:
    st.title("⚙️ Panel Control")
    busqueda = st.text_input("🔍 Buscador Universal", placeholder="¿Qué deseas buscar?")
    st.divider()
    if st.button("🧹 Limpiar Filtros"):
        st.rerun()

# 4. CUERPO PRINCIPAL (Interfaz Limpia)
st.title("🛡️ Sistema Quevedo")

# Fila de Métricas (Aquí conectarás finanzas.obtener_balance() etc.)
m1, m2 = st.columns(2)
with m1:
    st.metric("Balance Total", "$ 0.00") # Aquí conectaremos tu motor de finanzas
with m2:
    st.metric("Estado Glucosa", "Estable", delta="Semaforo: Verde")

st.divider()

# 5. HUB DE ACCESOS RÁPIDOS (Botones grandes para celular)
st.subheader("🔗 Accesos Directos")
col_a, col_b = st.columns(2)
col_c, col_d = st.columns(2)

with col_a:
    st.link_button("💊 Farmacia GBC", "https://farmaciagbc.com.do/") 
with col_b:
    st.link_button("🏥 Farmacia Carol/Value", "https://www.farmaciacarol.com/")
with col_c:
    st.link_button("📧 Gmail", "https://mail.google.com/")
with col_d:
    if st.button("📊 Generar PDF (Pronto)"):
        st.info("Función en desarrollo para el siguiente bloque.")

# 6. ESPACIO PARA TABLAS
st.subheader("📝 Registros Recientes")
# Aquí es donde la barra de búsqueda hará su magia filtrando los datos
if busqueda:
    st.write(f"Filtrando resultados para: {busqueda}")
else:
    st.write("Mostrando últimos movimientos...")
