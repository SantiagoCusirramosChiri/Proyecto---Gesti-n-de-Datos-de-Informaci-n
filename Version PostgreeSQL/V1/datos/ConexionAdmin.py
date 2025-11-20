# ConexionAdmin.py

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from rutas import ruta_recurso
import os

class ConexionAdmin:
    """
    Clase para conexión administrativa a PostgreSQL.
    Permite ejecutar scripts SQL directamente usando psycopg2.
    """

    def __init__(self, user, password, host="localhost", port=5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

        # Script para crear la base de datos
        self.script_creacion_bd = ruta_recurso("cosasDB/creacionPrev.sql")

        # Rutas de los scripts en orden de ejecución
        self.rutas_scripts = [
            ruta_recurso("cosasDB/base_datos.sql"),
            ruta_recurso("cosasDB/triggers.sql"),
            ruta_recurso("cosasDB/procedimientos.sql"),
            ruta_recurso("cosasDB/insertgod.sql")
        ]

    def conectar(self, database="postgres"):
        """
        Establece conexión a una base de datos específica.
        """
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print(f"✓ Conexión administrativa exitosa a la base '{database}'")
        except psycopg2.Error as e:
            print(f"✗ Error al conectar a '{database}': {e}")
            self.conn = None
            self.cursor = None

    def ejecutar_script(self, ruta_script):
        """
        Ejecuta un archivo SQL completo.
        """
        if not self.conn or not self.cursor:
            print("✗ No hay conexión activa. Conecte primero.")
            return False

        try:
            with open(ruta_script, "r", encoding="utf-8") as f:
                sql_script = f.read()

            # Ejecutar el script completo
            self.cursor.execute(sql_script)
            self.conn.commit()
            
            print(f"✓ Script '{os.path.basename(ruta_script)}' ejecutado correctamente")
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Error ejecutando script '{os.path.basename(ruta_script)}':")
            print(f"  {e}")
            self.conn.rollback()
            return False
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {ruta_script}")
            return False

    def crear_base_datos(self, nombre_bd):
        """
        Crea una base de datos nueva.
        Debe estar conectado a 'postgres' y con AUTOCOMMIT activado.
        """
        if not self.conn or not self.cursor:
            print("✗ No hay conexión activa.")
            return False

        try:
            # Activar AUTOCOMMIT para poder crear bases de datos
            old_isolation_level = self.conn.isolation_level
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Verificar si la base de datos existe
            self.cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (nombre_bd,)
            )
            
            if self.cursor.fetchone():
                print(f"⚠ La base de datos '{nombre_bd}' ya existe. Será eliminada y recreada.")
                
                # Terminar todas las conexiones activas a la base de datos
                self.cursor.execute(sql.SQL("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = %s AND pid <> pg_backend_pid()
                """), (nombre_bd,))
                
                # Eliminar la base de datos
                self.cursor.execute(sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(nombre_bd)
                ))
                print(f"✓ Base de datos '{nombre_bd}' eliminada")

            # Crear la base de datos
            self.cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(nombre_bd)
            ))
            print(f"✓ Base de datos '{nombre_bd}' creada exitosamente")

            # Restaurar el nivel de aislamiento
            self.conn.set_isolation_level(old_isolation_level)
            return True

        except psycopg2.Error as e:
            print(f"✗ Error al crear la base de datos '{nombre_bd}': {e}")
            return False

    def cargar_todos_los_scripts(self):
        """
        Ejecuta todos los scripts en el orden definido en self.rutas_scripts.
        """
        print("\n" + "="*50)
        print("EJECUTANDO SCRIPTS DE CONFIGURACIÓN")
        print("="*50)
        
        exitos = 0
        fallos = 0
        
        for script in self.rutas_scripts:
            if self.ejecutar_script(script):
                exitos += 1
            else:
                fallos += 1
        
        print("\n" + "="*50)
        print(f"RESUMEN: {exitos} exitosos, {fallos} fallidos")
        print("="*50 + "\n")

    def crear_base_y_ejecutar_scripts(self, nombre_bd):
        """
        1. Se conecta a 'postgres' y crea la base de datos
        2. Se conecta a la nueva base de datos
        3. Ejecuta todos los scripts de configuración
        """
        print("\n" + "="*60)
        print(f"INICIANDO CONFIGURACIÓN DE BASE DE DATOS: {nombre_bd}")
        print("="*60 + "\n")

        # Paso 1: Conectar a postgres y crear la base de datos
        self.conectar("postgres")
        if not self.crear_base_datos(nombre_bd):
            print("✗ No se pudo crear la base de datos. Proceso abortado.")
            self.desconectar()
            return False
        self.desconectar()

        # Paso 2: Conectar a la nueva base de datos
        self.conectar(nombre_bd)
        if not self.conn:
            print("✗ No se pudo conectar a la nueva base de datos.")
            return False

        # Paso 3: Ejecutar todos los scripts
        self.cargar_todos_los_scripts()
        
        # Paso 4: Cerrar conexión
        self.desconectar()
        
        print("\n" + "="*60)
        print(f"CONFIGURACIÓN COMPLETADA: {nombre_bd}")
        print("="*60 + "\n")
        return True

    def desconectar(self):
        """
        Cierra el cursor y la conexión de manera segura.
        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if self.conn:
            self.conn.close()
            self.conn = None
            print("✓ Conexión administrativa cerrada\n")


