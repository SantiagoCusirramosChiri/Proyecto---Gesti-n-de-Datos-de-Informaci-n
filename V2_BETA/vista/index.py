# vista/index.py
import customtkinter as ctk
from PIL import Image

def abrir_index(nombre_empresa: str, id_empresa: int):

    ventana_presentacion = ctk.CTk()
    ventana_presentacion.title(f"IRONtomb - {nombre_empresa}")
    ventana_presentacion.geometry("1400x800")
    ventana_presentacion.resizable(True, True)

    ctk.set_appearance_mode("dark")
    ventana_presentacion.configure(fg_color="#1a1a1a")

    sidebar = ctk.CTkFrame(
        ventana_presentacion,
        width=280,
        corner_radius=0,
        fg_color="#242424"
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    sidebar_scroll = ctk.CTkScrollableFrame(
        sidebar,
        fg_color="transparent",
        scrollbar_button_color="#DC143C",
        scrollbar_button_hover_color="#B71C1C"
    )
    sidebar_scroll.pack(fill="both", expand=True)

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

    separador = ctk.CTkFrame(sidebar_scroll, height=2, fg_color="#3a3a3a")
    separador.pack(fill="x", padx=20, pady=(0, 20))

    menu_expandido = {"actual": None}

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

    def crear_menu_acordeon(parent, texto, icono, submenus=None, es_presentacion=False):
        frame_contenedor = ctk.CTkFrame(parent, fg_color="transparent")
        frame_contenedor.pack(fill="x", padx=15, pady=5)

        frame_submenu = None
        if submenus:
            frame_submenu = ctk.CTkFrame(frame_contenedor, fg_color="transparent")

        estado = {"expandido": False}

        def toggle_acordeon():
            if menu_expandido["actual"] is not None and menu_expandido["actual"] != estado:
                menu_expandido["actual"]["expandido"] = False
                if menu_expandido["actual"]["frame"] is not None:
                    menu_expandido["actual"]["frame"].pack_forget()
                menu_expandido["actual"]["boton"].configure(
                    fg_color="transparent",
                    text=f"  {menu_expandido['actual']['icono']}  {menu_expandido['actual']['texto']}"
                )

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

            sidebar_scroll._parent_canvas.configure(scrollregion=sidebar_scroll._parent_canvas.bbox("all"))

        btn_principal = ctk.CTkButton(
            frame_contenedor,
            text=f"  {icono}  {texto}",
            command=toggle_acordeon,
            height=50,
            corner_radius=10,
            fg_color="#DC143C" if es_presentacion else "transparent",
            hover_color="#DC143C",
            text_color="white",
            font=("Arial", 13, "bold"),
            anchor="w",
            border_spacing=10
        )
        btn_principal.pack(fill="x")

        if submenus:
            for submenu_texto in submenus:
                crear_submenu_item(frame_submenu, submenu_texto)

        return frame_contenedor

    crear_menu_acordeon(sidebar_scroll, "Presentación", "🏠", es_presentacion=True)

    crear_menu_acordeon(
        sidebar_scroll,
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
        sidebar_scroll,
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
        sidebar_scroll,
        "Inventario",
        "📦",
        [
            "Listar Stock Actual",
            "Registrar Producto",
            "Ver Movimientos"
        ]
    )

    crear_menu_acordeon(
        sidebar_scroll,
        "Clientes",
        "👥",
        [
            "Listar Clientes",
            "Registrar Nuevo Cliente",
            "Ver Historial de Compras"
        ]
    )

    crear_menu_acordeon(
        sidebar_scroll,
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

    separador_inferior = ctk.CTkFrame(sidebar, height=2, fg_color="#3a3a3a")
    separador_inferior.pack(fill="x", padx=20, pady=(20, 20))

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

    area_principal = ctk.CTkFrame(ventana_presentacion, fg_color="#1a1a1a", corner_radius=0)
    area_principal.pack(side="right", fill="both", expand=True)

    header = ctk.CTkFrame(area_principal, height=80, fg_color="#242424", corner_radius=0)
    header.pack(fill="x", padx=0, pady=0)
    header.pack_propagate(False)

    label_titulo_seccion = ctk.CTkLabel(
        header,
        text="🎯 Presentación del Sistema",
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

    contenedor_scroll = ctk.CTkScrollableFrame(
        area_principal,
        fg_color="transparent",
        scrollbar_button_color="#DC143C",
        scrollbar_button_hover_color="#B71C1C"
    )
    contenedor_scroll.pack(fill="both", expand=True, padx=30, pady=20)

    label_bienvenida = ctk.CTkLabel(
        contenedor_scroll,
        text="Bienvenido a IRONtomb\n\nSistema de Gestión Documentaria e Inventario.",
        font=("Arial", 18, "bold"),
        text_color="white",
        justify="center"
    )
    label_bienvenida.pack(pady=50)

    ventana_presentacion.update_idletasks()
    x = (ventana_presentacion.winfo_screenwidth() // 2) - (ventana_presentacion.winfo_width() // 2)
    y = (ventana_presentacion.winfo_screenheight() // 2) - (ventana_presentacion.winfo_height() // 2)
    ventana_presentacion.geometry(f"+{x}+{y}")

    ventana_presentacion.mainloop()


# # Para pruebas
# if __name__ == "__main__":
#     abrir_index("Transportes El Rápido SAC", 1)
