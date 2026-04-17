# --- IMPORTACIÓN DE TUS MÓDULOS ---
from modulos import finanzas as fn
from modulos import biomonitor as bio

# --- SECCIÓN DE MÉTRICAS (Uso de tus funciones factorizadas) ---
col1, col2 = st.columns(2)

with col1:
    # Llamamos a la función que ya creaste en tu módulo
    balance = fn.obtener_balance() 
    st.metric("Balance Total", f"$ {balance:,.2f}")

with col2:
    # Supongamos que bio.ultimo_registro() devuelve un diccionario o tupla
    ultima_glucosa, estado = bio.obtener_estado_salud() 
    # Aquí aplicamos el SEMÁFORO visual
    color = "normal" if 80 <= ultima_glucosa <= 130 else "inverse"
    st.metric("Glucosa", f"{ultima_glucosa} mg/dL", delta=estado, delta_color=color)

st.divider()

# --- SECCIÓN DE TABLA FILTRADA ---
st.subheader("📝 Historial Inteligente")

# Usamos el buscador lateral para filtrar a través del módulo de finanzas
if busqueda:
    datos = fn.buscar_registros(busqueda)
else:
    datos = fn.obtener_ultimos(10)

st.dataframe(datos, use_container_width=True, hide_index=True)

# --- BOTÓN DE BORRADO SEGURO ---
with st.expander("⚠️ Zona de Peligro"):
    id_borrar = st.number_input("ID del registro a eliminar", min_value=1, step=1)
    if st.button("Confirmar Borrado", type="primary"):
        # Llamada al motor de borrado en el módulo factorizado
        exito = fn.eliminar_registro(id_borrar)
        if exito:
            st.success(f"Registro {id_borrar} borrado correctamente.")
            st.rerun()
        else:
            st.error("No se pudo eliminar el registro. Verifica el ID.")
