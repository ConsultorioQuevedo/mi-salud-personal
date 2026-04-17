import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importación de los núcleos refactorizados
from modulos.finanzas import GestorFinanciero
from modulos.biomonitor import BiomonitorGlucosa
from modulos.escaner import EscanerInteligente
from modulos.asistente import AsistenteInteligenteQuevedo

# --- Configuración de la Experiencia de Usuario ---
st.set_page_config(
    page_title="Quevedo OS - Sistema Inteligente",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para la "Limpieza Visual"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- Inicialización de Motores Reales ---
@st.cache_resource
def inicializar_sistemas():
    return {
        "finanzas": GestorFinanciero(),
        "salud": BiomonitorGlucosa(),
        "ia": AsistenteInteligenteQuevedo(),
        "escaner": EscanerInteligente()
    }

motores = inicializar_sistemas()

# --- Título y Encabezado ---
st.title("🤖 Asistente Inteligente Integral")
st.caption(f"Conectado a 'base_datos_quevedo.db' | {datetime.now().strftime('%d/%m/%Y')}")

# --- Panel Lateral (Entrada de Datos Unificada) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
    st.header("Centro de Control")
    
    modulo = st.selectbox("Seleccionar Módulo", ["Finanzas", "Salud (Glucosa)", "Escáner IA"])
    
    with st.form("registro_datos"):
        if modulo == "Finanzas":
            tipo_f = st.radio("Tipo", ["Ingreso", "Gasto"])
            monto = st.number_input("Monto (€)", min_value=0.0, step=10.0)
            cat = st.text_input("Categoría", "Varios")
            desc = st.text_input("Descripción")
            
        elif modulo == "Salud (Glucosa)":
            monto = st.number_input("Nivel Glucosa (mg/dL)", min_value=0, max_value=500)
            momento = st.selectbox("Momento", ["Ayunas", "Post-Prandial", "Antes de dormir"])
            
        elif modulo == "Escáner IA":
            archivo = st.file_uploader("Subir Documento", type=['jpg', 'png', 'pdf'])
            monto = 0 # Placeholder para el botón

        submit = st.form_submit_button("🚀 Ejecutar Acción")

# --- Lógica de Procesamiento ---
if submit:
    if modulo == "Finanzas":
        motores["finanzas"].registrar_transaccion(tipo_f.lower(), monto, cat, desc)
        st.success("💰 Finanzas actualizadas.")
    
    elif modulo == "Salud (Glucosa)":
        estado, mensaje = motores["salud"].interpretar_nivel(monto)
        motores["salud"].registrar_medicion(monto, estado)
        st.info(mensaje)
        
    elif modulo == "Escáner IA" and archivo:
        with st.spinner("Procesando con IA..."):
            # Simulamos el guardado y proceso del escaner refactorizado
            info = motores["escaner"].clasificar_y_extraer(f"Factura detectada en {archivo.name}")
            st.json(info)

# --- Visualización de Datos (Dashboard 360°) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔎 Monitor de Actividad Reciente")
    # Extraemos datos reales de la DB para el DataFrame
    try:
        with motores["finanzas"]._conectar() as conn:
            df_fin = pd.read_sql_query("SELECT fecha, tipo, monto, categoria FROM transacciones ORDER BY fecha DESC LIMIT 10", conn)
            st.dataframe(df_fin, use_container_width=True)
    except:
        st.info("No hay transacciones registradas aún.")

with col2:
    st.subheader("📊 Métricas de Estado")
    bal = motores["finanzas"].obtener_balance_total()
    st.metric("Ahorro Neto", f"{bal.get('ahorro_neto', 0):.2f} €", delta=f"{bal.get('ingreso', 0)} total")
    
    resumen_salud = motores["salud"].obtener_resumen_semanal() if hasattr(motores["salud"], 'obtener_resumen_semanal') else {}
    st.metric("Promedio Glucosa", f"{resumen_salud.get('promedio', 0)} mg/dL")

# --- Sección de Inteligencia Predictiva ---
st.divider()
st.subheader("🔮 Proyecciones del Asistente IA")

col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    if st.button("Analizar Tendencia Financiera"):
        pred = motores["ia"].predecir_tendencia("finanzas")
        if pred:
            st.write(f"Previsión para el próximo periodo: **{pred:.2f} €**")
            st.progress(min(max(pred/5000, 0.0), 1.0))

with col_ia2:
    if st.button("Analizar Tendencia de Salud"):
        pred_s = motores["ia"].predecir_tendencia("glucosa")
        if pred_s:
            st.write(f"Nivel de glucosa estimado: **{pred_s:.2f} mg/dL**")
            if pred_s > 140: st.warning("Tendencia al alza detectada.")
            else: st.success("Tendencia estable.")
