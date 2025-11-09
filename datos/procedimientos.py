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

# ============================================================================
# PROCEDIMIENTOS DE INSERCIÓN - MAESTROS
# ============================================================================

def sp_insertar_ubicacion(descripcion):
    """
    Inserta una nueva ubicación en la base de datos.
    
    :param descripcion: Descripción de la ubicación
    :return: ID de la ubicación insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_ubicacion", (descripcion,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_identidad(tipo_identificacion, codigo_documento):
    """
    Inserta una nueva identidad en la base de datos.
    
    :param tipo_identificacion: Tipo de identificación (DNI, etc.)
    :param codigo_documento: Código del documento
    :return: ID de la identidad insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_identidad", (tipo_identificacion, codigo_documento))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_cliente(nombre, apellido, id_ubicacion, id_identidad):
    """
    Inserta un nuevo cliente en la base de datos.
    
    :param nombre: Nombre del cliente
    :param apellido: Apellido del cliente
    :param id_ubicacion: ID de la ubicación
    :param id_identidad: ID de la identidad
    :return: ID del cliente insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_cliente", (nombre, apellido, id_ubicacion, id_identidad))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_empresa(nombre, razon_social, ruc, id_ubicacion):
    """
    Inserta una nueva empresa en la base de datos.
    
    :param nombre: Nombre de la empresa
    :param razon_social: Razón social de la empresa
    :param ruc: RUC de la empresa (11 dígitos)
    :param id_ubicacion: ID de la ubicación
    :return: ID de la empresa insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_empresa", (nombre, razon_social, ruc, id_ubicacion))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_conductor(nombre, n_licencia):
    """
    Inserta un nuevo conductor en la base de datos.
    
    :param nombre: Nombre del conductor
    :param n_licencia: Número de licencia
    :return: ID del conductor insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_conductor", (nombre, n_licencia))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_vehiculo(descripcion, placa):
    """
    Inserta un nuevo vehículo en la base de datos.
    
    :param descripcion: Descripción del vehículo
    :param placa: Placa del vehículo
    :return: ID del vehículo insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_vehiculo", (descripcion, placa))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_producto(nombre, descripcion, precio_base, stock, unidad_medida):
    """
    Inserta un nuevo producto en la base de datos.
    
    :param nombre: Nombre del producto
    :param descripcion: Descripción del producto
    :param precio_base: Precio base del producto
    :param stock: Stock inicial
    :param unidad_medida: Unidad de medida
    :return: ID del producto insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_producto", (nombre, descripcion, precio_base, stock, unidad_medida))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_forma_pago(nombre, descripcion):
    """
    Inserta una nueva forma de pago en la base de datos.
    
    :param nombre: Nombre de la forma de pago
    :param descripcion: Descripción de la forma de pago
    :return: ID de la forma de pago insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_forma_pago", (nombre, descripcion))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_moneda(codigo_iso, nombre):
    """
    Inserta una nueva moneda en la base de datos.
    
    :param codigo_iso: Código ISO de la moneda
    :param nombre: Nombre de la moneda
    :return: ID de la moneda insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_moneda", (codigo_iso, nombre))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# ============================================================================
# PROCEDIMIENTOS DE INSERCIÓN - TRANSACCIONALES
# ============================================================================

def sp_insertar_encabezado_documento(tipo_doc, fecha_emision, id_empresa, id_cliente, id_forma_pago, id_moneda):
    """
    Inserta un nuevo encabezado de documento en la base de datos.
    
    :param tipo_doc: Tipo de documento (Boleta, Factura, etc.)
    :param fecha_emision: Fecha de emisión
    :param id_empresa: ID de la empresa
    :param id_cliente: ID del cliente
    :param id_forma_pago: ID de la forma de pago
    :param id_moneda: ID de la moneda
    :return: ID del documento insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_encabezado_documento", 
                       (tipo_doc, fecha_emision, id_empresa, id_cliente, id_forma_pago, id_moneda))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_detalle_documento(id_documento, id_producto, cantidad, subtotal, igv, importe):
    """
    Inserta un nuevo detalle de documento en la base de datos.
    
    :param id_documento: ID del documento
    :param id_producto: ID del producto
    :param cantidad: Cantidad del producto
    :param subtotal: Subtotal del detalle
    :param igv: IGV del detalle
    :param importe: Importe total del detalle
    :return: ID del detalle insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_detalle_documento", 
                       (id_documento, id_producto, cantidad, subtotal, igv, importe))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_encabezado_guia(id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado, 
                               motivo_traslado, direccion_partida, direccion_llegada, 
                               id_conductor, id_vehiculo):
    """
    Inserta un nuevo encabezado de guía en la base de datos.
    
    :param id_doc_venta: ID del documento de venta
    :param nro_guia: Número de guía
    :param fecha_emision: Fecha de emisión
    :param fecha_inicio_traslado: Fecha de inicio de traslado
    :param motivo_traslado: Motivo del traslado
    :param direccion_partida: Dirección de partida
    :param direccion_llegada: Dirección de llegada
    :param id_conductor: ID del conductor
    :param id_vehiculo: ID del vehículo
    :return: ID de la guía insertada
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_encabezado_guia", 
                       (id_doc_venta, nro_guia, fecha_emision, fecha_inicio_traslado,
                        motivo_traslado, direccion_partida, direccion_llegada,
                        id_conductor, id_vehiculo))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_insertar_detalle_guia(id_guia, id_producto, descripcion, unidad_medida, 
                            unidad_peso_bruto, peso_total_carga, modalidad_trans,
                            transbordo_prog, categoriaM1_L, retorno_envases, 
                            vehiculo_vacio, id_conductor, id_vehiculo):
    """
    Inserta un nuevo detalle de guía en la base de datos.
    
    :param id_guia: ID de la guía
    :param id_producto: ID del producto
    :param descripcion: Descripción del producto
    :param unidad_medida: Unidad de medida
    :param unidad_peso_bruto: Unidad de peso bruto
    :param peso_total_carga: Peso total de la carga
    :param modalidad_trans: Modalidad de transporte
    :param transbordo_prog: Transbordo programado
    :param categoriaM1_L: Categoría M1/L
    :param retorno_envases: Retorno de envases
    :param vehiculo_vacio: Vehículo vacío
    :param id_conductor: ID del conductor
    :param id_vehiculo: ID del vehículo
    :return: ID del detalle de guía insertado
    """
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_insertar_detalle_guia", 
                       (id_guia, id_producto, descripcion, unidad_medida,
                        unidad_peso_bruto, peso_total_carga, modalidad_trans,
                        transbordo_prog, categoriaM1_L, retorno_envases,
                        vehiculo_vacio, id_conductor, id_vehiculo))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados[0][0] if resultados else None

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()