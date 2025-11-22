# index.py - VERSIÓN FINAL CON PUNTO INDICADOR (●)
from rutas import ruta_recurso
import customtkinter as ctk
from PIL import Image
import os
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


class SeccionColapsable(ctk.CTkFrame):
    """Frame colapsable con indicadores visuales ▼/▲"""
    
    def __init__(self, parent, titulo, icono="📁", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.expandido = False
        self.botones = {}  # Diccionario: nombre -> botón
        self.titulo_base = titulo
        self.icono = icono
        
        self.btn_toggle = ctk.CTkButton(
            self,
            text=f"{icono} {titulo} ▼",
            command=self.toggle,
            anchor="w",
            font=("Arial", 13, "bold"),
            fg_color=COLOR_FONDO_TERCIARIO,
            hover_color=COLOR_ROJO_PRIMARY,
            text_color=COLOR_TEXTO,
            height=45,
            corner_radius=8
        )
        self.btn_toggle.pack(fill="x", pady=2)
        
        self.frame_opciones = ctk.CTkFrame(self, fg_color="transparent")
        
    def agregar_opcion(self, nombre, texto, comando):
        """Agrega una opción al menú colapsable"""
        btn = ctk.CTkButton(
            self.frame_opciones,
            text=f"   → {texto}",
            command=comando,
            anchor="w",
            font=("Arial", 12),
            fg_color="transparent",
            hover_color=COLOR_FONDO_TERCIARIO,
            text_color=COLOR_TEXTO_SECUNDARIO,
            height=38,
            corner_radius=6
        )
        btn.pack(fill="x", pady=1, padx=(10, 0))
        self.botones[nombre] = btn
        return btn
    
    def toggle(self):
        """Expande o colapsa la sección"""
        if self.expandido:
            self.frame_opciones.pack_forget()
            self.expandido = False
            self.btn_toggle.configure(
                text=f"{self.icono} {self.titulo_base} ▼",
                fg_color=COLOR_FONDO_TERCIARIO
            )
        else:
            self.frame_opciones.pack(fill="x", pady=(2, 8))
            self.expandido = True
            self.btn_toggle.configure(
                text=f"{self.icono} {self.titulo_base} ▲",
                fg_color=COLOR_ROJO_PRIMARY
            )
    
    def expandir(self):
        """Expande la sección si no está expandida"""
        if not self.expandido:
            self.toggle()
    
    def colapsar(self):
        """Colapsa la sección si está expandida"""
        if self.expandido:
            self.toggle()
    
    def marcar_activo(self, nombre):
        """Marca un botón como activo con punto (●) y resaltado"""
        if nombre in self.botones:
            btn = self.botones[nombre]
            # Obtener el texto original sin el punto
            texto_original = btn.cget("text").replace("● ", "").replace("   → ", "")
            
            self.botones[nombre].configure(
                text=f"   ● {texto_original}",  # ← PUNTO INDICADOR
                fg_color=COLOR_ROJO_PRIMARY,
                text_color="#FFFFFF",  # Blanco para contraste
                font=("Arial", 12, "bold")
            )
    
    def desmarcar_todos(self):
        """Desmarca todos los botones de esta sección"""
        for nombre, btn in self.botones.items():
            # Obtener texto original sin modificadores
            texto_original = btn.cget("text").replace("● ", "").replace("   → ", "").replace("   ", "")
            
            btn.configure(
                text=f"   → {texto_original}",
                fg_color="transparent",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 12)
            )


class SistemaApp:
    
    def __init__(self, nombre_usuario: str, id_empresa: int):
        self.nombre_usuario = nombre_usuario
        self.id_empresa = id_empresa
        
        self.ventana = ctk.CTk()
        self.ventana.title(f"IRONtomb - Sistema de Gestión | {nombre_usuario}")
        self.ventana.geometry("1400x800")
        self.ventana.configure(fg_color=COLOR_FONDO)
        
        self.secciones = {}
        self.opcion_activa = None
        
        self._centrar_ventana()
        self._crear_barra_superior()
        self._crear_contenedor_principal()
        self._crear_footer()
        
        self.cargar_listar_documentos()
    
    def _centrar_ventana(self):
        self.ventana.update_idletasks()
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 800) // 2
        self.ventana.geometry(f"1400x800+{x}+{y}")
    
    def _crear_barra_superior(self):
        frame_superior = ctk.CTkFrame(
            self.ventana,
            height=65,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=0
        )
        frame_superior.pack(fill="x", side="top")
        frame_superior.pack_propagate(False)
        
        self._cargar_logo(frame_superior)
        
        label_titulo = ctk.CTkLabel(
            frame_superior,
            text="IRONtomb",
            font=("Arial Black", 22, "bold"),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_titulo.pack(side="left", padx=10)
        
        frame_usuario = ctk.CTkFrame(frame_superior, fg_color="transparent")
        frame_usuario.pack(side="right", padx=20)
        
        label_usuario = ctk.CTkLabel(
            frame_usuario,
            text=f"👤 {self.nombre_usuario}",
            font=("Arial", 13, "bold"),
            text_color=COLOR_TEXTO
        )
        label_usuario.pack(side="left", padx=10)
        
        label_id = ctk.CTkLabel(
            frame_usuario,
            text=f"ID: {self.id_empresa}",
            font=("Arial", 11),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_id.pack(side="left", padx=5)
        
        btn_cerrar = ctk.CTkButton(
            frame_superior,
            text="🚪 Cerrar Sesión",
            command=self._cerrar_sesion,
            width=130,
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            text_color=COLOR_ROJO_PRIMARY,
            hover_color=COLOR_FONDO_TERCIARIO,
            border_width=2,
            border_color=COLOR_ROJO_PRIMARY,
            corner_radius=8
        )
        btn_cerrar.pack(side="right", padx=10)
    
    def _cargar_logo(self, frame):
        try:
            ruta_logo = ruta_recurso(os.path.join("recursos", "simbolo.png"))
            
            if os.path.exists(ruta_logo):
                logo = ctk.CTkImage(
                    light_image=Image.open(ruta_logo),
                    dark_image=Image.open(ruta_logo),
                    size=(45, 45)
                )
                label_logo = ctk.CTkLabel(frame, image=logo, text="")
                label_logo.pack(side="left", padx=10)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
    
    def _crear_contenedor_principal(self):
        frame_contenedor = ctk.CTkFrame(self.ventana, fg_color="transparent")
        frame_contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.frame_menu = ctk.CTkFrame(
            frame_contenedor,
            width=260,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE
        )
        self.frame_menu.pack(side="left", fill="y", padx=(0, 10))
        self.frame_menu.pack_propagate(False)
        
        self.frame_menu_scroll = ctk.CTkScrollableFrame(
            self.frame_menu,
            fg_color="transparent"
        )
        self.frame_menu_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.frame_contenido = ctk.CTkScrollableFrame(
            frame_contenedor,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE
        )
        self.frame_contenido.pack(side="right", fill="both", expand=True)
        
        self._generar_menu()
    
    def _generar_menu(self):
        try:
            ruta_logo = ruta_recurso(os.path.join("recursos", "simbolo.png"))
            if os.path.exists(ruta_logo):
                logo = ctk.CTkImage(
                    light_image=Image.open(ruta_logo),
                    dark_image=Image.open(ruta_logo),
                    size=(70, 70)
                )
                label_logo = ctk.CTkLabel(self.frame_menu_scroll, image=logo, text="")
                label_logo.pack(pady=(5, 15))
        except:
            pass
        
        # MAESTROS
        seccion_maestros = SeccionColapsable(
            self.frame_menu_scroll,
            titulo="MAESTROS",
            icono="📁"
        )
        seccion_maestros.pack(fill="x", pady=2)
        seccion_maestros.agregar_opcion("conductores", "Conductores", self.cargar_conductores)
        seccion_maestros.agregar_opcion("vehiculos", "Vehículos", self.cargar_vehiculos)
        seccion_maestros.agregar_opcion("formas_pago", "Formas de Pago", self.cargar_formas_pago)
        seccion_maestros.agregar_opcion("monedas", "Monedas", self.cargar_monedas)
        seccion_maestros.agregar_opcion("ubicaciones", "Ubicaciones", self.cargar_ubicaciones)
        seccion_maestros.agregar_opcion("identidades", "Identidades", self.cargar_identidades)
        self.secciones["maestros"] = seccion_maestros
        
        # CLIENTES
        seccion_clientes = SeccionColapsable(
            self.frame_menu_scroll,
            titulo="CLIENTES",
            icono="👥"
        )
        seccion_clientes.pack(fill="x", pady=2)
        seccion_clientes.agregar_opcion("listar_clientes", "Listar Clientes", self.cargar_listar_clientes)
        seccion_clientes.agregar_opcion("registrar_cliente", "Registrar Cliente", self.cargar_registrar_cliente)
        self.secciones["clientes"] = seccion_clientes
        
        # INVENTARIO
        seccion_inventario = SeccionColapsable(
            self.frame_menu_scroll,
            titulo="INVENTARIO",
            icono="📦"
        )
        seccion_inventario.pack(fill="x", pady=2)
        seccion_inventario.agregar_opcion("stock", "Stock", self.cargar_inventario_stock)
        seccion_inventario.agregar_opcion("registrar_producto", "Registrar Producto", self.cargar_registrar_producto)
        seccion_inventario.agregar_opcion("movimientos", "Movimientos", self.cargar_movimientos)
        self.secciones["inventario"] = seccion_inventario
        
        # DOCUMENTOS
        seccion_documentos = SeccionColapsable(
            self.frame_menu_scroll,
            titulo="DOCUMENTOS",
            icono="📄"
        )
        seccion_documentos.pack(fill="x", pady=2)
        seccion_documentos.agregar_opcion("crear_documento", "Crear Documento", self.cargar_crear_documento)
        seccion_documentos.agregar_opcion("listar_documentos", "Listar Documentos", self.cargar_listar_documentos)
        self.secciones["documentos"] = seccion_documentos
        
        # GUÍAS
        seccion_guias = SeccionColapsable(
            self.frame_menu_scroll,
            titulo="GUÍAS DE REMISIÓN",
            icono="🚚"
        )
        seccion_guias.pack(fill="x", pady=2)
        seccion_guias.agregar_opcion("crear_guia", "Crear Guía", self.cargar_crear_guia)
        seccion_guias.agregar_opcion("listar_guias", "Listar Guías", self.cargar_listar_guias)
        self.secciones["guias"] = seccion_guias
    
    def _marcar_opcion_activa(self, seccion, opcion):
        """Marca opción activa con punto (●)"""
        for sec in self.secciones.values():
            sec.desmarcar_todos()
        
        if seccion in self.secciones:
            self.secciones[seccion].expandir()
            self.secciones[seccion].marcar_activo(opcion)
        
        self.opcion_activa = (seccion, opcion)
    
    def _crear_footer(self):
        frame_footer = ctk.CTkFrame(
            self.ventana,
            height=32,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=0
        )
        frame_footer.pack(fill="x", side="bottom")
        frame_footer.pack_propagate(False)
        
        label_footer = ctk.CTkLabel(
            frame_footer,
            text="© 2024 IRONtomb - Sistema de Gestión Empresarial | Todos los derechos reservados",
            font=("Arial", 10),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_footer.pack(pady=6)
    
    def _limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    def _cerrar_sesion(self):
        self.ventana.destroy()
        try:
            from vista.login import abrir_login
            abrir_login()
        except:
            print("No se pudo reabrir el login")
    
    # ==================== MÉTODOS DE CARGA ====================
    
    def cargar_conductores(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "conductores")
        try:
            from vista.modulos import maestro_conductores
            maestro_conductores.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Conductores: {e}")
    
    def cargar_vehiculos(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "vehiculos")
        try:
            from vista.modulos import maestro_vehiculos
            maestro_vehiculos.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Vehículos: {e}")
    
    def cargar_formas_pago(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "formas_pago")
        try:
            from vista.modulos import maestro_formas_pago
            maestro_formas_pago.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Formas de Pago: {e}")
    
    def cargar_monedas(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "monedas")
        try:
            from vista.modulos import maestro_monedas
            maestro_monedas.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Monedas: {e}")
    
    def cargar_ubicaciones(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "ubicaciones")
        try:
            from vista.modulos import maestro_ubicaciones
            maestro_ubicaciones.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Ubicaciones: {e}")
    
    def cargar_identidades(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("maestros", "identidades")
        try:
            from vista.modulos import maestro_identidades
            maestro_identidades.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Identidades: {e}")
    
    def cargar_listar_clientes(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("clientes", "listar_clientes")
        try:
            from vista.modulos import clientes_listar
            clientes_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Clientes: {e}")
    
    def cargar_registrar_cliente(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("clientes", "registrar_cliente")
        try:
            from vista.modulos import clientes_registrar
            clientes_registrar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Registro de Cliente: {e}")
    
    def cargar_inventario_stock(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("inventario", "stock")
        try:
            from vista.modulos import inventario_stock
            inventario_stock.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Stock: {e}")
    
    def cargar_registrar_producto(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("inventario", "registrar_producto")
        try:
            from vista.modulos import inventario_registrar
            inventario_registrar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Registro de Producto: {e}")
    
    def cargar_movimientos(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("inventario", "movimientos")
        try:
            from vista.modulos import inventario_movimientos
            inventario_movimientos.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Movimientos: {e}")
    
    def cargar_crear_documento(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("documentos", "crear_documento")
        try:
            from vista.modulos import documentos_crear
            documentos_crear.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Crear Documentos: {e}")
    
    def cargar_listar_documentos(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("documentos", "listar_documentos")
        try:
            from vista.modulos import documentos_listar
            documentos_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Listar Documentos: {e}")
    
    def cargar_crear_guia(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("guias", "crear_guia")
        try:
            from vista.modulos import guias_crear
            guias_crear.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Crear Guías: {e}")
    
    def cargar_listar_guias(self):
        self._limpiar_contenido()
        self._marcar_opcion_activa("guias", "listar_guias")
        try:
            from vista.modulos import guias_listar
            guias_listar.mostrar(self.frame_contenido, self.id_empresa)
        except Exception as e:
            self._mostrar_error(f"Error al cargar Listar Guías: {e}")
    
    def _mostrar_error(self, mensaje: str):
        label = ctk.CTkLabel(
            self.frame_contenido,
            text=f"❌ {mensaje}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label.pack(pady=50)
    
    def iniciar(self):
        self.ventana.mainloop()


def abrir_index(nombre_usuario: str, id_empresa: int):
    app = SistemaApp(nombre_usuario, id_empresa)
    app.iniciar()


if __name__ == "__main__":
    abrir_index("Empresa Demo", 1)