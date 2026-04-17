import streamlit as st
from modulos.motor import MotorQuevedo

# Iniciamos el motor una sola vez
if 'motor' not in st.session_state:
    st.session_state.motor = MotorQuevedo()

m = st.session_state.motor

st.set_page_config(page_title="Quevedo System Pro", layout="wide")

# --- BARRA LATERAL: CONECTIVIDAD TOTAL ---
with st.sidebar:
    st.title("🛡️ Centro de Control")
    st.subheader("🔗 Enlaces de Interés")
    st.link_button("💊 Farmacia GBC", "https://farmaciagbc.com.do/")
    st.link_button("🏥 Farmacia Carol", "https://farmaciacarol.com/")
    st.link_button("📧 Mi Gmail", "https://mail.google.com/")
    
    st.divider()
    if st.button("📄 Crear Reporte PDF"):
        archivo_pdf = m.generar_reporte_pdf()
        st.download_button("⬇️ Descargar Ahora", archivo_pdf, "Reporte_Quevedo.pdf")

# --- CUERPO PRINCIPAL: LIMPIEZA VISUAL ---
st.title("🤖 Dashboard Inteligente")

# Buscador Universal
busqueda = st.text_input("🔍 Buscar en todo el sistema...")

t1, t2 = st.tabs(["💰 Finanzas Pro", "🩸 Biomonitor de Salud"])

with t1:
    df_f = m.obtener_datos("finanzas")
    if busqueda: # Filtro inteligente
        df_f = df_f[df_f.astype(str).apply(lambda x: busqueda.lower() in x.str.lower()).any(axis=1)]
    st.dataframe(df_f, use_container_width=True)
    
    # Zona de Borrado
    id_del = st.number_input("ID para borrar", step=1, key="del_f")
    if st.button("Confirmar Eliminación"):
        if m.ejecutar_borrado("finanzas", id_del):
            st.success("Borrado con éxito"); st.rerun()

# (La pestaña de Salud sigue la misma lógica limpia)
