# inventario_registrar.py

import customtkinter as ctk
from tkinter import messagebox
from datos import procedimientos
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra pantalla principal para registrar nuevos productos
def mostrar(frame_contenido, id_empresa):
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
        border_width=2,
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
        text_color=COLOR_TEXTO_SECUNDARIO
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


# Abre ventana modal con formulario para crear o editar producto
def abrir_formulario_producto(frame_principal, id_empresa, producto_editar=None, callback_actualizar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Producto" if not producto_editar else "Editar Producto")
    ventana_form.geometry("600x700")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 600, 700)
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="➕ Registrar Producto" if not producto_editar else "✏️ Editar Producto",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre del Producto:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Cuaderno College 100 hojas",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_descripcion.pack(fill="x", pady=(0, 5))
    
    entry_descripcion = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Cuaderno A4 de 100 hojas, marca Justus",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_descripcion.pack(fill="x", pady=(0, 15))
    
    label_precio = ctk.CTkLabel(
        frame_campos,
        text="Precio Base (S/):",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_precio.pack(fill="x", pady=(0, 5))
    
    entry_precio = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 8.50",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_precio.pack(fill="x", pady=(0, 15))
    
    label_stock = ctk.CTkLabel(
        frame_campos,
        text="Stock Inicial:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_stock.pack(fill="x", pady=(0, 5))
    
    entry_stock = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 100",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_stock.pack(fill="x", pady=(0, 15))
    
    label_unidad = ctk.CTkLabel(
        frame_campos,
        text="Unidad de Medida:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_unidad.pack(fill="x", pady=(0, 5))
    
    combo_unidad = ctk.CTkComboBox(
        frame_campos,
        values=["UND", "KG", "LT", "M", "M2", "M3", "CAJA", "PAQUETE"],
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_unidad.pack(fill="x", pady=(0, 30))
    combo_unidad.set("UND")
    
    if producto_editar:
        entry_nombre.insert(0, producto_editar[1])
        entry_descripcion.insert(0, producto_editar[2])
        entry_precio.insert(0, str(producto_editar[3]))
        entry_stock.insert(0, str(producto_editar[4]))
        combo_unidad.set(producto_editar[5])
    
    def guardar():
        nombre = entry_nombre.get().strip()
        descripcion = entry_descripcion.get().strip()
        precio_str = entry_precio.get().strip()
        stock_str = entry_stock.get().strip()
        unidad_medida = combo_unidad.get()
        
        if not nombre or not descripcion or not precio_str or not stock_str:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana_form)
            return
        
        try:
            precio_base = float(precio_str)
            stock = int(stock_str)
            
            if precio_base <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0", parent=ventana_form)
                return
            
            if stock < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo", parent=ventana_form)
                return
            
        except ValueError:
            messagebox.showerror("Error", "Precio o stock inválido", parent=ventana_form)
            return
        
        try:
            if producto_editar:
                procedimientos.actualizar_producto(producto_editar[0], nombre, descripcion, precio_base, stock, unidad_medida)
                messagebox.showinfo("✅ Éxito", "Producto actualizado correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_producto(nombre, descripcion, precio_base, stock, unidad_medida)
                messagebox.showinfo("✅ Éxito", f"Producto '{nombre}' registrado correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            if callback_actualizar:
                callback_actualizar()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar: {str(e)}", parent=ventana_form)
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
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
        height=45,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Guardar",
        command=guardar,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=45,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    entry_nombre.focus()


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")