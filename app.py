import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF

class MotorQuevedo:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_db(self):
        """Crea las tablas de Finanzas y Salud si no existen."""
        with self._conectar() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS finanzas 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, monto REAL, categoria TEXT, fecha DATETIME)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS salud 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, nivel INTEGER, estado TEXT, fecha DATETIME)""")

    # --- FUNCIONES DE CONTROL ---
    def ejecutar_borrado(self, tabla, id_reg):
        """Borra cualquier registro por su ID."""
        with self._conectar() as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_reg,))
            return cur.rowcount > 0

    def obtener_datos(self, tabla):
        """Trae los datos para las tablas y el buscador."""
        with self._conectar() as conn:
            return pd.read_sql_query(f"SELECT * FROM {tabla} ORDER BY fecha DESC", conn)

    def registrar_salud(self, nivel):
        """Lógica de semáforo integrada."""
        estado = "Verde" if 70 <= nivel <= 140 else "Rojo" if nivel < 70 else "Amarillo"
        with self._conectar() as conn:
            conn.execute("INSERT INTO salud (nivel, estado, fecha) VALUES (?, ?, ?)", 
                         (nivel, estado, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # --- GENERADOR DE PDF ---
    def generar_reporte_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "REPORTE SISTEMA QUEVEDO", 0, 1, "C")
        # Aquí el motor extrae los datos y los plasma en el papel digital
        return pdf.output(dest='S').encode('latin-1')
