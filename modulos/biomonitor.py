import sqlite3
import pandas as pd
from datetime import datetime
import logging

class BiomonitorGlucosa:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS salud (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nivel INTEGER NOT NULL,
            nota TEXT,
            estado TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self._conectar() as conn:
            conn.execute(query)

    def _evaluar_estado(self, nivel: int):
        """Lógica de semáforo médico para robustez de datos."""
        if nivel < 70: return "Bajo (Hipoglucemia)"
        if 70 <= nivel <= 140: return "Normal"
        if 140 < nivel <= 180: return "Elevado"
        return "Muy Alto (Hiperglucemia)"

    def registrar_lectura(self, nivel: int, nota: str = ""):
        """Registra lectura con clasificación de estado automática."""
        if not (20 <= nivel <= 600): # Rango de seguridad de glucómetros
            raise ValueError("Nivel de glucosa fuera de rango lógico.")
            
        estado = self._evaluar_estado(nivel)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with self._conectar() as conn:
                conn.execute("""
                    INSERT INTO salud (nivel, nota, estado, fecha)
                    VALUES (?, ?, ?, ?)
                """, (nivel, nota, estado, fecha))
                conn.commit()
                return True
        except sqlite3.Error as e:
            logging.error(f"Error en salud: {e}")
            return False

    def obtener_historial(self):
        """Retorna historial completo con estados."""
        try:
            with self._conectar() as conn:
                return pd.read_sql_query("SELECT fecha as Fecha, nivel as Nivel, estado as Estado, nota as Nota FROM salud ORDER BY fecha DESC", conn)
        except Exception:
            return pd.DataFrame()

    def obtener_ultimo_registro(self):
        """Retorna la última métrica para el panel general."""
        try:
            with self._conectar() as conn:
                res = conn.execute("SELECT nivel FROM salud ORDER BY fecha DESC LIMIT 1").fetchone()
                return res[0] if res else 0
        except:
            return 0
