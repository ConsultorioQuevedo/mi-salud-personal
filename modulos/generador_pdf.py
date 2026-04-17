import sqlite3
from fpdf import FPDF
from datetime import datetime
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='📄 [PDF-GEN]: %(message)s')

class ReporteQuevedo(FPDF):
    """Clase personalizada para el diseño del PDF."""
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'SISTEMA INTELIGENTE QUEVEDO - REPORTE INTEGRAL', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

class GeneradorPDF:
    """Motor de extracción y generación de informes."""
    
    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path

    def _obtener_datos(self, query: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error al extraer datos para PDF: {e}")
            return []

    def crear_reporte_mensual(self, nombre_archivo: str = "Reporte_Quevedo.pdf"):
        """Genera un PDF con secciones de Finanzas y Salud."""
        pdf = ReporteQuevedo()
        pdf.add_page()
        
        # --- SECCIÓN 1: FINANZAS ---
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, '1. RESUMEN FINANCIERO', 0, 1, 'L', fill=True)
        pdf.ln(4)
        
        pdf.set_font('Arial', '', 10)
        transacciones = self._obtener_datos("SELECT fecha, tipo, monto, categoria FROM transacciones ORDER BY fecha DESC LIMIT 15")
        
        # Encabezados de tabla
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 8, 'Fecha', 1)
        pdf.cell(30, 8, 'Tipo', 1)
        pdf.cell(40, 8, 'Monto', 1)
        pdf.cell(80, 8, 'Categoría', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 10)
        for fecha, tipo, monto, cat in transacciones:
            pdf.cell(40, 8, str(fecha)[:10], 1)
            pdf.cell(30, 8, str(tipo).capitalize(), 1)
            pdf.cell(40, 8, f"{monto:.2f} EUR", 1)
            pdf.cell(80, 8, str(cat), 1)
            pdf.ln()
        
        pdf.ln(10)

        # --- SECCIÓN 2: SALUD (GLUCOSA) ---
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '2. MONITOREO DE SALUD (GLUCOSA)', 0, 1, 'L', fill=True)
        pdf.ln(4)
        
        mediciones = self._obtener_datos("SELECT fecha, nivel, estado FROM registro_glucosa ORDER BY fecha DESC LIMIT 15")
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 8, 'Fecha y Hora', 1)
        pdf.cell(60, 8, 'Nivel (mg/dL)', 1)
        pdf.cell(70, 8, 'Estado/Alerta', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 10)
        for fecha, nivel, estado in mediciones:
            pdf.cell(60, 8, str(fecha), 1)
            pdf.cell(60, 8, f"{nivel} mg/dL", 1)
            pdf.cell(70, 8, str(estado), 1)
            pdf.ln()

        # --- SECCIÓN 3: NOTA DE INTELIGENCIA ---
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, "Nota: Este reporte ha sido generado automáticamente por el Sistema Quevedo. Las proyecciones de IA deben usarse como referencia y no como consejo médico o financiero profesional.")

        try:
            pdf.output(nombre_archivo)
            logging.info(f"✅ Reporte generado exitosamente: {nombre_archivo}")
            return nombre_archivo
        except Exception as e:
            logging.error(f"❌ Fallo al escribir PDF: {e}")
            return None

if __name__ == "__main__":
    # Prueba rápida del generador
    gen = GeneradorPDF()
    gen.crear_reporte_mensual("Resumen_Abril_2026.pdf")
