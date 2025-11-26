from datos.conexion import ConexionDB
from typing import Tuple, Optional, Dict, List

class RegistroBL:
    @staticmethod
    def obtener_ubicaciones_activas() -> Optional[List[Dict]]:
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
                ubicacion = {
                    'id_ubicacion': fila.get('id_ubicacion'),
                    'descripcion': fila.get('descripcion')
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
    def validar_ubicacion_existe(id_ubicacion: int) -> Tuple[bool, str]:
        if not id_ubicacion or id_ubicacion <= 0:
            return False, "Debe seleccionar una ubicación válida"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT COUNT(*) as total 
                FROM mae_ubicacion 
                WHERE id_ubicacion = :id_ubicacion 
                AND activo = TRUE
            """
            resultado = db.ejecutar(sql, {"id_ubicacion": id_ubicacion})
            
            if resultado and resultado[0]['total'] > 0:
                return True, "Ubicación válida"
            else:
                return False, "La ubicación seleccionada no existe o está inactiva"
                
        except Exception as e:
            print(f"❌ Error validando ubicación: {e}")
            return False, f"Error al validar ubicación: {str(e)}"
        finally:
            db.desconectar()

    @staticmethod
    def registrar_empresa(nombre: str, razon_social: str, ruc: str, 
                         id_ubicacion: int) -> Tuple[bool, str, Optional[int]]:
        # Validaciones previas
        if not nombre or not razon_social or not ruc:
            return False, "Todos los campos son obligatorios", None

        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres", None

        if len(razon_social) > 100:
            return False, "La razón social no puede exceder 100 caracteres", None

        if len(ruc) != 11 or not ruc.isdigit():
            return False, "El RUC debe tener 11 dígitos numéricos", None

        if not id_ubicacion or id_ubicacion <= 0:
            return False, "Debe seleccionar una ubicación válida", None

        # Validar que la ubicación existe
        ubicacion_valida, mensaje_ubicacion = RegistroBL.validar_ubicacion_existe(id_ubicacion)
        if not ubicacion_valida:
            return False, mensaje_ubicacion, None

        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_registrar_empresa(
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:razon AS VARCHAR(100)),
                    CAST(:ruc AS CHAR(11)),
                    :id_ubicacion
                )
            """
            
            resultados = db.ejecutar(sql, {
                "nombre": nombre,
                "razon": razon_social,
                "ruc": ruc,
                "id_ubicacion": id_ubicacion
            })

            if not resultados or len(resultados) == 0:
                return False, "Error desconocido en el registro", None

            fila = resultados[0]
            mensaje = fila.get("mensaje", "").strip()
            id_empresa = fila.get("id_empresa")


            if "ERROR" in mensaje.upper():
                print(f"❌ {mensaje}")
                return False, mensaje, None
            elif mensaje in ["EMPRESA CREADA", "EMPRESA REACTIVADA"]:
                print(f"✅ {mensaje} - ID: {id_empresa}")
                return True, mensaje, id_empresa
            elif mensaje == "EMPRESA YA EXISTE (ACTIVA)":
                print(f"⚠️ {mensaje} - ID: {id_empresa}")
                return False, mensaje, id_empresa
            else:
                return False, mensaje, id_empresa

        except Exception as e:
            print(f"❌ Error al registrar empresa: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al registrar empresa: {str(e)}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_ruc(ruc: str) -> Tuple[bool, str]:
        if not ruc or ruc.strip() == "":
            return False, "El RUC no puede estar vacío"
        
        if len(ruc) != 11:
            return False, "El RUC debe tener exactamente 11 dígitos"
        
        if not ruc.isdigit():
            return False, "El RUC solo puede contener números"
        
        # Validar que empiece con 10 o 20 (empresas en Perú)
        if not (ruc.startswith('10') or ruc.startswith('20')):
            return False, "El RUC debe comenzar con 10 o 20"
        
        return True, "RUC válido"

    @staticmethod
    def validar_ruc_disponible(ruc: str) -> Tuple[bool, str]:
        # Primero validar formato
        ruc_valido, mensaje_validacion = RegistroBL.validar_ruc(ruc)
        if not ruc_valido:
            return False, mensaje_validacion
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT COUNT(*) as total, 
                       MAX(activo) as activo,
                       MAX(nombre) as nombre_existente
                FROM mae_empresa 
                WHERE RUC = :ruc
            """
            resultados = db.ejecutar(sql, {"ruc": ruc})
            
            if resultados and resultados[0]["total"] > 0:
                if resultados[0]["activo"]:
                    return False, f"RUC ya registrado con la empresa: {resultados[0]['nombre_existente']}"
                else:
                    return True, "RUC disponible (empresa inactiva puede ser reactivada)"
            
            return True, "RUC disponible"
            
        except Exception as e:
            print(f"❌ Error validando RUC: {e}")
            return False, f"Error al validar RUC: {str(e)}"
        finally:
            db.desconectar()

    @staticmethod
    def validar_nombre_empresa(nombre: str) -> Tuple[bool, str]:
        """
        Valida el nombre de la empresa.
        
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        
        return True, "Nombre válido"

    @staticmethod
    def validar_razon_social(razon_social: str) -> Tuple[bool, str]:
        if not razon_social or razon_social.strip() == "":
            return False, "La razón social no puede estar vacía"
        
        if len(razon_social) > 100:
            return False, "La razón social no puede exceder 100 caracteres"
        
        if len(razon_social) < 3:
            return False, "La razón social debe tener al menos 3 caracteres"
        
        return True, "Razón social válida"

    @staticmethod
    def insertar_ubicacion(descripcion: str) -> Tuple[bool, str, Optional[int]]:
        if not descripcion or descripcion.strip() == "":
            return False, "La descripción de la ubicación no puede estar vacía", None
        
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
                return True, "Ubicación creada correctamente", id_ubicacion
            else:
                return False, "No se pudo insertar la ubicación", None
                
        except Exception as e:
            print(f"❌ Error al insertar ubicación: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar ubicación: {str(e)}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def obtener_resultado_completo(nombre: str, razon_social: str, ruc: str, 
                                   id_ubicacion: int) -> Optional[Dict]:
        exito, mensaje, id_empresa = RegistroBL.registrar_empresa(
            nombre, razon_social, ruc, id_ubicacion
        )
        
        if "CREADA" in mensaje:
            tipo_operacion = "creacion"
        elif "REACTIVADA" in mensaje:
            tipo_operacion = "reactivacion"
        elif "YA EXISTE" in mensaje:
            tipo_operacion = "existe"
        else:
            tipo_operacion = "error"
        
        return {
            "exito": exito,
            "mensaje": mensaje,
            "id_empresa": id_empresa,
            "tipo_operacion": tipo_operacion
        }