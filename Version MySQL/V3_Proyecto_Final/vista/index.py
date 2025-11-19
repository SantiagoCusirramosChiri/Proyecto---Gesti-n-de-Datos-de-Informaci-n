# index.py

import customtkinter as ctk
from PIL import Image
import os
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


class SistemaApp:
    
    # Inicializa la aplicación principal con datos del usuario y empresa
    def __init__(self, nombre_usuario: str, id_empresa: int):
        self.nombre_usuario = nombre_usuario
        self.id_empresa = id_empresa
        
        self.ventana = ctk.CTk()
        self.ventana.title(f"IRONtomb - Sistema de Gestión | {nombre_usuario}")
        self.ventana.geometry("1400x800")
        self.ventana.configure(fg_color=COLOR_FONDO)
        
        self._centrar_ventana()
        self._crear_barra_superior()
        self._crear_contenedor_principal()
        self._crear_footer()
        
        self.cargar_listar_documentos()
    
    # Centra la ventana principal en la pantalla
    def _centrar_ventana(self):
        self.ventana.update_idletasks()
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 800) // 2
        self.ventana.geometry(f"1400x800+{x}+{y}")
    
    # Crea la barra superior con logo, título y datos del usuario
    def _crear_barra_superior(self):
        frame_superior = ctk.CTkFrame(
            self.ventana,
            height=60,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=0
        )
        frame_superior.pack(fill="x", side="top")
        frame_superior.pack_propagate(False)
        
        self._cargar_logo(frame_superior)
        
        label_titulo = ctk.CTkLabel(
            frame_superior,
            text="IRONtomb",
            font=("Arial Black", 20, "bold"),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_titulo.pack(side="left", padx=10)
        
        frame_usuario = ctk.CTkFrame(frame_superior, fg_color="transparent")
        frame_usuario.pack(side="right", padx=20)
        
        label_usuario = ctk.CTkLabel(
            frame_usuario,
            text=f"👤 {self.nombre_usuario}",
            font=("Arial", 12, "bold"),
            text_color=COLOR_TEXTO
        )
        label_usuario.pack(side="left", padx=10)
        
        label_id = ctk.CTkLabel(
            frame_usuario,
            text=f"ID: {self.id_empresa}",
            font=("Arial", 10),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_id.pack(side="left", padx=5)
        
        btn_cerrar = ctk.CTkButton(
            frame_superior,
            text="🚪 Cerrar Sesión",
            command=self._cerrar_sesion,
            width=120,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color="transparent",
            text_color=COLOR_ROJO_PRIMARY,
            hover_color=COLOR_FONDO,
            border_width=2,
            border_color=COLOR_ROJO_PRIMARY,
            corner_radius=8
        )
        btn_cerrar.pack(side="right", padx=10)
    
    # Carga el logo del sistema en la barra superior
    def _cargar_logo(self, frame):
        try:
            ruta_logo = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "recursos",
                "simbolo.png"
            )
            if os.path.exists(ruta_logo):
                logo = ctk.CTkImage(
                    light_image=Image.open(ruta_logo),
                    dark_image=Image.open(ruta_logo),
                    size=(40, 40)
                )
                label_logo = ctk.CTkLabel(frame, image=logo, text="")
                label_logo.pack(side="left", padx=10)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
    
    # Crea el contenedor principal con menú lateral y área de contenido
    def _crear_contenedor_principal(self):
        frame_contenedor = ctk.CTkFrame(self.ventana, fg_color="transparent")
        frame_contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.frame_menu = ctk.CTkFrame(
            frame_contenedor,
            width=280,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=10,
            border_width=2,
            border_color=COLOR_BORDE
        )
        self.frame_menu.pack(side="left", fill="y", padx=(0, 10))
        self.frame_menu.pack_propagate(False)
        
        self.frame_menu_scroll = ctk.CTkScrollableFrame(
            self.frame_menu,
            fg_color="transparent"
        )
        self.frame_menu_scroll.pack(fill="both", expand=True)
        
        self.frame_contenido = ctk.CTkScrollableFrame(
            frame_contenedor,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=10,
            border_width=2,
            border_color=COLOR_BORDE
        )
        self.frame_contenido.pack(side="right", fill="both", expand=True)
        
        self._generar_menu()
    
    # Genera el menú de navegación con todas las opciones del sistema
    def _generar_menu(self):
        try:
            ruta_logo = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "recursos",
                "simbolo.png"
            )
            if os.path.exists(ruta_logo):
                logo = ctk.CTkImage(
                    light_image=Image.open(ruta_logo),
                    dark_image=Image.open(ruta_logo),
                    size=(80, 80)
                )
                label_logo = ctk.CTkLabel(self.frame_menu_scroll, image=logo, text="")
                label_logo.pack(pady=10)
        except:
            pass
        
        self._crear_seccion("📁 MAESTROS")
        self._crear_boton_menu("  → Conductores", self.cargar_conductores)
        self._crear_boton_menu("  → Vehículos", self.cargar_vehiculos)
        self._crear_boton_menu("  → Formas de Pago", self.cargar_formas_pago)
        self._crear_boton_menu("  → Monedas", self.cargar_monedas)
        self._crear_boton_menu("  → Ubicaciones", self.cargar_ubicaciones)
        self._crear_boton_menu("  → Identidades", self.cargar_identidades)
        self._crear_separador()
        
        self._crear_seccion("👥 CLIENTES")
        self._crear_boton_menu("  → Listar Clientes", self.cargar_listar_clientes)
        self._crear_boton_menu("  → Registrar Cliente", self.cargar_registrar_cliente)
        self._crear_separador()
        
        self._crear_seccion("📦 INVENTARIO")
        self._crear_boton_menu("  → Stock", self.cargar_inventario_stock)
        self._crear_boton_menu("  → Registrar Producto", self.cargar_registrar_producto)
        self._crear_boton_menu("  → Movimientos", self.cargar_movimientos)
        self._crear_separador()
        
        self._crear_seccion("📄 DOCUMENTOS")
        self._crear_boton_menu("  → Crear Documento", self.cargar_crear_documento)
        self._crear_boton_menu("  → Listar Documentos", self.cargar_listar_documentos)
        self._crear_separador()
        
        self._crear_seccion("🚚 GUÍAS DE REMISIÓN")
        self._crear_boton_menu("  → Crear Guía", self.cargar_crear_guia)
        self._crear_boton_menu("  → Listar Guías", self.cargar_listar_guias)
    
    # Crea un botón en el menú de navegación
    def _crear_boton_menu(self, texto: str, comando, destacado: bool = False):
        if destacado:
            btn = ctk.CTkButton(
                self.frame_menu_scroll,
                text=texto,
                command=comando,
                anchor="w",
                font=("Arial", 12, "bold"),
                fg_color=COLOR_ROJO_PRIMARY,
                hover_color=COLOR_ROJO_HOVER,
                height=40
            )
        else:
            btn = ctk.CTkButton(
                self.frame_menu_scroll,
                text=texto,
                command=comando,
                anchor="w",
                font=("Arial", 11),
                fg_color="transparent",
                hover_color=COLOR_FONDO,
                text_color=COLOR_TEXTO,
                height=35
            )
        btn.pack(fill="x", padx=10, pady=2)

    # Crea una etiqueta de sección en el menú
    def _crear_seccion(self, texto: str):
        label = ctk.CTkLabel(
            self.frame_menu_scroll,
            text=texto,
            font=("Arial", 11, "bold"),
            text_color=COLOR_ROJO_PRIMARY,
            anchor="w"
        )
        label.pack(fill="x", padx=10, pady=(10, 5))

    # Crea una línea separadora en el menú
    def _crear_separador(self):
        separador = ctk.CTkFrame(
            self.frame_menu_scroll,
            height=2,
            fg_color=COLOR_BORDE
        )
        separador.pack(fill="x", padx=20, pady=8)
    
    # Crea el pie de página con información de copyright
    def _crear_footer(self):
        frame_footer = ctk.CTkFrame(
            self.ventana,
            height=30,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=0
        )
        frame_footer.pack(fill="x", side="bottom")
        frame_footer.pack_propagate(False)
        
        label_footer = ctk.CTkLabel(
            frame_footer,
            text="© 2024 IRONtomb - Sistema de Gestión Empresarial | Todos los derechos reservados",
            font=("Arial", 9),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_footer.pack(pady=5)
    
    # Limpia el contenido del frame principal
    def _limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    # Cierra sesión y vuelve a la pantalla de login
    def _cerrar_sesion(self):
        self.ventana.destroy()
        try:
            from vista.login import abrir_login
            abrir_login()
        except:
            print("No se pudo reabrir el login")
    
    # Carga el módulo de gestión de conductores
    def cargar_conductores(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_conductores
            maestro_conductores.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Conductores: {e}")
    
    # Carga el módulo de gestión de vehículos
    def cargar_vehiculos(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_vehiculos
            maestro_vehiculos.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Vehículos: {e}")
    
    # Carga el módulo de gestión de formas de pago
    def cargar_formas_pago(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_formas_pago
            maestro_formas_pago.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Formas de Pago: {e}")
    
    # Carga el módulo de gestión de monedas
    def cargar_monedas(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_monedas
            maestro_monedas.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Monedas: {e}")
    
    # Carga el módulo de gestión de ubicaciones
    def cargar_ubicaciones(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_ubicaciones
            maestro_ubicaciones.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Ubicaciones: {e}")
    
    # Carga el módulo de gestión de identidades
    def cargar_identidades(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import maestro_identidades
            maestro_identidades.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Identidades: {e}")
    
    # Carga el módulo de listado de clientes
    def cargar_listar_clientes(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import clientes_listar
            clientes_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Clientes: {e}")

    # Carga el módulo de registro de clientes
    def cargar_registrar_cliente(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import clientes_registrar
            clientes_registrar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Registro de Cliente: {e}")
    
    # Carga el módulo de visualización de stock de inventario
    def cargar_inventario_stock(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import inventario_stock
            inventario_stock.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Stock: {e}")

    # Carga el módulo de registro de productos
    def cargar_registrar_producto(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import inventario_registrar
            inventario_registrar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Registro de Producto: {e}")
    
    # Carga el módulo de movimientos de inventario
    def cargar_movimientos(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import inventario_movimientos
            inventario_movimientos.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Movimientos: {e}")
    
    # Carga el módulo de creación de documentos
    def cargar_crear_documento(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import documentos_crear
            documentos_crear.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Crear Documentos: {e}")
    
    # Carga el módulo de listado de documentos
    def cargar_listar_documentos(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import documentos_listar
            documentos_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Listar Documentos: {e}")
    
    # Carga el módulo de creación de guías de remisión
    def cargar_crear_guia(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import guias_crear
            guias_crear.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Crear Guías: {e}")
    
    # Carga el módulo de listado de guías de remisión
    def cargar_listar_guias(self):
        self._limpiar_contenido()
        try:
            from vista.modulos import guias_listar
            guias_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Listar Guías: {e}")
    
    # Muestra un mensaje de error en el área de contenido
    def _mostrar_error(self, mensaje: str):
        label = ctk.CTkLabel(
            self.frame_contenido,
            text=f"❌ {mensaje}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label.pack(pady=50)
    
    # Inicia el bucle principal de la aplicación
    def iniciar(self):
        self.ventana.mainloop()


# Punto de entrada para abrir la aplicación principal
def abrir_index(nombre_usuario: str, id_empresa: int):
    app = SistemaApp(nombre_usuario, id_empresa)
    app.iniciar()


if __name__ == "__main__":
    abrir_index("Empresa Demo", 1)