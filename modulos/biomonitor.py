import sqlite3
import pandas as pd
from datetime import datetime

class BiomonitorGlucosa:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _inicializar_db(self):
        query = """CREATE TABLE IF NOT EXISTS salud (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nivel INTEGER, nota TEXT, fecha DATETIME)"""
        with self._conectar() as conn:
            conn.execute(query)

    def registrar_lectura(self, nivel, nota):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._conectar() as conn:
            conn.execute("INSERT INTO salud (nivel, nota, fecha) VALUES (?,?,?)", (nivel, nota, fecha))

    def obtener_historial(self):
        with self._conectar() as conn:
            return pd.read_sql_query("SELECT fecha as Fecha, nivel as Nivel, nota as Nota FROM salud ORDER BY fecha DESC", conn)

    def obtener_ultimo_registro(self):
        try:
            with self._conectar() as conn:
                res = conn.execute("SELECT nivel FROM salud ORDER BY fecha DESC LIMIT 1").fetchone()
                return res[0] if res else 0
        except: return 0
