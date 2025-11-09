# datos/procedimientos.py
from datos.conexion import ConexionDB
from mysql.connector import Error

# --- Función para login de usuario ---
def sp_login_usuario(usuario, contrasena):
    """
    Llama al procedimiento almacenado 'sp_login_usuario' en MySQL.
    Devuelve los resultados del procedimiento o lanza una excepción.
    """
    db = ConexionDB()  # Usa los valores por defecto de conexion.py
    db.conectar()
    cursor = db.obtener_cursor()
    resultados = None

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        # Llamada al procedimiento almacenado
        cursor.callproc("sp_login_usuario", (usuario, contrasena))
        
        # Extraer los resultados del procedimiento
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# --- Función para registrar usuario ---
def sp_registrar_usuario(usuario, contrasena, nombre):
    """
    Llama al procedimiento almacenado 'sp_registrar_usuario' en MySQL.
    """
    db = ConexionDB()  # Usa la conexión por defecto
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_registrar_usuario", (usuario, contrasena, nombre))
        db.conexion.commit()  # Confirmar cambios
        return True
    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()
