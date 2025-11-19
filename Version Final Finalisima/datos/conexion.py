# conexion.py

import mysql.connector
from mysql.connector import Error

class ConexionDB:
    # Variable global de clase para almacenar la contraseña
    _password_global = None
    
    def __init__(self, host="localhost", user="root", password=None, database="sistema_documentos"):
        self.host = host
        self.user = user
        # Si no se pasa password, usar la global. Si se pasa, usar esa.
        self.password = password if password is not None else self._password_global
        self.database = database
        self.conexion = None

    # Se establece la conexión con la base de datos MySQL
    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                print(f"Conexión exitosa a la base de datos '{self.database}'")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    # Se cierra la conexión activa con la base de datos
    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión cerrada correctamente")

    # Se retorna un cursor para ejecutar consultas SQL
    def obtener_cursor(self):
        if self.conexion and self.conexion.is_connected():
            return self.conexion.cursor()
        else:
            print("No hay conexión activa a la base de datos")
            return None
    
    # Método para establecer la contraseña global
    @classmethod
    def set_password_global(cls, password):
        """Establece la contraseña global para todas las instancias"""
        cls._password_global = password
    
    # Método para obtener la contraseña global
    @classmethod
    def get_password_global(cls):
        """Obtiene la contraseña global almacenada"""
        return cls._password_global