from datos.conexion import ConexionDB
from typing import Optional, Dict

class LoginBL:

    @staticmethod
    def validar_login(usuario: str, contrasena: str) -> Optional[Dict]:
        """
        Valida credenciales usando el SP sp_login_empresa.
        Retorna los datos de la empresa si el login es exitoso, None si falla.
        """
        if not usuario or not contrasena:
            print("❌ Usuario o contraseña vacíos")
            return None

        db = ConexionDB()
        db.conectar()

        try:
            sql = "SELECT * FROM sp_login_empresa(CAST(:usuario AS VARCHAR), CAST(:clave AS CHAR(11)))"
            parametros = {"usuario": usuario, "clave": contrasena}
            resultados = db.ejecutar(sql, parametros)

            if not resultados:
                print("❌ Sin resultados del procedimiento")
                return None

            fila = resultados[0]
            mensaje = fila.get("mensaje", "").strip().upper()

            if mensaje == "LOGIN EXITOSO":
                datos_empresa = {
                    "mensaje": fila["mensaje"],
                    "id_empresa": int(fila["id_empresa"]),
                    "nombre_empresa": fila["nombre_empresa"],
                    "razon_social_empresa": fila["razon_social_empresa"]
                }
                print(f"✅ Login exitoso - Empresa: {datos_empresa['nombre_empresa']}")
                return datos_empresa
            else:
                print(f"❌ Login fallido: {mensaje}")
                return None

        except Exception as e:
            print(f"❌ Error en validación de login: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            db.desconectar()

    @staticmethod
    def obtener_datos_empresa(usuario: str, ruc: str) -> Optional[Dict]:
        """
        Alias de validar_login para mantener compatibilidad.
        Usa validar_login internamente.
        """
        return LoginBL.validar_login(usuario, ruc)

    @staticmethod
    def obtener_id_empresa(usuario: str, ruc: str) -> Optional[int]:
        """
        Obtiene solo el ID de la empresa después del login.
        Usa validar_login internamente.
        """
        datos = LoginBL.validar_login(usuario, ruc)
        return datos["id_empresa"] if datos else None