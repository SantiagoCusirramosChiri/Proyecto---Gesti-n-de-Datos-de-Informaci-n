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
    COLOR_ADVERTENCIA_HOVER,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
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
    
    # ============= HEADER =============
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
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E"
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
    
    # ============= BARRA DE BÚSQUEDA =============
    frame_busqueda = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_busqueda.pack(fill="x", pady=(0, 15))
    
    frame_busqueda_inner = ctk.CTkFrame(frame_busqueda, fg_color="transparent")
    frame_busqueda_inner.pack(fill="x", padx=15, pady=12)
    
    label_buscar = ctk.CTkLabel(
        frame_busqueda_inner,
        text="🔍 Buscar:",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E"
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda_inner,
        placeholder_text="Buscar por nombre de producto...",
        placeholder_text_color="#2C2C2E",  # ✅ OSCURO
        width=450,
        height=38,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_buscar.pack(side="left", fill="x", expand=True)
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_stock(frame_lista, entry_buscar, label_contador))
    
    btn_limpiar = ctk.CTkButton(
        frame_busqueda_inner,
        text="✖️",
        command=lambda: limpiar_busqueda(entry_buscar, frame_lista, label_contador),
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        width=40,
        height=38,
        corner_radius=8,
        border_width=2,
        border_color=COLOR_BORDE
    )
    btn_limpiar.pack(side="left", padx=(10, 0))
    
    # ============= TABLA DE STOCK =============
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_stock(frame_lista, entry_buscar, label_contador)


def cargar_stock(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de productos con niveles de stock"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get().strip() if entry_buscar else ""
        
        if termino_busqueda:
            productos = StockBL.buscar_productos_stock(termino_busqueda)
        else:
            productos = StockBL.obtener_productos_con_stock()
        
        # ============= ACTUALIZAR CONTADOR =============
        if label_contador:
            if productos:
                total = len(productos)
                agotados = sum(1 for p in productos if p['nivel_stock'] == 'AGOTADO')
                bajo = sum(1 for p in productos if p['nivel_stock'] == 'BAJO')
                
                texto = f"({total} producto{'s' if total != 1 else ''}"
                if agotados > 0:
                    texto += f" • {agotados} agotado{'s' if agotados != 1 else ''}"
                if bajo > 0:
                    texto += f" • {bajo} con stock bajo"
                texto += ")"
                
                label_contador.configure(text=texto)
            else:
                label_contador.configure(text="(0 productos)")
        
        # ============= MENSAJE VACÍO =============
        if not productos or len(productos) == 0:
            frame_vacio = ctk.CTkFrame(
                frame_lista,
                fg_color=COLOR_FONDO_SECUNDARIO,
                corner_radius=15,
                border_width=1,
                border_color=COLOR_BORDE
            )
            frame_vacio.pack(fill="both", expand=True, padx=50, pady=50)
            
            icono = "🔍" if termino_busqueda else "📦"
            mensaje = "No se encontraron resultados" if termino_busqueda else "No hay productos en inventario"
            
            label_icono = ctk.CTkLabel(
                frame_vacio,
                text=icono,
                font=("Arial", 80)
            )
            label_icono.pack(pady=(50, 20))
            
            label_mensaje = ctk.CTkLabel(
                frame_vacio,
                text=mensaje,
                font=("Arial", 16),
                text_color="#666666"
            )
            label_mensaje.pack(pady=(0, 20))
            
            if termino_busqueda:
                label_sugerencia = ctk.CTkLabel(
                    frame_vacio,
                    text=f"Búsqueda: '{termino_busqueda}'",
                    font=("Arial", 12),
                    text_color="#666666"
                )
                label_sugerencia.pack(pady=(0, 50))
            else:
                label_placeholder = ctk.CTkLabel(
                    frame_vacio,
                    text="",
                    height=20
                )
                label_placeholder.pack(pady=(0, 50))
            
            return
        
        # ============= TABLA DE DATOS =============
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
            
            # ============= BOTONES DE ACCIÓN =============
            frame_acciones = ctk.CTkFrame(frame_fila, fg_color="transparent")
            frame_acciones.pack(side="right", padx=5)
            
            # Botón Entrada (VERDE - Aumenta stock)
            btn_entrada = ctk.CTkButton(
                frame_acciones,
                text="➕ Entrada",
                command=lambda p=producto: ajustar_stock_dialog(p, 'ENTRADA', frame_lista, entry_buscar, label_contador),
                font=("Arial", 10, "bold"),
                fg_color=COLOR_EXITO,
                hover_color=COLOR_EXITO_HOVER,
                width=85,
                height=30,
                corner_radius=6
            )
            btn_entrada.pack(side="left", padx=2)
            
            # Botón Salida (ROJO - Reduce stock)
            btn_salida = ctk.CTkButton(
                frame_acciones,
                text="➖ Salida",
                command=lambda p=producto: ajustar_stock_dialog(p, 'SALIDA', frame_lista, entry_buscar, label_contador),
                font=("Arial", 10, "bold"),
                fg_color=COLOR_ERROR,
                hover_color=COLOR_ERROR_HOVER,
                width=85,
                height=30,
                corner_radius=6
            )
            btn_salida.pack(side="left", padx=2)
            
    except Exception as e:
        frame_error = ctk.CTkFrame(
            frame_lista,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_ERROR
        )
        frame_error.pack(fill="both", expand=True, padx=50, pady=50)
        
        label_icono_error = ctk.CTkLabel(
            frame_error,
            text="❌",
            font=("Arial", 80)
        )
        label_icono_error.pack(pady=(50, 20))
        
        label_error = ctk.CTkLabel(
            frame_error,
            text="Error al cargar stock",
            font=("Arial", 16, "bold"),
            text_color=COLOR_ERROR
        )
        label_error.pack(pady=(0, 10))
        
        label_detalle = ctk.CTkLabel(
            frame_error,
            text=str(e),
            font=("Arial", 12),
            text_color="#666666"
        )
        label_detalle.pack(pady=(0, 50), padx=30)
        
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_stock(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de productos"""
    cargar_stock(frame_lista, entry_buscar, label_contador)


def limpiar_busqueda(entry_buscar, frame_lista, label_contador):
    """Limpia el campo de búsqueda y recarga todos los productos"""
    entry_buscar.delete(0, 'end')
    cargar_stock(frame_lista, entry_buscar, label_contador)


def ajustar_stock_dialog(producto, tipo_movimiento, frame_lista, entry_buscar=None, label_contador=None):
    """Abre ventana modal para ajustar stock mediante entrada o salida"""
    id_producto = producto['id_producto']
    nombre = producto['nombre']
    stock_actual = producto['stock']
    
    # ============= CONTROL DE CAMBIOS =============
    cambios_realizados = {'hubo_cambios': False}
    
    ventana = ctk.CTkToplevel()
    ventana.title(f"{'➕ Entrada' if tipo_movimiento == 'ENTRADA' else '➖ Salida'} de Stock")
    ventana.geometry("500x420")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana, 500, 420)
    
    frame = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ============= TÍTULO =============
    es_entrada = tipo_movimiento == 'ENTRADA'
    
    label_titulo = ctk.CTkLabel(
        frame,
        text=f"{'➕ Entrada' if es_entrada else '➖ Salida'} de Stock",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_EXITO if es_entrada else COLOR_ERROR
    )
    label_titulo.pack(pady=(20, 15))
    
    # ============= INFO DEL PRODUCTO =============
    frame_info = ctk.CTkFrame(
        frame,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=8,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", padx=30, pady=(0, 20))
    
    label_producto = ctk.CTkLabel(
        frame_info,
        text=f"📦 Producto: {nombre}",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",
        anchor="w"
    )
    label_producto.pack(fill="x", padx=15, pady=(12, 5))
    
    label_stock_actual = ctk.CTkLabel(
        frame_info,
        text=f"Stock actual: {stock_actual} unidades",
        font=("Arial", 11),
        text_color="#666666",
        anchor="w"
    )
    label_stock_actual.pack(fill="x", padx=15, pady=(0, 12))
    
    # ============= CAMPO CANTIDAD =============
    frame_campos = ctk.CTkFrame(frame, fg_color="transparent")
    frame_campos.pack(fill="x", padx=30)
    
    label_cantidad = ctk.CTkLabel(
        frame_campos,
        text="Cantidad *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",
        anchor="w"
    )
    label_cantidad.pack(fill="x", pady=(0, 5))
    
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True
    
    entry_cantidad = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ingrese cantidad",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_cantidad.pack(fill="x", pady=(0, 10))
    entry_cantidad.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # ============= AYUDA =============
    frame_ayuda = ctk.CTkFrame(
        frame_campos,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=8,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_ayuda.pack(fill="x", pady=(0, 25))
    
    texto_ayuda = f"{'Aumentará' if es_entrada else 'Reducirá'} el stock del producto"
    label_ayuda = ctk.CTkLabel(
        frame_ayuda,
        text=f"💡 {texto_ayuda}",
        font=("Arial", 10),
        text_color="#666666",
        anchor="w"
    )
    label_ayuda.pack(fill="x", padx=12, pady=10)
    
    entry_cantidad.focus()
    
    # ============= FUNCIÓN GUARDAR CON CONFIRMACIÓN =============
    def guardar_con_confirmacion():
        """Solicita confirmación antes de guardar"""
        cantidad_str = entry_cantidad.get().strip()
        
        # Validar primero
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
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        accion = "aumentar" if es_entrada else "reducir"
        nuevo_stock = stock_actual + cantidad if es_entrada else stock_actual - cantidad
        
        respuesta = messagebox.askyesno(
            "Confirmar Movimiento",
            f"¿Está seguro que desea {accion} el stock?\n\n"
            f"📦 Producto: {nombre}\n"
            f"📊 Stock actual: {stock_actual}\n"
            f"{'➕' if es_entrada else '➖'} Cantidad: {cantidad}\n"
            f"📈 Stock final: {nuevo_stock}",
            parent=ventana
        )
        
        if not respuesta:
            return
        
        # Guardar
        btn_guardar.configure(text="⏳ Guardando...", state="disabled")
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
    
    # ============= FUNCIÓN CANCELAR CON CONFIRMACIÓN =============
    def cancelar_con_confirmacion():
        """Solicita confirmación antes de cancelar si hay cambios"""
        if cambios_realizados['hubo_cambios']:
            respuesta = messagebox.askyesno(
                "Confirmar Cancelación",
                "¿Está seguro que desea cancelar?\n\nSe perderán todos los cambios realizados.",
                parent=ventana
            )
            if respuesta:
                ventana.destroy()
        else:
            ventana.destroy()
    
    # ============= BOTONES =============
    frame_botones = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botones.pack(fill="x", padx=30, pady=(0, 20))
    
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
        text="💾 Guardar",
        command=guardar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO if es_entrada else COLOR_ERROR,
        hover_color=COLOR_EXITO_HOVER if es_entrada else COLOR_ERROR_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    # Atajos de teclado
    entry_cantidad.bind("<Return>", lambda e: guardar_con_confirmacion())
    ventana.bind("<Escape>", lambda e: cancelar_con_confirmacion())


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")