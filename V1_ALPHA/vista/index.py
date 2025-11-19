# vista/index.py
import customtkinter as ctk
from PIL import Image
from datetime import datetime
from tkinter import messagebox
from datos import procedimientos

# ============================================================================
# COLORES DEL SISTEMA
# ============================================================================
COLOR_FONDO = "#1a1a1a"
COLOR_SIDEBAR = "#242424"
COLOR_HEADER = "#242424"
COLOR_ROJO = "#DC143C"
COLOR_ROJO_HOVER = "#B71C1C"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SEC = "#8a8a8a"
COLOR_CARD = "#2a2a2a"
COLOR_SUCCESS = "#28a745"
COLOR_WARNING = "#ffc107"
COLOR_INFO = "#17a2b8"

# ============================================================================
# FUNCIÓN PRINCIPAL PARA ABRIR DASHBOARD
# ============================================================================
def abrir_dashboard(nombre_empresa, id_empresa):
    """Abre la ventana principal del dashboard"""
    
    # Crear ventana principal
    ventana = ctk.CTk()
    ventana.title(f"IRONtomb - {nombre_empresa}")
    ventana.geometry("1400x800")
    ventana.resizable(True, True)
    ventana.configure(fg_color=COLOR_FONDO)
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (1400 // 2)
    y = (ventana.winfo_screenheight() // 2) - (800 // 2)
    ventana.geometry(f"1400x800+{x}+{y}")

    # ============================================================================
    # SIDEBAR
    # ============================================================================
    sidebar = ctk.CTkFrame(ventana, width=280, corner_radius=0, fg_color=COLOR_SIDEBAR)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    sidebar_scroll = ctk.CTkScrollableFrame(
        sidebar, fg_color="transparent",
        scrollbar_button_color=COLOR_ROJO,
        scrollbar_button_hover_color=COLOR_ROJO_HOVER
    )
    sidebar_scroll.pack(fill="both", expand=True)

    # Logo y título
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

    ctk.CTkLabel(sidebar_scroll, text="IRONtomb", font=("Arial Black", 24, "bold"), text_color=COLOR_ROJO).pack(pady=(0, 5))
    ctk.CTkLabel(sidebar_scroll, text=nombre_empresa, font=("Arial", 11), text_color=COLOR_TEXTO_SEC).pack(pady=(0, 30))
    ctk.CTkFrame(sidebar_scroll, height=2, fg_color="#3a3a3a").pack(fill="x", padx=20, pady=(0, 20))

    # ============================================================================
    # ÁREA PRINCIPAL
    # ============================================================================
    area_principal = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO, corner_radius=0)
    area_principal.pack(side="right", fill="both", expand=True)

    # Header
    header = ctk.CTkFrame(area_principal, height=80, fg_color=COLOR_HEADER, corner_radius=0)
    header.pack(fill="x")
    header.pack_propagate(False)

    label_titulo_seccion = ctk.CTkLabel(header, text="🎯 Dashboard Principal", font=("Arial Black", 26, "bold"), text_color=COLOR_TEXTO)
    label_titulo_seccion.pack(side="left", padx=30, pady=20)

    fecha_actual = datetime.now().strftime("%A, %d de %B %Y")
    ctk.CTkLabel(header, text=fecha_actual, font=("Arial", 12), text_color=COLOR_TEXTO_SEC).pack(side="right", padx=30)

    # Contenedor principal scrollable
    contenedor_principal = ctk.CTkScrollableFrame(
        area_principal, fg_color="transparent",
        scrollbar_button_color=COLOR_ROJO,
        scrollbar_button_hover_color=COLOR_ROJO_HOVER
    )
    contenedor_principal.pack(fill="both", expand=True, padx=30, pady=20)

    # ============================================================================
    # FUNCIONES AUXILIARES
    # ============================================================================
    def limpiar_contenido():
        for widget in contenedor_principal.winfo_children():
            widget.destroy()

    def actualizar_titulo_header(titulo):
        label_titulo_seccion.configure(text=titulo)

    def crear_campo_form(parent, label_text, placeholder="", tipo="entry", opciones=None):
        """Crea un campo de formulario reutilizable"""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLOR_TEXTO, anchor="w").pack(anchor="w", pady=(10, 5))
        
        if tipo == "entry":
            campo = ctk.CTkEntry(parent, placeholder_text=placeholder, width=400, height=40, font=("Arial", 12),
                               fg_color=COLOR_FONDO, border_color=COLOR_ROJO, border_width=2, text_color=COLOR_TEXTO)
            campo.pack(anchor="w", pady=(0, 5))
            return campo
        elif tipo == "option":
            campo = ctk.CTkOptionMenu(parent, values=opciones, width=400, height=40, font=("Arial", 12),
                                     fg_color=COLOR_CARD, button_color=COLOR_ROJO, button_hover_color=COLOR_ROJO_HOVER)
            campo.pack(anchor="w", pady=(0, 5))
            return campo

    # ============================================================================
    # VISTA: DASHBOARD PRINCIPAL
    # ============================================================================
    def mostrar_dashboard():
        limpiar_contenido()
        actualizar_titulo_header("🎯 Dashboard Principal")
        
        try:
            docs_emitidos = procedimientos.sp_contar_documentos_emitidos(id_empresa)
            docs_pendientes = procedimientos.sp_contar_documentos_pendientes(id_empresa)
            guias_pendientes = procedimientos.sp_contar_guias_pendientes(id_empresa)
            stock_total = procedimientos.sp_stock_total_empresa(id_empresa)
            total_ventas = procedimientos.sp_total_ventas_empresa(id_empresa)
            clientes_activos = procedimientos.sp_contar_clientes_activos(id_empresa)

            frame_cards = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
            frame_cards.pack(fill="x", pady=(0, 30))

            def crear_card(parent, titulo, valor, color, icono):
                card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=15, border_width=2, border_color=color)
                card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
                ctk.CTkLabel(card, text=icono, font=("Arial", 40)).pack(pady=(20, 10))
                ctk.CTkLabel(card, text=str(valor), font=("Arial Black", 36, "bold"), text_color=color).pack()
                ctk.CTkLabel(card, text=titulo, font=("Arial", 12), text_color=COLOR_TEXTO_SEC).pack(pady=(5, 20))

            row1 = ctk.CTkFrame(frame_cards, fg_color="transparent")
            row1.pack(fill="x")
            crear_card(row1, "Documentos Emitidos", docs_emitidos, COLOR_SUCCESS, "✅")
            crear_card(row1, "Documentos Pendientes", docs_pendientes, COLOR_WARNING, "⏳")
            crear_card(row1, "Guías Pendientes", guias_pendientes, COLOR_INFO, "🚚")

            row2 = ctk.CTkFrame(frame_cards, fg_color="transparent")
            row2.pack(fill="x")
            crear_card(row2, "Stock Total", stock_total, COLOR_ROJO, "📦")
            crear_card(row2, "Total Ventas", f"S/ {total_ventas:,.2f}", COLOR_SUCCESS, "💰")
            crear_card(row2, "Clientes Activos", clientes_activos, COLOR_INFO, "👥")

            ctk.CTkLabel(contenedor_principal, text="⚡ Accesos Rápidos", font=("Arial Black", 20, "bold"), text_color=COLOR_TEXTO).pack(anchor="w", pady=(20, 10))
            frame_accesos = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
            frame_accesos.pack(fill="x")

            def crear_boton_acceso(texto, comando, icono):
                ctk.CTkButton(frame_accesos, text=f"{icono} {texto}", command=comando, height=60, font=("Arial", 14, "bold"),
                            fg_color=COLOR_CARD, hover_color=COLOR_ROJO, corner_radius=10).pack(side="left", padx=10, fill="x", expand=True)

            crear_boton_acceso("Ver Stock", mostrar_stock, "📦")
            crear_boton_acceso("Ver Clientes", mostrar_clientes, "👥")
            crear_boton_acceso("Ver Guías", mostrar_guias, "🚚")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar dashboard: {str(e)}")

    # ============================================================================
    # VISTA: STOCK
    # ============================================================================
    def mostrar_stock():
        limpiar_contenido()
        actualizar_titulo_header("📦 Inventario - Stock de Productos")
        
        # Botón para agregar producto
        ctk.CTkButton(contenedor_principal, text="➕ Agregar Producto", command=mostrar_form_producto,
                     height=45, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, hover_color=COLOR_ROJO_HOVER).pack(anchor="e", pady=(0, 15))
        
        try:
            productos = procedimientos.sp_listar_stock_empresa(id_empresa)
            if not productos:
                ctk.CTkLabel(contenedor_principal, text="No hay productos registrados", font=("Arial", 16), text_color=COLOR_TEXTO_SEC).pack(pady=50)
                return

            frame_tabla = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=10)
            frame_tabla.pack(fill="both", expand=True, pady=10)

            headers = ["ID", "Producto", "Descripción", "Stock", "Unidad"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(frame_tabla, text=header, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, corner_radius=5,
                           width=200 if i > 0 else 80).grid(row=0, column=i, padx=5, pady=10, sticky="ew")

            for idx, producto in enumerate(productos, start=1):
                color_fila = COLOR_SIDEBAR if idx % 2 == 0 else "transparent"
                for i, dato in enumerate(producto):
                    ctk.CTkLabel(frame_tabla, text=str(dato), font=("Arial", 11), fg_color=color_fila,
                               width=200 if i > 0 else 80).grid(row=idx, column=i, padx=5, pady=5, sticky="ew")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # ============================================================================
    # FORMULARIO: CREAR PRODUCTO
    # ============================================================================
    def mostrar_form_producto():
        limpiar_contenido()
        actualizar_titulo_header("📦 Registrar Nuevo Producto")
        
        frame_form = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=15, border_width=2, border_color=COLOR_ROJO)
        frame_form.pack(fill="both", expand=True, padx=50, pady=30)
        
        ctk.CTkLabel(frame_form, text="Complete los datos del producto", font=("Arial", 16, "bold"), text_color=COLOR_TEXTO).pack(pady=20)
        
        entry_nombre = crear_campo_form(frame_form, "Nombre del Producto *", "Ej: Cuaderno A4")
        entry_desc = crear_campo_form(frame_form, "Descripción *", "Descripción detallada")
        entry_precio = crear_campo_form(frame_form, "Precio Base *", "0.00")
        entry_stock = crear_campo_form(frame_form, "Stock Inicial *", "0")
        entry_unidad = crear_campo_form(frame_form, "Unidad de Medida *", "UND, KG, LT, etc")
        
        def guardar_producto():
            try:
                nombre = entry_nombre.get()
                desc = entry_desc.get()
                precio = float(entry_precio.get())
                stock = int(entry_stock.get())
                unidad = entry_unidad.get()
                
                if not all([nombre, desc, unidad]):
                    messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios")
                    return
                
                id_producto = procedimientos.sp_insertar_producto(nombre, desc, precio, stock, unidad)
                messagebox.showinfo("Éxito", f"Producto registrado con ID: {id_producto}")
                mostrar_stock()
            except ValueError:
                messagebox.showerror("Error", "Verifique que precio y stock sean números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botones.pack(pady=30)
        ctk.CTkButton(frame_botones, text="💾 Guardar Producto", command=guardar_producto, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_SUCCESS, hover_color="#1e7e34").pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="❌ Cancelar", command=mostrar_stock, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_TEXTO_SEC, hover_color="#6c757d").pack(side="left", padx=10)

    # ============================================================================
    # VISTA: CLIENTES
    # ============================================================================
    def mostrar_clientes():
        limpiar_contenido()
        actualizar_titulo_header("👥 Gestión de Clientes")
        
        ctk.CTkButton(contenedor_principal, text="➕ Agregar Cliente", command=mostrar_form_cliente,
                     height=45, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, hover_color=COLOR_ROJO_HOVER).pack(anchor="e", pady=(0, 15))
        
        try:
            clientes = procedimientos.sp_listar_clientes_empresa(id_empresa)
            if not clientes:
                ctk.CTkLabel(contenedor_principal, text="No hay clientes registrados", font=("Arial", 16), text_color=COLOR_TEXTO_SEC).pack(pady=50)
                return

            frame_tabla = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=10)
            frame_tabla.pack(fill="both", expand=True, pady=10)

            headers = ["ID", "Nombre", "Apellido", "Ubicación", "Tipo Doc", "N° Documento"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(frame_tabla, text=header, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, corner_radius=5, width=150).grid(row=0, column=i, padx=5, pady=10, sticky="ew")

            for idx, cliente in enumerate(clientes, start=1):
                color_fila = COLOR_SIDEBAR if idx % 2 == 0 else "transparent"
                for i, dato in enumerate(cliente):
                    ctk.CTkLabel(frame_tabla, text=str(dato), font=("Arial", 11), fg_color=color_fila, width=150).grid(row=idx, column=i, padx=5, pady=5, sticky="ew")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # ============================================================================
    # FORMULARIO: CREAR CLIENTE
    # ============================================================================
    def mostrar_form_cliente():
        limpiar_contenido()
        actualizar_titulo_header("👥 Registrar Nuevo Cliente")
        
        frame_form = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=15, border_width=2, border_color=COLOR_ROJO)
        frame_form.pack(fill="both", expand=True, padx=50, pady=30)
        
        ctk.CTkLabel(frame_form, text="Complete los datos del cliente", font=("Arial", 16, "bold"), text_color=COLOR_TEXTO).pack(pady=20)
        
        entry_nombre = crear_campo_form(frame_form, "Nombre *", "Nombre del cliente")
        entry_apellido = crear_campo_form(frame_form, "Apellido *", "Apellido del cliente")
        entry_direccion = crear_campo_form(frame_form, "Dirección/Ubicación *", "Av. Principal 123")
        
        tipo_doc = crear_campo_form(frame_form, "Tipo de Documento *", tipo="option", opciones=["DNI", "RUC", "Carnet de Extranjería", "Pasaporte"])
        entry_num_doc = crear_campo_form(frame_form, "Número de Documento *", "00000000")
        
        def guardar_cliente():
            try:
                nombre = entry_nombre.get()
                apellido = entry_apellido.get()
                direccion = entry_direccion.get()
                tipo_ident = tipo_doc.get()
                num_doc = entry_num_doc.get()
                
                if not all([nombre, apellido, direccion, num_doc]):
                    messagebox.showwarning("Campos vacíos", "Complete todos los campos")
                    return
                
                # Insertar ubicación
                id_ubicacion = procedimientos.sp_insertar_ubicacion(direccion)
                # Insertar identidad
                id_identidad = procedimientos.sp_insertar_identidad(tipo_ident, num_doc)
                # Insertar cliente
                id_cliente = procedimientos.sp_insertar_cliente(nombre, apellido, id_ubicacion, id_identidad)
                
                messagebox.showinfo("Éxito", f"Cliente registrado con ID: {id_cliente}")
                mostrar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botones.pack(pady=30)
        ctk.CTkButton(frame_botones, text="💾 Guardar Cliente", command=guardar_cliente, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_SUCCESS, hover_color="#1e7e34").pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="❌ Cancelar", command=mostrar_clientes, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_TEXTO_SEC, hover_color="#6c757d").pack(side="left", padx=10)

    # ============================================================================
    # VISTA: GUÍAS
    # ============================================================================
    def mostrar_guias():
        limpiar_contenido()
        actualizar_titulo_header("🚚 Guías de Remisión")
        
        ctk.CTkButton(contenedor_principal, text="➕ Crear Guía", command=mostrar_form_guia,
                     height=45, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, hover_color=COLOR_ROJO_HOVER).pack(anchor="e", pady=(0, 15))
        
        try:
            guias = procedimientos.sp_listar_guias_empresa(id_empresa)
            if not guias:
                ctk.CTkLabel(contenedor_principal, text="No hay guías registradas", font=("Arial", 16), text_color=COLOR_TEXTO_SEC).pack(pady=50)
                return

            frame_tabla = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=10)
            frame_tabla.pack(fill="both", expand=True, pady=10)

            headers = ["N° Guía", "Emisión", "Traslado", "Conductor", "Vehículo", "Estado"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(frame_tabla, text=header, font=("Arial", 13, "bold"), fg_color=COLOR_ROJO, corner_radius=5, width=150).grid(row=0, column=i, padx=5, pady=10, sticky="ew")

            for idx, guia in enumerate(guias, start=1):
                datos = [guia[1], guia[2], guia[3], guia[7], guia[8], guia[9]]
                color_fila = COLOR_SIDEBAR if idx % 2 == 0 else "transparent"
                for i, dato in enumerate(datos):
                    ctk.CTkLabel(frame_tabla, text=str(dato), font=("Arial", 11), fg_color=color_fila, width=150).grid(row=idx, column=i, padx=5, pady=5, sticky="ew")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # ============================================================================
    # FORMULARIO: CREAR GUÍA
    # ============================================================================
    def mostrar_form_guia():
        limpiar_contenido()
        actualizar_titulo_header("🚚 Crear Guía de Remisión")
        
        frame_form = ctk.CTkFrame(contenedor_principal, fg_color=COLOR_CARD, corner_radius=15, border_width=2, border_color=COLOR_ROJO)
        frame_form.pack(fill="both", expand=True, padx=50, pady=30)
        
        ctk.CTkLabel(frame_form, text="Datos de la Guía de Remisión", font=("Arial", 16, "bold"), text_color=COLOR_TEXTO).pack(pady=20)
        
        entry_nro_guia = crear_campo_form(frame_form, "Número de Guía *", "GR-0001")
        entry_motivo = crear_campo_form(frame_form, "Motivo de Traslado *", "Entrega de productos")
        entry_dir_partida = crear_campo_form(frame_form, "Dirección de Partida *", "Av. Principal 123")
        entry_dir_llegada = crear_campo_form(frame_form, "Dirección de Llegada *", "Calle Secundaria 456")
        
        # Aquí deberías cargar conductores y vehículos reales de tu BD
        entry_conductor = crear_campo_form(frame_form, "Nombre del Conductor *", "Juan Pérez")
        entry_licencia = crear_campo_form(frame_form, "N° Licencia *", "B12345678")
        entry_vehiculo = crear_campo_form(frame_form, "Descripción Vehículo *", "Camioneta Toyota")
        entry_placa = crear_campo_form(frame_form, "Placa *", "ABC-123")
        
        def guardar_guia():
            try:
                nro_guia = entry_nro_guia.get()
                motivo = entry_motivo.get()
                dir_partida = entry_dir_partida.get()
                dir_llegada = entry_dir_llegada.get()
                conductor_nombre = entry_conductor.get()
                licencia = entry_licencia.get()
                vehiculo_desc = entry_vehiculo.get()
                placa = entry_placa.get()
                
                if not all([nro_guia, motivo, dir_partida, dir_llegada, conductor_nombre, licencia, vehiculo_desc, placa]):
                    messagebox.showwarning("Campos vacíos", "Complete todos los campos")
                    return
                
                # Insertar conductor y vehículo
                id_conductor = procedimientos.sp_insertar_conductor(conductor_nombre, licencia)
                id_vehiculo = procedimientos.sp_insertar_vehiculo(vehiculo_desc, placa)
                
                # Para la guía necesitas un id_doc_venta (deberías seleccionarlo de documentos existentes)
                # Por ahora usamos 1 como ejemplo
                fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                
                id_guia = procedimientos.sp_insertar_encabezado_guia(
                    1, nro_guia, fecha_hoy, fecha_hoy,
                    motivo, dir_partida, dir_llegada,
                    id_conductor, id_vehiculo
                )
                
                messagebox.showinfo("Éxito", f"Guía creada con ID: {id_guia}")
                mostrar_guias()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botones.pack(pady=30)
        ctk.CTkButton(frame_botones, text="💾 Guardar Guía", command=guardar_guia, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_SUCCESS, hover_color="#1e7e34").pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="❌ Cancelar", command=mostrar_guias, width=200, height=50,
                     font=("Arial", 14, "bold"), fg_color=COLOR_TEXTO_SEC, hover_color="#6c757d").pack(side="left", padx=10)

    # ============================================================================
    # MENÚS DEL SIDEBAR
    # ============================================================================
    def crear_menu_item(parent, texto, icono, comando, es_activo=False):
        ctk.CTkButton(parent, text=f"  {icono}  {texto}", command=comando, height=50, corner_radius=10,
                     fg_color=COLOR_ROJO if es_activo else "transparent", hover_color=COLOR_ROJO,
                     text_color=COLOR_TEXTO, font=("Arial", 13, "bold"), anchor="w", border_spacing=10).pack(fill="x", padx=15, pady=5)

    crear_menu_item(sidebar_scroll, "Dashboard", "🎯", mostrar_dashboard, True)
    crear_menu_item(sidebar_scroll, "Inventario", "📦", mostrar_stock)
    crear_menu_item(sidebar_scroll, "Clientes", "👥", mostrar_clientes)
    crear_menu_item(sidebar_scroll, "Guías de Remisión", "🚚", mostrar_guias)

    ctk.CTkFrame(sidebar, height=2, fg_color="#3a3a3a").pack(fill="x", padx=20, pady=20)

    def cerrar_sesion():
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar sesión?", parent=ventana):
            ventana.destroy()
            from vista.login import crear_ventana_login
            ventana_login = crear_ventana_login()
            ventana_login.mainloop()

    ctk.CTkButton(sidebar, text="  🚪  Cerrar Sesión", command=cerrar_sesion, height=50, corner_radius=10,
                 fg_color="transparent", hover_color=COLOR_ROJO_HOVER, text_color=COLOR_TEXTO,
                 font=("Arial", 13, "bold"), anchor="w", border_spacing=10).pack(fill="x", padx=15, pady=(0, 20))

    mostrar_dashboard()
    ventana.mainloop()

if __name__ == "__main__":
    abrir_dashboard("Librería Test", 1)