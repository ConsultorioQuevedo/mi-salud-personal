import sqlite3
from fpdf import FPDF
from datetime import datetime
import io

class ReporteQuevedo(FPDF):
    def header(self):
        # Fondo decorativo para el título
        self.set_fill_color(31, 73, 125)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 15, 'SISTEMA INTELIGENTE QUEVEDO', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, f'REPORTE INTEGRAL - {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()} | Sistema de Gestión Privado', 0, 0, 'C')

class GeneradorPDF:
    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path

    def generar_pdf_bytes(self):
        """Genera el PDF y lo devuelve como bytes para descargar en Streamlit."""
        pdf = ReporteQuevedo()
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)

        # --- SECCIÓN 1: FINANZAS ---
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, ' 1. RESUMEN DE FINANZAS', 0, 1, 'L', fill=True)
        pdf.ln(5)

        # Encabezados
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(35, 8, 'Fecha', 1)
        pdf.cell(25, 8, 'Tipo', 1)
        pdf.cell(40, 8, 'Monto', 1)
        pdf.cell(90, 8, 'Categoría', 1)
        pdf.ln()

        pdf.set_font('Arial', '', 10)
        with sqlite3.connect(self.db_path) as conn:
            datos = conn.execute("SELECT fecha, tipo, monto, categoria FROM transacciones ORDER BY fecha DESC LIMIT 20").fetchall()
            for fecha, tipo, monto, cat in datos:
                pdf.cell(35, 8, str(fecha)[:10], 1)
                pdf.cell(25, 8, str(tipo).capitalize(), 1)
                pdf.cell(40, 8, f"$ {monto:,.2f}", 1)
                pdf.cell(90, 8, str(cat), 1)
                pdf.ln()

        pdf.ln(10)

        # --- SECCIÓN 2: SALUD ---
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, ' 2. CONTROL DE GLUCOSA', 0, 1, 'L', fill=True)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 8, 'Fecha y Hora', 1)
        pdf.cell(60, 8, 'Nivel (mg/dL)', 1)
        pdf.cell(70, 8, 'Interpretación', 1)
        pdf.ln()

        pdf.set_font('Arial', '', 10)
        with sqlite3.connect(self.db_path) as conn:
            salud = conn.execute("SELECT fecha, nivel, estado FROM registro_glucosa ORDER BY fecha DESC LIMIT 20").fetchall()
            for f, n, e in salud:
                pdf.cell(60, 8, str(f), 1)
                pdf.cell(60, 8, f"{n} mg/dL", 1)
                pdf.cell(70, 8, str(e), 1)
                pdf.ln()

        # Retornar como salida de bytes
        return pdf.output(dest='S').encode('latin-1')
