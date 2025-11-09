# logica/RegistroBL.py
from datos import procedimientos

class RegistroBL:
    @staticmethod
    def registrar_empresa(nombre: str, razon_social: str, ruc: str, id_ubicacion: int = 1):
        """
        Registra una nueva empresa en el sistema.
        
        :param nombre: Nombre de la empresa
        :param razon_social: Razón social de la empresa
        :param ruc: RUC de 11 dígitos
        :param id_ubicacion: ID de la ubicación (por defecto 1)
        :return: Tupla (éxito: bool, mensaje: str)
        """
        # Validaciones básicas
        if not nombre or not razon_social or not ruc:
            return False, "Todos los campos son obligatorios"
        
        if len(ruc) != 11 or not ruc.isdigit():
            return False, "El RUC debe tener 11 dígitos numéricos"

        try:
            # Llamar al procedimiento almacenado
            resultados = procedimientos.sp_registrar_empresa(nombre, razon_social, ruc, id_ubicacion)
            
            if resultados and len(resultados) > 0:
                mensaje = resultados[0][0]  # Primer elemento del primer resultado
                
                if "ERROR" in mensaje.upper():
                    return False, mensaje
                else:
                    return True, mensaje
            else:
                return False, "Error desconocido en el registro"

        except Exception as e:
            return False, f"Error al registrar empresa: {str(e)}"