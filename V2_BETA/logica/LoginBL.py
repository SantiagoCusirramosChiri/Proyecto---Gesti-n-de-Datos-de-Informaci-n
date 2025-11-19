# logica/LoginBL.py
from datos import procedimientos

class LoginBL:
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
        
    @staticmethod
    def obtener_id_empresa(usuario: str, ruc: str) -> int:
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            if resultados and len(resultados) > 0:
                return resultados[0][0] 
            return 1
        except Exception as e:
            print(f"Error al obtener ID de empresa: {e}")
            return 1