import customtkinter as ctk
from tkinter import messagebox
from logica.ClienteBL import ClienteBL
from logica.RegistroBL import RegistroBL
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
        border_width=1,
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
        text_color="#666666"
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


def abrir_formulario(frame_principal, id_empresa, cliente_editar=None, callback_actualizar=None):
    es_edicion = cliente_editar is not None
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Cliente" if es_edicion else "Registrar Cliente")
    ventana_form.geometry("600x750")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 600, 750)
    
    cambios_realizados = {'hubo_cambios': False}
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="✏️ Editar Cliente" if es_edicion else "➕ Registrar Cliente",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ADVERTENCIA if es_edicion else COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True
    
    # Campo: Nombre
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  #  OSCURO
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Juan",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    entry_nombre.bind("<KeyRelease>", registrar_cambio)  #  Detecta cambios
    
    # Campo: Apellido
    label_apellido = ctk.CTkLabel(
        frame_campos,
        text="Apellido *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  #  OSCURO
        anchor="w"
    )
    label_apellido.pack(fill="x", pady=(0, 5))
    
    entry_apellido = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Pérez García",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_apellido.pack(fill="x", pady=(0, 20))
    entry_apellido.bind("<KeyRelease>", registrar_cambio)  #  Detecta cambios
    
    # Campo: Ubicación
    label_ubicacion = ctk.CTkLabel(
        frame_campos,
        text="Ubicación *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # OSCURO
        anchor="w"
    )
    label_ubicacion.pack(fill="x", pady=(0, 5))
    
    ubicaciones = RegistroBL.obtener_ubicaciones_activas()
    ubicaciones_dict = {}
    ubicaciones_lista = []
    
    if ubicaciones:
        ubicaciones_dict = {ub['descripcion']: ub['id_ubicacion'] for ub in ubicaciones}
        ubicaciones_lista = list(ubicaciones_dict.keys())
    
    combo_ubicacion = ctk.CTkComboBox(
        frame_campos,
        values=ubicaciones_lista if ubicaciones_lista else ["No hay ubicaciones"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,
        button_hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER,
        text_color="#2C2C2E",  #  OSCURO
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E",  #  OSCURO
        state="readonly"
    )
    combo_ubicacion.pack(fill="x", pady=(0, 20))
    combo_ubicacion.bind("<<ComboboxSelected>>", registrar_cambio)  # ✅ Detecta cambios
    
    if ubicaciones_lista:
        combo_ubicacion.set(ubicaciones_lista[0])
    else:
        combo_ubicacion.set("No hay ubicaciones")
    
    # Campo: Tipo de Documento
    label_tipo_doc = ctk.CTkLabel(
        frame_campos,
        text="Tipo de Documento *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  #  OSCURO
        anchor="w"
    )
    label_tipo_doc.pack(fill="x", pady=(0, 5))
    
    combo_tipo_doc = ctk.CTkComboBox(
        frame_campos,
        values=["DNI", "RUC", "CE", "PASAPORTE"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,
        button_hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER,
        text_color="#2C2C2E",  #  OSCURO
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E",  #  OSCURO
        state="readonly"
    )
    combo_tipo_doc.set("DNI")
    combo_tipo_doc.pack(fill="x", pady=(0, 15))
    combo_tipo_doc.bind("<<ComboboxSelected>>", registrar_cambio)  #  Detecta cambios
    
    # Campo: Número de Documento
    label_num_doc = ctk.CTkLabel(
        frame_campos,
        text="Número de Documento *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  #  OSCURO
        anchor="w"
    )
    label_num_doc.pack(fill="x", pady=(0, 5))
    
    entry_num_doc = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 12345678",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_num_doc.pack(fill="x", pady=(0, 10))
    entry_num_doc.bind("<KeyRelease>", registrar_cambio)  #  Detecta cambios
    
    # Ayuda
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 Si no encuentra la ubicación, créela primero en el menú de Ubicaciones",
        font=("Arial", 10),
        text_color="#666666",
        anchor="w",
        wraplength=500
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    # Cargar datos si es edición
    if es_edicion:
        if isinstance(cliente_editar, dict):
            entry_nombre.insert(0, cliente_editar.get('nombre', ''))
            entry_apellido.insert(0, cliente_editar.get('apellido', ''))
            combo_tipo_doc.set(cliente_editar.get('tipo_identificacion', 'DNI'))
            entry_num_doc.insert(0, cliente_editar.get('codigo_documento', ''))
            
            ubicacion_actual = cliente_editar.get('ubicacion', '')
            if ubicacion_actual in ubicaciones_lista:
                combo_ubicacion.set(ubicacion_actual)
        else:
            entry_nombre.insert(0, cliente_editar[1])
            entry_apellido.insert(0, cliente_editar[2])
        
        cambios_realizados['hubo_cambios'] = False  # Resetear después de cargar
    
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

    def guardar_con_confirmacion():
        """Valida, confirma y guarda el cliente"""
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        ubicacion_seleccionada = combo_ubicacion.get()
        tipo_doc = combo_tipo_doc.get()
        num_doc = entry_num_doc.get().strip()
        
        # Validaciones
        if not nombre or not apellido:
            messagebox.showerror("Error", "Complete nombre y apellido", parent=ventana_form)
            return
        
        if not ubicaciones_lista or ubicacion_seleccionada == "No hay ubicaciones":
            messagebox.showerror(
                "Error", 
                "Debe crear al menos una ubicación primero.\nVaya al menú de Ubicaciones.",
                parent=ventana_form
            )
            return
        
        if not num_doc:
            messagebox.showerror("Error", "Ingrese el número de documento", parent=ventana_form)
            return
        
        nombre_valido, mensaje_nombre = ClienteBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            return
        
        apellido_valido, mensaje_apellido = ClienteBL.validar_apellido(apellido)
        if not apellido_valido:
            messagebox.showerror("Error", mensaje_apellido, parent=ventana_form)
            return
        
        id_ubicacion = ubicaciones_dict.get(ubicacion_seleccionada)
        if not id_ubicacion:
            messagebox.showerror("Error", "Ubicación inválida", parent=ventana_form)
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        if es_edicion:
            respuesta = messagebox.askyesno(
                "Confirmar Actualización",
                f"¿Está seguro que desea actualizar este cliente?\n\n"
                f"👤 Cliente: {nombre} {apellido}\n"
                f"📄 Documento: {tipo_doc} - {num_doc}\n"
                f"📍 Ubicación: {ubicacion_seleccionada}",
                parent=ventana_form
            )
        else:
            respuesta = messagebox.askyesno(
                "Confirmar Registro",
                f"¿Está seguro que desea registrar este cliente?\n\n"
                f"👤 Cliente: {nombre} {apellido}\n"
                f"📄 Documento: {tipo_doc} - {num_doc}\n"
                f"📍 Ubicación: {ubicacion_seleccionada}",
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
                if isinstance(cliente_editar, dict):
                    id_cliente = cliente_editar['id_cliente']
                    id_identidad = cliente_editar['id_identidad']
                else:
                    id_cliente = cliente_editar[0]
                    messagebox.showerror(
                        "Error",
                        "Formato de cliente no soportado para edición",
                        parent=ventana_form
                    )
                    btn_guardar.configure(text="💾 Guardar", state="normal")
                    btn_cancelar.configure(state="normal")
                    return
                
                exito, mensaje = ClienteBL.actualizar_cliente(
                    id_cliente=id_cliente,
                    nombre=nombre,
                    apellido=apellido,
                    id_ubicacion=id_ubicacion,
                    id_identidad=id_identidad
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
            
            else:
                exito_identidad, mensaje_identidad, id_identidad = ClienteBL.buscar_o_crear_identidad(
                    tipo_identificacion=tipo_doc,
                    codigo_documento=num_doc
                )
                
                if not exito_identidad:
                    messagebox.showerror("❌ Error", mensaje_identidad, parent=ventana_form)
                    btn_guardar.configure(text="💾 Guardar", state="normal")
                    btn_cancelar.configure(state="normal")
                    return
                
                exito, mensaje, id_cliente = ClienteBL.insertar_cliente(
                    nombre=nombre,
                    apellido=apellido,
                    id_ubicacion=id_ubicacion,
                    id_identidad=id_identidad
                )
                
                if exito:
                    messagebox.showinfo(
                        "✅ Éxito", 
                        f"{mensaje}\n\nID Cliente: {id_cliente}\nID Identidad: {id_identidad}",
                        parent=ventana_form
                    )
                    ventana_form.destroy()
                    
                    if callback_actualizar:
                        callback_actualizar()
                else:
                    messagebox.showerror("❌ Error", mensaje, parent=ventana_form)
                    btn_guardar.configure(text="💾 Guardar", state="normal")
                    btn_cancelar.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar:\n{str(e)}", parent=ventana_form)
            btn_guardar.configure(text="💾 Guardar", state="normal")
            btn_cancelar.configure(state="normal")
            print(f"❌ Error al guardar cliente: {e}")
            import traceback
            traceback.print_exc()
    
    # ============= BOTONES =============
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
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
        command=guardar_con_confirmacion,  #  CON CONFIRMACIÓN
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,
        hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    # Atajos de teclado
    entry_nombre.bind("<Return>", lambda e: entry_apellido.focus())
    entry_apellido.bind("<Return>", lambda e: entry_num_doc.focus())
    entry_num_doc.bind("<Return>", lambda e: guardar_con_confirmacion())
    ventana_form.bind("<Escape>", lambda e: cancelar_con_confirmacion())
    
    entry_nombre.focus()


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")