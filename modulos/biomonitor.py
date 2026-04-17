import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple

class BiomonitorGlucosa:
    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_bd()

    def _conectar(self):
        # Esencial para que no choque el celular con la PC
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_bd(self):
        query = """
            CREATE TABLE IF NOT EXISTS registro_glucosa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nivel REAL NOT NULL,
                estado TEXT NOT NULL,
                fecha DATETIME NOT NULL
            )
        """
        with self._conectar() as conn:
            conn.execute(query)

    # --- MODIFICADO PARA LA NUBE ---
    def registrar_lectura(self, nivel: float):
        """Recibe el nivel desde la web y lo procesa."""
        if nivel <= 0: return False
        
        # Usamos tu lógica de semáforo internamente
        estado, _ = self.interpretar_nivel(nivel)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = "INSERT INTO registro_glucosa (nivel, estado, fecha) VALUES (?, ?, ?)"
        try:
            with self._conectar() as conn:
                conn.execute(query, (nivel, estado, fecha))
                conn.commit()
            return True
        except Exception:
            return False

    def interpretar_nivel(self, nivel: float) -> Tuple[str, str]:
        """Lógica de semáforo inteligente."""
        if nivel < 70:
            return "Rojo", "🚨 Hipoglucemia: Actúe de inmediato."
        elif 70 <= nivel <= 140:
            return "Verde", "✅ Normal: Nivel estable."
        elif 141 <= nivel <= 180:
            return "Amarillo", "⚠️ Precaución: Nivel elevado."
        else:
            return "Rojo", "🚨 Hiperglucemia: Busque ayuda médica."

    # --- REQUERIDO PARA LA TABLA EN EL CELULAR ---
    def obtener_historial(self) -> pd.DataFrame:
        """Devuelve todos los registros para la barra de búsqueda."""
        query = "SELECT id as ID, fecha as Fecha, nivel as Nivel, estado as Estado FROM registro_glucosa ORDER BY fecha DESC"
        try:
            with self._conectar() as conn:
                return pd.read_sql_query(query, conn)
        except:
            return pd.DataFrame()

    def obtener_ultimo_registro(self) -> float:
        """Para mostrar en la métrica principal del dashboard."""
        try:
            with self._conectar() as conn:
                res = conn.execute("SELECT nivel FROM registro_glucosa ORDER BY fecha DESC LIMIT 1").fetchone()
                return res[0] if res else 0.0
        except:
            return 0.0

    # --- REQUERIDO PARA LA LÍNEA 40 (LIMPIEZA) ---
    def ejecutar_borrado(self, tabla: str, id_registro: int) -> bool:
        """Borrado robusto por ID."""
        if tabla != "registro_glucosa": return False
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM registro_glucosa WHERE id = ?", (id_registro,))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
