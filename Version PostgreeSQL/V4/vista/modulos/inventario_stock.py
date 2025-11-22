# vista/modulos/inventario_stock.py

import customtkinter as ctk
from tkinter import messagebox
from logica.StockBL import StockBL
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ADVERTENCIA,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_INFO,
    COLOR_INFO_HOVER,
    obtener_color_stock
)


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de control de stock con búsqueda y acciones"""
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
    
    label_contador = ctk.CTkLabel(
        frame_header,
        text="",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_contador.pack(side="left", padx=20)
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_stock(frame_lista, entry_buscar, label_contador),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_INFO,
        hover_color=COLOR_INFO_HOVER,
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
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_stock(frame_lista, entry_buscar, label_contador))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_stock(frame_lista, entry_buscar, label_contador)


def cargar_stock(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de productos con niveles de stock"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            productos = StockBL.buscar_productos_stock(termino_busqueda)
        else:
            productos = StockBL.obtener_productos_con_stock()
        
        if label_contador:
            if productos:
                total = len(productos)
                agotados = sum(1 for p in productos if p['nivel_stock'] == 'AGOTADO')
                bajo = sum(1 for p in productos if p['nivel_stock'] == 'BAJO')
                
                texto = f"({total} productos"
                if agotados > 0:
                    texto += f", {agotados} agotados"
                if bajo > 0:
                    texto += f", {bajo} con stock bajo"
                texto += ")"
                
                label_contador.configure(text=texto)
            else:
                label_contador.configure(text="(0 productos)")
        
        if not productos or len(productos) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "📦 No hay productos en inventario"
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text=mensaje,
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
        
        for producto in productos:
            nivel = producto['nivel_stock']
            if nivel == 'AGOTADO':
                estado_stock = "❌ Agotado"
            elif nivel == 'BAJO':
                estado_stock = "⚠️ Bajo"
            else:
                estado_stock = "✅ Normal"
            
            frame_fila = tabla.agregar_fila([
                producto['id_producto'],
                producto['nombre'],
                producto['descripcion'],
                f"S/ {producto['precio_base']:.2f}",
                producto['stock'],
                producto['unidad_medida'],
                estado_stock
            ])
            
            def crear_funcion_entrada(p):
                return lambda: ajustar_stock_dialog(p, 'ENTRADA', frame_lista, entry_buscar, label_contador)
            
            def crear_funcion_salida(p):
                return lambda: ajustar_stock_dialog(p, 'SALIDA', frame_lista, entry_buscar, label_contador)
            
            botones = [
                ('➕ Entrada', crear_funcion_entrada(producto)),
                ('➖ Salida', crear_funcion_salida(producto))
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
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_stock(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de productos"""
    cargar_stock(frame_lista, entry_buscar, label_contador)


def ajustar_stock_dialog(producto, tipo_movimiento, frame_lista, entry_buscar=None, label_contador=None):
    """Abre ventana modal para ajustar stock mediante entrada o salida"""
    id_producto = producto['id_producto']
    nombre = producto['nombre']
    stock_actual = producto['stock']
    
    ventana = ctk.CTkToplevel()
    ventana.title(f"{'➕ Entrada' if tipo_movimiento == 'ENTRADA' else '➖ Salida'} de Stock")
    ventana.geometry("450x380")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana, 450, 380)
    
    frame = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
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
        text="Cantidad *",
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
    entry_cantidad.pack(fill="x", padx=40, pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame,
        text=f"💡 {'Aumentará' if tipo_movimiento == 'ENTRADA' else 'Reducirá'} el stock del producto.",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_ayuda.pack(fill="x", padx=40, pady=(0, 30))
    
    entry_cantidad.focus()
    
    def guardar():
        """Valida y guarda el ajuste de stock"""
        cantidad_str = entry_cantidad.get()
        
        valido, mensaje, cantidad = StockBL.validar_cantidad(cantidad_str)
        if not valido:
            messagebox.showerror("Error", mensaje, parent=ventana)
            entry_cantidad.focus()
            return
        
        if tipo_movimiento == 'SALIDA':
            suficiente, mensaje_stock = StockBL.validar_stock_suficiente(id_producto, cantidad)
            if not suficiente:
                messagebox.showerror("Error", mensaje_stock, parent=ventana)
                return
        
        btn_guardar.configure(text="Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana.update()
        
        try:
            exito, mensaje = StockBL.ajustar_stock(id_producto, cantidad, tipo_movimiento)
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana)
                ventana.destroy()
                
                cargar_stock(frame_lista, entry_buscar, label_contador)
            else:
                messagebox.showerror("❌ Error", mensaje, parent=ventana)
                btn_guardar.configure(text="💾 Guardar", state="normal")
                btn_cancelar.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana)
            btn_guardar.configure(text="💾 Guardar", state="normal")
            btn_cancelar.configure(state="normal")
            print(f"❌ Error al guardar: {e}")
            import traceback
            traceback.print_exc()
    
    frame_botones = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana.destroy,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        border_width=2,
        border_color=COLOR_ERROR,
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
    ventana.bind("<Escape>", lambda e: ventana.destroy())


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")