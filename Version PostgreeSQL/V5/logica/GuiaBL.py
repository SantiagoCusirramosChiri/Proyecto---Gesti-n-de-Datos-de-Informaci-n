# logica/GuiaBL.py

from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class GuiaBL:
    """
    Capa de Lógica de Negocio para Guías de Remisión.
    Maneja todas las operaciones relacionadas con guías de remisión.
    """

    @staticmethod
    def obtener_guias_empresa(id_empresa: int, filtro: str = "TODOS") -> Optional[List[Dict]]:
        """
        Obtiene guías de remisión de una empresa con filtro opcional.
        
        Args:
            id_empresa: ID de la empresa
            filtro: Filtro de estado ('TODOS', 'PENDIENTE', 'EMITIDO', 'ANULADO')
        
        Returns:
            List[Dict]: Lista de guías
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_guias_empresa(:id_empresa)"
            resultados = db.ejecutar(sql, {"id_empresa": id_empresa})
            
            if not resultados:
                print("ℹ️ No hay guías registradas")
                return []
            
            # Convertir a diccionarios
            guias = []
            for fila in resultados:
                guia = {
                    'id_guia': fila.get('id_guia'),
                    'nro_guia': fila.get('nro_guia'),
                    'fecha_emision': fila.get('fecha_emision'),
                    'fecha_traslado': fila.get('fecha_inicio_traslado'),  # Campo correcto
                    'motivo_traslado': fila.get('motivo_traslado'),
                    'punto_partida': fila.get('direccion_partida'),  # Campo correcto
                    'punto_llegada': fila.get('direccion_llegada'),  # Campo correcto
                    'conductor': fila.get('conductor'),
                    'vehiculo': fila.get('vehiculo'),
                    'estado_guia': fila.get('estado_guia'),
                    'tipo_doc': fila.get('tipo_doc'),
                    'id_documento': fila.get('id_documento'),
                    'documento_relacionado': f"{fila.get('tipo_doc', '')} #{fila.get('id_documento', '')}" if fila.get('id_documento') else 'N/A',
                    'fecha_emision_formateada': GuiaBL._formatear_fecha(fila.get('fecha_emision')),
                    'fecha_traslado_formateada': GuiaBL._formatear_fecha(fila.get('fecha_inicio_traslado'))
                }
                
                # Aplicar filtro
                if filtro != "TODOS" and guia['estado_guia'] != filtro:
                    continue
                
                guias.append(guia)
            
            print(f"✅ Se obtuvieron {len(guias)} guías")
            return guias
            
        except Exception as e:
            print(f"❌ Error al obtener guías: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def _formatear_fecha(fecha) -> str:
        """
        Formatea una fecha al formato DD/MM/YYYY.
        
        Args:
            fecha: Fecha a formatear
        
        Returns:
            str: Fecha formateada
        """
        if fecha is None:
            return "N/A"
        
        if isinstance(fecha, datetime):
            return fecha.strftime('%d/%m/%Y')
        elif hasattr(fecha, 'strftime'):
            return fecha.strftime('%d/%m/%Y')
        else:
            return str(fecha)

    @staticmethod
    def obtener_detalle_guia(id_guia: int) -> Optional[List[Dict]]:
        """
        Obtiene el detalle de productos de una guía.
        
        Args:
            id_guia: ID de la guía
        
        Returns:
            List[Dict]: Lista de productos de la guía
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_detalle_guia(:id_guia)"
            resultados = db.ejecutar(sql, {"id_guia": id_guia})
            
            if not resultados:
                print(f"ℹ️ No hay detalles para la guía {id_guia}")
                return []
            
            detalles = []
            for fila in resultados:
                detalle = {
                    'producto': fila.get('producto'),
                    'descripcion': fila.get('descripcion', ''),
                    'unidad_medida': fila.get('unidad_medida', 'UND'),
                    'peso_total': fila.get('peso_total_carga', 0.0),
                    'modalidad': fila.get('modalidad_trans', 'N/A')
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
    def actualizar_estado_guia(id_guia: int, nuevo_estado: str) -> Tuple[bool, str]:
        """
        Actualiza el estado de una guía.
        
        Args:
            id_guia: ID de la guía
            nuevo_estado: Nuevo estado ('EMITIDO' o 'ANULADO')
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not id_guia or id_guia <= 0:
            return False, "ID de guía inválido"
        
        if nuevo_estado not in ['EMITIDO', 'ANULADO']:
            return False, "Estado inválido. Use 'EMITIDO' o 'ANULADO'"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_estado_guia(
                    :id_guia,
                    CAST(:nuevo_estado AS VARCHAR(10))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_guia": id_guia,
                "nuevo_estado": nuevo_estado
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', f'Guía {nuevo_estado.lower()} correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, f"No se pudo {nuevo_estado.lower()} la guía"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar estado: {error_msg}")
            
            # Detectar errores comunes
            if 'pendiente' in error_msg.lower():
                return False, "Solo se pueden anular guías pendientes"
            
            if 'emitida' in error_msg.lower() or 'anulada' in error_msg.lower():
                return False, "No se puede modificar una guía que ya está emitida o anulada"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar estado: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def formatear_estado_badge(estado: str) -> Tuple[str, str]:
        """
        Obtiene el emoji y color del badge según el estado.
        
        Args:
            estado: Estado de la guía
        
        Returns:
            Tuple[str, str]: (emoji, color_tipo)
        """
        if estado == "EMITIDO":
            return "✅", "success"
        elif estado == "ANULADO":
            return "❌", "error"
        else:  # PENDIENTE
            return "⏳", "warning"

    @staticmethod
    def obtener_conductores_combo() -> List[Tuple]:
        """
        Obtiene conductores para ComboBox.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, nombre, licencia)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_conductores_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay conductores disponibles")
                return []
            
            conductores = []
            for fila in resultados:
                conductores.append((
                    fila.get('id_conductor'),
                    fila.get('nombre'),
                    fila.get('n_licencia')
                ))
            
            print(f"✅ Se obtuvieron {len(conductores)} conductores")
            return conductores
            
        except Exception as e:
            print(f"❌ Error al obtener conductores: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_vehiculos_combo() -> List[Tuple]:
        """
        Obtiene vehículos para ComboBox.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, placa, descripcion)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_vehiculos_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay vehículos disponibles")
                return []
            
            vehiculos = []
            for fila in resultados:
                vehiculos.append((
                    fila.get('id_vehiculo'),
                    fila.get('placa'),
                    fila.get('descripcion', '')
                ))
            
            print(f"✅ Se obtuvieron {len(vehiculos)} vehículos")
            return vehiculos
            
        except Exception as e:
            print(f"❌ Error al obtener vehículos: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_ubicaciones_combo() -> List[Tuple]:
        """
        Obtiene ubicaciones para ComboBox.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, descripcion)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_ubicaciones_combo()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay ubicaciones disponibles")
                return []
            
            ubicaciones = []
            for fila in resultados:
                ubicaciones.append((
                    fila.get('id_ubicacion'),
                    fila.get('descripcion')
                ))
            
            print(f"✅ Se obtuvieron {len(ubicaciones)} ubicaciones")
            return ubicaciones
            
        except Exception as e:
            print(f"❌ Error al obtener ubicaciones: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_documentos_combo() -> List[Tuple]:
        """
        Obtiene documentos emitidos para ComboBox.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, tipo_doc, numero)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT id_documento, tipo_doc 
                FROM trs_encabezado_documento 
                WHERE estado_doc = 'EMITIDO'
                ORDER BY id_documento DESC
                LIMIT 50
            """
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay documentos emitidos disponibles")
                return []
            
            documentos = []
            for fila in resultados:
                documentos.append((
                    fila.get('id_documento'),
                    fila.get('tipo_doc')
                ))
            
            print(f"✅ Se obtuvieron {len(documentos)} documentos")
            return documentos
            
        except Exception as e:
            print(f"❌ Error al obtener documentos: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_estadisticas_guias(id_empresa: int) -> Dict:
        """
        Obtiene estadísticas de guías de una empresa.
        
        Args:
            id_empresa: ID de la empresa
        
        Returns:
            Dict: Estadísticas de guías
        """
        guias = GuiaBL.obtener_guias_empresa(id_empresa, "TODOS")
        
        if not guias:
            return {
                'total': 0,
                'pendientes': 0,
                'emitidas': 0,
                'anuladas': 0
            }
        
        pendientes = sum(1 for g in guias if g['estado_guia'] == 'PENDIENTE')
        emitidas = sum(1 for g in guias if g['estado_guia'] == 'EMITIDO')
        anuladas = sum(1 for g in guias if g['estado_guia'] == 'ANULADO')
        
        return {
            'total': len(guias),
            'pendientes': pendientes,
            'emitidas': emitidas,
            'anuladas': anuladas
        }

    @staticmethod
    def obtener_documentos_emitidos(id_empresa: int) -> Optional[List[Tuple]]:
        """
        Obtiene documentos emitidos para crear guías.
        
        Args:
            id_empresa: ID de la empresa
        
        Returns:
            List[Tuple]: Lista de tuplas (id, tipo_doc, fecha, cliente)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT 
                    d.id_documento,
                    d.tipo_doc,
                    d.fecha_emision,
                    CONCAT(c.nombre, ' ', COALESCE(c.apellido, '')) AS cliente
                FROM trs_encabezado_documento d
                INNER JOIN mae_cliente c ON d.id_cliente = c.id_cliente
                WHERE d.id_empresa = :id_empresa
                  AND d.estado_doc = 'EMITIDO'
                ORDER BY d.fecha_emision DESC
                LIMIT 50
            """
            
            resultados = db.ejecutar(sql, {"id_empresa": id_empresa})
            
            if not resultados:
                print("ℹ️ No hay documentos emitidos disponibles")
                return []
            
            documentos = []
            for fila in resultados:
                documentos.append((
                    fila.get('id_documento'),
                    fila.get('tipo_doc'),
                    fila.get('fecha_emision'),
                    fila.get('cliente')
                ))
            
            print(f"✅ Se obtuvieron {len(documentos)} documentos emitidos")
            return documentos
            
        except Exception as e:
            print(f"❌ Error al obtener documentos emitidos: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_productos_documento(id_documento: int) -> Optional[List[Tuple]]:
        """
        Obtiene productos de un documento para la guía.
        
        Args:
            id_documento: ID del documento
        
        Returns:
            List[Tuple]: Lista de tuplas (id_producto, nombre, cantidad, unidad_medida)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT 
                    p.id_producto,
                    p.nombre,
                    d.cantidad,
                    p.unidad_medida
                FROM trs_detalle_documento d
                INNER JOIN mae_producto p ON d.id_producto = p.id_producto
                WHERE d.id_documento = :id_documento
                ORDER BY p.nombre
            """
            
            resultados = db.ejecutar(sql, {"id_documento": id_documento})
            
            if not resultados:
                print(f"ℹ️ No hay productos en el documento {id_documento}")
                return []
            
            productos = []
            for fila in resultados:
                productos.append((
                    fila.get('id_producto'),
                    fila.get('nombre'),
                    fila.get('cantidad'),
                    fila.get('unidad_medida')
                ))
            
            print(f"✅ Se obtuvieron {len(productos)} productos del documento")
            return productos
            
        except Exception as e:
            print(f"❌ Error al obtener productos del documento: {e}")
            return []
            
        finally:
            db.desconectar()

    @staticmethod
    def verificar_guia_existe(nro_guia: str) -> bool:
        """
        Verifica si ya existe una guía con ese número.
        
        Args:
            nro_guia: Número de guía a verificar
        
        Returns:
            bool: True si existe, False si no
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT COUNT(*) as cantidad
                FROM trs_encabezado_guia
                WHERE nro_guia = :nro_guia
            """
            
            resultado = db.ejecutar(sql, {"nro_guia": nro_guia})
            
            if resultado and len(resultado) > 0:
                cantidad = resultado[0].get('cantidad', 0)
                existe = cantidad > 0
                
                if existe:
                    print(f"⚠️ La guía {nro_guia} ya existe")
                
                return existe
            
            return False
            
        except Exception as e:
            print(f"❌ Error al verificar guía: {e}")
            return False
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_numero_guia(nro_guia: str) -> Tuple[bool, str]:
        """
        Valida el formato del número de guía.
        
        Args:
            nro_guia: Número de guía a validar
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not nro_guia or nro_guia.strip() == "":
            return False, "El número de guía no puede estar vacío"
        
        nro_guia = nro_guia.strip()
        
        if len(nro_guia) < 5:
            return False, "El número de guía debe tener al menos 5 caracteres"
        
        if len(nro_guia) > 20:
            return False, "El número de guía no puede exceder 20 caracteres"
        
        return True, "Número de guía válido"

    @staticmethod
    def validar_fecha_traslado(fecha_emision: str, fecha_traslado: str) -> Tuple[bool, str]:
        """
        Valida que la fecha de traslado no sea anterior a la emisión.
        
        Returns:
            Tuple[bool, str]: (válida, mensaje)
        """
        try:
            fecha_em = datetime.strptime(fecha_emision, '%Y-%m-%d')
            fecha_tr = datetime.strptime(fecha_traslado, '%Y-%m-%d')
            
            if fecha_tr < fecha_em:
                return False, "La fecha de traslado no puede ser anterior a la fecha de emisión"
            
            return True, "Fechas válidas"
            
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"

    @staticmethod
    def insertar_encabezado_guia(id_doc_venta: int, nro_guia: str, fecha_emision: str,
                                  fecha_traslado: str, motivo: str, dir_partida: str,
                                  dir_llegada: str, id_conductor: int, 
                                  id_vehiculo: int) -> Tuple[bool, str, Optional[int]]:
        """
        Inserta el encabezado de una guía de remisión.
        
        Returns:
            Tuple[bool, str, Optional[int]]: (éxito, mensaje, id_guia)
        """
        # Validaciones
        valido_nro, msg_nro = GuiaBL.validar_numero_guia(nro_guia)
        if not valido_nro:
            return False, msg_nro, None
        
        valido_fecha, msg_fecha = GuiaBL.validar_fecha_traslado(fecha_emision, fecha_traslado)
        if not valido_fecha:
            return False, msg_fecha, None
        
        if not motivo or motivo.strip() == "":
            return False, "El motivo de traslado es obligatorio", None
        
        if not dir_partida or dir_partida.strip() == "":
            return False, "La dirección de partida es obligatoria", None
        
        if not dir_llegada or dir_llegada.strip() == "":
            return False, "La dirección de llegada es obligatoria", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_encabezado_guia(
                    :id_doc_venta,
                    CAST(:nro_guia AS VARCHAR(20)),
                    CAST(:fecha_emision AS DATE),
                    CAST(:fecha_traslado AS DATE),
                    CAST(:motivo AS VARCHAR(100)),
                    CAST(:dir_partida AS VARCHAR(150)),
                    CAST(:dir_llegada AS VARCHAR(150)),
                    :id_conductor,
                    :id_vehiculo
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_doc_venta": id_doc_venta,
                "nro_guia": nro_guia,
                "fecha_emision": fecha_emision,
                "fecha_traslado": fecha_traslado,
                "motivo": motivo,
                "dir_partida": dir_partida,
                "dir_llegada": dir_llegada,
                "id_conductor": id_conductor,
                "id_vehiculo": id_vehiculo
            })
            
            if resultado and len(resultado) > 0:
                id_guia = resultado[0].get('id_guia')
                print(f"✅ Guía creada con ID: {id_guia}")
                return True, f"Guía N° {nro_guia} creada correctamente", id_guia
            else:
                return False, "No se pudo crear la guía", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar guía: {error_msg}")
            
            if 'duplicate' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El número de guía {nro_guia} ya existe", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al crear guía: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def insertar_detalle_guia(id_guia: int, id_producto: int, descripcion: str,
                             unidad_medida: str, unidad_peso_bruto: str, peso_total: float,
                             modalidad: str, transbordo: str, categoria: str,
                             retorno: str, vehiculo_vacio: str, id_conductor: int,
                             id_vehiculo: int) -> Tuple[bool, str]:
        """
        Inserta el detalle de una guía de remisión.
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_detalle_guia(
                    :id_guia,
                    :id_producto,
                    CAST(:descripcion AS VARCHAR(100)),
                    CAST(:unidad_medida AS VARCHAR(10)),
                    CAST(:unidad_peso_bruto AS VARCHAR(10)),
                    CAST(:peso_total AS NUMERIC(10,2)),
                    CAST(:modalidad AS VARCHAR(20)),
                    CAST(:transbordo AS CHAR(2)),
                    CAST(:categoria AS CHAR(2)),
                    CAST(:retorno AS CHAR(2)),
                    CAST(:vehiculo_vacio AS CHAR(2)),
                    :id_conductor,
                    :id_vehiculo
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_guia": id_guia,
                "id_producto": id_producto,
                "descripcion": descripcion[:100] if descripcion else "",  # Limitar a 100
                "unidad_medida": unidad_medida[:10] if unidad_medida else "UND",
                "unidad_peso_bruto": unidad_peso_bruto[:10] if unidad_peso_bruto else "KG",
                "peso_total": peso_total,
                "modalidad": modalidad[:20] if modalidad else "PRIVADO",
                "transbordo": transbordo[:2] if transbordo else "NO",  # CHAR(2)
                "categoria": categoria[:2] if categoria else "NO",    # CHAR(2)
                "retorno": retorno[:2] if retorno else "NO",        # CHAR(2)
                "vehiculo_vacio": vehiculo_vacio[:2] if vehiculo_vacio else "NO",  # CHAR(2)
                "id_conductor": id_conductor,
                "id_vehiculo": id_vehiculo
            })
            
            print(f"✅ Detalle de guía insertado para producto {id_producto}")
            return True, "Detalle insertado correctamente"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar detalle de guía: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar detalle: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def crear_guia_completa(id_doc_venta: int, nro_guia: str, fecha_emision: str,
                           fecha_traslado: str, motivo: str, dir_partida: str,
                           dir_llegada: str, id_conductor: int, id_vehiculo: int,
                           productos: List[Dict]) -> Tuple[bool, str, Optional[int]]:
        """
        Crea una guía completa con encabezado y detalles.
        
        Args:
            productos: Lista de diccionarios con productos
        
        Returns:
            Tuple[bool, str, Optional[int]]: (éxito, mensaje, id_guia)
        """
        # Validar que haya productos
        if not productos or len(productos) == 0:
            return False, "Debe seleccionar al menos un producto", None
        
        # Insertar encabezado
        exito_enc, mensaje_enc, id_guia = GuiaBL.insertar_encabezado_guia(
            id_doc_venta, nro_guia, fecha_emision, fecha_traslado,
            motivo, dir_partida, dir_llegada, id_conductor, id_vehiculo
        )
        
        if not exito_enc:
            return False, mensaje_enc, None
        
        # Insertar detalles
        errores = []
        for prod in productos:
            exito_det, mensaje_det = GuiaBL.insertar_detalle_guia(
                id_guia=id_guia,
                id_producto=prod['id'],
                descripcion=prod['nombre'],
                unidad_medida=prod['unidad_medida'],
                unidad_peso_bruto="KG",
                peso_total=0.00,
                modalidad="PRIVADO",
                transbordo="NO",
                categoria="NO",
                retorno="NO",
                vehiculo_vacio="NO",
                id_conductor=id_conductor,
                id_vehiculo=id_vehiculo
            )
            
            if not exito_det:
                errores.append(f"Producto {prod['nombre']}: {mensaje_det}")
        
        if errores:
            return False, f"Errores al insertar detalles:\n" + "\n".join(errores), id_guia
        
        return True, f"Guía N° {nro_guia} creada correctamente\n\nEstado: PENDIENTE", id_guia