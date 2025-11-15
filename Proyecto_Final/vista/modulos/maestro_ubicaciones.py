# maestro_ubicaciones.py

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


# Muestra interfaz de gestión de ubicaciones con búsqueda
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="📍 Gestión de Ubicaciones",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Ubicación",
        command=lambda: abrir_formulario_ubicacion(frame_principal, id_empresa),
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
        command=lambda: cargar_ubicaciones(frame_lista, entry_buscar),
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
        placeholder_text="Buscar por descripción...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_ubicaciones(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_ubicaciones(frame_lista, entry_buscar)


# Carga y muestra tabla de ubicaciones activas
def cargar_ubicaciones(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_ubicaciones_activas()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="📍 No hay ubicaciones registradas",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Descripción', 'Estado', 'Acciones'],
            [60, 500, 100, 250]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for ubicacion in resultado:
            id_ubicacion = ubicacion[0]
            descripcion = ubicacion[1]
            activo = ubicacion[2]
            
            if termino_busqueda:
                if termino_busqueda not in descripcion.lower():
                    continue
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([id_ubicacion, descripcion, estado])
            
            botones = [
                ('✏️ Editar', lambda u=ubicacion: editar_ubicacion(frame_lista, u)),
                ('🗑️ Desactivar', lambda id=id_ubicacion, d=descripcion: desactivar_ubicacion(id, d, frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar ubicaciones:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de ubicaciones
def filtrar_ubicaciones(frame_lista, entry_buscar):
    cargar_ubicaciones(frame_lista, entry_buscar)


# Abre ventana modal con formulario para crear o editar ubicación
def abrir_formulario_ubicacion(frame_principal, id_empresa, ubicacion_editar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Ubicación" if not ubicacion_editar else "Editar Ubicación")
    ventana_form.geometry("550x400")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 550, 400)
    
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
        text="➕ Registrar Ubicación" if not ubicacion_editar else "✏️ Editar Ubicación",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción de la Ubicación:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_descripcion.pack(fill="x", pady=(0, 5))
    
    entry_descripcion = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Avenida San Martín 507",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_descripcion.pack(fill="x", pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 Puede incluir calle, número, distrito, ciudad, etc.",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    if ubicacion_editar:
        entry_descripcion.insert(0, ubicacion_editar[1])
    
    def guardar():
        descripcion = entry_descripcion.get().strip()
        
        if not descripcion:
            messagebox.showerror("Error", "Complete el campo de descripción", parent=ventana_form)
            return
        
        if len(descripcion) < 10:
            messagebox.showerror("Error", "La descripción debe tener al menos 10 caracteres", parent=ventana_form)
            return
        
        try:
            if ubicacion_editar:
                procedimientos.actualizar_ubicacion(ubicacion_editar[0], descripcion)
                messagebox.showinfo("✅ Éxito", "Ubicación actualizada correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_ubicacion(descripcion)
                messagebox.showinfo("✅ Éxito", "Ubicación registrada correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            frame_lista = frame_principal.winfo_children()[-1]
            cargar_ubicaciones(frame_lista)
            
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
    
    entry_descripcion.bind("<Return>", lambda e: guardar())
    entry_descripcion.focus()


# Abre formulario de edición con datos de la ubicación seleccionada
def editar_ubicacion(frame_lista, ubicacion):
    frame_principal = frame_lista.master
    abrir_formulario_ubicacion(frame_principal, None, ubicacion)


# Desactiva ubicación tras confirmación del usuario
def desactivar_ubicacion(id_ubicacion, descripcion, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar la ubicación:\n{descripcion}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_ubicacion(id_ubicacion)
            messagebox.showinfo("✅ Éxito", "Ubicación desactivada correctamente")
            cargar_ubicaciones(frame_lista, entry_buscar)
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