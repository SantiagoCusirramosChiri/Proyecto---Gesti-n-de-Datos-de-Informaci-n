# inventario_stock.py

import customtkinter as ctk
from tkinter import messagebox
from datos import procedimientos
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ADVERTENCIA,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    obtener_color_stock
)


# Muestra interfaz de control de stock con búsqueda y acciones
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="📦 Control de Stock",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_stock(frame_lista, entry_buscar),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_actualizar.pack(side="right", padx=5)
    
    frame_busqueda = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_busqueda.pack(fill="x", pady=(0, 15))
    
    label_buscar = ctk.CTkLabel(
        frame_busqueda,
        text="🔍 Buscar:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda,
        placeholder_text="Buscar por nombre de producto...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_stock(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_stock(frame_lista, entry_buscar)


# Carga y muestra tabla de productos con niveles de stock
def cargar_stock(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_productos_activos()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="📦 No hay productos en inventario",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Nombre', 'Descripción', 'Precio', 'Stock', 'Unidad', 'Estado', 'Acciones'],
            [50, 180, 250, 80, 80, 70, 100, 200]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for producto in resultado:
            id_producto = producto[0]
            nombre = producto[1]
            descripcion = producto[2]
            precio_base = producto[3]
            stock = producto[4]
            unidad_medida = producto[5]
            
            if termino_busqueda:
                if termino_busqueda not in nombre.lower():
                    continue
            
            color_stock = obtener_color_stock(stock)
            
            if stock <= 0:
                estado_stock = "❌ Agotado"
            elif stock <= 25:
                estado_stock = "⚠️ Bajo"
            else:
                estado_stock = "✅ Normal"
            
            frame_fila = tabla.agregar_fila([
                id_producto,
                nombre,
                descripcion,
                f"S/ {precio_base:.2f}",
                stock,
                unidad_medida,
                estado_stock
            ])
            
            botones = [
                ('➕ Entrada', lambda p=producto: ajustar_stock_dialog(p, 'ENTRADA', frame_lista, entry_buscar)),
                ('➖ Salida', lambda p=producto: ajustar_stock_dialog(p, 'SALIDA', frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar stock:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de productos
def filtrar_stock(frame_lista, entry_buscar):
    cargar_stock(frame_lista, entry_buscar)


# Abre ventana modal para ajustar stock mediante entrada o salida
def ajustar_stock_dialog(producto, tipo_movimiento, frame_lista, entry_buscar):
    id_producto = producto[0]
    nombre = producto[1]
    stock_actual = producto[4]
    
    ventana = ctk.CTkToplevel()
    ventana.title(f"{'➕ Entrada' if tipo_movimiento == 'ENTRADA' else '➖ Salida'} de Stock")
    ventana.geometry("450x350")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana, 450, 350)
    
    frame = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame,
        text=f"{'➕ Entrada' if tipo_movimiento == 'ENTRADA' else '➖ Salida'} de Stock",
        font=("Arial Black", 18, "bold"),
        text_color=COLOR_EXITO if tipo_movimiento == 'ENTRADA' else COLOR_ADVERTENCIA
    )
    label_titulo.pack(pady=(20, 10))
    
    label_producto = ctk.CTkLabel(
        frame,
        text=f"Producto: {nombre}",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO
    )
    label_producto.pack(pady=5)
    
    label_stock_actual = ctk.CTkLabel(
        frame,
        text=f"Stock actual: {stock_actual}",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_stock_actual.pack(pady=(0, 20))
    
    label_cantidad = ctk.CTkLabel(
        frame,
        text="Cantidad:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_cantidad.pack(fill="x", padx=40, pady=(0, 5))
    
    entry_cantidad = ctk.CTkEntry(
        frame,
        placeholder_text="Ingrese cantidad",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_cantidad.pack(fill="x", padx=40, pady=(0, 30))
    entry_cantidad.focus()
    
    def guardar():
        cantidad_str = entry_cantidad.get().strip()
        
        if not cantidad_str:
            messagebox.showerror("Error", "Ingrese una cantidad", parent=ventana)
            return
        
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0", parent=ventana)
                return
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido", parent=ventana)
            return
        
        try:
            procedimientos.ajustar_stock_producto(id_producto, cantidad, tipo_movimiento)
            messagebox.showinfo("✅ Éxito", f"Stock {'aumentado' if tipo_movimiento == 'ENTRADA' else 'reducido'} correctamente", parent=ventana)
            ventana.destroy()
            cargar_stock(frame_lista, entry_buscar)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana)
    
    frame_botones = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana.destroy,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO,
        text_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY,
        height=40,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Guardar",
        command=guardar,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO if tipo_movimiento == 'ENTRADA' else COLOR_ADVERTENCIA,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    entry_cantidad.bind("<Return>", lambda e: guardar())


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")