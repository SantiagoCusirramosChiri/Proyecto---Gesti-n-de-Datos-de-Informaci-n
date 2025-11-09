# logica/LoginBL.py
from datos import procedimientos  # capa de datos

class LoginBL:
    @staticmethod
    def validar_login(usuario: str, contrasena: str) -> bool:
        """
        Valida el login de la empresa usando el procedimiento almacenado sp_login_usuario.
        :param usuario: Nombre de usuario
        :param contrasena: Contraseña
        :return: True si el login es correcto, False si falla
        """
        # Validación de campos vacíos
        if not usuario or not contrasena:
            return False

        try:
            # Llamamos al procedimiento real
            resultados = procedimientos.sp_login_empresa(usuario, contrasena)

            # Si el procedimiento devuelve al menos un registro, el login es correcto
            return len(resultados) > 0

        except Exception as e:
            print(f"Error al validar login: {e}")
            return False
        
    @staticmethod
    def obtener_id_empresa(usuario: str, ruc: str) -> int:
        """
        Obtiene el ID de la empresa después de un login exitoso.
        :param usuario: Nombre de la empresa
        :param ruc: RUC de la empresa
        :return: ID de la empresa
        """
        try:
            resultados = procedimientos.sp_login_empresa(usuario, ruc)
            if resultados and len(resultados) > 0:
                # Asumiendo que el primer elemento del primer resultado es el ID
                return resultados[0][0]  # Ajustar según la estructura real de tu SP
            return 1  # Valor por defecto si no se puede obtener
        except Exception as e:
            print(f"Error al obtener ID de empresa: {e}")
            return 1  # Valor por defecto en caso de error