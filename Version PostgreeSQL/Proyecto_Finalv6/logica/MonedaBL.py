from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class MonedaBL:
    @staticmethod
    def obtener_monedas_activas() -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_monedas_activas()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay monedas activas")
                return []
            
            monedas = []
            for fila in resultados:
                moneda = {
                    'id_moneda': fila.get('id_moneda'),
                    'codigo_iso': fila.get('codigo_iso'),
                    'nombre': fila.get('nombre'),
                    'activo': fila.get('activo')
                }
                monedas.append(moneda)
            
            print(f"✅ Se obtuvieron {len(monedas)} monedas")
            return monedas
            
        except Exception as e:
            print(f"❌ Error al obtener monedas: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_monedas(termino_busqueda: str) -> Optional[List[Dict]]:
        if not termino_busqueda:
            return MonedaBL.obtener_monedas_activas()
        
        monedas = MonedaBL.obtener_monedas_activas()
        
        if not monedas:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        monedas_filtradas = [
            moneda for moneda in monedas
            if (termino in moneda['codigo_iso'].lower() or
                termino in moneda['nombre'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(monedas_filtradas)} resultados")
        return monedas_filtradas

    @staticmethod
    def insertar_moneda(codigo_iso: str, nombre: str) -> Tuple[bool, str, Optional[int]]:
        # Validaciones
        if not codigo_iso or not nombre:
            return False, "Código ISO y nombre son obligatorios", None
        
        codigo_iso = codigo_iso.strip().upper()
        nombre = nombre.strip()
        
        if len(codigo_iso) != 3:
            return False, "El código ISO debe tener exactamente 3 caracteres", None
        
        if not codigo_iso.isalpha():
            return False, "El código ISO solo debe contener letras", None
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_moneda(
                    CAST(:codigo_iso AS VARCHAR(3)),
                    CAST(:nombre AS VARCHAR(50))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "codigo_iso": codigo_iso,
                "nombre": nombre
            })
            
            if resultado and len(resultado) > 0:
                id_moneda = resultado[0].get('id_moneda')
                print(f"✅ Moneda insertada con ID: {id_moneda}")
                return True, "Moneda registrada correctamente", id_moneda
            else:
                return False, "No se pudo insertar la moneda", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar moneda: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El código ISO '{codigo_iso}' ya está registrado", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar moneda: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_moneda(id_moneda: int, codigo_iso: str, nombre: str) -> Tuple[bool, str]:
        # Validaciones
        if not id_moneda or id_moneda <= 0:
            return False, "ID de moneda inválido"
        
        if not codigo_iso or not nombre:
            return False, "Código ISO y nombre son obligatorios"
        
        codigo_iso = codigo_iso.strip().upper()
        nombre = nombre.strip()
        
        if len(codigo_iso) != 3:
            return False, "El código ISO debe tener exactamente 3 caracteres"
        
        if not codigo_iso.isalpha():
            return False, "El código ISO solo debe contener letras"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_moneda(
                    :id_moneda,
                    CAST(:codigo_iso AS VARCHAR(3)),
                    CAST(:nombre AS VARCHAR(50))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_moneda": id_moneda,
                "codigo_iso": codigo_iso,
                "nombre": nombre
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Moneda actualizada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar la moneda"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar moneda: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"El código ISO '{codigo_iso}' ya está registrado"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar moneda: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_moneda(id_moneda: int) -> Tuple[bool, str]:
        if not id_moneda or id_moneda <= 0:
            return False, "ID de moneda inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_moneda(:id_moneda)"
            resultado = db.ejecutar(sql, {"id_moneda": id_moneda})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Moneda desactivada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar la moneda"
                
        except Exception as e:
            print(f"❌ Error al desactivar moneda: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar moneda: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_codigo_iso(codigo_iso: str) -> Tuple[bool, str]:
        if not codigo_iso or codigo_iso.strip() == "":
            return False, "El código ISO no puede estar vacío"
        
        codigo_iso = codigo_iso.strip().upper()
        
        if len(codigo_iso) != 3:
            return False, "El código ISO debe tener exactamente 3 caracteres"
        
        if not codigo_iso.isalpha():
            return False, "El código ISO solo debe contener letras"
        
        return True, "Código ISO válido"

    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        return True, "Nombre válido"

    @staticmethod
    def contar_monedas_activas() -> int:
        monedas = MonedaBL.obtener_monedas_activas()
        return len(monedas) if monedas else 0

    @staticmethod
    def obtener_moneda_por_id(id_moneda: int) -> Optional[Dict]:
        monedas = MonedaBL.obtener_monedas_activas()
        
        if not monedas:
            return None
        
        for moneda in monedas:
            if moneda['id_moneda'] == id_moneda:
                return moneda
        
        return None

    @staticmethod
    def obtener_monedas_combo() -> List[Dict]:
        monedas = MonedaBL.obtener_monedas_activas()
        
        if not monedas:
            return []
        
        return [
            {
                'id': moneda['id_moneda'],
                'texto': f"{moneda['codigo_iso']} - {moneda['nombre']}"
            }
            for moneda in monedas
        ]