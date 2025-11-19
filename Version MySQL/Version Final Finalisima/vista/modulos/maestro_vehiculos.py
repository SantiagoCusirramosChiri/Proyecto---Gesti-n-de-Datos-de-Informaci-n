# maestro_vehiculos.py

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


# Muestra interfaz de gestión de vehículos con búsqueda
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="🚗 Gestión de Vehículos",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nuevo Vehículo",
        command=lambda: abrir_formulario_vehiculo(frame_principal, id_empresa),
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
        command=lambda: cargar_vehiculos(frame_lista, entry_buscar),
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
        placeholder_text="Buscar por descripción o placa...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_vehiculos(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_vehiculos(frame_lista, entry_buscar)


# Carga y muestra tabla de vehículos activos
def cargar_vehiculos(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_vehiculos_activos()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="🚗 No hay vehículos registrados",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Descripción', 'Placa', 'Estado', 'Acciones'],
            [60, 300, 120, 100, 250]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for vehiculo in resultado:
            id_vehiculo = vehiculo[0]
            descripcion = vehiculo[1]
            placa = vehiculo[2]
            activo = vehiculo[3]
            
            if termino_busqueda:
                if termino_busqueda not in descripcion.lower() and termino_busqueda not in placa.lower():
                    continue
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([id_vehiculo, descripcion, placa, estado])
            
            botones = [
                ('✏️ Editar', lambda v=vehiculo: editar_vehiculo(frame_lista, v)),
                ('🗑️ Desactivar', lambda id=id_vehiculo, d=descripcion: desactivar_vehiculo(id, d, frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar vehículos:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de vehículos
def filtrar_vehiculos(frame_lista, entry_buscar):
    cargar_vehiculos(frame_lista, entry_buscar)


# Abre ventana modal con formulario para crear o editar vehículo
def abrir_formulario_vehiculo(frame_principal, id_empresa, vehiculo_editar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Vehículo" if not vehiculo_editar else "Editar Vehículo")
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
        text="➕ Registrar Vehículo" if not vehiculo_editar else "✏️ Editar Vehículo",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción del Vehículo:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_descripcion.pack(fill="x", pady=(0, 5))
    
    entry_descripcion = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Camioneta Toyota Hilux Blanca",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_descripcion.pack(fill="x", pady=(0, 20))
    
    label_placa = ctk.CTkLabel(
        frame_campos,
        text="Placa (8 caracteres máximo):",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_placa.pack(fill="x", pady=(0, 5))
    
    entry_placa = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: ABC-123",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_placa.pack(fill="x", pady=(0, 30))
    
    if vehiculo_editar:
        entry_descripcion.insert(0, vehiculo_editar[1])
        entry_placa.insert(0, vehiculo_editar[2])
    
    def guardar():
        descripcion = entry_descripcion.get().strip()
        placa = entry_placa.get().strip()
        
        if not descripcion or not placa:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana_form)
            return
        
        if len(placa) > 8:
            messagebox.showerror("Error", "La placa no puede tener más de 8 caracteres", parent=ventana_form)
            return
        
        try:
            if vehiculo_editar:
                procedimientos.actualizar_vehiculo(vehiculo_editar[0], descripcion, placa)
                messagebox.showinfo("✅ Éxito", "Vehículo actualizado correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_vehiculo(descripcion, placa)
                messagebox.showinfo("✅ Éxito", "Vehículo registrado correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            frame_lista = frame_principal.winfo_children()[-1]
            cargar_vehiculos(frame_lista)
            
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
    
    entry_descripcion.bind("<Return>", lambda e: entry_placa.focus())
    entry_placa.bind("<Return>", lambda e: guardar())


# Abre formulario de edición con datos del vehículo seleccionado
def editar_vehiculo(frame_lista, vehiculo):
    frame_principal = frame_lista.master
    abrir_formulario_vehiculo(frame_principal, None, vehiculo)


# Desactiva vehículo tras confirmación del usuario
def desactivar_vehiculo(id_vehiculo, descripcion, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar el vehículo:\n{descripcion}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_vehiculo(id_vehiculo)
            messagebox.showinfo("✅ Éxito", "Vehículo desactivado correctamente")
            cargar_vehiculos(frame_lista, entry_buscar)
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