# vista/modulos/maestro_conductores.py

import customtkinter as ctk
from tkinter import messagebox
from logica.ConductorBL import ConductorBL
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_INFO,
    COLOR_INFO_HOVER
)


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de gestión de conductores con búsqueda"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="👨‍✈️ Gestión de Conductores",
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
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nuevo Conductor",
        command=lambda: abrir_formulario_conductor(frame_principal, id_empresa, None, frame_lista, entry_buscar, label_contador),
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
        command=lambda: cargar_conductores(frame_lista, entry_buscar, label_contador),
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
        placeholder_text="Buscar por nombre o licencia...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_conductores(frame_lista, entry_buscar, label_contador))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_conductores(frame_lista, entry_buscar, label_contador)


def cargar_conductores(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de conductores activos"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            conductores = ConductorBL.buscar_conductores(termino_busqueda)
        else:
            conductores = ConductorBL.obtener_conductores_activos()
        
        if label_contador:
            total = len(conductores) if conductores else 0
            label_contador.configure(text=f"({total} conductores)")
        
        if not conductores or len(conductores) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "👨‍✈️ No hay conductores registrados"
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
            ['ID', 'Nombre', 'N° Licencia', 'Estado', 'Acciones'],
            [60, 250, 150, 100, 250]
        )
        
        for conductor in conductores:
            estado = "✅ Activo" if conductor['activo'] else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([
                conductor['id_conductor'],
                conductor['nombre'],
                conductor['licencia'],
                estado
            ])
            
            def crear_funcion_editar(c):
                return lambda: editar_conductor(c, frame_lista, entry_buscar, label_contador)
            
            def crear_funcion_desactivar(c):
                return lambda: desactivar_conductor_confirm(c, frame_lista, entry_buscar, label_contador)
            
            botones = [
                ('✏️ Editar', crear_funcion_editar(conductor)),
                ('🗑️ Desactivar', crear_funcion_desactivar(conductor))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar conductores:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_conductores(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de conductores"""
    cargar_conductores(frame_lista, entry_buscar, label_contador)


def abrir_formulario_conductor(frame_principal, id_empresa, conductor_editar=None, frame_lista=None, entry_buscar=None, label_contador=None):
    """Abre ventana modal con formulario para crear o editar conductor"""
    es_edicion = conductor_editar is not None
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Conductor" if es_edicion else "Registrar Conductor")
    ventana_form.geometry("500x480")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 480)
    
    frame_form = ctk.CTkFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="✏️ Editar Conductor" if es_edicion else "➕ Registrar Conductor",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY if es_edicion else COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre Completo *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Juan Pérez García",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 20))
    
    label_licencia = ctk.CTkLabel(
        frame_campos,
        text="N° Licencia (12 caracteres) *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_licencia.pack(fill="x", pady=(0, 5))
    
    entry_licencia = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: B12345678901",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_licencia.pack(fill="x", pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 La licencia debe comenzar con una letra (A, B, C)\nseguida de 11 dígitos o caracteres alfanuméricos.",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w",
        justify="left"
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    if es_edicion:
        entry_nombre.insert(0, conductor_editar['nombre'])
        entry_licencia.insert(0, conductor_editar['licencia'])
    
    def guardar():
        """Valida y guarda el conductor"""
        nombre = entry_nombre.get().strip()
        licencia = entry_licencia.get().strip()
        
        nombre_valido, mensaje_nombre = ConductorBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            entry_nombre.focus()
            return
        
        licencia_valida, mensaje_licencia = ConductorBL.validar_licencia(licencia)
        if not licencia_valida:
            messagebox.showerror("Error", mensaje_licencia, parent=ventana_form)
            entry_licencia.focus()
            return
        
        btn_guardar.configure(text="Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if es_edicion:
                exito, mensaje = ConductorBL.actualizar_conductor(
                    id_conductor=conductor_editar['id_conductor'],
                    nombre=nombre,
                    licencia=licencia
                )
            else:
                exito, mensaje, id_conductor = ConductorBL.insertar_conductor(
                    nombre=nombre,
                    licencia=licencia
                )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
                ventana_form.destroy()
                
                if frame_lista:
                    cargar_conductores(frame_lista, entry_buscar, label_contador)
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
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana_form.destroy,
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
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    entry_nombre.bind("<Return>", lambda e: entry_licencia.focus())
    entry_licencia.bind("<Return>", lambda e: guardar())
    ventana_form.bind("<Escape>", lambda e: ventana_form.destroy())
    
    entry_nombre.focus()


def editar_conductor(conductor, frame_lista, entry_buscar=None, label_contador=None):
    """Abre formulario de edición con datos del conductor seleccionado"""
    frame_principal = frame_lista.master
    abrir_formulario_conductor(frame_principal, None, conductor, frame_lista, entry_buscar, label_contador)


def desactivar_conductor_confirm(conductor, frame_lista, entry_buscar=None, label_contador=None):
    """Desactiva conductor tras confirmación del usuario"""
    nombre = conductor['nombre']
    id_conductor = conductor['id_conductor']
    licencia = conductor['licencia']
    
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar al conductor?\n\n{nombre}\nLicencia: {licencia}\n\nEsta acción marcará al conductor como inactivo."
    )
    
    if respuesta:
        exito, mensaje = ConductorBL.desactivar_conductor(id_conductor)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_conductores(frame_lista, entry_buscar, label_contador)
        else:
            messagebox.showerror("❌ Error", mensaje)


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")