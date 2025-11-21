# vista/modulos/maestro_formas_pago.py

import customtkinter as ctk
from tkinter import messagebox
from logica.FormaPagoBL import FormaPagoBL
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


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de gestión de formas de pago con búsqueda"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Header
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="💳 Gestión de Formas de Pago",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    # Contador
    label_contador = ctk.CTkLabel(
        frame_header,
        text="",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_contador.pack(side="left", padx=20)
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Forma de Pago",
        command=lambda: abrir_formulario_forma_pago(frame_principal, id_empresa, None, frame_lista, entry_buscar, label_contador),
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
        command=lambda: cargar_formas_pago(frame_lista, entry_buscar, label_contador),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_actualizar.pack(side="right", padx=5)
    
    # Búsqueda
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
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_formas_pago(frame_lista, entry_buscar, label_contador))
    
    # Tabla
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_formas_pago(frame_lista, entry_buscar, label_contador)


def cargar_formas_pago(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de formas de pago activas"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            formas_pago = FormaPagoBL.buscar_formas_pago(termino_busqueda)
        else:
            formas_pago = FormaPagoBL.obtener_formas_pago_activas()
        
        # Actualizar contador
        if label_contador:
            total = len(formas_pago) if formas_pago else 0
            label_contador.configure(text=f"({total} formas de pago)")
        
        if not formas_pago or len(formas_pago) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "💳 No hay formas de pago registradas"
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
            ['ID', 'Nombre', 'Descripción', 'Estado', 'Acciones'],
            [60, 200, 350, 100, 250]
        )
        
        for forma_pago in formas_pago:
            estado = "✅ Activo" if forma_pago['activo'] else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([
                forma_pago['id_forma_pago'],
                forma_pago['nombre'],
                forma_pago['descripcion'],
                estado
            ])
            
            botones = [
                ('✏️ Editar', lambda fp=forma_pago, fl=frame_lista, eb=entry_buscar, lc=label_contador: 
                    editar_forma_pago(fp, fl, eb, lc)),
                ('🗑️ Desactivar', lambda fp=forma_pago, fl=frame_lista, eb=entry_buscar, lc=label_contador: 
                    desactivar_forma_pago_confirm(fp, fl, eb, lc))
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
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_formas_pago(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de formas de pago"""
    cargar_formas_pago(frame_lista, entry_buscar, label_contador)


def abrir_formulario_forma_pago(frame_principal, id_empresa, forma_pago_editar=None, frame_lista=None, entry_buscar=None, label_contador=None):
    """Abre ventana modal con formulario para crear o editar forma de pago"""
    es_edicion = forma_pago_editar is not None
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Forma de Pago" if es_edicion else "Registrar Forma de Pago")
    ventana_form.geometry("500x500")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 500)
    
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
        text="✏️ Editar Forma de Pago" if es_edicion else "➕ Registrar Forma de Pago",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    # Campo: Nombre
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Efectivo, Tarjeta, Transferencia",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 20))
    
    # Campo: Descripción
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción *",
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
    entry_descripcion.pack(fill="x", pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 El nombre debe tener al menos 3 caracteres.\nLa descripción es obligatoria.",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w",
        justify="left"
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    # Llenar datos si es edición
    if es_edicion:
        entry_nombre.insert(0, forma_pago_editar['nombre'])
        entry_descripcion.insert(0, forma_pago_editar['descripcion'])
    
    def guardar():
        """Valida y guarda la forma de pago"""
        nombre = entry_nombre.get().strip()
        descripcion = entry_descripcion.get().strip()
        
        # Validar nombre
        nombre_valido, mensaje_nombre = FormaPagoBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            entry_nombre.focus()
            return
        
        # Validar descripción
        descripcion_valida, mensaje_desc = FormaPagoBL.validar_descripcion(descripcion)
        if not descripcion_valida:
            messagebox.showerror("Error", mensaje_desc, parent=ventana_form)
            entry_descripcion.focus()
            return
        
        # Deshabilitar botones
        btn_guardar.configure(text="Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if es_edicion:
                exito, mensaje = FormaPagoBL.actualizar_forma_pago(
                    id_forma_pago=forma_pago_editar['id_forma_pago'],
                    nombre=nombre,
                    descripcion=descripcion
                )
            else:
                exito, mensaje, id_forma_pago = FormaPagoBL.insertar_forma_pago(
                    nombre=nombre,
                    descripcion=descripcion
                )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
                ventana_form.destroy()
                
                # Recargar lista
                if frame_lista:
                    cargar_formas_pago(frame_lista, entry_buscar, label_contador)
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
    
    # Botones
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
    
    # Atajos
    entry_nombre.bind("<Return>", lambda e: entry_descripcion.focus())
    entry_descripcion.bind("<Return>", lambda e: guardar())
    ventana_form.bind("<Escape>", lambda e: ventana_form.destroy())
    
    entry_nombre.focus()


def editar_forma_pago(forma_pago, frame_lista, entry_buscar=None, label_contador=None):
    """Abre formulario de edición con datos de la forma de pago seleccionada"""
    frame_principal = frame_lista.master
    abrir_formulario_forma_pago(frame_principal, None, forma_pago, frame_lista, entry_buscar, label_contador)


def desactivar_forma_pago_confirm(forma_pago, frame_lista, entry_buscar=None, label_contador=None):
    """Desactiva forma de pago tras confirmación del usuario"""
    nombre = forma_pago['nombre']
    id_forma_pago = forma_pago['id_forma_pago']
    
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar la forma de pago?\n\n{nombre}\n\nEsta acción marcará la forma de pago como inactiva."
    )
    
    if respuesta:
        exito, mensaje = FormaPagoBL.desactivar_forma_pago(id_forma_pago)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_formas_pago(frame_lista, entry_buscar, label_contador)
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