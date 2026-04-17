import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, List, Tuple

class GestorFinanciero:
    """
    Gestión profesional de finanzas. 
    Incluye: Registro, Balance, Borrado Seguro y Listado para Dataframes.
    """

    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        # check_same_thread=False es vital para Streamlit Cloud
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_db(self):
        query = """
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT CHECK(tipo IN ('ingreso', 'gasto')),
                monto REAL NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT,
                fecha DATETIME NOT NULL
            )
        """
        try:
            with self._conectar() as conn:
                conn.execute(query)
        except sqlite3.Error as e:
            print(f"❌ Error DB: {e}")

    def registrar_transaccion(self, tipo: str, monto: float, categoria: str, descripcion: str = "") -> bool:
        if monto <= 0: return False
        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO transacciones (tipo, monto, categoria, descripcion, fecha) VALUES (?, ?, ?, ?, ?)"
        
        try:
            with self._conectar() as conn:
                conn.execute(query, (tipo.lower().strip(), monto, categoria.lower().strip(), descripcion, fecha))
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def obtener_balance(self) -> float:
        """Retorna el balance neto (Ingresos - Gastos). Requerido por app.py"""
        query = "SELECT tipo, SUM(monto) FROM transacciones GROUP BY tipo"
        balances = {"ingreso": 0.0, "gasto": 0.0}
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                for tipo, total in cursor.fetchall():
                    balances[tipo] = total or 0.0
            return float(balances["ingreso"] - balances["gasto"])
        except:
            return 0.0

    def listar_transacciones(self) -> pd.DataFrame:
        """Retorna el historial completo. Requerido por la tabla en app.py"""
        query = "SELECT id as ID, fecha as Fecha, tipo as Tipo, monto as Monto, categoria as Categoria, descripcion as Detalle FROM transacciones ORDER BY fecha DESC"
        try:
            with self._conectar() as conn:
                return pd.read_sql_query(query, conn)
        except:
            return pd.DataFrame()

    def ejecutar_borrado(self, tabla: str, id_registro: int) -> bool:
        """Borrado seguro por ID. Requerido por la línea 40 de app.py"""
        if tabla != "transacciones": return False
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_registro,))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False

    def verificar_presupuesto(self, categoria: str, limite: float):
        query = "SELECT SUM(monto) FROM transacciones WHERE tipo='gasto' AND categoria=?"
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (categoria.lower(),))
            total = cursor.fetchone()[0] or 0.0
            return total
