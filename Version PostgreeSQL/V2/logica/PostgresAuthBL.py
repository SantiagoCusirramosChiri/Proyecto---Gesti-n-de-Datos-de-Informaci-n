# logica/PostgresAuthBL.py

from datos.ConexionAdmin import ConexionAdmin

class PostgresAuthBL:
    """Lógica de negocio para autenticación de PostgreSQL y ejecución de scripts"""

    @staticmethod
    def validar_usuario_password_postgres(user, password, nombre_bd="sistema_documentos"):
        """
        Valida credenciales de PostgreSQL y configura la base de datos completa.
        
        Args:
            user (str): Usuario de PostgreSQL
            password (str): Contraseña de PostgreSQL
            nombre_bd (str): Nombre de la base de datos a crear (default: sistema_documentos)
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        # Validar que los campos no estén vacíos
        if not user or user.strip() == "":
            return False, "Debe ingresar un usuario"
        if not password or password.strip() == "":
            return False, "Debe ingresar una contraseña"

        # Crear conexión administrativa
        admin_db = ConexionAdmin(user=user, password=password)
        
        try:
            # Paso 1: Validar credenciales conectándose a postgres
            admin_db.conectar(database="postgres")
            
            if not admin_db.conn:
                return False, "Credenciales incorrectas o PostgreSQL no está disponible"
            
            print(f"✓ Credenciales validadas correctamente")
            admin_db.desconectar()
            
            # Paso 2: Crear base de datos y ejecutar todos los scripts
            print(f"\nIniciando configuración de la base de datos '{nombre_bd}'...")
            
            exito = admin_db.crear_base_y_ejecutar_scripts(nombre_bd)
            
            if exito:
                return True, f"Base de datos '{nombre_bd}' configurada exitosamente"
            else:
                return False, f"Error al configurar la base de datos '{nombre_bd}'"
                
        except Exception as e:
            admin_db.desconectar()  # Asegurar cierre en caso de error
            return False, f"Error durante la configuración: {str(e)}"

    @staticmethod
    def solo_validar_credenciales(user, password):
        """
        Solo valida las credenciales sin crear ni modificar bases de datos.
        
        Args:
            user (str): Usuario de PostgreSQL
            password (str): Contraseña de PostgreSQL
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        if not user or user.strip() == "":
            return False, "Debe ingresar un usuario"
        if not password or password.strip() == "":
            return False, "Debe ingresar una contraseña"

        admin_db = ConexionAdmin(user=user, password=password)
        
        try:
            admin_db.conectar(database="postgres")
            
            if not admin_db.conn:
                return False, "Credenciales incorrectas"
            
            admin_db.desconectar()
            return True, "Credenciales válidas"
            
        except Exception as e:
            return False, f"Error al validar credenciales: {str(e)}"

    @staticmethod
    def ejecutar_scripts_en_bd_existente(user, password, nombre_bd):
        """
        Ejecuta todos los scripts en una base de datos que ya existe.
        Útil para reconfigurar una base de datos sin eliminarla.
        
        Args:
            user (str): Usuario de PostgreSQL
            password (str): Contraseña de PostgreSQL
            nombre_bd (str): Nombre de la base de datos existente
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        if not user or user.strip() == "":
            return False, "Debe ingresar un usuario"
        if not password or password.strip() == "":
            return False, "Debe ingresar una contraseña"
        if not nombre_bd or nombre_bd.strip() == "":
            return False, "Debe especificar el nombre de la base de datos"

        admin_db = ConexionAdmin(user=user, password=password)
        
        try:
            admin_db.conectar(database=nombre_bd)
            
            if not admin_db.conn:
                return False, f"No se pudo conectar a la base de datos '{nombre_bd}'"
            
            print(f"\nEjecutando scripts en la base de datos '{nombre_bd}'...")
            admin_db.cargar_todos_los_scripts()
            admin_db.desconectar()
            
            return True, f"Scripts ejecutados exitosamente en '{nombre_bd}'"
            
        except Exception as e:
            admin_db.desconectar()
            return False, f"Error al ejecutar scripts: {str(e)}"

