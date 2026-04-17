import sqlite3
import numpy as np
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from sklearn.linear_model import LinearRegression

# Configuración de registro profesional
logging.basicConfig(level=logging.INFO, format='🧠 [IA-CORE]: %(message)s')

class AsistenteInteligenteQuevedo:
    """
    Motor central de inteligencia. 
    Aplica modelos de regresión lineal para predecir tendencias de salud y finanzas.
    """

    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path
        self.modelos: Dict[str, LinearRegression] = {
            "finanzas": LinearRegression(),
            "glucosa": LinearRegression()
        }
        self.estados_entrenamiento: Dict[str, bool] = {
            "finanzas": False,
            "glucosa": False
        }

    def _cargar_datos_desde_db(self, tipo: str) -> Tuple[List[float], List[float]]:
        """Extrae datos de la DB para alimentar el modelo."""
        query_map = {
            "glucosa": "SELECT nivel FROM registro_glucosa ORDER BY fecha ASC",
            "finanzas": "SELECT (SUM(monto) FILTER (WHERE tipo='ingreso') - SUM(monto) FILTER (WHERE tipo='gasto')) FROM transacciones GROUP BY date(fecha) ORDER BY fecha ASC"
        }
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query_map.get(tipo, ""))
                datos = [float(fila[0]) for fila in cursor.fetchall() if fila[0] is not None]
                return list(range(len(datos))), datos
        except sqlite3.Error as e:
            logging.error(f"Error accediendo a datos de {tipo}: {e}")
            return [], []

    def entrenar(self, tipo: str):
        """Entrena un modelo específico basado en el historial histórico."""
        indices, valores = self._cargar_datos_desde_db(tipo)
        
        if len(valores) < 3: # Umbral mínimo para una tendencia básica
            logging.warning(f"Muestras insuficientes para {tipo} ({len(valores)}/3).")
            return

        X = np.array(indices).reshape(-1, 1)
        y = np.array(valores)
        
        self.modelos[tipo].fit(X, y)
        self.estados_entrenamiento[tipo] = True
        logging.info(f"✅ Modelo de {tipo} optimizado y listo.")

    def predecir_tendencia(self, tipo: str, pasos_futuros: int = 1) -> Optional[float]:
        """Calcula la proyección matemática para el siguiente periodo."""
        if not self.estados_entrenamiento.get(tipo):
            self.entrenar(tipo)
            if not self.estados_entrenamiento.get(tipo):
                return None

        # Obtener el último índice conocido
        indices, _ = self._cargar_datos_desde_db(tipo)
        ultimo_indice = indices[-1] if indices else 0
        
        punto_futuro = np.array([[ultimo_indice + pasos_futuros]])
        prediccion = self.modelos[tipo].predict(punto_futuro)[0]
        
        logging.info(f"🔮 Proyección {tipo} para T+{pasos_futuros}: {prediccion:.2f}")
        return float(prediccion)

    # --- Fachada de Integración (Interfaz Simplificada) ---
    def procesar_comando(self, comando: str, parametros: Dict[str, Any]):
        """Punto de entrada único para el asistente."""
        try:
            if comando == "predecir_salud":
                return self.predecir_tendencia("glucosa")
            elif comando == "predecir_ahorro":
                return self.predecir_tendencia("finanzas")
            else:
                logging.error(f"Comando '{comando}' no reconocido.")
        except Exception as e:
            logging.error(f"Fallo en ejecución de comando: {e}")

# --- Simulación de Operación Centralizada ---
if __name__ == "__main__":
    # Inicializamos el asistente apuntando a la base de datos real
    brain = AsistenteInteligenteQuevedo()
    
    print("\n" + "—"*45)
    print("💎 NÚCLEO DE INTELIGENCIA PREDICTIVA QUEVEDO")
    print("—"*45)

    # El asistente analiza los datos que ya existen en tu sistema
    brain.entrenar("glucosa")
    brain.entrenar("finanzas")

    # Realizamos proyecciones inteligentes
    print("\n--- RESULTADOS DEL ANÁLISIS ---")
    brain.procesar_comando("predecir_salud", {})
    brain.procesar_comando("predecir_ahorro", {})

    print("\n✅ Inteligencia sincronizada con éxito.")
