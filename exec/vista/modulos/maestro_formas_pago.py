# maestro_formas_pago.py

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
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra interfaz de gestión de formas de pago con búsqueda
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="💳 Gestión de Formas de Pago",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Forma de Pago",
        command=lambda: abrir_formulario_forma_pago(frame_principal, id_empresa),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_nuevo.pack(side="right", padx=5)
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_formas_pago(frame_lista, entry_buscar),
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
        placeholder_text="Buscar por nombre...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_formas_pago(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_formas_pago(frame_lista, entry_buscar)


# Carga y muestra tabla de formas de pago activas
def cargar_formas_pago(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_formas_pago_activas()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="💳 No hay formas de pago registradas",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Nombre', 'Descripción', 'Estado', 'Acciones'],
            [60, 200, 350, 100, 250]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for forma_pago in resultado:
            id_forma_pago = forma_pago[0]
            nombre = forma_pago[1]
            descripcion = forma_pago[2]
            activo = forma_pago[3]
            
            if termino_busqueda:
                if termino_busqueda not in nombre.lower():
                    continue
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([id_forma_pago, nombre, descripcion, estado])
            
            botones = [
                ('✏️ Editar', lambda fp=forma_pago: editar_forma_pago(frame_lista, fp)),
                ('🗑️ Desactivar', lambda id=id_forma_pago, n=nombre: desactivar_forma_pago(id, n, frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar formas de pago:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de formas de pago
def filtrar_formas_pago(frame_lista, entry_buscar):
    cargar_formas_pago(frame_lista, entry_buscar)


# Abre ventana modal con formulario para crear o editar forma de pago
def abrir_formulario_forma_pago(frame_principal, id_empresa, forma_pago_editar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Forma de Pago" if not forma_pago_editar else "Editar Forma de Pago")
    ventana_form.geometry("500x450")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 450)
    
    frame_form = ctk.CTkFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="➕ Registrar Forma de Pago" if not forma_pago_editar else "✏️ Editar Forma de Pago",
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
        placeholder_text="Ej: Efectivo",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 20))
    
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
        placeholder_text="Ej: Pago en moneda física",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_descripcion.pack(fill="x", pady=(0, 30))
    
    if forma_pago_editar:
        entry_nombre.insert(0, forma_pago_editar[1])
        entry_descripcion.insert(0, forma_pago_editar[2])
    
    def guardar():
        nombre = entry_nombre.get().strip()
        descripcion = entry_descripcion.get().strip()
        
        if not nombre or not descripcion:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana_form)
            return
        
        if len(nombre) < 3:
            messagebox.showerror("Error", "El nombre debe tener al menos 3 caracteres", parent=ventana_form)
            return
        
        try:
            if forma_pago_editar:
                procedimientos.actualizar_forma_pago(forma_pago_editar[0], nombre, descripcion)
                messagebox.showinfo("✅ Éxito", "Forma de pago actualizada correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_forma_pago(nombre, descripcion)
                messagebox.showinfo("✅ Éxito", "Forma de pago registrada correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            frame_lista = frame_principal.winfo_children()[-1]
            cargar_formas_pago(frame_lista)
            
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
    
    entry_nombre.bind("<Return>", lambda e: entry_descripcion.focus())
    entry_descripcion.bind("<Return>", lambda e: guardar())


# Abre formulario de edición con datos de la forma de pago seleccionada
def editar_forma_pago(frame_lista, forma_pago):
    frame_principal = frame_lista.master
    abrir_formulario_forma_pago(frame_principal, None, forma_pago)


# Desactiva forma de pago tras confirmación del usuario
def desactivar_forma_pago(id_forma_pago, nombre, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar la forma de pago:\n{nombre}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_forma_pago(id_forma_pago)
            messagebox.showinfo("✅ Éxito", "Forma de pago desactivada correctamente")
            cargar_formas_pago(frame_lista, entry_buscar)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al desactivar: {str(e)}")


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")