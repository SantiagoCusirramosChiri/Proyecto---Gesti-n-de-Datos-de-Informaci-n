# maestro_identidades.py

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


# Muestra interfaz de gestión de identidades con búsqueda
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="🪪 Gestión de Identidades",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Identidad",
        command=lambda: abrir_formulario_identidad(frame_principal, id_empresa),
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
        command=lambda: cargar_identidades(frame_lista, entry_buscar),
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
        placeholder_text="Buscar por tipo o código de documento...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_identidades(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_identidades(frame_lista, entry_buscar)


# Carga y muestra tabla de identidades activas
def cargar_identidades(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_identidades_activas()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="🪪 No hay identidades registradas",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Tipo Identificación', 'Código Documento', 'Estado', 'Acciones'],
            [60, 200, 200, 100, 250]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for identidad in resultado:
            id_identidad = identidad[0]
            tipo_identificacion = identidad[1]
            codigo_documento = identidad[2]
            activo = identidad[3]
            
            if termino_busqueda:
                if termino_busqueda not in tipo_identificacion.lower() and termino_busqueda not in codigo_documento.lower():
                    continue
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([id_identidad, tipo_identificacion, codigo_documento, estado])
            
            botones = [
                ('✏️ Editar', lambda i=identidad: editar_identidad(frame_lista, i)),
                ('🗑️ Desactivar', lambda id=id_identidad, c=codigo_documento: desactivar_identidad(id, c, frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar identidades:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de identidades
def filtrar_identidades(frame_lista, entry_buscar):
    cargar_identidades(frame_lista, entry_buscar)


# Abre ventana modal con formulario para crear o editar identidad
def abrir_formulario_identidad(frame_principal, id_empresa, identidad_editar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Identidad" if not identidad_editar else "Editar Identidad")
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
        text="➕ Registrar Identidad" if not identidad_editar else "✏️ Editar Identidad",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_tipo = ctk.CTkLabel(
        frame_campos,
        text="Tipo de Identificación:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_tipo.pack(fill="x", pady=(0, 5))
    
    combo_tipo = ctk.CTkComboBox(
        frame_campos,
        values=["DNI", "RUC", "Pasaporte", "Carnet Extranjería", "Otro"],
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        dropdown_fg_color=COLOR_FONDO_SECUNDARIO
    )
    combo_tipo.pack(fill="x", pady=(0, 20))
    combo_tipo.set("DNI")
    
    label_codigo = ctk.CTkLabel(
        frame_campos,
        text="Código de Documento:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_codigo.pack(fill="x", pady=(0, 5))
    
    entry_codigo = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 12345678",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_codigo.pack(fill="x", pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 DNI: 8 dígitos | RUC: 11 dígitos | Otros: hasta 15 caracteres",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    if identidad_editar:
        combo_tipo.set(identidad_editar[1])
        entry_codigo.insert(0, identidad_editar[2])
    
    def guardar():
        tipo_identificacion = combo_tipo.get().strip()
        codigo_documento = entry_codigo.get().strip()
        
        if not tipo_identificacion or not codigo_documento:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana_form)
            return
        
        if tipo_identificacion == "DNI" and (len(codigo_documento) != 8 or not codigo_documento.isdigit()):
            messagebox.showerror("Error", "El DNI debe tener exactamente 8 dígitos numéricos", parent=ventana_form)
            return
        
        if tipo_identificacion == "RUC" and (len(codigo_documento) != 11 or not codigo_documento.isdigit()):
            messagebox.showerror("Error", "El RUC debe tener exactamente 11 dígitos numéricos", parent=ventana_form)
            return
        
        if len(codigo_documento) > 15:
            messagebox.showerror("Error", "El código no puede tener más de 15 caracteres", parent=ventana_form)
            return
        
        try:
            if identidad_editar:
                procedimientos.actualizar_identidad(identidad_editar[0], tipo_identificacion, codigo_documento)
                messagebox.showinfo("✅ Éxito", "Identidad actualizada correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_identidad(tipo_identificacion, codigo_documento)
                messagebox.showinfo("✅ Éxito", "Identidad registrada correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            frame_lista = frame_principal.winfo_children()[-1]
            cargar_identidades(frame_lista)
            
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
    
    entry_codigo.bind("<Return>", lambda e: guardar())


# Abre formulario de edición con datos de la identidad seleccionada
def editar_identidad(frame_lista, identidad):
    frame_principal = frame_lista.master
    abrir_formulario_identidad(frame_principal, None, identidad)


# Desactiva identidad tras confirmación del usuario
def desactivar_identidad(id_identidad, codigo_documento, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar la identidad con código:\n{codigo_documento}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_identidad(id_identidad)
            messagebox.showinfo("✅ Éxito", "Identidad desactivada correctamente")
            cargar_identidades(frame_lista, entry_buscar)
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