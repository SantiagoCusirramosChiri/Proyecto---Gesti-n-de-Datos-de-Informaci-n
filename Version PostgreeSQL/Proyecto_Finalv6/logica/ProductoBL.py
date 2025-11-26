from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class ProductoBL:
    UNIDADES_MEDIDA = ["UND", "KG", "LT", "M", "M2", "M3", "CAJA", "PAQUETE"]

    @staticmethod
    def obtener_productos_activos() -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_productos_activos()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay productos activos")
                return []
            
            productos = []
            for fila in resultados:
                producto = {
                    'id_producto': fila.get('id_producto'),
                    'nombre': fila.get('nombre'),
                    'descripcion': fila.get('descripcion'),
                    'precio_base': fila.get('precio_base'),
                    'stock': fila.get('stock'),
                    'unidad_medida': fila.get('unidad_medida'),
                    'activo': fila.get('activo')
                }
                productos.append(producto)
            
            print(f"✅ Se obtuvieron {len(productos)} productos")
            return productos
            
        except Exception as e:
            print(f"❌ Error al obtener productos: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def insertar_producto(nombre: str, descripcion: str, precio_base: float, 
                         stock: int, unidad_medida: str) -> Tuple[bool, str, Optional[int]]:
        # Validaciones
        if not nombre or not descripcion:
            return False, "Nombre y descripción son obligatorios", None
        
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres", None
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres", None
        
        if len(descripcion) > 255:
            return False, "La descripción no puede exceder 255 caracteres", None
        
        if precio_base <= 0:
            return False, "El precio debe ser mayor a 0", None
        
        if stock < 0:
            return False, "El stock no puede ser negativo", None
        
        if unidad_medida not in ProductoBL.UNIDADES_MEDIDA:
            return False, f"Unidad de medida inválida. Use: {', '.join(ProductoBL.UNIDADES_MEDIDA)}", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_producto(
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:descripcion AS VARCHAR(255)),
                    CAST(:precio_base AS NUMERIC(10,2)),
                    :stock,
                    CAST(:unidad_medida AS VARCHAR(10))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio_base": precio_base,
                "stock": stock,
                "unidad_medida": unidad_medida
            })
            
            if resultado and len(resultado) > 0:
                id_producto = resultado[0].get('id_producto')
                print(f"✅ Producto insertado con ID: {id_producto}")
                return True, f"Producto '{nombre}' registrado correctamente", id_producto
            else:
                return False, "No se pudo insertar el producto", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar producto: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El producto '{nombre}' ya está registrado", None
            
            if 'reactivado' in error_msg.lower():
                return False, "Este producto ya existe y fue reactivado automáticamente", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar producto: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_producto(id_producto: int, nombre: str, descripcion: str,
                           precio_base: float, stock: int, unidad_medida: str) -> Tuple[bool, str]:
        # Validaciones
        if not id_producto or id_producto <= 0:
            return False, "ID de producto inválido"
        
        if not nombre or not descripcion:
            return False, "Nombre y descripción son obligatorios"
        
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        if len(descripcion) > 255:
            return False, "La descripción no puede exceder 255 caracteres"
        
        if precio_base <= 0:
            return False, "El precio debe ser mayor a 0"
        
        if stock < 0:
            return False, "El stock no puede ser negativo"
        
        if unidad_medida not in ProductoBL.UNIDADES_MEDIDA:
            return False, f"Unidad de medida inválida"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_producto(
                    :id_producto,
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:descripcion AS VARCHAR(255)),
                    CAST(:precio_base AS NUMERIC(10,2)),
                    :stock,
                    CAST(:unidad_medida AS VARCHAR(10))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_producto": id_producto,
                "nombre": nombre,
                "descripcion": descripcion,
                "precio_base": precio_base,
                "stock": stock,
                "unidad_medida": unidad_medida
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Producto actualizado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar el producto"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar producto: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El nombre '{nombre}' ya está registrado"
            
            if 'precio' in error_msg.lower() and '50%' in error_msg.lower():
                return False, "El nuevo precio no puede ser menor al 50% del precio anterior"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar producto: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_producto(id_producto: int) -> Tuple[bool, str]:
        if not id_producto or id_producto <= 0:
            return False, "ID de producto inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_producto(:id_producto)"
            resultado = db.ejecutar(sql, {"id_producto": id_producto})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Producto desactivado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar el producto"
                
        except Exception as e:
            print(f"❌ Error al desactivar producto: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar producto: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        nombre = nombre.strip()
        
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        return True, "Nombre válido"

    @staticmethod
    def validar_descripcion(descripcion: str) -> Tuple[bool, str]:
        if not descripcion or descripcion.strip() == "":
            return False, "La descripción no puede estar vacía"
        
        descripcion = descripcion.strip()
        
        if len(descripcion) > 255:
            return False, "La descripción no puede exceder 255 caracteres"
        
        return True, "Descripción válida"

    @staticmethod
    def validar_precio(precio_str: str) -> Tuple[bool, str, Optional[float]]:
        if not precio_str or precio_str.strip() == "":
            return False, "El precio no puede estar vacío", None
        
        try:
            precio = float(precio_str.strip())
            
            if precio <= 0:
                return False, "El precio debe ser mayor a 0", None
            
            if precio > 999999.99:
                return False, "El precio no puede exceder 999,999.99", None
            
            return True, "Precio válido", precio
            
        except ValueError:
            return False, "Ingrese un precio válido (ej: 8.50)", None

    @staticmethod
    def validar_stock(stock_str: str) -> Tuple[bool, str, Optional[int]]:
        if not stock_str or stock_str.strip() == "":
            return False, "El stock no puede estar vacío", None
        
        try:
            stock = int(stock_str.strip())
            
            if stock < 0:
                return False, "El stock no puede ser negativo", None
            
            if stock > 100000:
                return False, "El stock no puede exceder 100,000 unidades", None
            
            return True, "Stock válido", stock
            
        except ValueError:
            return False, "Ingrese un stock válido (número entero)", None

    @staticmethod
    def obtener_producto_por_id(id_producto: int) -> Optional[Dict]:
        productos = ProductoBL.obtener_productos_activos()
        
        if not productos:
            return None
        
        for producto in productos:
            if producto['id_producto'] == id_producto:
                return producto
        
        return None

    @staticmethod
    def contar_productos_activos() -> int:
        productos = ProductoBL.obtener_productos_activos()
        return len(productos) if productos else 0

    @staticmethod
    def obtener_productos_combo() -> List[Dict]:
        productos = ProductoBL.obtener_productos_activos()
        
        if not productos:
            return []
        
        return [
            {
                'id': producto['id_producto'],
                'texto': f"{producto['nombre']} - S/ {producto['precio_base']:.2f}"
            }
            for producto in productos
        ]