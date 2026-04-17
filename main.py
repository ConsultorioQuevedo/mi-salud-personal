import sys
import os

# Esto le dice a Python que busque módulos en la carpeta donde está main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from modulos.finanzas import GestorFinanciero
# ... el resto de tus imports


import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Importación de tus módulos core
from modulos.finanzas import GestorFinanciero
from modulos.biomonitor import BiomonitorGlucosa
from modulos.asistente import AsistenteInteligenteQuevedo
from modulos.generador_pdf import GeneradorPDF

# Configuración de la interfaz
st.set_page_config(page_title="Quevedo Smart System", layout="wide", page_icon="🤖")

@st.cache_resource
def cargar_motores():
    return {
        "finanzas": GestorFinanciero(),
        "salud": BiomonitorGlucosa(),
        "ia": AsistenteInteligenteQuevedo(),
        "pdf": GeneradorPDF()
    }

motores = cargar_motores()

st.title("🤖 Centro de Control Inteligente")

# --- BLOQUE DE VISUALIZACIÓN Y LIMPIEZA ---
col_tablas, col_ia = st.columns([2, 1])

with col_tablas:
    tab1, tab2 = st.tabs(["💰 Finanzas", "🩸 Salud"])
    
    with tab1:
        st.subheader("Historial Financiero")
        with motores["finanzas"]._conectar() as conn:
            df_f = pd.read_sql_query("SELECT * FROM transacciones ORDER BY fecha DESC", conn)
        
        if not df_f.empty:
            st.dataframe(df_f, use_container_width=True)
            with st.expander("🗑️ Zona de Limpieza (Finanzas)"):
                id_f = st.number_input("ID a borrar (Finanzas)", min_value=1, step=1, key="del_f")
                if st.button("Eliminar Registro Financiero"):
                    if motores["finanzas"].ejecutar_borrado("transacciones", id_f):
                        st.success(f"ID {id_f} borrado.")
                        st.rerun()
        else:
            st.info("Sin datos financieros.")

    with tab2:
        st.subheader("Historial Glucosa")
        with motores["salud"]._conectar() as conn:
            df_s = pd.read_sql_query("SELECT * FROM registro_glucosa ORDER BY fecha DESC", conn)
        
        if not df_s.empty:
            st.dataframe(df_s, use_container_width=True)
            with st.expander("🗑️ Zona de Limpieza (Salud)"):
                id_s = st.number_input("ID a borrar (Salud)", min_value=1, step=1, key="del_s")
                if st.button("Eliminar Registro de Salud"):
                    if motores["salud"].ejecutar_borrado("registro_glucosa", id_s):
                        st.success(f"ID {id_s} borrado.")
                        st.rerun()
        else:
            st.info("Sin registros médicos.")

# --- BLOQUE DE INTELIGENCIA PREDICTIVA ---
with col_ia:
    st.subheader("🔮 Proyecciones IA")
    if st.button("🔄 Recalcular Tendencias (IA)"):
        motores["ia"].entrenar("finanzas")
        motores["ia"].entrenar("glucosa")
        
        f_pred = motores["ia"].predecir_tendencia("finanzas")
        s_pred = motores["ia"].predecir_tendencia("glucosa")
        
        st.metric("Balance Próximo Mes", f"{f_pred:.2f} €" if f_pred else "N/A")
        st.metric("Nivel Glucosa Est.", f"{s_pred:.2f} mg/dL" if s_pred else "N/A")

# --- BARRA LATERAL: INGRESO Y REPORTES ---
with st.sidebar:
    st.header("📥 Nuevo Registro")
    mod = st.radio("Módulo", ["Finanzas", "Salud"])
    
    if mod == "Finanzas":
        t = st.selectbox("Tipo", ["ingreso", "gasto"])
        m = st.number_input("Monto", min_value=0.0)
        c = st.text_input("Categoría")
        if st.button("Guardar Finanzas"):
            motores["finanzas"].registrar_transaccion(t, m, c)
            st.rerun()
            
    elif mod == "Salud":
        n = st.number_input("Nivel", min_value=0)
        if st.button("Guardar Glucosa"):
            est, _ = motores["salud"].interpretar_nivel(n)
            motores["salud"].registrar_medicion(n, est)
            st.rerun()

    # --- SECCIÓN DE PDF (Nueva) ---
    st.divider()
    st.header("📄 Reportes PDF")
    if st.button("Generar Informe Consolidado"):
        with st.spinner("Creando PDF..."):
            nombre_reporte = f"Reporte_{datetime.now().strftime('%Y%m%d')}.pdf"
            ruta_pdf = motores["pdf"].crear_reporte_mensual(nombre_reporte)
            
            if ruta_pdf and os.path.exists(ruta_pdf):
                with open(ruta_pdf, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF",
                        data=f,
                        file_name=nombre_reporte,
                        mime="application/pdf"
                    )
                st.success("Reporte generado con éxito.")
            else:
                st.error("No se pudo generar el archivo.")
