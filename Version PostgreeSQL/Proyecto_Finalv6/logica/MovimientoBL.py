from datos.conexion import ConexionDB
from typing import List, Dict, Optional
from datetime import datetime


class MovimientoBL:
    @staticmethod
    def obtener_movimientos_inventario(limite: int = 100) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_movimientos_inventario() LIMIT :limite"
            resultados = db.ejecutar(sql, {"limite": limite})
            
            if not resultados:
                print("ℹ️ No hay movimientos de inventario registrados")
                return []
            
            movimientos = []
            for fila in resultados:
                movimiento = {
                    'id_documento': fila.get('id_documento'),
                    'tipo_doc': fila.get('tipo_doc'),
                    'fecha': fila.get('fecha'),
                    'producto': fila.get('producto'),
                    'cantidad': fila.get('cantidad'),
                    'estado': fila.get('estado'),
                    'tipo_movimiento': fila.get('tipo_movimiento', 'SALIDA'),
                    'fecha_formateada': MovimientoBL._formatear_fecha(fila.get('fecha'))
                }
                movimientos.append(movimiento)
            
            print(f"✅ Se obtuvieron {len(movimientos)} movimientos")
            return movimientos
            
        except Exception as e:
            print(f"❌ Error al obtener movimientos: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def _formatear_fecha(fecha) -> str:
        if fecha is None:
            return "N/A"
        
        if isinstance(fecha, datetime):
            return fecha.strftime('%d/%m/%Y')
        elif isinstance(fecha, str):
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                return fecha_obj.strftime('%d/%m/%Y')
            except:
                return fecha
        else:
            return str(fecha)

    @staticmethod
    def buscar_movimientos(termino_busqueda: str, limite: int = 100) -> Optional[List[Dict]]:
        if not termino_busqueda:
            return MovimientoBL.obtener_movimientos_inventario(limite)
        
        movimientos = MovimientoBL.obtener_movimientos_inventario(limite)
        
        if not movimientos:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        # Filtrar movimientos
        movimientos_filtrados = [
            movimiento for movimiento in movimientos
            if (termino in movimiento['producto'].lower() or
                termino in movimiento['tipo_doc'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(movimientos_filtrados)} resultados")
        return movimientos_filtrados

    @staticmethod
    def obtener_movimientos_por_producto(id_producto: int, limite: int = 50) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_obtener_movimientos_por_producto(:id_producto)
                LIMIT :limite
            """
            
            resultados = db.ejecutar(sql, {
                "id_producto": id_producto,
                "limite": limite
            })
            
            if not resultados:
                return []
            
            movimientos = []
            for fila in resultados:
                movimiento = {
                    'id_documento': fila.get('id_documento'),
                    'tipo_doc': fila.get('tipo_doc'),
                    'fecha': fila.get('fecha'),
                    'producto': fila.get('producto'),
                    'cantidad': fila.get('cantidad'),
                    'estado': fila.get('estado'),
                    'tipo_movimiento': fila.get('tipo_movimiento', 'SALIDA'),
                    'fecha_formateada': MovimientoBL._formatear_fecha(fila.get('fecha'))
                }
                movimientos.append(movimiento)
            
            return movimientos
            
        except Exception as e:
            print(f"❌ Error al obtener movimientos por producto: {e}")
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_movimientos_por_fecha(fecha_inicio: str, fecha_fin: str) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_obtener_movimientos_por_fecha(
                    CAST(:fecha_inicio AS DATE),
                    CAST(:fecha_fin AS DATE)
                )
                ORDER BY fecha DESC
            """
            
            resultados = db.ejecutar(sql, {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            })
            
            if not resultados:
                return []
            
            movimientos = []
            for fila in resultados:
                movimiento = {
                    'id_documento': fila.get('id_documento'),
                    'tipo_doc': fila.get('tipo_doc'),
                    'fecha': fila.get('fecha'),
                    'producto': fila.get('producto'),
                    'cantidad': fila.get('cantidad'),
                    'estado': fila.get('estado'),
                    'tipo_movimiento': fila.get('tipo_movimiento', 'SALIDA'),
                    'fecha_formateada': MovimientoBL._formatear_fecha(fila.get('fecha'))
                }
                movimientos.append(movimiento)
            
            return movimientos
            
        except Exception as e:
            print(f"❌ Error al obtener movimientos por fecha: {e}")
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_estadisticas_movimientos() -> Dict:
        movimientos = MovimientoBL.obtener_movimientos_inventario(1000)
        
        if not movimientos:
            return {
                'total': 0,
                'entradas': 0,
                'salidas': 0,
                'emitidos': 0,
                'pendientes': 0,
                'anulados': 0
            }
        
        entradas = sum(1 for m in movimientos if m['tipo_movimiento'] == 'ENTRADA')
        salidas = sum(1 for m in movimientos if m['tipo_movimiento'] == 'SALIDA')
        emitidos = sum(1 for m in movimientos if m['estado'] == 'EMITIDO')
        pendientes = sum(1 for m in movimientos if m['estado'] == 'PENDIENTE')
        anulados = sum(1 for m in movimientos if m['estado'] == 'ANULADO')
        
        return {
            'total': len(movimientos),
            'entradas': entradas,
            'salidas': salidas,
            'emitidos': emitidos,
            'pendientes': pendientes,
            'anulados': anulados
        }

    @staticmethod
    def obtener_productos_mas_movidos(limite: int = 10) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT 
                    p.nombre AS producto,
                    COUNT(d.id_producto) AS total_movimientos,
                    SUM(d.cantidad) AS cantidad_total
                FROM trs_detalle_documento d
                JOIN mae_producto p ON d.id_producto = p.id_producto
                JOIN trs_encabezado_documento e ON d.id_documento = e.id_documento
                WHERE e.estado_doc = 'EMITIDO'
                GROUP BY p.nombre
                ORDER BY total_movimientos DESC
                LIMIT :limite
            """
            
            resultados = db.ejecutar(sql, {"limite": limite})
            
            if not resultados:
                return []
            
            productos = []
            for fila in resultados:
                producto = {
                    'producto': fila.get('producto'),
                    'total_movimientos': fila.get('total_movimientos'),
                    'cantidad_total': fila.get('cantidad_total')
                }
                productos.append(producto)
            
            return productos
            
        except Exception as e:
            print(f"❌ Error al obtener productos más movidos: {e}")
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def formatear_tipo_movimiento(tipo_movimiento: str, cantidad: int) -> tuple:
        if tipo_movimiento == 'SALIDA':
            return f"➖ SALIDA ({cantidad})", "error"
        else:
            return f"➕ ENTRADA ({cantidad})", "success"

    @staticmethod
    def formatear_estado(estado: str) -> str:
        if estado == 'EMITIDO':
            return "✅ Emitido"
        elif estado == 'PENDIENTE':
            return "⏳ Pendiente"
        elif estado == 'ANULADO':
            return "❌ Anulado"
        else:
            return estado