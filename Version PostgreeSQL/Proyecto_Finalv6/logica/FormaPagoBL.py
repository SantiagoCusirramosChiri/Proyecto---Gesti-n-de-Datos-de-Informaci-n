from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class FormaPagoBL:
    @staticmethod
    def obtener_formas_pago_activas() -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_formas_pago_activas()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay formas de pago activas")
                return []
            
            formas_pago = []
            for fila in resultados:
                forma_pago = {
                    'id_forma_pago': fila.get('id_forma_pago'),
                    'nombre': fila.get('nombre'),
                    'descripcion': fila.get('descripcion'),
                    'activo': fila.get('activo')
                }
                formas_pago.append(forma_pago)
            
            print(f"✅ Se obtuvieron {len(formas_pago)} formas de pago")
            return formas_pago
            
        except Exception as e:
            print(f"❌ Error al obtener formas de pago: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_formas_pago(termino_busqueda: str) -> Optional[List[Dict]]:
        if not termino_busqueda:
            return FormaPagoBL.obtener_formas_pago_activas()
        
        formas_pago = FormaPagoBL.obtener_formas_pago_activas()
        
        if not formas_pago:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        formas_pago_filtradas = [
            forma_pago for forma_pago in formas_pago
            if (termino in forma_pago['nombre'].lower() or
                termino in forma_pago['descripcion'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(formas_pago_filtradas)} resultados")
        return formas_pago_filtradas

    @staticmethod
    def insertar_forma_pago(nombre: str, descripcion: str) -> Tuple[bool, str, Optional[int]]:
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
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_forma_pago(
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:descripcion AS VARCHAR(255))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "nombre": nombre,
                "descripcion": descripcion
            })
            
            if resultado and len(resultado) > 0:
                id_forma_pago = resultado[0].get('id_forma_pago')
                print(f"✅ Forma de pago insertada con ID: {id_forma_pago}")
                return True, "Forma de pago registrada correctamente", id_forma_pago
            else:
                return False, "No se pudo insertar la forma de pago", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar forma de pago: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"La forma de pago '{nombre}' ya está registrada", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar forma de pago: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_forma_pago(id_forma_pago: int, nombre: str, descripcion: str) -> Tuple[bool, str]:
        # Validaciones
        if not id_forma_pago or id_forma_pago <= 0:
            return False, "ID de forma de pago inválido"
        
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
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_forma_pago(
                    :id_forma_pago,
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:descripcion AS VARCHAR(255))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_forma_pago": id_forma_pago,
                "nombre": nombre,
                "descripcion": descripcion
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Forma de pago actualizada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar la forma de pago"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar forma de pago: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El nombre '{nombre}' ya está registrado"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar forma de pago: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_forma_pago(id_forma_pago: int) -> Tuple[bool, str]:
        if not id_forma_pago or id_forma_pago <= 0:
            return False, "ID de forma de pago inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_forma_pago(:id_forma_pago)"
            resultado = db.ejecutar(sql, {"id_forma_pago": id_forma_pago})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Forma de pago desactivada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar la forma de pago"
                
        except Exception as e:
            print(f"❌ Error al desactivar forma de pago: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar forma de pago: {str(e)}"
            
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
    def contar_formas_pago_activas() -> int:
        formas_pago = FormaPagoBL.obtener_formas_pago_activas()
        return len(formas_pago) if formas_pago else 0

    @staticmethod
    def obtener_forma_pago_por_id(id_forma_pago: int) -> Optional[Dict]:
        formas_pago = FormaPagoBL.obtener_formas_pago_activas()
        
        if not formas_pago:
            return None
        
        for forma_pago in formas_pago:
            if forma_pago['id_forma_pago'] == id_forma_pago:
                return forma_pago
        
        return None

    @staticmethod
    def obtener_formas_pago_combo() -> List[Dict]:
        formas_pago = FormaPagoBL.obtener_formas_pago_activas()
        
        if not formas_pago:
            return []
        
        return [
            {
                'id': forma_pago['id_forma_pago'],
                'texto': forma_pago['nombre']
            }
            for forma_pago in formas_pago
        ]