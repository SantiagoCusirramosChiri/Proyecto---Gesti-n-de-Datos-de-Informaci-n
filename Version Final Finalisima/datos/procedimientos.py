# procedimientos.py

from datos.conexion import ConexionDB
from mysql.connector import Error


# Autenticación

# Valida credenciales de empresa y retorna datos de sesión
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


# Registra una nueva empresa en el sistema
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


# Listado

# Lista todas las guías de remisión de una empresa
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


# Lista guías pendientes de una empresa
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


# Lista productos con detalles de una empresa
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


# Lista stock disponible de productos de una empresa
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


# Lista clientes asociados a una empresa
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

# Inserción - Maestras

# Inserta o reactiva una ubicación
def sp_insertar_ubicacion(descripcion):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_ubicacion FROM mae_ubicacion WHERE descripcion = %s AND activo = FALSE",
            (descripcion,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_ubicacion SET activo = TRUE WHERE id_ubicacion = %s",
                (existe_inactivo[0],)
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_ubicacion", (descripcion,))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta o reactiva una identidad
def sp_insertar_identidad(tipo_identificacion, codigo_documento):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_identidad FROM mae_identidad WHERE tipo_identificacion = %s AND codigo_documento = %s AND activo = FALSE",
            (tipo_identificacion, codigo_documento)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_identidad SET activo = TRUE WHERE id_identidad = %s",
                (existe_inactivo[0],)
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_identidad", (tipo_identificacion, codigo_documento))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta un nuevo cliente
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


# Inserta una nueva empresa
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


# Inserta o reactiva un conductor
def sp_insertar_conductor(nombre, n_licencia):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_conductor FROM mae_conductor WHERE n_licencia = %s AND activo = FALSE",
            (n_licencia,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_conductor SET nombre = %s, activo = TRUE WHERE id_conductor = %s",
                (nombre, existe_inactivo[0])
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_conductor", (nombre, n_licencia))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta o reactiva un vehículo
def sp_insertar_vehiculo(descripcion, placa):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_vehiculo FROM mae_vehiculo WHERE placa = %s AND activo = FALSE",
            (placa,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_vehiculo SET descripcion = %s, activo = TRUE WHERE id_vehiculo = %s",
                (descripcion, existe_inactivo[0])
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_vehiculo", (descripcion, placa))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta o reactiva una forma de pago
def sp_insertar_forma_pago(nombre, descripcion):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_forma_pago FROM mae_forma_pago WHERE nombre = %s AND activo = FALSE",
            (nombre,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_forma_pago SET descripcion = %s, activo = TRUE WHERE id_forma_pago = %s",
                (descripcion, existe_inactivo[0])
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_forma_pago", (nombre, descripcion))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta o reactiva una moneda
def sp_insertar_moneda(codigo_iso, nombre):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_moneda FROM mae_moneda WHERE codigo_iso = %s AND activo = FALSE",
            (codigo_iso,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_moneda SET nombre = %s, activo = TRUE WHERE id_moneda = %s",
                (nombre, existe_inactivo[0])
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_moneda", (codigo_iso, nombre))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserta o reactiva un producto
def sp_insertar_producto(nombre, descripcion, precio_base, stock, unidad_medida):
    db = ConexionDB()
    db.conectar()
    
    if not db.conexion:
        raise Exception("No se pudo conectar a la base de datos.")

    try:
        cursor = db.conexion.cursor()
        
        cursor.execute(
            "SELECT id_producto FROM mae_producto WHERE nombre = %s AND activo = FALSE",
            (nombre,)
        )
        existe_inactivo = cursor.fetchone()
        
        if existe_inactivo:
            cursor.execute(
                "UPDATE mae_producto SET descripcion = %s, precio_base = %s, stock = stock + %s, unidad_medida = %s, activo = TRUE WHERE id_producto = %s",
                (descripcion, precio_base, stock, unidad_medida, existe_inactivo[0])
            )
            db.conexion.commit()
            cursor.close()
            return existe_inactivo[0]
        else:
            cursor.callproc("sp_insertar_producto", (nombre, descripcion, precio_base, stock, unidad_medida))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            
            db.conexion.commit()
            cursor.close()
            return resultados[0][0] if resultados else None

    except Error as e:
        if db.conexion:
            db.conexion.rollback()
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        if db.conexion and db.conexion.is_connected():
            db.desconectar()


# Inserción - Transaccionales

# Inserta encabezado de documento de venta
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


# Inserta detalle de productos en documento
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


# Inserta encabezado de guía de remisión
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


# Inserta detalle de productos en guía de remisión
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


# CRUD - Conductores

# Obtiene lista de conductores activos
def obtener_conductores_activos():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_conductores_activos")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de un conductor
def actualizar_conductor(id_conductor, nombre, n_licencia):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_conductor", (id_conductor, nombre, n_licencia))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente un conductor
def desactivar_conductor(id_conductor):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_conductor", (id_conductor,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Vehículos

# Obtiene lista de vehículos activos
def obtener_vehiculos_activos():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_vehiculos_activos")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de un vehículo
def actualizar_vehiculo(id_vehiculo, descripcion, placa):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_vehiculo", (id_vehiculo, descripcion, placa))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente un vehículo
def desactivar_vehiculo(id_vehiculo):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_vehiculo", (id_vehiculo,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Formas de pago

# Obtiene lista de formas de pago activas
def obtener_formas_pago_activas():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_formas_pago_activas")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()

# Actualiza datos de una forma de pago
def actualizar_forma_pago(id_forma_pago, nombre, descripcion):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_forma_pago", (id_forma_pago, nombre, descripcion))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente una forma de pago
def desactivar_forma_pago(id_forma_pago):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_forma_pago", (id_forma_pago,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Monedas

# Obtiene lista de monedas activas
def obtener_monedas_activas():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_monedas_activas")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de una moneda
def actualizar_moneda(id_moneda, codigo_iso, nombre):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_moneda", (id_moneda, codigo_iso, nombre))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente una moneda
def desactivar_moneda(id_moneda):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_moneda", (id_moneda,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Ubicaciones

# Obtiene lista de ubicaciones activas
def obtener_ubicaciones_activas():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_ubicaciones_activas")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de una ubicación
def actualizar_ubicacion(id_ubicacion, descripcion):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_ubicacion", (id_ubicacion, descripcion))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente una ubicación
def desactivar_ubicacion(id_ubicacion):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_ubicacion", (id_ubicacion,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Identidades

# Obtiene lista de identidades activas
def obtener_identidades_activas():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_identidades_activas")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de una identidad
def actualizar_identidad(id_identidad, tipo_identificacion, codigo_documento):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_identidad", (id_identidad, tipo_identificacion, codigo_documento))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente una identidad
def desactivar_identidad(id_identidad):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_identidad", (id_identidad,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Clientes

# Obtiene lista de clientes activos
def obtener_clientes_activos():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_clientes_activos")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de un cliente
def actualizar_cliente(id_cliente, nombre, apellido, id_ubicacion, id_identidad):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_cliente", (id_cliente, nombre, apellido, id_ubicacion, id_identidad))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente un cliente
def desactivar_cliente(id_cliente):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_cliente", (id_cliente,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# CRUD - Productos

# Obtiene lista de productos activos
def obtener_productos_activos():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_productos_activos")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza datos de un producto
def actualizar_producto(id_producto, nombre, descripcion, precio_base, stock, unidad_medida):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_producto", (id_producto, nombre, descripcion, precio_base, stock, unidad_medida))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Desactiva lógicamente un producto
def desactivar_producto(id_producto):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_desactivar_producto", (id_producto,))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Ajusta stock de un producto manualmente
def ajustar_stock_producto(id_producto, cantidad, tipo_movimiento):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_ajustar_stock_producto", (id_producto, cantidad, tipo_movimiento))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        db.conexion.commit()
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Movimientos de inventario

# Obtiene historial de movimientos de stock
def obtener_movimientos_inventario():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_movimientos_inventario")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Documentos

# Obtiene documentos de venta de una empresa
def obtener_documentos_empresa(id_empresa):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_documentos_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene detalle de productos de un documento
def obtener_detalle_documento(id_documento):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_detalle_documento", (id_documento,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza estado de un documento
def actualizar_estado_documento(id_documento, nuevo_estado):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_estado_documento", (id_documento, nuevo_estado))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Guías de remisión

# Obtiene todas las guías de una empresa
def obtener_guias_empresa(id_empresa):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_guias_empresa", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene detalle de productos de una guía
def obtener_detalle_guia(id_guia):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_detalle_guia", (id_guia,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Actualiza estado de una guía
def actualizar_estado_guia(id_guia, nuevo_estado):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_actualizar_estado_guia", (id_guia, nuevo_estado))
        db.conexion.commit()

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Funciones para ComboBox

# Obtiene ubicaciones para combo box
def obtener_ubicaciones_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_ubicaciones_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene identidades para combo box
def obtener_identidades_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_identidades_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene clientes para combo box
def obtener_clientes_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_clientes_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene formas de pago para combo box
def obtener_formas_pago_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_formas_pago_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene monedas para combo box
def obtener_monedas_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_monedas_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene productos para combo box
def obtener_productos_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_productos_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene conductores para combo box
def obtener_conductores_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_conductores_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene vehículos para combo box
def obtener_vehiculos_combo():
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_vehiculos_combo")
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene documentos emitidos para crear guías
def obtener_documentos_emitidos(id_empresa):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_documentos_emitidos", (id_empresa,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Obtiene productos de un documento para la guía
def obtener_productos_documento(id_documento):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_obtener_productos_documento", (id_documento,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()


# Verifica si un número de guía ya existe
def verificar_guia_existe(nro_guia):
    db = ConexionDB()
    db.conectar()
    cursor = db.obtener_cursor()

    if not cursor:
        raise Exception("No se pudo obtener cursor de la base de datos.")

    try:
        cursor.callproc("sp_verificar_guia_existe", (nro_guia,))
        
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        
        return resultados[0][0] > 0 if resultados else False

    except Error as e:
        raise Exception(f"Error en procedimiento MySQL: {e}")
    finally:
        db.desconectar()