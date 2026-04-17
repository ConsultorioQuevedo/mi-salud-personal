
import pandas as pd
import os
import sys
from datetime import datetime

# ==========================================
# REFUERZO DE RUTAS (LIMPIEZA VISUAL)
# ==========================================
# Esto asegura que Python encuentre la carpeta 'modulos' siempre
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.append(base_path)

# ==========================================
# IMPORTACIÓN DE MÓDULOS
# ==========================================
try:
    from modulos.finanzas import GestorFinanciero
    from modulos.biomonitor import BiomonitorGlucosa
    from modulos.asistente import AsistenteInteligenteQuevedo
    from modulos.generador_pdf import GeneradorPDF
except ModuleNotFoundError as e:
    st.error(f"❌ Error de estructura: No se encuentra el módulo '{e.name}'.")
    st.info("Asegúrate de que la carpeta se llame 'modulos' y tenga un archivo '__init__.py' adentro.")
    st.stop()

# ==========================================
# CONFIGURACIÓN DE LA APP
# ==========================================
st.set_page_config(page_title="Quevedo Smart System", layout="wide", page_icon="🤖")

# Inicializar clases
finanzas = GestorFinanciero()
salud = BiomonitorGlucosa()
asistente = AsistenteInteligenteQuevedo()
pdf = GeneradorPDF()

# --- Interfaz Principal ---
st.title("🤖 Centro de Control Inteligente Quevedo")
st.markdown("---")

# Sidebar para navegación o acciones rápidas
with st.sidebar:
    st.header("⚙️ Panel de Control")
    if st.button("📄 Generar Reporte PDF"):
        # Lógica para recolectar datos y generar PDF
        pdf.crear_reporte(finanzas.obtener_resumen(), salud.obtener_datos())
        st.success("¡Reporte generado con éxito!")

# --- Organización en Columnas ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Gestión Financiera")
    with st.expander("Añadir Transacción", expanded=False):
        tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.01)
        descr = st.text_input("Descripción")
        if st.button("Guardar Finanzas"):
            finanzas.registrar(tipo, monto, descr)
            st.success("Registrado.")
    
    # Mostrar tabla de finanzas
    df_fin = finanzas.listar_transacciones()
    st.dataframe(df_fin, use_container_width=True)

with col2:
    st.subheader("🩸 Monitor de Salud")
    with st.expander("Registrar Glucosa", expanded=False):
        nivel = st.number_input("Nivel (mg/dL)", min_value=0, max_value=500)
        nota = st.text_input("Nota (ej. Ayunas, Post-comida)")
        if st.button("Guardar Salud"):
            salud.registrar(nivel, nota)
            st.success("Nivel guardado.")
            
    # Mostrar tabla de salud
    df_salud = salud.listar_registros()
    st.dataframe(df_salud, use_container_width=True)

st.markdown("---")

# --- Sección de IA ---
st.subheader("🧠 Asistente Predictivo")
pregunta = st.chat_input("Pregúntale algo a tu sistema...")
if pregunta:
    respuesta = asistente.responder(pregunta)
    st.write(f"**Asistente:** {respuesta}")

# --- Botón de Limpieza Visual ---
if st.sidebar.button("🗑️ Limpiar Base de Datos"):
    if st.sidebar.checkbox("Confirmar borrado total"):
        finanzas.borrar_todo()
        salud.borrar_todo()
        st.rerun()
