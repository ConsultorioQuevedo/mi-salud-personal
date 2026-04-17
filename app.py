import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Configuración de rutas
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.append(base_path)

try:
    from modulos.finanzas import GestorFinanciero
    from modulos.biomonitor import BiomonitorGlucosa
    
    finanzas = GestorFinanciero()
    salud = BiomonitorGlucosa()
except Exception as e:
    st.error(f"Error de importación: {e}")
    st.stop()

st.set_page_config(page_title="Quevedo Smart System", layout="wide")

# --- INTERFAZ ---
st.title("🤖 Quevedo Smart System")
menu = st.sidebar.radio("Navegación", ["📊 Panel General", "💰 Finanzas", "🩸 Salud"])

if menu == "📊 Panel General":
    col1, col2 = st.columns(2)
    with col1:
        resumen = finanzas.obtener_balance_total()
        st.metric("Balance Neto", f"$ {resumen['ahorro_neto']:,.2f}")
    with col2:
        ultimo = salud.obtener_ultimo_registro()
        # Semáforo de salud
        color = "normal" if 70 <= ultimo <= 140 else "inverse"
        st.metric("Última Glucosa", f"{ultimo} mg/dL", delta_color=color)

elif menu == "💰 Finanzas":
    st.header("💰 Gestión Financiera")
    
    with st.expander("➕ Nueva Transacción"):
        c1, c2, c3 = st.columns(3)
        t = c1.selectbox("Tipo", ["Ingreso", "Gasto"])
        m = c2.number_input("Monto", min_value=0.0)
        cat = c3.text_input("Categoría (ej. Comida, Nómina)")
        desc = st.text_input("Descripción")
        if st.button("Guardar"):
            finanzas.registrar_transaccion(t, m, cat, desc)
            st.success("Registrado correctamente")
            st.rerun()

    st.subheader("🔍 Historial de Movimientos")
    busqueda = st.text_input("Filtrar por descripción o categoría")
    df_fin = finanzas.listar_transacciones()
    
    if not df_fin.empty:
        if busqueda:
            df_fin = df_fin[df_fin.astype(str).apply(lambda x: busqueda.lower() in x.str.lower()).any(axis=1)]
        st.dataframe(df_fin, use_container_width=True)

elif menu == "🩸 Salud":
    st.header("🩸 Monitor de Salud")
    
    with st.expander("💉 Registrar Glucosa"):
        n = st.number_input("Nivel (mg/dL)", min_value=0)
        notase = st.text_input("Nota (ej. Ayunas, Post-comida)")
        if st.button("Guardar Lectura"):
            salud.registrar_lectura(n, notase)
            st.success("Lectura guardada")
            st.rerun()

    st.subheader("📈 Historial de Salud")
    df_salud = salud.obtener_historial()
    if not df_salud.empty:
        st.line_chart(df_salud.set_index('Fecha')['Nivel'])
        st.dataframe(df_salud, use_container_width=True)
