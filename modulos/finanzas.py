import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

class GestorFinanciero:
    """
    Clase para la gestión profesional de finanzas personales.
    Maneja transacciones, balances, alertas de presupuesto y metas de ahorro.
    """

    def __init__(self, db_path: str = "base_datos_quevedo.db"):
        self.db_path = db_path
        self._inicializar_db()

    def _conectar(self):
        """Crea una conexión a la base de datos."""
        return sqlite3.connect(self.db_path)

    def _inicializar_db(self):
        """Asegura que la estructura de la tabla exista al iniciar."""
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
            print(f"❌ Error crítico al inicializar base de datos: {e}")

    def registrar_transaccion(self, tipo: str, monto: float, categoria: str, descripcion: str = "") -> bool:
        """
        Registra una nueva entrada financiera con validación de datos.
        """
        if monto <= 0:
            print("⚠️ El monto debe ser un valor positivo.")
            return False

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO transacciones (tipo, monto, categoria, descripcion, fecha) VALUES (?, ?, ?, ?, ?)"
        
        try:
            with self._conectar() as conn:
                conn.execute(query, (tipo.lower().strip(), monto, categoria.lower().strip(), descripcion, fecha))
                conn.commit()
            print(f"✅ {tipo.capitalize()} registrado: {monto:.2f}€ en '{categoria}'")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error al registrar transacción: {e}")
            return False

    def obtener_balance_total(self) -> dict:
        """Calcula el balance actual consolidado."""
        query = "SELECT tipo, SUM(monto) FROM transacciones GROUP BY tipo"
        balances = {"ingreso": 0.0, "gasto": 0.0}
        
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                for tipo, total in cursor.fetchall():
                    balances[tipo] = total or 0.0
            
            balances["ahorro_neto"] = balances["ingreso"] - balances["gasto"]
            return balances
        except sqlite3.Error as e:
            print(f"❌ Error al calcular saldos: {e}")
            return balances

    def verificar_presupuesto(self, categoria: str, limite: float):
        """Analiza si los gastos de una categoría han superado el umbral definido."""
        query = "SELECT SUM(monto) FROM transacciones WHERE tipo='gasto' AND categoria=?"
        
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (categoria.lower(),))
                resultado = cursor.fetchone()[0]
                total = resultado if resultado else 0.0
                
                if total > limite:
                    print(f"⚠️ ALERTA: Exceso en '{categoria}'. Gastado: {total:.2f} | Límite: {limite:.2f}")
                else:
                    print(f"✅ Presupuesto '{categoria}' OK: {total:.2f}/{limite:.2f}")
                return total
        except sqlite3.Error as e:
            print(f"❌ Error al verificar presupuesto: {e}")

    @staticmethod
    def calcular_progreso_ahorro(meta: float, monto_actual: float):
        """Método estático para calcular proyecciones de ahorro."""
        if meta <= 0: return 0
        progreso = (monto_actual / meta) * 100
        print(f"💎 Meta de Ahorro: {progreso:.1f}% completo ({monto_actual:.2f} / {meta:.2f})")
        return progreso

# --- Interfaz de ejecución (Simulación de Seguridad y Pruebas) ---
if __name__ == "__main__":
    # Inicialización del sistema inteligente
    app_finanzas = GestorFinanciero()
    
    # Simulación de autenticación (Aquí se conectaría con tu módulo 'asistente.py')
    print("🔐 Accediendo al Sistema de Gestión Quevedo...")
    
    # Ejemplo de uso robusto
    app_finanzas.registrar_transaccion("ingreso", 2500.0, "Nomina", "Pago abril 2026")
    app_finanzas.registrar_transaccion("gasto", 45.50, "Comida", "Cena restaurante")
    
    # Resumen 360°
    stats = app_finanzas.obtener_balance_total()
    print(f"\n📊 RESUMEN FINANCIERO:")
    print(f"   Total Ingresos: {stats['ingreso']:.2f}")
    print(f"   Total Gastos:   {stats['gasto']:.2f}")
    print(f"   Ahorro Real:    {stats['ahorro_neto']:.2f}")
    
    # Alertas
    app_finanzas.verificar_presupuesto("comida", 100.0)
    
    # Planificación
    app_finanzas.calcular_progreso_ahorro(10000.0, stats['ahorro_neto'])
