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
