# documentos_crear.py

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from decimal import Decimal
from datos import procedimientos
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra pantalla principal para crear documentos de venta
def mostrar(frame_contenido, id_empresa):
    if isinstance(id_empresa, (tuple, list)):
        for item in id_empresa:
            if isinstance(item, int):
                id_empresa = item
                break
        else:
            try:
                id_empresa = int(id_empresa[1]) if len(id_empresa) > 1 else int(id_empresa[0])
            except (ValueError, IndexError, TypeError):
                messagebox.showerror("Error", "ID de empresa inválido")
                return
    
    try:
        id_empresa = int(id_empresa)
    except (ValueError, TypeError):
        messagebox.showerror("Error", f"ID de empresa inválido: {id_empresa}")
        return
    
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="📄 Crear Documentos",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 30))
    
    frame_info = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=2,
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
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nuevo Documento",
        command=lambda: abrir_formulario_documento(frame_principal, id_empresa),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=250,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


# Abre ventana modal para crear documento de venta
def abrir_formulario_documento(frame_principal, id_empresa):
    carrito_productos = []
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Crear Nuevo Documento")
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
        text="📄 Crear Nuevo Documento",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=30)
    
    frame_row1 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row1.pack(fill="x", pady=(0, 15))
    
    frame_tipo = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_tipo.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_tipo = ctk.CTkLabel(
        frame_tipo,
        text="Tipo de Documento:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_tipo.pack(fill="x", pady=(0, 5))
    
    combo_tipo = ctk.CTkComboBox(
        frame_tipo,
        values=["Boleta", "Factura"],
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_tipo.pack(fill="x")
    combo_tipo.set("Boleta")
    
    frame_fecha = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_fecha.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_fecha = ctk.CTkLabel(
        frame_fecha,
        text="Fecha de Emisión:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_fecha.pack(fill="x", pady=(0, 5))
    
    entry_fecha = ctk.CTkEntry(
        frame_fecha,
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_fecha.pack(fill="x")
    entry_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    label_cliente = ctk.CTkLabel(
        frame_campos,
        text="Cliente:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_cliente.pack(fill="x", pady=(10, 5))
    
    clientes = procedimientos.obtener_clientes_combo()
    clientes_dict = {f"{c[1]} {c[2]}": c[0] for c in clientes}
    clientes_lista = list(clientes_dict.keys())
    
    combo_cliente = ctk.CTkComboBox(
        frame_campos,
        values=clientes_lista if clientes_lista else ["No hay clientes"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_cliente.pack(fill="x", pady=(0, 15))
    if clientes_lista:
        combo_cliente.set(clientes_lista[0])
    
    frame_row2 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row2.pack(fill="x", pady=(0, 15))
    
    frame_forma_pago = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_forma_pago.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_forma_pago = ctk.CTkLabel(
        frame_forma_pago,
        text="Forma de Pago:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_forma_pago.pack(fill="x", pady=(0, 5))
    
    formas_pago = procedimientos.obtener_formas_pago_combo()
    formas_pago_dict = {f"{fp[1]}": fp[0] for fp in formas_pago}
    formas_pago_lista = list(formas_pago_dict.keys())
    
    combo_forma_pago = ctk.CTkComboBox(
        frame_forma_pago,
        values=formas_pago_lista if formas_pago_lista else ["No hay formas de pago"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_forma_pago.pack(fill="x")
    if formas_pago_lista:
        combo_forma_pago.set(formas_pago_lista[0])
    
    frame_moneda = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_moneda.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_moneda = ctk.CTkLabel(
        frame_moneda,
        text="Moneda:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_moneda.pack(fill="x", pady=(0, 5))
    
    monedas = procedimientos.obtener_monedas_combo()
    monedas_dict = {f"{m[1]} - {m[2]}": m[0] for m in monedas}
    monedas_lista = list(monedas_dict.keys())
    
    combo_moneda = ctk.CTkComboBox(
        frame_moneda,
        values=monedas_lista if monedas_lista else ["No hay monedas"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_moneda.pack(fill="x")
    if monedas_lista:
        combo_moneda.set(monedas_lista[0])
    
    frame_separador = ctk.CTkFrame(frame_campos, height=2, fg_color=COLOR_BORDE)
    frame_separador.pack(fill="x", pady=20)
    
    label_productos = ctk.CTkLabel(
        frame_campos,
        text="🛒 Agregar Productos",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_productos.pack(fill="x", pady=(0, 15))
    
    frame_add_producto = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_add_producto.pack(fill="x", pady=(0, 20))
    
    productos = procedimientos.obtener_productos_combo()
    productos_dict = {f"{p[1]} (Stock: {p[3]})": (p[0], p[2], p[3]) for p in productos}
    productos_lista = list(productos_dict.keys())
    
    combo_producto = ctk.CTkComboBox(
        frame_add_producto,
        values=productos_lista if productos_lista else ["No hay productos"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        width=400
    )
    combo_producto.pack(side="left", padx=(0, 10))
    if productos_lista:
        combo_producto.set(productos_lista[0])
    
    entry_cantidad = ctk.CTkEntry(
        frame_add_producto,
        placeholder_text="Cantidad",
        height=40,
        width=100,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_cantidad.pack(side="left", padx=(0, 10))
    entry_cantidad.insert(0, "1")
    
    frame_carrito = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_carrito.pack(fill="both", expand=True)
    
    # Agrega producto seleccionado al carrito
    def agregar_al_carrito():
        producto_seleccionado = combo_producto.get()
        cantidad_str = entry_cantidad.get().strip()
        
        if not productos_lista:
            messagebox.showerror("Error", "No hay productos disponibles", parent=ventana_form)
            return
        
        if not cantidad_str or not cantidad_str.isdigit():
            messagebox.showerror("Error", "Ingrese una cantidad válida", parent=ventana_form)
            return
        
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0", parent=ventana_form)
            return
        
        producto_info = productos_dict.get(producto_seleccionado)
        id_producto, precio, stock = producto_info
        
        precio_float = float(precio) if isinstance(precio, Decimal) else precio
        
        if cantidad > stock:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock}", parent=ventana_form)
            return
        
        for item in carrito_productos:
            if item['id'] == id_producto:
                item['cantidad'] += cantidad
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
    
    btn_agregar = ctk.CTkButton(
        frame_add_producto,
        text="➕ Agregar",
        command=agregar_al_carrito,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        width=120,
        corner_radius=10
    )
    btn_agregar.pack(side="left")
    
    actualizar_carrito(frame_carrito, carrito_productos)
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=30, pady=(20, 20))
    
    # Valida y guarda documento con sus detalles
    def guardar_documento():
        if not clientes_lista or not formas_pago_lista or not monedas_lista:
            messagebox.showerror("Error", "Faltan datos maestros", parent=ventana_form)
            return
        
        if len(carrito_productos) == 0:
            messagebox.showerror("Error", "Debe agregar al menos un producto", parent=ventana_form)
            return
        
        try:
            tipo_doc = combo_tipo.get()
            fecha = entry_fecha.get()
            id_cliente = clientes_dict[combo_cliente.get()]
            id_forma_pago = formas_pago_dict[combo_forma_pago.get()]
            id_moneda = monedas_dict[combo_moneda.get()]
            
            id_empresa_int = id_empresa
            if isinstance(id_empresa_int, (tuple, list)):
                for item in id_empresa_int:
                    if isinstance(item, int):
                        id_empresa_int = item
                        break
                else:
                    try:
                        id_empresa_int = int(id_empresa_int[1]) if len(id_empresa_int) > 1 else int(id_empresa_int[0])
                    except (ValueError, IndexError, TypeError):
                        raise ValueError(f"ID de empresa inválido: {id_empresa}")
            
            id_empresa_int = int(id_empresa_int)
            
            id_documento = procedimientos.sp_insertar_encabezado_documento(
                tipo_doc, fecha, id_empresa_int, id_cliente, id_forma_pago, id_moneda
            )
            
            for item in carrito_productos:
                id_producto = item['id']
                cantidad = int(item['cantidad'])
                precio = float(item['precio'])
                
                subtotal = round(cantidad * precio, 2)
                igv = round(subtotal * 0.18, 2)
                importe = round(subtotal + igv, 2)
                
                print(f"📊 Insertando detalle: Producto {id_producto}, Cant: {cantidad}, "
                      f"Subtotal: {subtotal}, IGV: {igv}, Importe: {importe}")
                
                procedimientos.sp_insertar_detalle_documento(
                    id_documento, id_producto, cantidad, subtotal, igv, importe
                )
            
            messagebox.showinfo("✅ Éxito", 
                f"Documento N° {id_documento} creado correctamente\n\nEstado: PENDIENTE",
                parent=ventana_form)
            
            ventana_form.destroy()
            
        except Exception as e:
            import traceback
            error_detallado = traceback.format_exc()
            print(f"❌ ERROR COMPLETO:\n{error_detallado}")
            messagebox.showerror("❌ Error", f"Error al crear documento:\n{str(e)}", parent=ventana_form)
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana_form.destroy,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO,
        text_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY,
        height=50,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Crear Documento",
        command=guardar_documento,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))


# Actualiza visualización del carrito de productos
def actualizar_carrito(frame_carrito, carrito_productos):
    for widget in frame_carrito.winfo_children():
        widget.destroy()
    
    if len(carrito_productos) == 0:
        label_vacio = ctk.CTkLabel(
            frame_carrito,
            text="🛒 Carrito vacío",
            font=("Arial", 14),
            text_color=COLOR_TEXTO_SECUNDARIO
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
    
    total_general = 0
    
    for i, item in enumerate(carrito_productos):
        precio = float(item['precio'])
        cantidad = int(item['cantidad'])
        subtotal = precio * cantidad
        total_general += subtotal
        
        frame_item = ctk.CTkFrame(frame_lista, fg_color=COLOR_FONDO_SECUNDARIO, corner_radius=8)
        frame_item.pack(fill="x", padx=5, pady=5)
        
        label_producto = ctk.CTkLabel(
            frame_item,
            text=f"{item['nombre']} x{cantidad}",
            font=("Arial", 12, "bold"),
            text_color=COLOR_TEXTO,
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


# Elimina un producto del carrito
def eliminar_del_carrito(indice, frame_carrito, carrito_productos):
    carrito_productos.pop(indice)
    actualizar_carrito(frame_carrito, carrito_productos)


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")