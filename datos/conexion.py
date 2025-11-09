import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self, host="localhost", user="root", password="12345678", database="sistema_documentos"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None

    def conectar(self):
        """Establece la conexión a la base de datos."""
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

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión cerrada correctamente")

    def obtener_cursor(self):
        """Devuelve un cursor de la conexión para ejecutar consultas."""
        if self.conexion and self.conexion.is_connected():
            return self.conexion.cursor()
        else:
            print("No hay conexión activa a la base de datos")
            return None

