import streamlit as st
import pandas as pd
import os
import sys

# Configuración de rutas
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.append(base_path)

from modulos.finanzas import GestorFinanciero
from modulos.biomonitor import BiomonitorGlucosa

finanzas = GestorFinanciero()
salud = BiomonitorGlucosa()

st.set_page_config(page_title="Quevedo Smart System", layout="wide")
st.title("🤖 Quevedo Smart System")

menu = st.sidebar.radio("Menú", ["Resumen", "Finanzas", "Salud"])

if menu == "Resumen":
    res = finanzas.obtener_balance_total()
    st.metric("Balance Neto", f"$ {res['ahorro_neto']:,.2f}")
    
    ultimo = salud.obtener_ultimo_registro()
    # SEMÁFORO DE SALUD
    if ultimo == 0:
        st.warning("No hay registros de salud hoy.")
    elif ultimo < 70 or ultimo > 140:
        st.error(f"⚠️ Alerta: Glucosa fuera de rango ({ultimo} mg/dL)")
    else:
        st.success(f"✅ Glucosa estable ({ultimo} mg/dL)")

elif menu == "Finanzas":
    st.header("💰 Gestión de Finanzas")
    # BARRA DE BÚSQUEDA
    busqueda = st.text_input("🔍 Buscar en transacciones...")
    
    df_fin = finanzas.listar_transacciones() # <--- LA FUNCIÓN CLAVE
    
    if not df_fin.empty:
        if busqueda:
            df_fin = df_fin[df_fin.astype(str).apply(lambda x: busqueda.lower() in x.str.lower()).any(axis=1)]
        st.dataframe(df_fin, use_container_width=True)

elif menu == "Salud":
    st.header("🩸 Monitor de Salud")
    df_salud = salud.obtener_historial()
    st.dataframe(df_salud, use_container_width=True)
