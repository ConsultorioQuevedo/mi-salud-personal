import sqlite3
import pandas as pd
from datetime import datetime
import logging

class GestorFinanciero:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()
        logging.basicConfig(level=logging.INFO)

    def _conectar(self):
        """Establece conexión con soporte para tipos de datos de SQLite."""
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_db(self):
        """Crea la estructura profesional de tablas."""
        query = """
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT CHECK(tipo IN ('ingreso', 'gasto')),
            monto REAL NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            with self._conectar() as conn:
                conn.execute(query)
        except sqlite3.Error as e:
            logging.error(f"Error al inicializar DB Finanzas: {e}")

    def registrar_transaccion(self, tipo: str, monto: float, categoria: str, descripcion: str = ""):
        """Registra transacciones con validación de entrada."""
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        
        tipo = tipo.lower().strip()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with self._conectar() as conn:
                conn.execute("""
                    INSERT INTO transacciones (tipo, monto, categoria, descripcion, fecha)
                    VALUES (?, ?, ?, ?, ?)
                """, (tipo, monto, categoria.strip(), descripcion.strip(), fecha))
                conn.commit()
                return True
        except sqlite3.Error as e:
            logging.error(f"Error al registrar transacción: {e}")
            return False

    def obtener_balance_total(self) -> dict:
        """Calcula métricas financieras completas."""
        balances = {"ingreso": 0.0, "gasto": 0.0, "ahorro_neto": 0.0}
        query = "SELECT tipo, SUM(monto) FROM transacciones GROUP BY tipo"
        
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                for tipo, total in cursor.fetchall():
                    if tipo in balances:
                        balances[tipo] = total or 0.0
                balances["ahorro_neto"] = balances["ingreso"] - balances["gasto"]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener balances: {e}")
        return balances

    def listar_transacciones(self, filtro: str = ""):
        """Retorna un DataFrame con búsqueda integrada."""
        try:
            with self._conectar() as conn:
                query = "SELECT fecha as Fecha, tipo as Tipo, monto as Monto, categoria as Categoria, descripcion as Detalle FROM transacciones"
                df = pd.read_sql_query(query, conn)
                if filtro:
                    mask = df.apply(lambda x: x.astype(str).str.contains(filtro, case=False)).any(axis=1)
                    df = df[mask]
                return df
        except Exception as e:
            logging.error(f"Error al listar transacciones: {e}")
            return pd.DataFrame()
