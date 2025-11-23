# datos/ConexionAdmin.py - SOLO EJECUTA EL BAT

import os
import sys
import subprocess

class ConexionAdmin:
    """
    Clase para ejecutar el .bat que crea el usuario lolcito.
    """

    def __init__(self, user, password, host="localhost", port=5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def crear_usuario_con_bat(self):
        """
        Ejecuta el .bat para crear el usuario lolcito.
        
        Returns:
            bool: True si el usuario fue creado exitosamente, False en caso contrario
        """
        print("Ejecutando script para crear usuario...\n")

        # Ruta del .bat (en la raíz del proyecto)
        proyecto_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bat_path = os.path.join(proyecto_raiz, "crear_usuario.bat")
        
        if not os.path.exists(bat_path):
            print(f"✗ No se encontró el archivo: {bat_path}")
            print(f"\nAsegúrate de que 'crear_usuario.bat' esté en la raíz del proyecto:")
            print(f"  {proyecto_raiz}")
            return False

        try:
            # Ejecutar el .bat con la contraseña en variable de entorno
            resultado = subprocess.run(
                [bat_path],
                env={**os.environ, "PGPASSWORD": self.password},
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=proyecto_raiz
            )
            
            # Mostrar la salida del .bat
            if resultado.stdout:
                print(resultado.stdout)
            
            if resultado.returncode == 0:
                return True
            else:
                if resultado.stderr:
                    print(f"✗ Error: {resultado.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Error ejecutando .bat: {e}")
            import traceback
            traceback.print_exc()
            return False