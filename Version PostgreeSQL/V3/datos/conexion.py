# datos/conexion.py - SOLO SQLALCHEMY

import os
import sys

# ✅ CRÍTICO: Configurar encoding ANTES de importar cualquier cosa
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# ✅ Monkey patch para forzar cp1252 al leer archivos del sistema
if sys.platform == 'win32':
    import locale
    _original_getpreferredencoding = locale.getpreferredencoding
    
    def _custom_getpreferredencoding(do_setlocale=True):
        return 'cp1252'
    
    locale.getpreferredencoding = _custom_getpreferredencoding

# AHORA SÍ importar las librerías
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2  # Solo para la función creator

# Restaurar el encoding original
if sys.platform == 'win32':
    locale.getpreferredencoding = _original_getpreferredencoding

class ConexionDB:
    """
    Clase para manejar la conexión a PostgreSQL usando SQLAlchemy.
    Ejecuta procedimientos, triggers y queries, devolviendo resultados como diccionarios.
    """

    def __init__(
        self,
        host="localhost",
        user="lolcito",
        password="12345678",
        database="sistema_documentos",
        port=5432
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

        self.engine = None
        self.session = None

    def conectar(self):
        """Crea el engine y la sesión SQLAlchemy"""
        try:
            # Crear conexión directa sin DSN
            def get_connection():
                conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    user=self.user,
                    password=self.password
                )
                # Configurar UTF-8 después de conectar
                conn.set_client_encoding('UTF8')
                return conn
            
            # Crear engine sin URL de conexión
            self.engine = create_engine(
                'postgresql+psycopg2://',
                creator=get_connection,
                echo=False,
                pool_pre_ping=True,
                isolation_level="AUTOCOMMIT"  # ✅ Para permitir CREATE DATABASE
            )
            
            # Probar conexión
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print(f"Conexión SQLAlchemy exitosa a '{self.database}'")
            
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            import traceback
            traceback.print_exc()
            self.engine = None
            self.session = None

    def crear_base_datos_y_ejecutar_scripts(self):
        """
        Crea la base de datos y ejecuta todos los scripts de configuración.
        IMPORTANTE: El usuario 'lolcito' debe existir previamente.
        """
        from rutas import ruta_recurso
        
        print("\n" + "="*60)
        print("CONFIGURANDO BASE DE DATOS")
        print("="*60 + "\n")

        try:
            # Paso 1: Conectar a 'postgres' para crear la BD
            print("[1/3] Conectando a 'postgres' para crear la base de datos...")
            
            # Crear engine temporal para postgres con AUTOCOMMIT
            def get_postgres_connection():
                conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname="postgres",
                    user=self.user,
                    password=self.password
                )
                conn.set_client_encoding('UTF8')
                return conn
            
            engine_postgres = create_engine(
                'postgresql+psycopg2://',
                creator=get_postgres_connection,
                echo=False,
                isolation_level="AUTOCOMMIT"
            )

            # Paso 2: Ejecutar creacionPrev.sql
            print("[2/3] Creando base de datos 'sistema_documentos'...")
            script_path = ruta_recurso("cosasDB/creacionPrev.sql")
            
            with open(script_path, "r", encoding="utf-8", errors='replace') as f:
                sql_script = f.read()
            
            # Ejecutar con SQLAlchemy
            with engine_postgres.connect() as conn:
                # Ejecutar comando por comando
                comandos = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
                for comando in comandos:
                    if comando:
                        try:
                            conn.execute(text(comando))
                        except Exception as e:
                            if "already exists" not in str(e):
                                print(f"  ⚠ Advertencia: {e}")

            engine_postgres.dispose()
            print("✓ Base de datos creada exitosamente")

            # Paso 3: Conectar a la nueva BD y ejecutar scripts de estructura
            print("[3/3] Ejecutando scripts de estructura...")
            
            # Crear engine para la nueva BD (SIN AUTOCOMMIT para estos scripts)
            def get_new_db_connection():
                conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    user=self.user,
                    password=self.password
                )
                conn.set_client_encoding('UTF8')
                return conn
            
            self.engine = create_engine(
                'postgresql+psycopg2://',
                creator=get_new_db_connection,
                echo=False,
                pool_pre_ping=True
            )

            # Ejecutar scripts
            rutas_scripts = [
                ruta_recurso("cosasDB/base_datos.sql"),
                ruta_recurso("cosasDB/triggers.sql"),
                ruta_recurso("cosasDB/procedimientos.sql"),
                ruta_recurso("cosasDB/insertgod.sql")
            ]

            exitos = 0
            fallos = 0

            with self.engine.connect() as conn:
                for script in rutas_scripts:
                    try:
                        print(f"  Ejecutando {os.path.basename(script)}...")
                        with open(script, "r", encoding="utf-8", errors='replace') as f:
                            sql_content = f.read()
                        
                        # Ejecutar dentro de una transacción
                        trans = conn.begin()
                        try:
                            conn.execute(text(sql_content))
                            trans.commit()
                            exitos += 1
                            print(f"  ✓ OK")
                        except Exception as e:
                            trans.rollback()
                            raise e
                            
                    except Exception as e:
                        print(f"  ✗ Error: {e}")
                        fallos += 1

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print("\n" + "="*60)
            print(f"✓ CONFIGURACIÓN COMPLETADA ({exitos} exitosos, {fallos} fallidos)")
            print("="*60 + "\n")

            return fallos == 0

        except Exception as e:
            print(f"✗ Error en la configuración: {e}")
            import traceback
            traceback.print_exc()
            return False

    def desconectar(self):
        """Cierra sesión y engine"""
        if self.session:
            self.session.close()
            print("Sesión SQLAlchemy cerrada")
        if self.engine:
            self.engine.dispose()
            print("Engine SQLAlchemy cerrado")

    def ejecutar(self, sql, parametros=None):
        """
        Ejecuta SQL (procedimientos, triggers y selects) y retorna resultado como lista de diccionarios.
        IMPORTANTE: Hace COMMIT automático para operaciones de escritura (INSERT, UPDATE, DELETE).
        """
        if not self.engine:
            print("No hay conexión activa")
            return None
        
        try:
            with self.engine.connect() as conn:
                # Iniciar transacción explícita
                trans = conn.begin()
                
                try:
                    # Ejecutar SQL
                    resultado = conn.execute(text(sql), parametros or {})
                    
                    # ✅ COMMIT para operaciones de escritura
                    trans.commit()
                    
                    # Si retorna filas, convertir a lista de diccionarios
                    if resultado.returns_rows:
                        return resultado.mappings().all()
                    
                    return None
                    
                except Exception as e:
                    # Si hay error, hacer ROLLBACK
                    trans.rollback()
                    raise e
                    
        except Exception as e:
            print("Error al ejecutar SQL:", e)
            import traceback
            traceback.print_exc()
            return None