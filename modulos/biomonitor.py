import sqlite3
import pandas as pd

class BiomonitorGlucosa:
    def __init__(self, db_path="base_datos_quevedo.db"):
        self.db_path = db_path

    def registrar(self, nivel, nota):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO salud (nivel, nota, fecha) 
            VALUES (?, ?, ?)
        """, (nivel, nota, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

    # ESTA ES LA FUNCIÓN QUE TE ESTÁ DANDO EL ERROR
    def listar_registros(self):
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT fecha as Fecha, nivel as Nivel, nota as Nota FROM salud ORDER BY fecha DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception:
            # Si la tabla no existe o hay error, devuelve un DataFrame vacío con las columnas correctas
            return pd.DataFrame(columns=['Fecha', 'Nivel', 'Nota'])

    def obtener_ultimo_registro(self):
        df = self.listar_registros()
        if not df.empty:
            return df['Nivel'].iloc[0]
        return 0
