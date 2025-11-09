from datos.conexion import ConexionDB
from mysql.connector import Error


def sp_login_empresa(usuario, clave):
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


def sp_listar_guias_empresa(id_empresa):
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

def sp_detalle_productos_empresa(id_empresa):
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

def sp_listar_clientes_empresa(id_empresa):
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

def sp_contar_documentos_emitidos(id_empresa):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.execute(f"CALL sp_contar_documentos_emitidos({id_empresa}, @total)")
        cursor.execute("SELECT @total AS total")
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else 0

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


def sp_contar_documentos_pendientes(id_empresa):
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

def sp_insertar_ubicacion(descripcion):
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


def sp_insertar_encabezado_documento(tipo_doc, fecha_emision, id_empresa, id_cliente, id_forma_pago, id_moneda):
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