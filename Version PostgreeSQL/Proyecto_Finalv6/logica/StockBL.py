# logica/StockBL.py

from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class StockBL:

    @staticmethod
    def obtener_productos_con_stock() -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_productos_activos()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay productos en inventario")
                return []
            
            # Convertir resultados a lista de diccionarios
            productos = []
            for fila in resultados:
                producto = {
                    'id_producto': fila.get('id_producto'),
                    'nombre': fila.get('nombre'),
                    'descripcion': fila.get('descripcion'),
                    'precio_base': fila.get('precio_base'),
                    'stock': fila.get('stock'),
                    'unidad_medida': fila.get('unidad_medida'),
                    'activo': fila.get('activo'),
                    'nivel_stock': StockBL._calcular_nivel_stock(fila.get('stock', 0))
                }
                productos.append(producto)
            
            print(f" Se obtuvieron {len(productos)} productos")
            return productos
            
        except Exception as e:
            print(f" Error al obtener productos: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def _calcular_nivel_stock(stock: int) -> str:
        if stock <= 0:
            return 'AGOTADO'
        elif stock <= 25:
            return 'BAJO'
        else:
            return 'NORMAL'

    @staticmethod
    def buscar_productos_stock(termino_busqueda: str) -> Optional[List[Dict]]:
        if not termino_busqueda:
            return StockBL.obtener_productos_con_stock()
        
        productos = StockBL.obtener_productos_con_stock()
        
        if not productos:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        # Filtrar productos
        productos_filtrados = [
            producto for producto in productos
            if (termino in producto['nombre'].lower() or
                termino in producto['descripcion'].lower())
        ]
        
        print(f" Búsqueda '{termino}': {len(productos_filtrados)} resultados")
        return productos_filtrados

    @staticmethod
    def ajustar_stock(id_producto: int, cantidad: int, tipo_movimiento: str) -> Tuple[bool, str]:

        # Validaciones
        if not id_producto or id_producto <= 0:
            return False, "ID de producto inválido"
        
        if not cantidad or cantidad <= 0:
            return False, "La cantidad debe ser mayor a 0"
        
        if tipo_movimiento not in ['ENTRADA', 'SALIDA']:
            return False, "Tipo de movimiento inválido. Use 'ENTRADA' o 'SALIDA'"
        
        # Validar stock suficiente para salidas
        if tipo_movimiento == 'SALIDA':
            producto = StockBL.obtener_producto_por_id(id_producto)
            if not producto:
                return False, "Producto no encontrado"
            
            if producto['stock'] < cantidad:
                return False, f"Stock insuficiente. Disponible: {producto['stock']}, Solicitado: {cantidad}"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_ajustar_stock_producto(
                    :id_producto,
                    :cantidad,
                    CAST(:tipo_movimiento AS VARCHAR(10))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_producto": id_producto,
                "cantidad": cantidad,
                "tipo_movimiento": tipo_movimiento
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', f'Stock {"aumentado" if tipo_movimiento == "ENTRADA" else "reducido"} correctamente')
                print(f" {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo ajustar el stock"
                
        except Exception as e:
            error_msg = str(e)
            print(f" Error al ajustar stock: {error_msg}")
            
            # Detectar errores comunes
            if 'stock negativo' in error_msg.lower() or 'insufficient' in error_msg.lower():
                return False, "No hay suficiente stock para realizar la salida"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al ajustar stock: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_cantidad(cantidad_str: str) -> Tuple[bool, str, Optional[int]]:
        if not cantidad_str or cantidad_str.strip() == "":
            return False, "La cantidad no puede estar vacía", None
        
        try:
            cantidad = int(cantidad_str.strip())
            
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0", None
            
            if cantidad > 10000:
                return False, "La cantidad no puede exceder 10,000 unidades", None
            
            return True, "Cantidad válida", cantidad
            
        except ValueError:
            return False, "Ingrese un número válido", None

    @staticmethod
    def obtener_producto_por_id(id_producto: int) -> Optional[Dict]:
        productos = StockBL.obtener_productos_con_stock()
        
        if not productos:
            return None
        
        for producto in productos:
            if producto['id_producto'] == id_producto:
                return producto
        
        return None

    @staticmethod
    def obtener_estadisticas_stock() -> Dict:
        productos = StockBL.obtener_productos_con_stock()
        
        if not productos:
            return {
                'total': 0,
                'agotados': 0,
                'bajo_stock': 0,
                'stock_normal': 0,
                'valor_total': 0.0
            }
        
        agotados = sum(1 for p in productos if p['nivel_stock'] == 'AGOTADO')
        bajo_stock = sum(1 for p in productos if p['nivel_stock'] == 'BAJO')
        stock_normal = sum(1 for p in productos if p['nivel_stock'] == 'NORMAL')
        valor_total = sum(p['stock'] * p['precio_base'] for p in productos)
        
        return {
            'total': len(productos),
            'agotados': agotados,
            'bajo_stock': bajo_stock,
            'stock_normal': stock_normal,
            'valor_total': valor_total
        }

    @staticmethod
    def obtener_productos_bajo_stock() -> List[Dict]:
        productos = StockBL.obtener_productos_con_stock()
        
        if not productos:
            return []
        
        return [
            producto for producto in productos
            if producto['nivel_stock'] in ['AGOTADO', 'BAJO']
        ]

    @staticmethod
    def validar_stock_suficiente(id_producto: int, cantidad_requerida: int) -> Tuple[bool, str]:
        producto = StockBL.obtener_producto_por_id(id_producto)
        
        if not producto:
            return False, "Producto no encontrado"
        
        if producto['stock'] < cantidad_requerida:
            return False, f"Stock insuficiente. Disponible: {producto['stock']}, Requerido: {cantidad_requerida}"
        
        return True, "Stock suficiente"

    @staticmethod
    def obtener_historial_movimientos(id_producto: int) -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_obtener_historial_stock(:id_producto)
                ORDER BY fecha DESC
                LIMIT 50
            """
            
            resultados = db.ejecutar(sql, {"id_producto": id_producto})
            
            if not resultados:
                return []
            
            movimientos = []
            for fila in resultados:
                movimiento = {
                    'id_movimiento': fila.get('id_movimiento'),
                    'fecha': fila.get('fecha'),
                    'tipo_movimiento': fila.get('tipo_movimiento'),
                    'cantidad': fila.get('cantidad'),
                    'stock_anterior': fila.get('stock_anterior'),
                    'stock_nuevo': fila.get('stock_nuevo'),
                    'usuario': fila.get('usuario', 'Sistema')
                }
                movimientos.append(movimiento)
            
            return movimientos
            
        except Exception as e:
            print(f"❌ Error al obtener historial: {e}")
            return None
            
        finally:
            db.desconectar()