import sqlite3
import pandas as pd

class GestorFinanciero:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path

    def registrar(self, tipo, monto, descripcion):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO finanzas (tipo, monto, descripcion, fecha) 
            VALUES (?, ?, ?, ?)
        """, (tipo, monto, descripcion, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

    def listar_transacciones(self):
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT fecha as Fecha, tipo as Tipo, monto as Monto, descripcion as Detalle FROM finanzas ORDER BY fecha DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception:
            return pd.DataFrame(columns=['Fecha', 'Tipo', 'Monto', 'Detalle'])

    # ESTA ES LA FUNCIÓN QUE FALTA
    def obtener_balance(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Calculamos Ingresos - Gastos directamente en SQL
            cursor.execute("SELECT SUM(CASE WHEN tipo = 'Ingreso' THEN monto ELSE -monto END) FROM finanzas")
            balance = cursor.fetchone()[0]
            conn.close()
            return balance if balance else 0.0
        except Exception:
            return 0.0

    def borrar_todo(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM finanzas")
        conn.commit()
        conn.close()
