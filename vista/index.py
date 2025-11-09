# vista/index.py
import customtkinter as ctk
from PIL import Image

def abrir_index(nombre_empresa, id_empresa):
    """Abre el dashboard principal del sistema"""
    
    # --- Ventana principal ---
    ventana_dashboard = ctk.CTk()
    ventana_dashboard.title(f"IRONtomb - {nombre_empresa}")
    ventana_dashboard.geometry("1400x800")
    ventana_dashboard.resizable(True, True)
    
    # Configurar tema oscuro
    ctk.set_appearance_mode("dark")
    ventana_dashboard.configure(fg_color="#1a1a1a")
    
    # --- SIDEBAR (Menú lateral) ---
    sidebar = ctk.CTkFrame(
        ventana_dashboard, 
        width=280, 
        corner_radius=0, 
        fg_color="#242424"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    # Frame scrollable para el contenido del sidebar
    sidebar_scroll = ctk.CTkScrollableFrame(
        sidebar,
        fg_color="transparent",
        scrollbar_button_color="#DC143C",
        scrollbar_button_hover_color="#B71C1C"
    )
    sidebar_scroll.pack(fill="both", expand=True)
    
    # Logo y título en sidebar
    frame_logo = ctk.CTkFrame(sidebar_scroll, fg_color="transparent")
    frame_logo.pack(pady=(30, 20))
    
    try:
        imagen_logo = ctk.CTkImage(
            light_image=Image.open("recursos/simbolo.png"),
            dark_image=Image.open("recursos/simbolo.png"),
            size=(60, 60)
        )
        label_logo = ctk.CTkLabel(frame_logo, image=imagen_logo, text="")
        label_logo.pack()
    except:
        label_logo_alt = ctk.CTkLabel(frame_logo, text="🔥", font=("Arial", 40))
        label_logo_alt.pack()
    
    label_sistema = ctk.CTkLabel(
        sidebar_scroll,
        text="IRONtomb",
        font=("Arial Black", 24, "bold"),
        text_color="#DC143C"
    )
    label_sistema.pack(pady=(0, 5))
    
    label_empresa = ctk.CTkLabel(
        sidebar_scroll,
        text=nombre_empresa,
        font=("Arial", 11),
        text_color="#8a8a8a"
    )
    label_empresa.pack(pady=(0, 30))
    
    # Separador
    separador = ctk.CTkFrame(sidebar_scroll, height=2, fg_color="#3a3a3a")
    separador.pack(fill="x", padx=20, pady=(0, 20))
    
    # Variable para rastrear el menú actualmente expandido
    menu_expandido = {"actual": None}
    
    # --- Función para crear submenú item ---
    def crear_submenu_item(parent, texto, comando=None):
        btn = ctk.CTkButton(
            parent,
            text=f"  • {texto}",
            command=comando,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#3a3a3a",
            text_color="#b0b0b0",
            font=("Arial", 11),
            anchor="w",
            border_spacing=10
        )
        btn.pack(fill="x", padx=(30, 15), pady=2)
        return btn
    
    # --- Función para crear menú con acordeón ---
   # --- Función para crear menú con acordeón ---
    def crear_menu_acordeon(parent, texto, icono, submenus=None, es_dashboard=False):
        # Frame contenedor
        frame_contenedor = ctk.CTkFrame(parent, fg_color="transparent")
        frame_contenedor.pack(fill="x", padx=15, pady=5)

        # Frame para submenú (si existe)
        frame_submenu = None
        if submenus:
            frame_submenu = ctk.CTkFrame(frame_contenedor, fg_color="transparent")

        # Estado del acordeón
        estado = {"expandido": False}

        def toggle_acordeon():
            # Si hay otro menú expandido, cerrarlo
            if menu_expandido["actual"] is not None and menu_expandido["actual"] != estado:
                menu_expandido["actual"]["expandido"] = False
                # ✅ Verificar que el frame exista antes de cerrarlo
                if menu_expandido["actual"]["frame"] is not None:
                    menu_expandido["actual"]["frame"].pack_forget()
                menu_expandido["actual"]["boton"].configure(
                    fg_color="transparent",
                    text=f"  {menu_expandido['actual']['icono']}  {menu_expandido['actual']['texto']}"
                )

            # Si no tiene submenú, solo activar el botón
            if not submenus:
                btn_principal.configure(fg_color="#DC143C")
                if menu_expandido["actual"]:
                    menu_expandido["actual"]["boton"].configure(fg_color="transparent")
                menu_expandido["actual"] = {
                    "expandido": False,
                    "frame": None,
                    "boton": btn_principal,
                    "icono": icono,
                    "texto": texto
                }
                return

            # Toggle del submenú
            if estado["expandido"]:
                frame_submenu.pack_forget()
                btn_principal.configure(
                    fg_color="transparent",
                    text=f"  {icono}  {texto}"
                )
                estado["expandido"] = False
                menu_expandido["actual"] = None
            else:
                frame_submenu.pack(fill="x", pady=(5, 5))
                btn_principal.configure(
                    fg_color="#DC143C",
                    text=f"  {icono}  {texto}  ▼"
                )
                estado["expandido"] = True
                menu_expandido["actual"] = {
                    "expandido": True,
                    "frame": frame_submenu,
                    "boton": btn_principal,
                    "icono": icono,
                    "texto": texto
                }

            # 🔥 Actualizar el scroll del sidebar
            sidebar_scroll._parent_canvas.configure(scrollregion=sidebar_scroll._parent_canvas.bbox("all"))

        # Botón principal
        btn_principal = ctk.CTkButton(
            frame_contenedor,
            text=f"  {icono}  {texto}",
            command=toggle_acordeon,
            height=50,
            corner_radius=10,
            fg_color="#DC143C" if es_dashboard else "transparent",
            hover_color="#DC143C",
            text_color="white",
            font=("Arial", 13, "bold"),
            anchor="w",
            border_spacing=10
        )
        btn_principal.pack(fill="x")

        # Crear items del submenú
        if submenus:
            for submenu_texto in submenus:
                crear_submenu_item(frame_submenu, submenu_texto)

        return frame_contenedor
    
    # --- MENÚS DEL SIDEBAR ---
    crear_menu_acordeon(sidebar, "Dashboard", "🏠", es_dashboard=True)
    
    crear_menu_acordeon(
        sidebar, 
        "Documentos", 
        "📄",
        [
            "Crear Nuevo Documento",
            "Listar Todos los Documentos",
            "Ver Detalle de Productos",
            "Documentos Emitidos",
            "Documentos Pendientes"
        ]
    )
    
    crear_menu_acordeon(
        sidebar,
        "Guías de Remisión",
        "🚚",
        [
            "Crear Nueva Guía",
            "Listar Todas las Guías",
            "Guías Pendientes",
            "Ver Detalles de Guía"
        ]
    )
    
    crear_menu_acordeon(
        sidebar,
        "Inventario",
        "📦",
        [
            "Listar Stock Actual",
            "Registrar Producto",
            "Ver Movimientos"
        ]
    )
    
    crear_menu_acordeon(
        sidebar,
        "Clientes",
        "👥",
        [
            "Listar Clientes",
            "Registrar Nuevo Cliente",
            "Ver Historial de Compras"
        ]
    )
    
    crear_menu_acordeon(
        sidebar,
        "Maestros",
        "⚙️",
        [
            "Ubicaciones",
            "Identidades",
            "Conductores",
            "Vehículos",
            "Formas de Pago",
            "Monedas"
        ]
    )
    
    # Separador inferior
    separador_inferior = ctk.CTkFrame(sidebar, height=2, fg_color="#3a3a3a")
    separador_inferior.pack(fill="x", padx=20, pady=(20, 20))
    
    # Botón cerrar sesión (abajo)
    btn_cerrar = ctk.CTkButton(
        sidebar,
        text="  🚪  Cerrar Sesión",
        height=50,
        corner_radius=10,
        fg_color="transparent",
        hover_color="#B71C1C",
        text_color="white",
        font=("Arial", 13, "bold"),
        anchor="w",
        border_spacing=10
    )
    btn_cerrar.pack(fill="x", padx=15, pady=(0, 20))
    
    # --- ÁREA PRINCIPAL DE CONTENIDO ---
    area_principal = ctk.CTkFrame(ventana_dashboard, fg_color="#1a1a1a", corner_radius=0)
    area_principal.pack(side="right", fill="both", expand=True)
    
    # --- HEADER ---
    header = ctk.CTkFrame(area_principal, height=80, fg_color="#242424", corner_radius=0)
    header.pack(fill="x", padx=0, pady=0)
    header.pack_propagate(False)
    
    label_titulo_seccion = ctk.CTkLabel(
        header,
        text="📊 Dashboard Principal",
        font=("Arial Black", 26, "bold"),
        text_color="white"
    )
    label_titulo_seccion.pack(side="left", padx=30, pady=20)
    
    label_fecha = ctk.CTkLabel(
        header,
        text="Domingo, 09 de Noviembre 2025",
        font=("Arial", 12),
        text_color="#8a8a8a"
    )
    label_fecha.pack(side="right", padx=30)
    
    # --- CONTENIDO PRINCIPAL (Scrollable) ---
    contenedor_scroll = ctk.CTkScrollableFrame(
        area_principal,
        fg_color="transparent",
        scrollbar_button_color="#DC143C",
        scrollbar_button_hover_color="#B71C1C"
    )
    contenedor_scroll.pack(fill="both", expand=True, padx=30, pady=20)
    
    # --- SECCIÓN: MÉTRICAS PRINCIPALES ---
    label_metricas = ctk.CTkLabel(
        contenedor_scroll,
        text="Métricas Principales",
        font=("Arial", 16, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_metricas.pack(fill="x", pady=(0, 15))
    
    # Grid de tarjetas de métricas
    frame_metricas = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
    frame_metricas.pack(fill="x", pady=(0, 30))
    
    # Configurar grid (3 columnas)
    frame_metricas.grid_columnconfigure((0, 1, 2), weight=1)
    
    def crear_tarjeta_metrica(parent, titulo, valor, icono, color_acento, fila, columna):
        tarjeta = ctk.CTkFrame(
            parent,
            fg_color="#242424",
            corner_radius=15,
            border_width=2,
            border_color="#2d2d2d"
        )
        tarjeta.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
        
        # Icono
        label_icono = ctk.CTkLabel(
            tarjeta,
            text=icono,
            font=("Arial", 40),
            text_color=color_acento
        )
        label_icono.pack(pady=(20, 5))
        
        # Valor
        label_valor = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Arial Black", 32, "bold"),
            text_color="white"
        )
        label_valor.pack(pady=5)
        
        # Título
        label_titulo_tarjeta = ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 12),
            text_color="#8a8a8a"
        )
        label_titulo_tarjeta.pack(pady=(0, 20))
        
        return tarjeta
    
    # Crear tarjetas de métricas (2 filas x 3 columnas) - Basadas en los SP disponibles
    crear_tarjeta_metrica(frame_metricas, "Docs. Emitidos", "0", "📝", "#4CAF50", 0, 0)
    crear_tarjeta_metrica(frame_metricas, "Docs. Pendientes", "0", "⏳", "#FF9800", 0, 1)
    crear_tarjeta_metrica(frame_metricas, "Guías Pendientes", "0", "🚚", "#2196F3", 0, 2)
    
    crear_tarjeta_metrica(frame_metricas, "Stock Total", "0 unid.", "📦", "#9C27B0", 1, 0)
    crear_tarjeta_metrica(frame_metricas, "Total Ventas", "S/ 0.00", "💰", "#DC143C", 1, 1)
    crear_tarjeta_metrica(frame_metricas, "Clientes Activos", "0", "👥", "#00BCD4", 1, 2)
    
    # --- SECCIÓN: ACCESOS RÁPIDOS ---
    label_accesos = ctk.CTkLabel(
        contenedor_scroll,
        text="Accesos Rápidos",
        font=("Arial", 16, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_accesos.pack(fill="x", pady=(20, 15))
    
    frame_accesos = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
    frame_accesos.pack(fill="x", pady=(0, 30))
    frame_accesos.grid_columnconfigure((0, 1, 2), weight=1)
    
    def crear_boton_acceso(parent, texto, icono, color, fila, columna):
        btn = ctk.CTkButton(
            parent,
            text=f"{icono}\n{texto}",
            height=120,
            corner_radius=15,
            fg_color=color,
            hover_color="#2d2d2d",
            text_color="white",
            font=("Arial", 14, "bold"),
            border_width=2,
            border_color="#3a3a3a"
        )
        btn.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
        return btn
    
    crear_boton_acceso(frame_accesos, "Nuevo Documento", "📄", "#242424", 0, 0)
    crear_boton_acceso(frame_accesos, "Nueva Guía Remisión", "🚚", "#242424", 0, 1)
    crear_boton_acceso(frame_accesos, "Registrar Cliente", "👤", "#242424", 0, 2)
    
    crear_boton_acceso(frame_accesos, "Ver Stock", "📦", "#242424", 1, 0)
    crear_boton_acceso(frame_accesos, "Ver Productos", "🏷️", "#242424", 1, 1)
    crear_boton_acceso(frame_accesos, "Gestionar Maestros", "⚙️", "#242424", 1, 2)
    
    # --- SECCIÓN: ACTIVIDAD RECIENTE ---
    label_actividad = ctk.CTkLabel(
        contenedor_scroll,
        text="Actividad Reciente",
        font=("Arial", 16, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_actividad.pack(fill="x", pady=(20, 15))
    
    frame_actividad = ctk.CTkFrame(contenedor_scroll, fg_color="#242424", corner_radius=15)
    frame_actividad.pack(fill="x", pady=(0, 20))
    
    # Mensaje cuando no hay actividad
    label_sin_actividad = ctk.CTkLabel(
        frame_actividad,
        text="No hay actividad reciente\n\nEmpieza creando tu primer documento o guía de remisión",
        font=("Arial", 13),
        text_color="#6a6a6a",
        justify="center"
    )
    label_sin_actividad.pack(pady=60)
    
    # Centrar ventana
    ventana_dashboard.update_idletasks()
    x = (ventana_dashboard.winfo_screenwidth() // 2) - (ventana_dashboard.winfo_width() // 2)
    y = (ventana_dashboard.winfo_screenheight() // 2) - (ventana_dashboard.winfo_height() // 2)
    ventana_dashboard.geometry(f"+{x}+{y}")
    
    ventana_dashboard.mainloop()


# Para pruebas (comentar cuando se integre)
if __name__ == "__main__":
    abrir_index("Transportes El Rápido SAC", 1)