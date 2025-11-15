# clientes_registrar.py

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


# Muestra pantalla principal de registro de clientes
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="👥 Registrar Clientes",
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
        text="👥",
        font=("Arial", 100)
    )
    label_icono.pack(pady=(50, 20))
    
    label_descripcion = ctk.CTkLabel(
        frame_info,
        text="Agregue nuevos clientes al sistema",
        font=("Arial", 16),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nuevo Cliente",
        command=lambda: abrir_formulario(frame_principal, id_empresa, None, None),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=250,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


# Abre formulario modal para registrar o editar cliente
def abrir_formulario(frame_principal, id_empresa, cliente_editar=None, callback_actualizar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Cliente" if not cliente_editar else "Editar Cliente")
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
        text="➕ Registrar Cliente" if not cliente_editar else "✏️ Editar Cliente",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Juan",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    
    label_apellido = ctk.CTkLabel(
        frame_campos,
        text="Apellido:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_apellido.pack(fill="x", pady=(0, 5))
    
    entry_apellido = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Pérez García",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_apellido.pack(fill="x", pady=(0, 20))
    
    label_ubicacion = ctk.CTkLabel(
        frame_campos,
        text="Ubicación:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_ubicacion.pack(fill="x", pady=(0, 5))
    
    ubicaciones = procedimientos.obtener_ubicaciones_combo()
    ubicaciones_dict = {f"{u[1]}": u[0] for u in ubicaciones}
    ubicaciones_lista = list(ubicaciones_dict.keys())
    
    combo_ubicacion = ctk.CTkComboBox(
        frame_campos,
        values=ubicaciones_lista if ubicaciones_lista else ["No hay ubicaciones"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_ubicacion.pack(fill="x", pady=(0, 20))
    if ubicaciones_lista:
        combo_ubicacion.set(ubicaciones_lista[0])
    
    label_identidad = ctk.CTkLabel(
        frame_campos,
        text="Documento de Identidad:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_identidad.pack(fill="x", pady=(0, 5))
    
    identidades = procedimientos.obtener_identidades_combo()
    identidades_dict = {f"{i[1]} - {i[2]}": i[0] for i in identidades}
    identidades_lista = list(identidades_dict.keys())
    
    combo_identidad = ctk.CTkComboBox(
        frame_campos,
        values=identidades_lista if identidades_lista else ["No hay identidades"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_identidad.pack(fill="x", pady=(0, 10))
    if identidades_lista:
        combo_identidad.set(identidades_lista[0])
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 Si no encuentra ubicación o identidad, créelas primero en Maestros",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    if cliente_editar:
        entry_nombre.insert(0, cliente_editar[1])
        entry_apellido.insert(0, cliente_editar[2])
    
    # Valida y guarda datos del cliente
    def guardar():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        ubicacion_seleccionada = combo_ubicacion.get()
        identidad_seleccionada = combo_identidad.get()
        
        if not nombre or not apellido:
            messagebox.showerror("Error", "Complete nombre y apellido", parent=ventana_form)
            return
        
        if not ubicaciones_lista or not identidades_lista:
            messagebox.showerror("Error", "Debe crear al menos una ubicación y una identidad primero", parent=ventana_form)
            return
        
        id_ubicacion = ubicaciones_dict.get(ubicacion_seleccionada)
        id_identidad = identidades_dict.get(identidad_seleccionada)
        
        try:
            if cliente_editar:
                procedimientos.actualizar_cliente(cliente_editar[0], nombre, apellido, id_ubicacion, id_identidad)
                messagebox.showinfo("✅ Éxito", "Cliente actualizado correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_cliente(nombre, apellido, id_ubicacion, id_identidad)
                messagebox.showinfo("✅ Éxito", "Cliente registrado correctamente", parent=ventana_form)
            
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
        height=40,
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
        height=40,
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