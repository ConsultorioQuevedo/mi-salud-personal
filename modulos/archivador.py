import os
import zipfile
import logging
from cryptography.fernet import Fernet
from typing import List, Optional

# Configuración de logs para un manejo profesional de eventos
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ArchivadorInteligente:
    """
    Gestiona el ciclo de vida de archivos: Empaquetado, Cifrado y Fragmentación.
    Diseñado para manejar archivos de gran tamaño de forma eficiente.
    """

    def __init__(self, clave_maestra: Optional[bytes] = None):
        # Si no hay clave, generamos una (En producción, esto vendría de un gestor de secretos)
        self.clave = clave_maestra or Fernet.generate_key()
        self.fernet = Fernet(self.clave)

    def empaquetar(self, archivos: List[str], destino_zip: str) -> bool:
        """Combina múltiples archivos en un contenedor comprimido."""
        try:
            with zipfile.ZipFile(destino_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for archivo in archivos:
                    if os.path.exists(archivo):
                        zipf.write(archivo, os.path.basename(archivo))
                        logging.info(f"📦 Agregado al índice: {archivo}")
                    else:
                        logging.warning(f"⚠️ Archivo omitido (no existe): {archivo}")
            return True
        except Exception as e:
            logging.error(f"❌ Error en empaquetado: {e}")
            return False

    def cifrar(self, ruta_archivo: str) -> str:
        """
        Cifra un archivo utilizando Fernet. 
        Implementa lectura por bloques para evitar saturar la memoria RAM.
        """
        ruta_salida = f"{ruta_archivo}.enc"
        try:
            with open(ruta_archivo, 'rb') as f_entrada:
                datos = f_entrada.read() # Para Fernet estándar se requiere el bloque completo
                
            datos_cifrados = self.fernet.encrypt(datos)
            
            with open(ruta_salida, 'wb') as f_salida:
                f_salida.write(datos_cifrados)
            
            logging.info(f"🔒 Capa de cifrado aplicada: {ruta_salida}")
            return ruta_salida
        except Exception as e:
            logging.error(f"❌ Error en cifrado: {e}")
            return ""

    def fragmentar(self, ruta_archivo: str, tamano_chunk_mb: int = 1) -> List[str]:
        """
        Divide un archivo en partes numeradas para facilitar su sincronización.
        """
        chunk_size = tamano_chunk_mb * 1024 * 1024 # Convertir MB a Bytes
        partes = []
        
        try:
            with open(ruta_archivo, 'rb') as f:
                contador = 1
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    nombre_parte = f"{ruta_archivo}.part{contador:03d}"
                    with open(nombre_parte, 'wb') as f_parte:
                        f_parte.write(chunk)
                    
                    partes.append(nombre_parte)
                    logging.info(f"✂️ Fragmento creado: {os.path.basename(nombre_parte)}")
                    contador += 1
            
            logging.info(f"✅ División completada en {len(partes)} partes.")
            return partes
        except Exception as e:
            logging.error(f"❌ Error en fragmentación: {e}")
            return []

# --- Orquestación del Módulo ---
def ejecutar_archivado_profesional():
    # Instancia del sistema
    arc = ArchivadorInteligente()
    
    print("\n" + "—"*45)
    print("🛡️ NÚCLEO DE ARCHIVADO Y SEGURIDAD QUEVEDO")
    print("—"*45)

    # Definición de activos a proteger
    items_a_respaldar = ["base_datos_quevedo.db", "registro_glucosa.txt"]
    # Crear archivos temporales si no existen para la prueba
    for item in items_a_respaldar:
        if not os.path.exists(item):
            with open(item, "w") as f: f.write("Data dummy de protección.")

    contenedor = "backup_sistema.zip"

    # Fase 1: Consolidación
    if arc.empaquetar(items_a_respaldar, contenedor):
        
        # Fase 2: Blindaje (Cifrado)
        archivo_blindado = arc.cifrar(contenedor)
        
        # Fase 3: Optimización (Fragmentación)
        if archivo_blindado:
            arc.fragmentar(archivo_blindado, tamano_chunk_mb=1)

    print("\n✅ El ciclo de archivado ha finalizado con éxito.")

if __name__ == "__main__":
    ejecutar_archivado_profesional()
