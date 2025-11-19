# LoginBL.py

from datos import procedimientos

class LoginBL:

    # Valida credenciales del usuario
    @staticmethod
    def validar_login(usuario: str, contrasena: str) -> bool:
        if not usuario or not contrasena:
            return False

        try:
            resultados = procedimientos.sp_login_empresa(usuario, contrasena)
            return len(resultados) > 0

        except Exception as e:
            print(f"Error al validar login: {e}")
            return False
        
    # Obtiene el ID numérico de la empresa
    @staticmethod
    def obtener_id_empresa(usuario: str, ruc: str) -> int:
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            
            if resultados and len(resultados) > 0:
                id_empresa = resultados[0][1]
                print(f"✅ ID Empresa obtenido: {id_empresa} (tipo: {type(id_empresa)})")
                return int(id_empresa)
            
            print("⚠️ No se encontraron resultados del login")
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener ID de empresa: {e}")
            print(f"   Resultados recibidos: {resultados if 'resultados' in locals() else 'N/A'}")
            return None
    
    # Obtiene todos los datos de la empresa
    @staticmethod
    def obtener_datos_empresa(usuario: str, ruc: str) -> dict:
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            
            if resultados and len(resultados) > 0:
                return {
                    'mensaje': resultados[0][0],
                    'id_empresa': int(resultados[0][1]),
                    'nombre': resultados[0][2],
                    'razon_social': resultados[0][3]
                }
            return None
            
        except Exception as e:
            print(f"Error al obtener datos de empresa: {e}")
            return None