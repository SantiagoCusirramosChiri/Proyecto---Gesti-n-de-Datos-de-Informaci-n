# logica/ConductorBL.py

from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple


class ConductorBL:
    """
    Capa de Lógica de Negocio para Conductores.
    Maneja todas las operaciones relacionadas con conductores.
    """

    @staticmethod
    def obtener_conductores_activos() -> Optional[List[Dict]]:
        """
        Obtiene todos los conductores activos.
        
        Returns:
            List[Dict]: Lista de conductores con sus datos
            None: Si hay error o no hay datos
        """
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_conductores_activos()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay conductores activos")
                return []
            
            # Convertir resultados a lista de diccionarios
            conductores = []
            for fila in resultados:
                conductor = {
                    'id_conductor': fila.get('id_conductor'),
                    'nombre': fila.get('nombre'),
                    'licencia': fila.get('n_licencia'),  # ⚠️ La columna se llama n_licencia en BD
                    'activo': fila.get('activo')
                }
                conductores.append(conductor)
            
            print(f"✅ Se obtuvieron {len(conductores)} conductores")
            return conductores
            
        except Exception as e:
            print(f"❌ Error al obtener conductores: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_conductores(termino_busqueda: str) -> Optional[List[Dict]]:
        """
        Busca conductores por nombre o licencia.
        
        Args:
            termino_busqueda: Término a buscar (case-insensitive)
        
        Returns:
            List[Dict]: Lista de conductores que coinciden con la búsqueda
        """
        if not termino_busqueda:
            return ConductorBL.obtener_conductores_activos()
        
        conductores = ConductorBL.obtener_conductores_activos()
        
        if not conductores:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        # Filtrar conductores
        conductores_filtrados = [
            conductor for conductor in conductores
            if (termino in conductor['nombre'].lower() or
                termino in conductor['licencia'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(conductores_filtrados)} resultados")
        return conductores_filtrados

    @staticmethod
    def insertar_conductor(nombre: str, licencia: str) -> Tuple[bool, str, Optional[int]]:
        """
        Inserta un nuevo conductor.
        
        Args:
            nombre: Nombre completo del conductor
            licencia: Número de licencia
        
        Returns:
            Tuple[bool, str, Optional[int]]: (éxito, mensaje, id_conductor)
        """
        # Validaciones
        if not nombre or not licencia:
            return False, "Nombre y licencia son obligatorios", None
        
        nombre = nombre.strip()
        licencia = licencia.strip().upper()
        
        if len(nombre) < 5:
            return False, "El nombre debe tener al menos 5 caracteres", None
        
        if len(nombre) > 100:
            return False, "El nombre no puede exceder 100 caracteres", None
        
        if len(licencia) != 12:
            return False, "La licencia debe tener exactamente 12 caracteres", None
        
        if not licencia[0].isalpha():
            return False, "La licencia debe comenzar con una letra (A, B, C, etc.)", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_conductor(
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:n_licencia AS CHAR(12))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "nombre": nombre,
                "n_licencia": licencia
            })
            
            if resultado and len(resultado) > 0:
                id_conductor = resultado[0].get('id_conductor')
                print(f"✅ Conductor insertado con ID: {id_conductor}")
                return True, "Conductor registrado correctamente", id_conductor
            else:
                return False, "No se pudo insertar el conductor", None
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al insertar conductor: {error_msg}")
            
            # Detectar errores comunes
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"La licencia '{licencia}' ya está registrada", None
            
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar conductor: {error_msg}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_conductor(id_conductor: int, nombre: str, licencia: str) -> Tuple[bool, str]:
        """
        Actualiza los datos de un conductor existente.
        
        Args:
            id_conductor: ID del conductor a actualizar
            nombre: Nuevo nombre
            licencia: Nueva licencia
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validaciones
        if not id_conductor or id_conductor <= 0:
            return False, "ID de conductor inválido"
        
        if not nombre or not licencia:
            return False, "Nombre y licencia son obligatorios"
        
        nombre = nombre.strip()
        licencia = licencia.strip().upper()
        
        if len(nombre) < 5:
            return False, "El nombre debe tener al menos 5 caracteres"
        
        if len(nombre) > 100:
            return False, "El nombre no puede exceder 100 caracteres"
        
        if len(licencia) != 12:
            return False, "La licencia debe tener exactamente 12 caracteres"
        
        if not licencia[0].isalpha():
            return False, "La licencia debe comenzar con una letra (A, B, C, etc.)"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_conductor(
                    :id_conductor,
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:n_licencia AS CHAR(12))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_conductor": id_conductor,
                "nombre": nombre,
                "n_licencia": licencia
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Conductor actualizado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar el conductor"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al actualizar conductor: {error_msg}")
            
            if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                return False, f"La licencia '{licencia}' ya está registrada"
            
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar conductor: {error_msg}"
            
        finally:
            db.desconectar()

    @staticmethod
    def desactivar_conductor(id_conductor: int) -> Tuple[bool, str]:
        """
        Desactiva un conductor (borrado lógico).
        
        Args:
            id_conductor: ID del conductor a desactivar
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not id_conductor or id_conductor <= 0:
            return False, "ID de conductor inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_conductor(:id_conductor)"
            resultado = db.ejecutar(sql, {"id_conductor": id_conductor})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Conductor desactivado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar el conductor"
                
        except Exception as e:
            print(f"❌ Error al desactivar conductor: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar conductor: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        """
        Valida que el nombre del conductor sea correcto.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        nombre = nombre.strip()
        
        if len(nombre) < 5:
            return False, "El nombre debe tener al menos 5 caracteres"
        
        if len(nombre) > 100:
            return False, "El nombre no puede exceder 100 caracteres"
        
        # Verificar que tenga al menos nombre y apellido
        if len(nombre.split()) < 2:
            return False, "Debe ingresar nombre y apellido"
        
        return True, "Nombre válido"

    @staticmethod
    def validar_licencia(licencia: str) -> Tuple[bool, str]:
        """
        Valida que la licencia del conductor sea correcta.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not licencia or licencia.strip() == "":
            return False, "La licencia no puede estar vacía"
        
        licencia = licencia.strip()
        
        if len(licencia) != 12:
            return False, "La licencia debe tener exactamente 12 caracteres"
        
        if not licencia[0].isalpha():
            return False, "La licencia debe comenzar con una letra (A, B, C, etc.)"
        
        if not licencia[1:].isalnum():
            return False, "La licencia debe contener solo letras y números"
        
        return True, "Licencia válida"

    @staticmethod
    def contar_conductores_activos() -> int:
        """
        Cuenta el número total de conductores activos.
        
        Returns:
            int: Número de conductores activos
        """
        conductores = ConductorBL.obtener_conductores_activos()
        return len(conductores) if conductores else 0

    @staticmethod
    def obtener_conductor_por_id(id_conductor: int) -> Optional[Dict]:
        """
        Obtiene un conductor específico por su ID.
        
        Args:
            id_conductor: ID del conductor a buscar
        
        Returns:
            Dict: Datos del conductor o None si no existe
        """
        conductores = ConductorBL.obtener_conductores_activos()
        
        if not conductores:
            return None
        
        for conductor in conductores:
            if conductor['id_conductor'] == id_conductor:
                return conductor
        
        return None

    @staticmethod
    def obtener_conductores_combo() -> List[Dict]:
        """
        Obtiene conductores en formato para ComboBox.
        
        Returns:
            List[Dict]: Lista de conductores con formato simplificado
        """
        conductores = ConductorBL.obtener_conductores_activos()
        
        if not conductores:
            return []
        
        return [
            {
                'id': conductor['id_conductor'],
                'texto': f"{conductor['nombre']} - Lic: {conductor['licencia']}"
            }
            for conductor in conductores
        ]