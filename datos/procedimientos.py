# datos/procedimientos.py
from datos.conexion import ConexionDB
from mysql.connector import Error


def sp_login_empresa(usuario, clave):
    """
    Llama al procedimiento almacenado 'sp_login_empresa' en MySQL.
    Devuelve los resultados del procedimiento o lanza una excepción.
    
    :param usuario: Nombre de la empresa
    :param clave: RUC de la empresa
    :return: Lista con resultados del login
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()
    resultados = None

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_login_empresa", (usuario, clave))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_registrar_empresa(nombre, razon_social, ruc, id_ubicacion):
    """
    Llama al procedimiento almacenado 'sp_registrar_empresa' en MySQL.
    Registra una nueva empresa o reactiva una existente.
    
    :param nombre: Nombre de la empresa
    :param razon_social: Razón social de la empresa
    :param ruc: RUC de 11 dígitos
    :param id_ubicacion: ID de la ubicación
    :return: Lista con resultados (mensaje y id_empresa)
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_registrar_empresa", (nombre, razon_social, ruc, id_ubicacion))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# ============================================================================
# PROCEDIMIENTOS DE CONSULTA DE GUÍAS
# ============================================================================

def sp_listar_guias_empresa(id_empresa):
    """
    Lista todas las guías de remisión de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Lista de guías con información completa
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_listar_guias_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_listar_guias_pendientes_empresa(id_empresa):
    """
    Lista las guías de remisión pendientes de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Lista de guías pendientes
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_listar_guias_pendientes_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# ============================================================================
# PROCEDIMIENTOS DE CONSULTA DE PRODUCTOS Y STOCK
# ============================================================================

def sp_detalle_productos_empresa(id_empresa):
    """
    Obtiene el detalle de productos vendidos por una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Lista de productos con cantidad, precio e importe
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_detalle_productos_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_listar_stock_empresa(id_empresa):
    """
    Lista el stock de productos de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Lista de productos con stock disponible
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_listar_stock_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# ============================================================================
# PROCEDIMIENTOS DE CONSULTA DE CLIENTES
# ============================================================================

def sp_listar_clientes_empresa(id_empresa):
    """
    Lista todos los clientes de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Lista de clientes con información completa
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_listar_clientes_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# ============================================================================
# PROCEDIMIENTOS CON PARÁMETROS OUT (Contadores y Totales)
# ============================================================================

def sp_contar_documentos_emitidos(id_empresa):
    """
    Cuenta los documentos emitidos de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Cantidad de documentos emitidos
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        # Para procedimientos con OUT, usamos una variable @total
        cursor.execute(f"CALL sp_contar_documentos_emitidos({id_empresa}, @total)")
        cursor.execute("SELECT @total AS total")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_contar_documentos_pendientes(id_empresa):
    """
    Cuenta los documentos pendientes de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Cantidad de documentos pendientes
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_contar_documentos_pendientes({id_empresa}, @total)")
        cursor.execute("SELECT @total AS total")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_contar_guias_pendientes(id_empresa):
    """
    Cuenta las guías de remisión pendientes de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Cantidad de guías pendientes
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_contar_guias_pendientes({id_empresa}, @total)")
        cursor.execute("SELECT @total AS total")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_stock_total_empresa(id_empresa):
    """
    Obtiene el stock total de productos de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Stock total
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_stock_total_empresa({id_empresa}, @total_stock)")
        cursor.execute("SELECT @total_stock AS total_stock")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_total_ventas_empresa(id_empresa):
    """
    Calcula el total de ventas de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Total de ventas en decimal
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_total_ventas_empresa({id_empresa}, @total_ventas)")
        cursor.execute("SELECT @total_ventas AS total_ventas")
        resultado = cursor.fetchone()
        
        return float(resultado[0]) if resultado and resultado[0] else 0.0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_contar_clientes_activos(id_empresa):
    """
    Cuenta los clientes activos de una empresa.
    
    :param id_empresa: ID de la empresa
    :return: Cantidad de clientes activos
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_contar_clientes_activos({id_empresa}, @total_clientes)")
        cursor.execute("SELECT @total_clientes AS total_clientes")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()