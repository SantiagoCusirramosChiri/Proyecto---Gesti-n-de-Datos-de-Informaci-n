from datos.conexion import ConexionDB
from typing import List, Dict, Optional, Tuple

class ClienteBL:
    @staticmethod
    def obtener_clientes_activos() -> Optional[List[Dict]]:
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_obtener_clientes_activos()"
            resultados = db.ejecutar(sql)
            
            if not resultados:
                print("ℹ️ No hay clientes activos")
                return []
            
            clientes = []
            for fila in resultados:
                cliente = {
                    'id_cliente': fila.get('id_cliente'),
                    'nombre': fila.get('nombre'),
                    'apellido': fila.get('apellido'),
                    'ubicacion': fila.get('ubicacion'),
                    'tipo_identificacion': fila.get('tipo_identificacion'),
                    'codigo_documento': fila.get('codigo_documento'),
                    'activo': fila.get('activo'),
                    'id_ubicacion': fila.get('id_ubicacion'),
                    'id_identidad': fila.get('id_identidad'),
                    'nombre_completo': f"{fila.get('nombre')} {fila.get('apellido')}"
                }
                clientes.append(cliente)
            
            print(f"✅ Se obtuvieron {len(clientes)} clientes")
            return clientes
            
        except Exception as e:
            print(f"❌ Error al obtener clientes: {e}")
            import traceback
            traceback.print_exc()
            return None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_clientes(termino_busqueda: str) -> Optional[List[Dict]]:
        if not termino_busqueda:
            return ClienteBL.obtener_clientes_activos()
        
        clientes = ClienteBL.obtener_clientes_activos()
        
        if not clientes:
            return []
        
        termino = termino_busqueda.lower().strip()
        
        clientes_filtrados = [
            cliente for cliente in clientes
            if (termino in cliente['nombre'].lower() or
                termino in cliente['apellido'].lower() or
                termino in cliente['codigo_documento'].lower() or
                termino in cliente['nombre_completo'].lower())
        ]
        
        print(f"🔍 Búsqueda '{termino}': {len(clientes_filtrados)} resultados")
        return clientes_filtrados

    @staticmethod
    def obtener_cliente_por_id(id_cliente: int) -> Optional[Dict]:
        clientes = ClienteBL.obtener_clientes_activos()
        
        if not clientes:
            return None
        
        for cliente in clientes:
            if cliente['id_cliente'] == id_cliente:
                return cliente
        
        return None

    @staticmethod
    def desactivar_cliente(id_cliente: int) -> Tuple[bool, str]:
        if not id_cliente or id_cliente <= 0:
            return False, "ID de cliente inválido"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = "SELECT * FROM sp_desactivar_cliente(:id_cliente)"
            resultado = db.ejecutar(sql, {"id_cliente": id_cliente})
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Cliente desactivado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo desactivar el cliente"
                
        except Exception as e:
            print(f"❌ Error al desactivar cliente: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al desactivar cliente: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def actualizar_cliente(id_cliente: int, nombre: str, apellido: str, 
                          id_ubicacion: int, id_identidad: int) -> Tuple[bool, str]:

        if not nombre or not apellido:
            return False, "Nombre y apellido son obligatorios"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        if len(apellido) > 50:
            return False, "El apellido no puede exceder 50 caracteres"
        
        if not id_ubicacion or id_ubicacion <= 0:
            return False, "Debe seleccionar una ubicación válida"
        
        if not id_identidad or id_identidad <= 0:
            return False, "Debe seleccionar una identidad válida"
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_actualizar_cliente(
                    :id_cliente,
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:apellido AS VARCHAR(50)),
                    :id_ubicacion,
                    :id_identidad
                )
            """
            
            resultado = db.ejecutar(sql, {
                "id_cliente": id_cliente,
                "nombre": nombre,
                "apellido": apellido,
                "id_ubicacion": id_ubicacion,
                "id_identidad": id_identidad
            })
            
            if resultado and len(resultado) > 0:
                mensaje = resultado[0].get('mensaje', 'Cliente actualizado correctamente')
                print(f"✅ {mensaje}")
                return True, mensaje
            else:
                return False, "No se pudo actualizar el cliente"
                
        except Exception as e:
            print(f"❌ Error al actualizar cliente: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al actualizar cliente: {str(e)}"
            
        finally:
            db.desconectar()

    @staticmethod
    def insertar_cliente(nombre: str, apellido: str, 
                        id_ubicacion: int, id_identidad: int) -> Tuple[bool, str, Optional[int]]:

        if not nombre or not apellido:
            return False, "Nombre y apellido son obligatorios", None
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres", None
        
        if len(apellido) > 50:
            return False, "El apellido no puede exceder 50 caracteres", None
        
        if not id_ubicacion or id_ubicacion <= 0:
            return False, "Debe seleccionar una ubicación válida", None
        
        if not id_identidad or id_identidad <= 0:
            return False, "Debe seleccionar una identidad válida", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_cliente(
                    CAST(:nombre AS VARCHAR(50)),
                    CAST(:apellido AS VARCHAR(50)),
                    :id_ubicacion,
                    :id_identidad
                )
            """
            
            resultado = db.ejecutar(sql, {
                "nombre": nombre,
                "apellido": apellido,
                "id_ubicacion": id_ubicacion,
                "id_identidad": id_identidad
            })
            
            if resultado and len(resultado) > 0:
                id_cliente = resultado[0].get('id_cliente')
                print(f"✅ Cliente insertado con ID: {id_cliente}")
                return True, "Cliente registrado correctamente", id_cliente
            else:
                return False, "No se pudo insertar el cliente", None
                
        except Exception as e:
            print(f"❌ Error al insertar cliente: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar cliente: {str(e)}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        if not nombre.replace(" ", "").isalpha():
            return False, "El nombre solo puede contener letras"
        
        return True, "Nombre válido"

    @staticmethod
    def validar_apellido(apellido: str) -> Tuple[bool, str]:
        if not apellido or apellido.strip() == "":
            return False, "El apellido no puede estar vacío"
        
        if len(apellido) > 50:
            return False, "El apellido no puede exceder 50 caracteres"
        
        if not apellido.replace(" ", "").isalpha():
            return False, "El apellido solo puede contener letras"
        
        return True, "Apellido válido"

    @staticmethod
    def contar_clientes_activos() -> int:
        clientes = ClienteBL.obtener_clientes_activos()
        return len(clientes) if clientes else 0

    @staticmethod
    def insertar_identidad(tipo_identificacion: str, codigo_documento: str) -> Tuple[bool, str, Optional[int]]:
        if not tipo_identificacion or not codigo_documento:
            return False, "Tipo de identificación y código son requeridos", None
        
        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT * FROM sp_insertar_identidad(
                    CAST(:tipo_identificacion AS VARCHAR(20)),
                    CAST(:codigo_documento AS VARCHAR(15))
                )
            """
            
            resultado = db.ejecutar(sql, {
                "tipo_identificacion": tipo_identificacion.upper(),
                "codigo_documento": codigo_documento.strip()
            })
            
            if resultado and len(resultado) > 0:
                fila = resultado[0]
                success = fila.get('success', False)
                message = fila.get('message', 'Error desconocido')
                id_identidad = fila.get('id_identidad')
                
                if success:
                    print(f"✅ Identidad creada con ID: {id_identidad}")
                    return True, message, id_identidad
                else:
                    print(f"⚠️ No se pudo crear identidad: {message}")
                    return False, message, None
            else:
                return False, "No se pudo crear la identidad", None
                
        except Exception as e:
            print(f"❌ Error al insertar identidad: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error al insertar identidad: {str(e)}", None
            
        finally:
            db.desconectar()

    @staticmethod
    def buscar_o_crear_identidad(tipo_identificacion: str, codigo_documento: str) -> Tuple[bool, str, Optional[int]]:

        db = ConexionDB()
        db.conectar()
        
        try:
            sql = """
                SELECT id_identidad, tipo_identificacion, codigo_documento, activo
                FROM mae_identidad
                WHERE codigo_documento = :codigo_documento
                AND activo = TRUE
                LIMIT 1
            """
            
            resultado = db.ejecutar(sql, {"codigo_documento": codigo_documento.strip()})
            
            if resultado and len(resultado) > 0:
                # Ya existe
                id_identidad = resultado[0].get('id_identidad')
                print(f"✅ Identidad ya existe con ID: {id_identidad}")
                return True, "Identidad encontrada", id_identidad
            
        except Exception as e:
            print(f"⚠️ Error al buscar identidad: {e}")
        finally:
            db.desconectar()
        
        # Si no existe, crearla
        return ClienteBL.insertar_identidad(tipo_identificacion, codigo_documento)