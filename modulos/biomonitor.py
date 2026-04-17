import sqlite3
from datetime import datetime
from typing import Optional, Tuple

class BiomonitorGlucosa:
    """
    Sistema robusto de control glucémico.
    Gestiona mediciones, interpretación de niveles y análisis de tendencias.
    """

    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_bd()

    def _conectar(self):
        """Establece conexión con la base de datos central."""
        return sqlite3.connect(self.db_path)

    def _inicializar_bd(self):
        """Crea la estructura necesaria si no existe."""
        query = """
            CREATE TABLE IF NOT EXISTS registro_glucosa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nivel REAL NOT NULL,
                estado TEXT NOT NULL,
                fecha DATETIME NOT NULL
            )
        """
        try:
            with self._conectar() as conn:
                conn.execute(query)
        except sqlite3.Error as e:
            print(f"❌ Error al inicializar biomonitor: {e}")

    # --- Módulo de Monitoreo ---
    def medir_glucosa(self) -> Optional[float]:
        """Solicita y valida la entrada del usuario."""
        try:
            entrada = input("👉 Ingrese nivel de glucosa (mg/dL): ")
            return float(entrada)
        except ValueError:
            print("⚠️ Valor inválido. Por favor, ingrese solo números.")
            return None

    # --- Módulo de Interpretación ---
    def interpretar_nivel(self, nivel: float) -> Tuple[str, str]:
        """Lógica de semáforo para diagnóstico rápido."""
        if nivel < 70:
            return "Rojo", "🚨 Peligro: Hipoglucemia. Actúe de inmediato."
        elif 70 <= nivel <= 140:
            return "Verde", "✅ Seguro: Nivel dentro del rango normal."
        elif 141 <= nivel <= 180:
            return "Amarillo", "⚠️ Precaución: Nivel elevado moderado."
        else:
            return "Rojo", "🚨 Peligro: Hiperglucemia. Busque ayuda médica."

    # --- Módulo de Registro ---
    def registrar_medicion(self, nivel: float, estado: str):
        """Guarda la medición en la base de datos central de forma persistente."""
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO registro_glucosa (nivel, estado, fecha) VALUES (?, ?, ?)"
        
        try:
            with self._conectar() as conn:
                conn.execute(query, (nivel, estado, fecha))
                conn.commit()
            print("🗂️ Registro guardado en la base de datos correctamente.")
        except sqlite3.Error as e:
            print(f"❌ Error al guardar en base de datos: {e}")

    # --- Módulo de Tendencias (Inteligente) ---
    def analizar_tendencias(self, limite_muestras: int = 5):
        """Analiza estadísticamente las últimas mediciones."""
        query = f"""
            SELECT nivel FROM registro_glucosa 
            ORDER BY fecha DESC LIMIT {limite_muestras}
        """
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                filas = cursor.fetchall()
                
                if not filas:
                    print("ℹ️ No hay suficientes datos para analizar tendencias.")
                    return

                niveles = [f[0] for f in filas]
                promedio = sum(niveles) / len(niveles)
                
                print(f"\n📊 ANÁLISIS DE TENDENCIA (Últimas {len(niveles)} mediciones):")
                print(f"   Promedio actual: {promedio:.1f} mg/dL")
                
                if promedio > 160:
                    print("   ⚠️ Estado: Tendencia ALTA detectada.")
                elif promedio < 80:
                    print("   ⚠️ Estado: Tendencia BAJA detectada.")
                else:
                    print("   ✅ Estado: Tendencia ESTABLE.")
                    
        except sqlite3.Error as e:
            print(f"❌ Error al analizar tendencias: {e}")

    # --- Módulo de Educación ---
    def dar_recomendacion(self, estado: str):
        """Provee consejos basados en el estado resultante."""
        consejos = {
            "Verde": "🍎 Mantenga su rutina y alimentación equilibrada.",
            "Amarillo": "⚠️ Controle su dieta y evite azúcares simples.",
            "Rojo": "🚨 Tome medidas inmediatas o contacte a su médico."
        }
        print(f"💡 RECOMENDACIÓN: {consejos.get(estado, 'Consulte a su médico.')}")

# --- Ejecución Principal (Orquestación) ---
def main():
    monitor = BiomonitorGlucosa()
    
    print("\n" + "="*40)
    print("  SISTEMA QUEVEDO: CONTROL DE GLUCOSA  ")
    print("="*40)
    
    nivel = monitor.medir_glucosa()
    
    if nivel is not None:
        estado, mensaje = monitor.interpretar_nivel(nivel)
        print(f"\nINTERPRETACIÓN: {mensaje}")
        
        monitor.registrar_medicion(nivel, estado)
        monitor.analizar_tendencias()
        monitor.dar_recomendacion(estado)
        
    print("\n✅ Proceso de salud finalizado.")

if __name__ == "__main__":
    main()
