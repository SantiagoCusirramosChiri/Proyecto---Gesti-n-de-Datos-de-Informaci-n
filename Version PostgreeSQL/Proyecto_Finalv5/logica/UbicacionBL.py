# logica/UbicacionBL.py

from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class UbicacionBL:
    """
    Capa de Lógica de Negocio para Ubicaciones.
    Maneja todas las operaciones relacionadas con ubicaciones.
    """

    @staticmethod
    def obtener_ubicaciones_activas() -> Optional[List[Dict]]:
        """
        Obtiene todas las ubicaciones activas.
        
        Returns:
            List[Dict]: Lista de ubicaciones con sus datos
            None: Si hay error o no hay datos
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_ubicaciones_activas()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay ubicaciones activas")
                return []
            
            # Convertir resultados a lista de diccionarios
            ubicaciones = []
            for fila in resultados:
                ubicacion = {
                    'id_ubicacion': fila.get('id_ubicacion'),
                    'descripcion': fila.get('descripcion'),
                    'activo': fila.get('activo')
                }
                ubicaciones.append(ubicacion)
            
            print(f"✅ Se obtuvieron {len(ubicaciones)} ubicaciones")
            return ubicaciones
            
        except Exception as e:
            print(f"❌ Error al obtener ubicaciones: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_ubicaciones(termino_busqueda: str) -> Optional[List[Dict]]:
        """
        Busca ubicaciones por descripción.
        
        Args:
            termino_busqueda: Término a buscar (case-insensitive)
        
        Returns:
            List[Dict]: Lista de ubicaciones que coinciden con la búsqueda
        """
        if not termino_busqueda:
            return UbicacionBL.obtener_ubicaciones_activas()
        
        ubicaciones = UbicacionBL.obtener_ubicaciones_activas()
        
        if not ubicaciones:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        # Filtrar ubicaciones
        ubicaciones_filtradas = [
            ubicacion for ubicacion in ubicaciones
            if termino in ubicacion['descripcion'].lower()
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(ubicaciones_filtradas)} resultados")
        return ubicaciones_filtradas

    @staticmethod
    def insertar_ubicacion(descripcion: str) -> Tuple[bool, str, Optional[int]]:
        """
        Inserta una nueva ubicación.
        
        Args:
            descripcion: Descripción de la ubicación
        
        Returns:
            Tuple[bool, str, Optional[int]]: (éxito, mensaje, id_ubicacion)
        """
        # Validaciones
        if not descripcion:
            return False, "La descripción es obligatoria", None
        
        descripcion = descripcion.strip()
        
        if len(descripcion) < 10:
            return False, "La descripción debe tener al menos 10 caracteres", None
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_ubicacion(
                    CAST(:descripcion AS VARCHAR(100))
                )
            """
            
            resultado = db.ejecutar(sql, {"descripcion": descripcion})
            
            if resultado and len(resultado) > 0:
                id_ubicacion = resultado[0].get('id_ubicacion')
                print(f"✅ Ubicación insertada con ID: {id_ubicacion}")
                return True, "Ubicación registrada correctamente", id_ubicacion
            else:
                return False, "No se pudo insertar la ubicación", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar ubicación: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, "Esta ubicación ya está registrada", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar ubicación: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_ubicacion(id_ubicacion: int, descripcion: str) -> Tuple[bool, str]:
        """
        Actualiza los datos de una ubicación existente.
        
        Args:
            id_ubicacion: ID de la ubicación a actualizar
            descripcion: Nueva descripción
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validaciones
        if not id_ubicacion or id_ubicacion <= 0:
            return False, "ID de ubicación inválido"
        
        if not descripcion:
            return False, "La descripción es obligatoria"
        
        descripcion = descripcion.strip()
        
        if len(descripcion) < 10:
            return False, "La descripción debe tener al menos 10 caracteres"
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_ubicacion(
                    :id_ubicacion,
                    CAST(:descripcion AS VARCHAR(100))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_ubicacion": id_ubicacion,
                "descripcion": descripcion
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Ubicación actualizada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar la ubicación"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar ubicación: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, "Esta descripción ya está registrada"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar ubicación: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_ubicacion(id_ubicacion: int) -> Tuple[bool, str]:
        """
        Desactiva una ubicación (borrado lógico).
        
        Args:
            id_ubicacion: ID de la ubicación a desactivar
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not id_ubicacion or id_ubicacion <= 0:
            return False, "ID de ubicación inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_ubicacion(:id_ubicacion)"
            resultado = db.ejecutar(sql, {"id_ubicacion": id_ubicacion})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Ubicación desactivada correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar la ubicación"
                
        except Exception as e:
            print(f"❌ Error al desactivar ubicación: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar ubicación: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_descripcion(descripcion: str) -> Tuple[bool, str]:
        """
        Valida que la descripción de la ubicación sea correcta.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not descripcion or descripcion.strip() == "":
            return False, "La descripción no puede estar vacía"
        
        descripcion = descripcion.strip()
        
        if len(descripcion) < 10:
            return False, "La descripción debe tener al menos 10 caracteres"
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres"
        
        return True, "Descripción válida"

    @staticmethod
    def obtener_ubicacion_por_id(id_ubicacion: int) -> Optional[Dict]:
        """
        Obtiene una ubicación específica por su ID.
        
        Args:
            id_ubicacion: ID de la ubicación a buscar
        
        Returns:
            Dict: Datos de la ubicación o None si no existe
        """
        ubicaciones = UbicacionBL.obtener_ubicaciones_activas()
        
        if not ubicaciones:
            return None
        
        for ubicacion in ubicaciones:
            if ubicacion['id_ubicacion'] == id_ubicacion:
                return ubicacion
        
        return None

    @staticmethod
    def obtener_ubicaciones_combo() -> List[Dict]:
        """
        Obtiene ubicaciones en formato para ComboBox.
        
        Returns:
            List[Dict]: Lista de ubicaciones con formato simplificado
        """
        ubicaciones = UbicacionBL.obtener_ubicaciones_activas()
        
        if not ubicaciones:
            return []
        
        return [
            {
                'id': ubicacion['id_ubicacion'],
                'texto': ubicacion['descripcion']
            }
            for ubicacion in ubicaciones
        ]