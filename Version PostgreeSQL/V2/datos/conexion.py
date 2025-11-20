# datos/conexion.py - CORREGIDO

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class ConexionDB:
    """
    Clase para manejar la conexión a PostgreSQL usando SQLAlchemy.
    Ejecuta procedimientos, triggers y queries, devolviendo resultados como diccionarios.
    """

    def __init__(
        self,
        host="localhost",
        user="root",
        password="santi",
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
            url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(url, echo=False)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print(f"Conexión SQLAlchemy exitosa a '{self.database}'")
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            self.engine = None
            self.session = None

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
        Ejecuta SQL (procedimientos, triggers, selects) y retorna resultado como lista de diccionarios.
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