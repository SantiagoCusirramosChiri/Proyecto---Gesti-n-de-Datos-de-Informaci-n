# conexion.py

import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self, host="localhost", user="root", password="santi", database="sistema_documentos"):
        self.host = host
        self.user = user
        self.password = password
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