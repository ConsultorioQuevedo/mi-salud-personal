import sqlite3
import pandas as pd
from datetime import datetime

class GestorFinanciero:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _inicializar_db(self):
        query = """CREATE TABLE IF NOT EXISTS transacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT, monto REAL, categoria TEXT, descripcion TEXT, fecha DATETIME)"""
        with self._conectar() as conn:
            conn.execute(query)

    def registrar_transaccion(self, tipo, monto, categoria, descripcion=""):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO transacciones (tipo, monto, categoria, descripcion, fecha) VALUES (?,?,?,?,?)"
        with self._conectar() as conn:
            conn.execute(query, (tipo.lower(), monto, categoria, descripcion, fecha))

    def obtener_balance_total(self):
        balances = {"ingreso": 0.0, "gasto": 0.0, "ahorro_neto": 0.0}
        try:
            with self._conectar() as conn:
                df = pd.read_sql_query("SELECT tipo, SUM(monto) as total FROM transacciones GROUP BY tipo", conn)
                for _, row in df.iterrows():
                    balances[row['tipo']] = row['total']
                balances["ahorro_neto"] = balances["ingreso"] - balances["gasto"]
        except: pass
        return balances

    def listar_transacciones(self):
        with self._conectar() as conn:
            return pd.read_sql_query("SELECT fecha as Fecha, tipo as Tipo, monto as Monto, categoria as Categoria, descripcion as Detalle FROM transacciones ORDER BY fecha DESC", conn)
