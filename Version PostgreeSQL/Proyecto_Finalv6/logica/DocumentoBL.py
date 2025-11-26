from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from decimal import Decimal


class DocumentoBL:
    TIPOS_DOCUMENTO = ["Boleta", "Factura"]

    @staticmethod
    def validar_id_empresa(id_empresa) -> Tuple[bool, str, Optional[int]]:
        try:
            # tupla o lista, extraer el entero
            if isinstance(id_empresa, (tuple, list)):
                for item in id_empresa:
                    if isinstance(item, int):
                        return True, "ID válido", item
                
                #  convertir el segundo elemento o el primero
                try:
                    id_int = int(id_empresa[1]) if len(id_empresa) > 1 else int(id_empresa[0])
                    return True, "ID válido", id_int
                except (ValueError, IndexError, TypeError):
                    return False, f"ID de empresa inválido: {id_empresa}", None
            
            # si es entero directo
            id_int = int(id_empresa)
            return True, "ID válido", id_int
            
        except (ValueError, TypeError):
            return False, f"ID de empresa inválido: {id_empresa}", None

    @staticmethod
    def obtener_clientes_combo() -> List[Tuple]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_clientes_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay clientes disponibles")
                return []
            
            clientes = []
            for fila in resultados:
                clientes.append((
                    fila.get('id_cliente'),
                    fila.get('nombre'),
                    fila.get('apellido', '')
                ))
            
            print(f"✅ Se obtuvieron {len(clientes)} clientes")
            return clientes
            
        except Exception as e:
            print(f"❌ Error al obtener clientes: {e}")
            import traceback
            traceback.print_exc()
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_formas_pago_combo() -> List[Tuple]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_formas_pago_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay formas de pago disponibles")
                return []
            
            formas_pago = []
            for fila in resultados:
                formas_pago.append((
                    fila.get('id_forma_pago'),
                    fila.get('nombre')
                ))
            
            print(f"✅ Se obtuvieron {len(formas_pago)} formas de pago")
            return formas_pago
            
        except Exception as e:
            print(f"❌ Error al obtener formas de pago: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_monedas_combo() -> List[Tuple]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_monedas_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay monedas disponibles")
                return []
            
            monedas = []
            for fila in resultados:
                monedas.append((
                    fila.get('id_moneda'),
                    fila.get('nombre'),
                    fila.get('codigo_iso')
                ))
            
            print(f"✅ Se obtuvieron {len(monedas)} monedas")
            return monedas
            
        except Exception as e:
            print(f"❌ Error al obtener monedas: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_productos_combo() -> List[Tuple]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_productos_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay productos disponibles")
                return []
            
            productos = []
            for fila in resultados:
                productos.append((
                    fila.get('id_producto'),
                    fila.get('nombre'),
                    fila.get('precio_base'),
                    fila.get('stock')
                ))
            
            print(f"✅ Se obtuvieron {len(productos)} productos")
            return productos
            
        except Exception as e:
            print(f"❌ Error al obtener productos: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_fecha(fecha_str: str) -> Tuple[bool, str]:
        if not fecha_str or fecha_str.strip() == "":
            return False, "La fecha no puede estar vacía"
        
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            fecha_hoy = datetime.now()
            
            if fecha > fecha_hoy:
                return False, "La fecha no puede ser futura"
            
            diferencia_dias = (fecha_hoy - fecha).days
            if diferencia_dias > 365:
                return False, "La fecha no puede ser mayor a 1 año atrás"
            
            return True, "Fecha válida"
            
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"

    @staticmethod
    def validar_carrito(carrito: List[Dict]) -> Tuple[bool, str]:
        if not carrito or len(carrito) == 0:
            return False, "Debe agregar al menos un producto"
        
        for item in carrito:
            if item['cantidad'] <= 0:
                return False, f"Cantidad inválida para {item['nombre']}"
            
            if item['precio'] <= 0:
                return False, f"Precio inválido para {item['nombre']}"
        
        return True, "Carrito válido"

    @staticmethod
    def calcular_subtotal(cantidad: int, precio: float) -> float:
        return round(cantidad * precio, 2)

    @staticmethod
    def calcular_igv(subtotal: float, porcentaje: float = 0.18) -> float:
        return round(subtotal * porcentaje, 2)

    @staticmethod
    def calcular_importe(subtotal: float, igv: float) -> float:
        return round(subtotal + igv, 2)

    # validaciones
    @staticmethod
    def insertar_encabezado_documento(tipo_doc: str, fecha: str, id_empresa: int,
                                      id_cliente: int, id_forma_pago: int, 
                                      id_moneda: int) -> Tuple[bool, str, Optional[int]]:
        if tipo_doc not in DocumentoBL.TIPOS_DOCUMENTO:
            return False, "Tipo de documento inválido", None
        
        fecha_valida, mensaje_fecha = DocumentoBL.validar_fecha(fecha)
        if not fecha_valida:
            return False, mensaje_fecha, None
        
        if not id_empresa or id_empresa <= 0:
            return False, "ID de empresa inválido", None
        
        if not id_cliente or id_cliente <= 0:
            return False, "Cliente no seleccionado", None
        
        if not id_forma_pago or id_forma_pago <= 0:
            return False, "Forma de pago no seleccionada", None
        
        if not id_moneda or id_moneda <= 0:
            return False, "Moneda no seleccionada", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_encabezado_documento(
                    CAST(:tipo_doc AS VARCHAR(10)),
                    CAST(:fecha AS DATE),
                    :id_empresa,
                    :id_cliente,
                    :id_forma_pago,
                    :id_moneda
                )
            """
            
            resultado = db.ejecutar(sql, {
                "tipo_doc": tipo_doc,
                "fecha": fecha,
                "id_empresa": id_empresa,
                "id_cliente": id_cliente,
                "id_forma_pago": id_forma_pago,
                "id_moneda": id_moneda
            })
            
            if resultado and len(resultado) > 0:
                id_documento = resultado[0].get('id_documento')
                print(f"✅ Encabezado de documento creado con ID: {id_documento}")
                return True, f"Documento N° {id_documento} creado", id_documento
            else:
                return False, "No se pudo crear el encabezado del documento", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar encabezado: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, f"Error al crear documento: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def insertar_detalle_documento(id_documento: int, id_producto: int, cantidad: int,
                                   subtotal: float, igv: float, importe: float) -> Tuple[bool, str]:
        if not id_documento or id_documento <= 0:
            return False, "ID de documento inválido"
        
        if not id_producto or id_producto <= 0:
            return False, "ID de producto inválido"
        
        if cantidad <= 0:
            return False, "Cantidad debe ser mayor a 0"
        
        if subtotal < 0 or igv < 0 or importe < 0:
            return False, "Montos no pueden ser negativos"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_detalle_documento(
                    :id_documento,
                    :id_producto,
                    :cantidad,
                    CAST(:subtotal AS NUMERIC(10,2)),
                    CAST(:igv AS NUMERIC(10,2)),
                    CAST(:importe AS NUMERIC(10,2))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_documento": id_documento,
                "id_producto": id_producto,
                "cantidad": cantidad,
                "subtotal": subtotal,
                "igv": igv,
                "importe": importe
            })
            
            print(f"✅ Detalle insertado: Producto {id_producto}, Cant: {cantidad}, "
                  f"Subtotal: {subtotal}, IGV: {igv}, Importe: {importe}")
            return True, "Detalle insertado correctamente"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar detalle: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar detalle: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def crear_documento_completo(tipo_doc: str, fecha: str, id_empresa: int,
                                id_cliente: int, id_forma_pago: int, id_moneda: int,
                                carrito: List[Dict]) -> Tuple[bool, str, Optional[int]]:
        # validar carrito
        carrito_valido, mensaje_carrito = DocumentoBL.validar_carrito(carrito)
        if not carrito_valido:
            return False, mensaje_carrito, None
        
        # validar ID empresa
        id_valido, mensaje_id, id_empresa_norm = DocumentoBL.validar_id_empresa(id_empresa)
        if not id_valido:
            return False, mensaje_id, None
        
        # insertar encabezado
        exito_enc, mensaje_enc, id_documento = DocumentoBL.insertar_encabezado_documento(
            tipo_doc, fecha, id_empresa_norm, id_cliente, id_forma_pago, id_moneda
        )
        
        if not exito_enc:
            return False, mensaje_enc, None
        
        # insertar detalles
        errores = []
        for item in carrito:
            id_producto = item['id']
            cantidad = int(item['cantidad'])
            precio = float(item['precio'])
            
            subtotal = DocumentoBL.calcular_subtotal(cantidad, precio)
            igv = DocumentoBL.calcular_igv(subtotal)
            importe = DocumentoBL.calcular_importe(subtotal, igv)
            
            exito_det, mensaje_det = DocumentoBL.insertar_detalle_documento(
                id_documento, id_producto, cantidad, subtotal, igv, importe
            )
            
            if not exito_det:
                errores.append(f"Producto {item['nombre']}: {mensaje_det}")
        
        if errores:
            return False, f"Errores al insertar detalles:\n" + "\n".join(errores), id_documento
        
        return True, f"Documento N° {id_documento} creado correctamente\n\nEstado: PENDIENTE", id_documento

    @staticmethod
    def calcular_total_carrito(carrito: List[Dict]) -> float:
        total = 0.0
        for item in carrito:
            precio = float(item['precio'])
            cantidad = int(item['cantidad'])
            total += precio * cantidad
        
        return round(total, 2)

    @staticmethod
    def obtener_documentos_empresa(id_empresa: int, filtro: str = "TODOS") -> Optional[List[Dict]]:
        # validar ID empresa
        id_valido, mensaje, id_empresa_norm = DocumentoBL.validar_id_empresa(id_empresa)
        if not id_valido:
            print(f"❌ {mensaje}")
            return None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_documentos_empresa(:id_empresa)"
            resultados = db.ejecutar(sql, {"id_empresa": id_empresa_norm})
            
            if not resultados:
                print("ℹ️ No hay documentos registrados")
                return []
            
            # convertir a diccionarios
            documentos = []
            for fila in resultados:
                documento = {
                    'id_documento': fila.get('id_documento'),
                    'tipo_doc': fila.get('tipo_doc'),
                    'fecha_emision': fila.get('fecha_emision'),
                    'cliente': fila.get('cliente'),
                    'forma_pago': fila.get('forma_pago'),
                    'moneda': fila.get('moneda'),
                    'estado_doc': fila.get('estado_doc'),
                    'fecha_formateada': DocumentoBL._formatear_fecha_doc(fila.get('fecha_emision'))
                }
                
                if filtro != "TODOS" and documento['estado_doc'] != filtro:
                    continue
                
                documentos.append(documento)
            
            print(f"✅ Se obtuvieron {len(documentos)} documentos")
            return documentos
            
        except Exception as e:
            print(f"❌ Error al obtener documentos: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def _formatear_fecha_doc(fecha) -> str:
        if fecha is None:
            return "N/A"
        
        if isinstance(fecha, datetime):
            return fecha.strftime('%d/%m/%Y')
        elif hasattr(fecha, 'strftime'):
            return fecha.strftime('%d/%m/%Y')
        else:
            return str(fecha)

    @staticmethod
    def obtener_detalle_documento(id_documento: int) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_detalle_documento(:id_documento)"
            resultados = db.ejecutar(sql, {"id_documento": id_documento})
            
            if not resultados:
                print(f"ℹ️ No hay detalles para el documento {id_documento}")
                return []
            
            detalles = []
            for fila in resultados:
                detalle = {
                    'producto': fila.get('producto'),
                    'cantidad': fila.get('cantidad'),
                    'subtotal': fila.get('subtotal'),
                    'igv': fila.get('igv'),
                    'importe': fila.get('importe')
                }
                detalles.append(detalle)
            
            print(f"✅ Se obtuvieron {len(detalles)} detalles")
            return detalles
            
        except Exception as e:
            print(f"❌ Error al obtener detalle: {e}")
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_estado_documento(id_documento: int, nuevo_estado: str) -> Tuple[bool, str]:
        if not id_documento or id_documento <= 0:
            return False, "ID de documento inválido"
        
        if nuevo_estado not in ['EMITIDO', 'ANULADO']:
            return False, "Estado inválido. Use 'EMITIDO' o 'ANULADO'"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_estado_documento(
                    :id_documento,
                    CAST(:nuevo_estado AS VARCHAR(10))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_documento": id_documento,
                "nuevo_estado": nuevo_estado
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', f'Documento {nuevo_estado.lower()} correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, f"No se pudo {nuevo_estado.lower()} el documento"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar estado: {error_msg}")
            
            # Detectar errores comunes
            if 'pendiente' in error_msg.lower():
                return False, "Solo se pueden anular documentos pendientes"
            
            if 'stock' in error_msg.lower() or 'insuficiente' in error_msg.lower():
                return False, "Stock insuficiente para emitir el documento"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar estado: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def formatear_estado_badge(estado: str) -> Tuple[str, str]:
        if estado == "EMITIDO":
            return "✅", "success"
        elif estado == "ANULADO":
            return "❌", "error"
        else:  # PENDIENTE
            return "⏳", "warning"

    @staticmethod
    def calcular_total_documento(detalles: List[Dict]) -> float:
        if not detalles:
            return 0.0
        
        total = sum(detalle.get('importe', 0) for detalle in detalles)
        return round(total, 2)

    @staticmethod
    def obtener_estadisticas_documentos(id_empresa: int) -> Dict:
        documentos = DocumentoBL.obtener_documentos_empresa(id_empresa, "TODOS")
        
        if not documentos:
            return {
                'total': 0,
                'pendientes': 0,
                'emitidos': 0,
                'anulados': 0,
                'boletas': 0,
                'facturas': 0
            }
        
        pendientes = sum(1 for d in documentos if d['estado_doc'] == 'PENDIENTE')
        emitidos = sum(1 for d in documentos if d['estado_doc'] == 'EMITIDO')
        anulados = sum(1 for d in documentos if d['estado_doc'] == 'ANULADO')
        boletas = sum(1 for d in documentos if d['tipo_doc'] == 'Boleta')
        facturas = sum(1 for d in documentos if d['tipo_doc'] == 'Factura')
        
        return {
            'total': len(documentos),
            'pendientes': pendientes,
            'emitidos': emitidos,
            'anulados': anulados,
            'boletas': boletas,
            'facturas': facturas
        }