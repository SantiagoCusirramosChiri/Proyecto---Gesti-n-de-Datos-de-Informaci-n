# logica/LoginBL.py
from datos import procedimientos

class LoginBL:
    @staticmethod
    def validar_login(usuario: str, contrasena: str) -> tuple[bool, str, dict]:
        if not usuario or not contrasena:
            return False, "Usuario y contraseña son obligatorios", {}
        
        if len(contrasena) != 11 or not contrasena.isdigit():
            return False, "El RUC debe tener 11 dígitos numéricos", {}

        try:
            resultados = procedimientos.sp_login_empresa(usuario.strip(), contrasena.strip())

            if not resultados or len(resultados) == 0:
                return False, "Usuario o contraseña incorrectos", {}
            
            primer_resultado = resultados[0]
            mensaje = primer_resultado[0]
            
            if "INCORRECTA" in mensaje or "INACTIVA" in mensaje:
                return False, mensaje, {}
            
            if len(primer_resultado) >= 4:
                datos_empresa = {
                    'id_empresa': primer_resultado[1],
                    'nombre': primer_resultado[2],
                    'razon_social': primer_resultado[3]
                }
                return True, "Login exitoso", datos_empresa
            
            return False, "Error al obtener datos de la empresa", {}

        except Exception as e:
            print(f"Error al validar login: {e}")
            return False, f"Error en el sistema: {str(e)}", {}