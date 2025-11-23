# logica/VehiculoBL.py

from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class VehiculoBL:
    """
    Capa de Lógica de Negocio para Vehículos.
    Maneja todas las operaciones relacionadas con vehículos.
    """

    @staticmethod
    def obtener_vehiculos_activos() -> Optional[List[Dict]]:
        """
        Obtiene todos los vehículos activos.
        
        Returns:
            List[Dict]: Lista de vehículos con sus datos
            None: Si hay error o no hay datos
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_vehiculos_activos()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay vehículos activos")
                return []
            
            # Convertir resultados a lista de diccionarios
            vehiculos = []
            for fila in resultados:
                vehiculo = {
                    'id_vehiculo': fila.get('id_vehiculo'),
                    'descripcion': fila.get('descripcion'),
                    'placa': fila.get('placa'),
                    'activo': fila.get('activo')
                }
                vehiculos.append(vehiculo)
            
            print(f"✅ Se obtuvieron {len(vehiculos)} vehículos")
            return vehiculos
            
        except Exception as e:
            print(f"❌ Error al obtener vehículos: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_vehiculos(termino_busqueda: str) -> Optional[List[Dict]]:
        """
        Busca vehículos por descripción o placa.
        
        Args:
            termino_busqueda: Término a buscar (case-insensitive)
        
        Returns:
            List[Dict]: Lista de vehículos que coinciden con la búsqueda
        """
        if not termino_busqueda:
            return VehiculoBL.obtener_vehiculos_activos()
        
        vehiculos = VehiculoBL.obtener_vehiculos_activos()
        
        if not vehiculos:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        # Filtrar vehículos
        vehiculos_filtrados = [
            vehiculo for vehiculo in vehiculos
            if (termino in vehiculo['descripcion'].lower() or
                termino in vehiculo['placa'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(vehiculos_filtrados)} resultados")
        return vehiculos_filtrados

    @staticmethod
    def insertar_vehiculo(descripcion: str, placa: str) -> Tuple[bool, str, Optional[int]]:
        """
        Inserta un nuevo vehículo.
        
        Args:
            descripcion: Descripción del vehículo
            placa: Placa del vehículo
        
        Returns:
            Tuple[bool, str, Optional[int]]: (éxito, mensaje, id_vehiculo)
        """
        # Validaciones
        if not descripcion or not placa:
            return False, "Descripción y placa son obligatorias", None
        
        descripcion = descripcion.strip()
        placa = placa.strip().upper()
        
        if len(descripcion) < 5:
            return False, "La descripción debe tener al menos 5 caracteres", None
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres", None
        
        if len(placa) > 8:
            return False, "La placa no puede exceder 8 caracteres", None
        
        if len(placa) < 6:
            return False, "La placa debe tener al menos 6 caracteres", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_vehiculo(
                    CAST(:descripcion AS VARCHAR(100)),
                    CAST(:placa AS VARCHAR(8))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "descripcion": descripcion,
                "placa": placa
            })
            
            if resultado and len(resultado) > 0:
                id_vehiculo = resultado[0].get('id_vehiculo')
                print(f"✅ Vehículo insertado con ID: {id_vehiculo}")
                return True, "Vehículo registrado correctamente", id_vehiculo
            else:
                return False, "No se pudo insertar el vehículo", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar vehículo: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"La placa '{placa}' ya está registrada", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar vehículo: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_vehiculo(id_vehiculo: int, descripcion: str, placa: str) -> Tuple[bool, str]:
        """
        Actualiza los datos de un vehículo existente.
        
        Args:
            id_vehiculo: ID del vehículo a actualizar
            descripcion: Nueva descripción
            placa: Nueva placa
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validaciones
        if not id_vehiculo or id_vehiculo <= 0:
            return False, "ID de vehículo inválido"
        
        if not descripcion or not placa:
            return False, "Descripción y placa son obligatorias"
        
        descripcion = descripcion.strip()
        placa = placa.strip().upper()
        
        if len(descripcion) < 5:
            return False, "La descripción debe tener al menos 5 caracteres"
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres"
        
        if len(placa) > 8:
            return False, "La placa no puede exceder 8 caracteres"
        
        if len(placa) < 6:
            return False, "La placa debe tener al menos 6 caracteres"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_vehiculo(
                    :id_vehiculo,
                    CAST(:descripcion AS VARCHAR(100)),
                    CAST(:placa AS VARCHAR(8))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_vehiculo": id_vehiculo,
                "descripcion": descripcion,
                "placa": placa
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Vehículo actualizado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar el vehículo"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar vehículo: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"La placa '{placa}' ya está registrada"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar vehículo: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_vehiculo(id_vehiculo: int) -> Tuple[bool, str]:
        """
        Desactiva un vehículo (borrado lógico).
        
        Args:
            id_vehiculo: ID del vehículo a desactivar
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not id_vehiculo or id_vehiculo <= 0:
            return False, "ID de vehículo inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_vehiculo(:id_vehiculo)"
            resultado = db.ejecutar(sql, {"id_vehiculo": id_vehiculo})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Vehículo desactivado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar el vehículo"
                
        except Exception as e:
            print(f"❌ Error al desactivar vehículo: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar vehículo: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_descripcion(descripcion: str) -> Tuple[bool, str]:
        """
        Valida que la descripción del vehículo sea correcta.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not descripcion or descripcion.strip() == "":
            return False, "La descripción no puede estar vacía"
        
        descripcion = descripcion.strip()
        
        if len(descripcion) < 5:
            return False, "La descripción debe tener al menos 5 caracteres"
        
        if len(descripcion) > 100:
            return False, "La descripción no puede exceder 100 caracteres"
        
        return True, "Descripción válida"

    @staticmethod
    def validar_placa(placa: str) -> Tuple[bool, str]:
        """
        Valida que la placa del vehículo sea correcta.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not placa or placa.strip() == "":
            return False, "La placa no puede estar vacía"
        
        placa = placa.strip()
        
        if len(placa) < 6:
            return False, "La placa debe tener al menos 6 caracteres"
        
        if len(placa) > 8:
            return False, "La placa no puede exceder 8 caracteres"
        
        return True, "Placa válida"

    @staticmethod
    def contar_vehiculos_activos() -> int:
        """
        Cuenta el número total de vehículos activos.
        
        Returns:
            int: Número de vehículos activos
        """
        vehiculos = VehiculoBL.obtener_vehiculos_activos()
        return len(vehiculos) if vehiculos else 0

    @staticmethod
    def obtener_vehiculo_por_id(id_vehiculo: int) -> Optional[Dict]:
        """
        Obtiene un vehículo específico por su ID.
        
        Args:
            id_vehiculo: ID del vehículo a buscar
        
        Returns:
            Dict: Datos del vehículo o None si no existe
        """
        vehiculos = VehiculoBL.obtener_vehiculos_activos()
        
        if not vehiculos:
            return None
        
        for vehiculo in vehiculos:
            if vehiculo['id_vehiculo'] == id_vehiculo:
                return vehiculo
        
        return None

    @staticmethod
    def obtener_vehiculos_combo() -> List[Dict]:
        """
        Obtiene vehículos en formato para ComboBox.
        
        Returns:
            List[Dict]: Lista de vehículos con formato simplificado
        """
        vehiculos = VehiculoBL.obtener_vehiculos_activos()
        
        if not vehiculos:
            return []
        
        return [
            {
                'id': vehiculo['id_vehiculo'],
                'texto': f"{vehiculo['placa']} - {vehiculo['descripcion']}"
            }
            for vehiculo in vehiculos
        ]