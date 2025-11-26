from datos.ConexionAdmin import ConexionAdmin
from datos.conexion import ConexionDB

class PostgresAuthBL:
    def __init__(self):
        pass
    
    def configurar_postgresql_completo(self, password_postgres):
        try:
            # crear usuario con .bat
            print("\n" + "="*60)
            print("PASO 1: CREANDO USUARIO LOLCITO")
            print("="*60 + "\n")
            
            admin = ConexionAdmin(user="postgres", password=password_postgres)
            
            if not admin.crear_usuario_con_bat():
                return False, "No se pudo crear el usuario lolcito. Verifica la contraseña de postgres."
            
            print("✓ Usuario creado exitosamente\n")
            
            # crear base de datos y ejecutar scripts
            print("="*60)
            print("PASO 2: CREANDO BASE DE DATOS Y ESTRUCTURA")
            print("="*60 + "\n")
            
            db = ConexionDB()
            
            if not db.crear_base_datos_y_ejecutar_scripts():
                return False, "No se pudo crear la base de datos o ejecutar los scripts de estructura."
            
            print("✓ Base de datos y estructura creadas exitosamente\n")
            
            print("="*60)
            print("✓ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
            print("="*60 + "\n")
            
            return True, "Configuración completada exitosamente"
            
        except Exception as e:
            print(f"\n✗ Error en configuración: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error inesperado: {str(e)}"