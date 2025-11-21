# vista/modulos/clientes_registrar.py

import customtkinter as ctk
from tkinter import messagebox
from logica.ClienteBL import ClienteBL
from logica.RegistroBL import RegistroBL
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
    """Muestra pantalla principal de registro de clientes"""
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


def abrir_formulario(frame_principal, id_empresa, cliente_editar=None, callback_actualizar=None):
    """Abre formulario modal para registrar o editar cliente"""
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Cliente" if not cliente_editar else "Editar Cliente")
    ventana_form.geometry("600x750")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 600, 750)
    
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
    
    # ========== CAMPO: NOMBRE ==========
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
        placeholder_text="Ej: Juan",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    
    # ========== CAMPO: APELLIDO ==========
    label_apellido = ctk.CTkLabel(
        frame_campos,
        text="Apellido *",
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
    
    # ========== CAMPO: UBICACIÓN ==========
    label_ubicacion = ctk.CTkLabel(
        frame_campos,
        text="Ubicación *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_ubicacion.pack(fill="x", pady=(0, 5))
    
    # Cargar ubicaciones usando RegistroBL
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
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        state="readonly"
    )
    combo_ubicacion.pack(fill="x", pady=(0, 20))
    
    if ubicaciones_lista:
        combo_ubicacion.set(ubicaciones_lista[0])
    else:
        combo_ubicacion.set("No hay ubicaciones")
    
    # ========== CAMPO: TIPO DE DOCUMENTO ==========
    label_tipo_doc = ctk.CTkLabel(
        frame_campos,
        text="Tipo de Documento *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
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
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        state="readonly"
    )
    combo_tipo_doc.set("DNI")
    combo_tipo_doc.pack(fill="x", pady=(0, 15))
    
    # ========== CAMPO: NÚMERO DE DOCUMENTO ==========
    label_num_doc = ctk.CTkLabel(
        frame_campos,
        text="Número de Documento *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_num_doc.pack(fill="x", pady=(0, 5))
    
    entry_num_doc = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: 12345678",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_num_doc.pack(fill="x", pady=(0, 10))
    
    label_ayuda = ctk.CTkLabel(
        frame_campos,
        text="💡 Si no encuentra la ubicación, créela primero en el menú de Ubicaciones",
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w",
        wraplength=500
    )
    label_ayuda.pack(fill="x", pady=(0, 30))
    
    # Si es edición, llenar campos
    if cliente_editar:
        # cliente_editar puede ser dict o tuple, manejar ambos casos
        if isinstance(cliente_editar, dict):
            entry_nombre.insert(0, cliente_editar.get('nombre', ''))
            entry_apellido.insert(0, cliente_editar.get('apellido', ''))
            combo_tipo_doc.set(cliente_editar.get('tipo_identificacion', 'DNI'))
            entry_num_doc.insert(0, cliente_editar.get('codigo_documento', ''))
            
            # Seleccionar ubicación
            ubicacion_actual = cliente_editar.get('ubicacion', '')
            if ubicacion_actual in ubicaciones_lista:
                combo_ubicacion.set(ubicacion_actual)
        else:
            # Formato tupla (legacy)
            entry_nombre.insert(0, cliente_editar[1])
            entry_apellido.insert(0, cliente_editar[2])
            # Para tupla no tenemos tipo_doc y num_doc fácilmente
    
    def guardar():
        """Valida y guarda datos del cliente"""
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
        
        # Validar nombre
        nombre_valido, mensaje_nombre = ClienteBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            return
        
        # Validar apellido
        apellido_valido, mensaje_apellido = ClienteBL.validar_apellido(apellido)
        if not apellido_valido:
            messagebox.showerror("Error", mensaje_apellido, parent=ventana_form)
            return
        
        # Obtener ID de ubicación
        id_ubicacion = ubicaciones_dict.get(ubicacion_seleccionada)
        if not id_ubicacion:
            messagebox.showerror("Error", "Ubicación inválida", parent=ventana_form)
            return
        
        # Deshabilitar botones
        btn_guardar.configure(text="Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if cliente_editar:
                # ========== EDITAR CLIENTE ==========
                if isinstance(cliente_editar, dict):
                    id_cliente = cliente_editar['id_cliente']
                    id_identidad = cliente_editar['id_identidad']
                else:
                    id_cliente = cliente_editar[0]
                    # Para legacy necesitaríamos obtener id_identidad
                    # Por ahora asumimos que es dict
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
                # ========== CREAR NUEVO CLIENTE ==========
                # 1. Primero buscar o crear la identidad
                exito_identidad, mensaje_identidad, id_identidad = ClienteBL.buscar_o_crear_identidad(
                    tipo_identificacion=tipo_doc,
                    codigo_documento=num_doc
                )
                
                if not exito_identidad:
                    messagebox.showerror("❌ Error", mensaje_identidad, parent=ventana_form)
                    btn_guardar.configure(text="💾 Guardar", state="normal")
                    btn_cancelar.configure(state="normal")
                    return
                
                # 2. Ahora crear el cliente con el id_identidad
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
    
    # ========== BOTONES ==========
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
    
    # Atajos de teclado
    entry_nombre.bind("<Return>", lambda e: entry_apellido.focus())
    entry_apellido.bind("<Return>", lambda e: entry_num_doc.focus())
    entry_num_doc.bind("<Return>", lambda e: guardar())
    ventana_form.bind("<Escape>", lambda e: ventana_form.destroy())
    
    entry_nombre.focus()


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")