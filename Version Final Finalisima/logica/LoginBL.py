# LoginBL.py

from datos import procedimientos

class LoginBL:

    # Valida credenciales del usuario
    @staticmethod
    def validar_login(usuario: str, contrasena: str) -> bool:
        if not usuario or not contrasena:
            print("❌ Usuario o contraseña vacíos")
            return False

        try:
            resultados = procedimientos.sp_login_empresa(usuario, contrasena)
            
            # Debug: ver qué está retornando
            print(f"🔍 Resultados del SP: {resultados}")
            
            # Verificar que haya resultados
            if not resultados or len(resultados) == 0:
                print("❌ Sin resultados del procedimiento")
                return False
            
            # Obtener el primer campo (mensaje)
            primera_fila = resultados[0]
            mensaje = str(primera_fila[0]).strip().upper()
            
            print(f"🔍 Mensaje recibido: '{mensaje}'")
            print(f"🔍 Cantidad de columnas: {len(primera_fila)}")
            
            # Login exitoso debe tener 4 columnas y el mensaje correcto
            if len(primera_fila) == 4 and mensaje == "LOGIN EXITOSO":
                print("✅ Login exitoso")
                return True
            
            # Si solo tiene 1 columna, es un error
            if len(primera_fila) == 1:
                print(f"❌ Login fallido: {mensaje}")
                return False
            
            print("❌ Formato de respuesta inesperado")
            return False

        except Exception as e:
            print(f"❌ Error al validar login: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    # Obtiene el ID numérico de la empresa
    @staticmethod
    def obtener_id_empresa(usuario: str, ruc: str) -> int:
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            
            if not resultados or len(resultados) == 0:
                print("⚠️ No se encontraron resultados del login")
                return None
            
            primera_fila = resultados[0]
            
            # Verificar que sea un login exitoso (4 columnas)
            if len(primera_fila) == 4:
                mensaje = str(primera_fila[0]).strip().upper()
                
                if mensaje == "LOGIN EXITOSO":
                    id_empresa = primera_fila[1]
                    print(f"✅ ID Empresa obtenido: {id_empresa} (tipo: {type(id_empresa)})")
                    return int(id_empresa)
                else:
                    print(f"⚠️ Mensaje inesperado: {mensaje}")
                    return None
            else:
                print(f"❌ Login fallido: {primera_fila[0]}")
                return None
            
        except Exception as e:
            print(f"❌ Error al obtener ID de empresa: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # Obtiene todos los datos de la empresa
    @staticmethod
    def obtener_datos_empresa(usuario: str, ruc: str) -> dict:
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            
            if not resultados or len(resultados) == 0:
                return None
            
            primera_fila = resultados[0]
            
            # Verificar que sea un login exitoso (4 columnas)
            if len(primera_fila) == 4:
                mensaje = str(primera_fila[0]).strip().upper()
                
                if mensaje == "LOGIN EXITOSO":
                    return {
                        'mensaje': primera_fila[0],
                        'id_empresa': int(primera_fila[1]),
                        'nombre': primera_fila[2],
                        'razon_social': primera_fila[3]
                    }
            
            print(f"❌ Error en login: {primera_fila[0]}")
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener datos de empresa: {e}")
            import traceback
            traceback.print_exc()
            return None