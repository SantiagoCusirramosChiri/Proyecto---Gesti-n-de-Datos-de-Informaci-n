# logica/MySQLAuthBL.py

from datos.conexion import ConexionDB

class MySQLAuthBL:
    """Lógica de negocio para autenticación de MySQL"""
    
    @staticmethod
    def validar_password_mysql(password):
        if not password or password.strip() == "":
            return False, "Debe ingresar una contraseña"
        
        # Crear instancia temporal para probar conexión
        db_test = ConexionDB(password=password)
        
        try:
            db_test.conectar()
            
            # Verificar si la conexión fue exitosa
            if db_test.conexion and db_test.conexion.is_connected():
                # Cerrar la conexión de prueba
                db_test.desconectar()
                
                # Guardar la contraseña globalmente para uso futuro
                ConexionDB.set_password_global(password)
                
                return True, "Conexión MySQL exitosa"
            else:
                return False, "No se pudo establecer conexión con MySQL"
                
        except Exception as e:
            return False, f"Error al conectar: {str(e)}"