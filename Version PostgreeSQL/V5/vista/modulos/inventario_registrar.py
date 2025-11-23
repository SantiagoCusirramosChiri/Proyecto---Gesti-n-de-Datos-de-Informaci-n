# vista/modulos/inventario_registrar.py

import customtkinter as ctk
from tkinter import messagebox
from logica.ProductoBL import ProductoBL
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
    COLOR_BORDE
)


def mostrar(frame_contenido, id_empresa):
    """Muestra pantalla principal para registrar nuevos productos"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="📦 Registrar Productos",
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
        text="📦",
        font=("Arial", 100)
    )
    label_icono.pack(pady=(50, 20))
    
    label_descripcion = ctk.CTkLabel(
        frame_info,
        text="Agregue nuevos productos al inventario",
        font=("Arial", 16),
        text_color="#666666"
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nuevo Producto",
        command=lambda: abrir_formulario_producto(frame_principal, id_empresa, None, None),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=250,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


def abrir_formulario_producto(frame_principal, id_empresa, producto_editar=None, callback_actualizar=None):
    """Abre ventana modal con formulario para crear o editar producto"""
    es_edicion = producto_editar is not None
    
    # ============= CONTROL DE CAMBIOS =============
    cambios_realizados = {'hubo_cambios': False}
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Producto" if es_edicion else "Registrar Producto")
    ventana_form.geometry("600x800")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 600, 800)
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ============= TÍTULO =============
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="✏️ Editar Producto" if es_edicion else "➕ Registrar Producto",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_ADVERTENCIA if es_edicion else COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    # ============= FORMULARIO =============
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    # ============= FUNCIÓN PARA REGISTRAR CAMBIOS =============
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True
    
    # Campo: Nombre del Producto
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre del Producto *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Cuaderno College 100 hojas",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    entry_nombre.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Campo: Descripción
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_descripcion.pack(fill="x", pady=(0, 5))
    
    entry_descripcion = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Cuaderno A4 de 100 hojas, marca Justus",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_descripcion.pack(fill="x", pady=(0, 15))
    entry_descripcion.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Campo: Precio Base
    label_precio = ctk.CTkLabel(
        frame_campos,
        text="Precio Base (S/) *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_precio.pack(fill="x", pady=(0, 5))
    
    entry_precio = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 8.50",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_precio.pack(fill="x", pady=(0, 15))
    entry_precio.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Campo: Stock Inicial
    label_stock = ctk.CTkLabel(
        frame_campos,
        text="Stock Inicial *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_stock.pack(fill="x", pady=(0, 5))
    
    entry_stock = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 100",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_stock.pack(fill="x", pady=(0, 15))
    entry_stock.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Campo: Unidad de Medida
    label_unidad = ctk.CTkLabel(
        frame_campos,
        text="Unidad de Medida *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_unidad.pack(fill="x", pady=(0, 5))
    
    combo_unidad = ctk.CTkComboBox(
        frame_campos,
        values=ProductoBL.UNIDADES_MEDIDA,
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,
        button_hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER
    )
    combo_unidad.pack(fill="x", pady=(0, 10))
    combo_unidad.set("UND")
    combo_unidad.bind("<<ComboboxSelected>>", registrar_cambio)  # ✅ Detecta cambios en combo
    
    # Ayuda de unidades de medida
    frame_ayuda = ctk.CTkFrame(
        frame_campos,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=8,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_ayuda.pack(fill="x", pady=(0, 20))
    
    label_ayuda = ctk.CTkLabel(
        frame_ayuda,
        text="💡 Unidades disponibles:\nUND=Unidad, KG=Kilogramo, LT=Litro, M=Metro,\nM2=Metro cuadrado, M3=Metro cúbico",
        font=("Arial", 10),
        text_color="#666666",
        anchor="w",
        justify="left"
    )
    label_ayuda.pack(fill="x", padx=12, pady=10)
    
    # Cargar datos si es edición
    if es_edicion:
        entry_nombre.insert(0, producto_editar['nombre'])
        entry_descripcion.insert(0, producto_editar['descripcion'])
        entry_precio.insert(0, str(producto_editar['precio_base']))
        entry_stock.insert(0, str(producto_editar['stock']))
        combo_unidad.set(producto_editar['unidad_medida'])
        cambios_realizados['hubo_cambios'] = False  # Resetear porque cargamos datos
    
    # ============= FUNCIÓN GUARDAR CON CONFIRMACIÓN =============
    def guardar_con_confirmacion():
        """Valida, confirma y guarda el producto"""
        nombre = entry_nombre.get()
        descripcion = entry_descripcion.get()
        precio_str = entry_precio.get()
        stock_str = entry_stock.get()
        unidad_medida = combo_unidad.get()
        
        # Validar nombre
        nombre_valido, mensaje_nombre = ProductoBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            entry_nombre.focus()
            return
        
        # Validar descripción
        descripcion_valida, mensaje_desc = ProductoBL.validar_descripcion(descripcion)
        if not descripcion_valida:
            messagebox.showerror("Error", mensaje_desc, parent=ventana_form)
            entry_descripcion.focus()
            return
        
        # Validar precio
        precio_valido, mensaje_precio, precio_base = ProductoBL.validar_precio(precio_str)
        if not precio_valido:
            messagebox.showerror("Error", mensaje_precio, parent=ventana_form)
            entry_precio.focus()
            return
        
        # Validar stock
        stock_valido, mensaje_stock, stock = ProductoBL.validar_stock(stock_str)
        if not stock_valido:
            messagebox.showerror("Error", mensaje_stock, parent=ventana_form)
            entry_stock.focus()
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        accion = "actualizar" if es_edicion else "registrar"
        respuesta = messagebox.askyesno(
            "Confirmar Operación",
            f"¿Está seguro que desea {accion} este producto?\n\n"
            f"📦 Producto: {nombre.strip()}\n"
            f"💰 Precio: S/ {precio_base:.2f}\n"
            f"📊 Stock: {stock} {unidad_medida}",
            parent=ventana_form
        )
        
        if not respuesta:
            return
        
        # Deshabilitar botones mientras se guarda
        btn_guardar.configure(text="⏳ Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if es_edicion:
                exito, mensaje = ProductoBL.actualizar_producto(
                    id_producto=producto_editar['id_producto'],
                    nombre=nombre.strip(),
                    descripcion=descripcion.strip(),
                    precio_base=precio_base,
                    stock=stock,
                    unidad_medida=unidad_medida
                )
            else:
                exito, mensaje, id_producto = ProductoBL.insertar_producto(
                    nombre=nombre.strip(),
                    descripcion=descripcion.strip(),
                    precio_base=precio_base,
                    stock=stock,
                    unidad_medida=unidad_medida
                )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
                ventana_form.destroy()
                
                if callback_actualizar:
                    callback_actualizar()
            else:
                messagebox.showerror("❌ Error", mensaje, parent=ventana_form)
                btn_guardar.configure(text="💾 Guardar", state="normal")
                btn_cancelar.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana_form)
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
                parent=ventana_form
            )
            if respuesta:
                ventana_form.destroy()
        else:
            ventana_form.destroy()
    
    # ============= BOTONES =============
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(10, 20))
    
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
        fg_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,
        hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    # Atajos de teclado
    ventana_form.bind("<Escape>", lambda e: cancelar_con_confirmacion())
    ventana_form.bind("<Return>", lambda e: guardar_con_confirmacion())
    
    # Focus inicial
    entry_nombre.focus()


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")