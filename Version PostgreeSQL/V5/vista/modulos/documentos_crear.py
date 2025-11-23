# vista/modulos/documentos_crear.py

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from logica.DocumentoBL import DocumentoBL
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


def mostrar(frame_contenido, id_empresa):
    id_valido, mensaje, id_empresa_norm = DocumentoBL.validar_id_empresa(id_empresa)
    if not id_valido:
        messagebox.showerror("Error", mensaje)
        return
    
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="📄 Crear Comprobante de Venta",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 30))
    
    frame_info = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="both", expand=True, padx=100, pady=50)
    
    label_icono = ctk.CTkLabel(
        frame_info,
        text="📄",
        font=("Arial", 100)
    )
    label_icono.pack(pady=(50, 20))
    
    label_descripcion = ctk.CTkLabel(
        frame_info,
        text="Cree boletas y facturas de venta",
        font=("Arial", 16),
        text_color="#666666"
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nuevo Documento",
        command=lambda: abrir_formulario_documento(frame_principal, id_empresa_norm),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=250,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


def abrir_formulario_documento(frame_principal, id_empresa):
    carrito_productos = []
    
    # ============= CONTROL DE CAMBIOS =============
    cambios_realizados = {'hubo_cambios': False}
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Crear Nuevo Comprobante")
    ventana_form.geometry("800x900")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 800, 900)
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="📄 Crear Nuevo Comprobante",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=30)
    
    # ============= FUNCIÓN PARA REGISTRAR CAMBIOS =============
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True
    
    # ============= FILA 1: TIPO Y FECHA =============
    frame_row1 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row1.pack(fill="x", pady=(0, 15))
    
    # Tipo de Documento
    frame_tipo = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_tipo.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_tipo = ctk.CTkLabel(
        frame_tipo,
        text="Tipo de Comprobante *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_tipo.pack(fill="x", pady=(0, 5))
    
    combo_tipo = ctk.CTkComboBox(
        frame_tipo,
        values=DocumentoBL.TIPOS_DOCUMENTO,
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_tipo.pack(fill="x")
    combo_tipo.set("Boleta")
    combo_tipo.bind("<<ComboboxSelected>>", registrar_cambio)
    
    # Fecha de Emisión
    frame_fecha = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_fecha.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_fecha = ctk.CTkLabel(
        frame_fecha,
        text="Fecha de Emisión *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_fecha.pack(fill="x", pady=(0, 5))
    
    entry_fecha = ctk.CTkEntry(
        frame_fecha,
        placeholder_text="YYYY-MM-DD",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_fecha.pack(fill="x")
    entry_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))
    entry_fecha.bind("<KeyRelease>", registrar_cambio)
    
    # ============= CLIENTE =============
    label_cliente = ctk.CTkLabel(
        frame_campos,
        text="Cliente *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_cliente.pack(fill="x", pady=(10, 5))
    
    clientes = DocumentoBL.obtener_clientes_combo()
    clientes_dict = {f"{c[1]} {c[2]}": c[0] for c in clientes}
    clientes_lista = list(clientes_dict.keys())
    
    combo_cliente = ctk.CTkComboBox(
        frame_campos,
        values=clientes_lista if clientes_lista else ["No hay clientes"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_cliente.pack(fill="x", pady=(0, 15))
    if clientes_lista:
        combo_cliente.set(clientes_lista[0])
    combo_cliente.bind("<<ComboboxSelected>>", registrar_cambio)
    
    # ============= FILA 2: FORMA DE PAGO Y MONEDA =============
    frame_row2 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row2.pack(fill="x", pady=(0, 15))
    
    # Forma de Pago
    frame_forma_pago = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_forma_pago.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_forma_pago = ctk.CTkLabel(
        frame_forma_pago,
        text="Forma de Pago *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_forma_pago.pack(fill="x", pady=(0, 5))
    
    formas_pago = DocumentoBL.obtener_formas_pago_combo()
    formas_pago_dict = {fp[1]: fp[0] for fp in formas_pago}
    formas_pago_lista = list(formas_pago_dict.keys())
    
    combo_forma_pago = ctk.CTkComboBox(
        frame_forma_pago,
        values=formas_pago_lista if formas_pago_lista else ["No hay formas de pago"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_forma_pago.pack(fill="x")
    if formas_pago_lista:
        combo_forma_pago.set(formas_pago_lista[0])
    combo_forma_pago.bind("<<ComboboxSelected>>", registrar_cambio)
    
    # Moneda
    frame_moneda = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_moneda.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_moneda = ctk.CTkLabel(
        frame_moneda,
        text="Moneda *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_moneda.pack(fill="x", pady=(0, 5))
    
    monedas = DocumentoBL.obtener_monedas_combo()
    monedas_dict = {f"{m[1]} ({m[2]})": m[0] for m in monedas}
    monedas_lista = list(monedas_dict.keys())
    
    combo_moneda = ctk.CTkComboBox(
        frame_moneda,
        values=monedas_lista if monedas_lista else ["No hay monedas"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_moneda.pack(fill="x")
    if monedas_lista:
        combo_moneda.set(monedas_lista[0])
    combo_moneda.bind("<<ComboboxSelected>>", registrar_cambio)
    
    # ============= AGREGAR PRODUCTOS =============
    label_productos = ctk.CTkLabel(
        frame_campos,
        text="Agregar Productos *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_productos.pack(fill="x", pady=(20, 5))
    
    frame_agregar = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_agregar.pack(fill="x", pady=(0, 15))
    
    productos = DocumentoBL.obtener_productos_combo()
    productos_dict = {f"{p[1]} (Stock: {p[3]})": (p[0], p[2], p[3]) for p in productos}
    productos_lista = list(productos_dict.keys())
    
    combo_producto = ctk.CTkComboBox(
        frame_agregar,
        values=productos_lista if productos_lista else ["No hay productos"],
        width=400,
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_producto.pack(side="left", padx=(0, 10))
    if productos_lista:
        combo_producto.set(productos_lista[0])
    
    entry_cantidad = ctk.CTkEntry(
        frame_agregar,
        placeholder_text="Cant.",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        width=80,
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_cantidad.pack(side="left", padx=(0, 10))
    entry_cantidad.insert(0, "1")
    
    def agregar_producto_wrapper():
        agregar_producto_al_carrito(
            combo_producto, entry_cantidad, productos_dict, productos_lista,
            carrito_productos, frame_carrito, ventana_form
        )
        cambios_realizados['hubo_cambios'] = True  # ✅ Marcar cambio al agregar producto
    
    btn_agregar = ctk.CTkButton(
        frame_agregar,
        text="➕ Agregar",
        command=agregar_producto_wrapper,
        width=120,
        height=40,
        font=("Arial", 11, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER
    )
    btn_agregar.pack(side="left")
    
    # ============= CARRITO =============
    label_carrito = ctk.CTkLabel(
        frame_campos,
        text="🛒 Carrito de Compras",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_carrito.pack(fill="x", pady=(20, 5))
    
    frame_carrito = ctk.CTkFrame(frame_campos, fg_color=COLOR_FONDO_TERCIARIO, corner_radius=10, height=300)
    frame_carrito.pack(fill="both", expand=True, pady=(0, 20))
    frame_carrito.pack_propagate(False)
    
    actualizar_carrito(frame_carrito, carrito_productos)
    
    # ============= FUNCIÓN GUARDAR CON CONFIRMACIÓN =============
    def guardar_con_confirmacion():
        """Valida, confirma y guarda el documento"""
        if not clientes_lista or not formas_pago_lista or not monedas_lista:
            messagebox.showerror("Error", "Faltan datos maestros (clientes, formas de pago o monedas)", parent=ventana_form)
            return
        
        carrito_valido, mensaje_carrito = DocumentoBL.validar_carrito(carrito_productos)
        if not carrito_valido:
            messagebox.showerror("Error", mensaje_carrito, parent=ventana_form)
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        tipo_doc = combo_tipo.get()
        cliente_nombre = combo_cliente.get()
        total_general = DocumentoBL.calcular_total_carrito(carrito_productos)
        
        respuesta = messagebox.askyesno(
            "Confirmar Creación",
            f"¿Está seguro que desea crear este documento?\n\n"
            f"📄 Tipo: {tipo_doc}\n"
            f"👤 Cliente: {cliente_nombre}\n"
            f"🛒 Productos: {len(carrito_productos)}\n"
            f"💰 Total: S/ {total_general:.2f}",
            parent=ventana_form
        )
        
        if not respuesta:
            return
        
        guardar_documento_completo(
            combo_tipo, entry_fecha, combo_cliente, combo_forma_pago,
            combo_moneda, clientes_dict, formas_pago_dict, monedas_dict,
            clientes_lista, formas_pago_lista, monedas_lista,
            carrito_productos, id_empresa, ventana_form
        )
    
    # ============= FUNCIÓN CANCELAR CON CONFIRMACIÓN =============
    def cancelar_con_confirmacion():
        """Solicita confirmación antes de cancelar si hay cambios"""
        if cambios_realizados['hubo_cambios'] or len(carrito_productos) > 0:
            respuesta = messagebox.askyesno(
                "Confirmar Cancelación",
                "¿Está seguro que desea cancelar?\n\nSe perderán todos los cambios realizados.",
                parent=ventana_form
            )
            if respuesta:
                ventana_form.destroy()
        else:
            ventana_form.destroy()
    
    # ============= BOTONES =============
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=30, pady=(20, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=cancelar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        border_width=2,
        border_color=COLOR_ERROR,
        height=50,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Crear Comprobante",
        command=guardar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    ventana_form.bind("<Escape>", lambda e: cancelar_con_confirmacion())


def agregar_producto_al_carrito(combo_producto, entry_cantidad, productos_dict, productos_lista,
                                carrito_productos, frame_carrito, ventana_form):
    producto_seleccionado = combo_producto.get()
    cantidad_str = entry_cantidad.get().strip()
    
    if not productos_lista:
        messagebox.showerror("Error", "No hay productos disponibles", parent=ventana_form)
        return
    
    if not cantidad_str or not cantidad_str.isdigit():
        messagebox.showerror("Error", "Ingrese una cantidad válida", parent=ventana_form)
        entry_cantidad.focus()
        return
    
    cantidad = int(cantidad_str)
    if cantidad <= 0:
        messagebox.showerror("Error", "La cantidad debe ser mayor a 0", parent=ventana_form)
        entry_cantidad.focus()
        return
    
    producto_info = productos_dict.get(producto_seleccionado)
    if not producto_info:
        messagebox.showerror("Error", "Producto no válido", parent=ventana_form)
        return
    
    id_producto, precio, stock = producto_info
    precio_float = float(precio)
    
    if cantidad > stock:
        messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock}", parent=ventana_form)
        return
    
    for item in carrito_productos:
        if item['id'] == id_producto:
            nuevo_total = item['cantidad'] + cantidad
            if nuevo_total > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock}", parent=ventana_form)
                return
            item['cantidad'] = nuevo_total
            actualizar_carrito(frame_carrito, carrito_productos)
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
            return
    
    carrito_productos.append({
        'id': id_producto,
        'nombre': producto_seleccionado.split(' (Stock:')[0],
        'cantidad': cantidad,
        'precio': precio_float
    })
    
    actualizar_carrito(frame_carrito, carrito_productos)
    entry_cantidad.delete(0, 'end')
    entry_cantidad.insert(0, "1")


def guardar_documento_completo(combo_tipo, entry_fecha, combo_cliente, combo_forma_pago,
                               combo_moneda, clientes_dict, formas_pago_dict, monedas_dict,
                               clientes_lista, formas_pago_lista, monedas_lista,
                               carrito_productos, id_empresa, ventana_form):
    try:
        tipo_doc = combo_tipo.get()
        fecha = entry_fecha.get()
        id_cliente = clientes_dict[combo_cliente.get()]
        id_forma_pago = formas_pago_dict[combo_forma_pago.get()]
        id_moneda = monedas_dict[combo_moneda.get()]
        
        exito, mensaje, id_documento = DocumentoBL.crear_documento_completo(
            tipo_doc, fecha, id_empresa, id_cliente, id_forma_pago,
            id_moneda, carrito_productos
        )
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
            ventana_form.destroy()
        else:
            messagebox.showerror("❌ Error", mensaje, parent=ventana_form)
        
    except Exception as e:
        import traceback
        error_detallado = traceback.format_exc()
        print(f"❌ ERROR COMPLETO:\n{error_detallado}")
        messagebox.showerror("❌ Error", f"Error al crear documento:\n{str(e)}", parent=ventana_form)


def actualizar_carrito(frame_carrito, carrito_productos):
    for widget in frame_carrito.winfo_children():
        widget.destroy()
    
    if len(carrito_productos) == 0:
        label_vacio = ctk.CTkLabel(
            frame_carrito,
            text="🛒 Carrito vacío",
            font=("Arial", 14),
            text_color="#666666"
        )
        label_vacio.pack(pady=30)
        return
    
    frame_lista = ctk.CTkScrollableFrame(
        frame_carrito,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=10,
        height=250
    )
    frame_lista.pack(fill="both", expand=True)
    
    total_general = DocumentoBL.calcular_total_carrito(carrito_productos)
    
    for i, item in enumerate(carrito_productos):
        precio = float(item['precio'])
        cantidad = int(item['cantidad'])
        subtotal = precio * cantidad
        
        frame_item = ctk.CTkFrame(frame_lista, fg_color=COLOR_FONDO_SECUNDARIO, corner_radius=8)
        frame_item.pack(fill="x", padx=5, pady=5)
        
        label_producto = ctk.CTkLabel(
            frame_item,
            text=f"{item['nombre']} x{cantidad}",
            font=("Arial", 12, "bold"),
            text_color="#2C2C2E",  # ✅ OSCURO
            anchor="w"
        )
        label_producto.pack(side="left", padx=15, pady=10)
        
        label_precio = ctk.CTkLabel(
            frame_item,
            text=f"S/ {subtotal:.2f}",
            font=("Arial", 12, "bold"),
            text_color=COLOR_EXITO
        )
        label_precio.pack(side="right", padx=15)
        
        btn_eliminar = ctk.CTkButton(
            frame_item,
            text="🗑️",
            command=lambda idx=i: eliminar_del_carrito(idx, frame_carrito, carrito_productos),
            width=40,
            height=30,
            font=("Arial", 12),
            fg_color=COLOR_ERROR,
            hover_color=COLOR_ERROR_HOVER,
            corner_radius=5
        )
        btn_eliminar.pack(side="right", padx=5)
    
    frame_total = ctk.CTkFrame(frame_carrito, fg_color="transparent")
    frame_total.pack(fill="x", pady=(10, 0))
    
    label_total = ctk.CTkLabel(
        frame_total,
        text=f"TOTAL: S/ {total_general:.2f}",
        font=("Arial Black", 16, "bold"),
        text_color=COLOR_EXITO
    )
    label_total.pack(side="right")


def eliminar_del_carrito(indice, frame_carrito, carrito_productos):
    carrito_productos.pop(indice)
    actualizar_carrito(frame_carrito, carrito_productos)


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")