import customtkinter as ctk
from tkinter import messagebox
from logica.ClienteBL import ClienteBL
from logica.RegistroBL import RegistroBL
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ADVERTENCIA,
    COLOR_ADVERTENCIA_HOVER,
    COLOR_INFO,
    COLOR_INFO_HOVER,
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
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="👥 Listado de Clientes",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    label_contador = ctk.CTkLabel(
        frame_header,
        text="",
        font=("Arial", 12),
        text_color="#2C2C2E"  #  OSCURO
    )
    label_contador.pack(side="left", padx=20)
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_clientes(frame_lista, entry_buscar, label_contador),
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
        text_color="#2C2C2E"  #  OSCURO
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda,
        placeholder_text="Buscar por nombre, apellido o documento...",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"  #  OSCURO
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_clientes(frame_lista, entry_buscar, label_contador))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_clientes(frame_lista, entry_buscar, label_contador)


def cargar_clientes(frame_lista, entry_buscar=None, label_contador=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            clientes = ClienteBL.buscar_clientes(termino_busqueda)
        else:
            clientes = ClienteBL.obtener_clientes_activos()
        
        if label_contador:
            total = len(clientes) if clientes else 0
            label_contador.configure(text=f"({total} clientes)")
        
        if not clientes or len(clientes) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "👥 No hay clientes registrados"
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text=mensaje,
                font=("Arial", 16),
                text_color="#666666"
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Nombre', 'Apellido', 'Tipo Doc', 'N° Doc', 'Ubicación', 'Acciones'],
            [50, 150, 150, 80, 100, 250, 200]
        )
        
        for cliente in clientes:
            frame_fila = tabla.agregar_fila([
                cliente['id_cliente'],
                cliente['nombre'],
                cliente['apellido'],
                cliente['tipo_identificacion'],
                cliente['codigo_documento'],
                cliente['ubicacion']
            ])
            
            frame_botones = ctk.CTkFrame(frame_fila, fg_color="transparent")
            frame_botones.pack(side="right", padx=5)
            
            btn_editar = ctk.CTkButton(
                frame_botones,
                text="✏️ Editar",
                command=lambda c=cliente: abrir_ventana_edicion(c, frame_lista, entry_buscar, label_contador),
                width=100,
                height=32,
                font=("Arial", 11, "bold"),
                fg_color=COLOR_ADVERTENCIA,
                hover_color=COLOR_ADVERTENCIA_HOVER,
                corner_radius=6
            )
            btn_editar.pack(side="left", padx=3)
            
            btn_desactivar = ctk.CTkButton(
                frame_botones,
                text="🗑️ Desactivar",
                command=lambda c=cliente: desactivar_cliente_confirm(c, frame_lista, entry_buscar, label_contador),
                width=110,
                height=32,
                font=("Arial", 11, "bold"),
                fg_color=COLOR_ERROR,
                hover_color=COLOR_ERROR_HOVER,
                corner_radius=6
            )
            btn_desactivar.pack(side="left", padx=3)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar clientes:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ERROR
        )
        label_error.pack(pady=50)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_clientes(frame_lista, entry_buscar, label_contador=None):
    cargar_clientes(frame_lista, entry_buscar, label_contador)


def abrir_ventana_edicion(cliente, frame_lista, entry_buscar=None, label_contador=None):
    cambios_realizados = {'hubo_cambios': False}
    
    ventana = ctk.CTkToplevel()
    ventana.title("✏️ Editar Cliente")
    ventana.geometry("500x600")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.configure(fg_color=COLOR_FONDO)  #  COLOR_FONDO en lugar de SECUNDARIO
    
    frame_form = ctk.CTkScrollableFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,  #  SECUNDARIO para el frame interno
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text=f"✏️ Editar Cliente",
        font=("Arial Black", 22, "bold"),  #  Tamaño consistente
        text_color=COLOR_ADVERTENCIA
    )
    label_titulo.pack(pady=(20, 10))
    
    label_id = ctk.CTkLabel(
        frame_form,
        text=f"ID: {cliente['id_cliente']}",
        font=("Arial", 11),
        text_color="#666666"
    )
    label_id.pack(pady=(0, 30))
    
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
        placeholder_text="Nombre del cliente",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        height=40,  #  Altura consistente
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        font=("Arial", 12),  #  Tamaño consistente
        text_color="#2C2C2E"
    )
    entry_nombre.insert(0, cliente['nombre'])
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
        placeholder_text="Apellido del cliente",
        placeholder_text_color="#2C2C2E",  #  PLACEHOLDER OSCURO
        height=40,  #  Altura consistente
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        font=("Arial", 12),  #  Tamaño consistente
        text_color="#2C2C2E"
    )
    entry_apellido.insert(0, cliente['apellido'])
    entry_apellido.pack(fill="x", pady=(0, 15))
    entry_apellido.bind("<KeyRelease>", registrar_cambio)  #  Detecta cambios
    
    # Campo: Ubicación
    label_ubicacion = ctk.CTkLabel(
        frame_campos,
        text="Ubicación *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  #  OSCURO
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
        values=ubicaciones_lista if ubicaciones_lista else ["Sin ubicaciones"],
        height=40,  #  Altura consistente
        fg_color=COLOR_FONDO_TERCIARIO,
        button_color=COLOR_ADVERTENCIA,
        button_hover_color=COLOR_ADVERTENCIA_HOVER,
        border_color=COLOR_BORDE,
        font=("Arial", 11),
        text_color="#2C2C2E",  #  OSCURO
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E",  #  OSCURO
        state="readonly"
    )
    
    ubicacion_actual = cliente['ubicacion']
    if ubicacion_actual in ubicaciones_lista:
        combo_ubicacion.set(ubicacion_actual)
    else:
        combo_ubicacion.set("Seleccione una ubicación")
    
    combo_ubicacion.pack(fill="x", pady=(0, 20))
    combo_ubicacion.bind("<<ComboboxSelected>>", registrar_cambio)  #  Detecta cambios
    
    # Frame info documento (no editable)
    frame_doc_info = ctk.CTkFrame(
        frame_campos,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=10,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_doc_info.pack(fill="x", pady=(0, 30))
    
    label_doc_titulo = ctk.CTkLabel(
        frame_doc_info,
        text="📄 Documento de Identidad (no editable)",
        font=("Arial", 11, "bold"),
        text_color="#666666"
    )
    label_doc_titulo.pack(pady=(10, 5), padx=15, anchor="w")
    
    label_doc_valor = ctk.CTkLabel(
        frame_doc_info,
        text=f"{cliente['tipo_identificacion']}: {cliente['codigo_documento']}",
        font=("Arial", 12),
        text_color="#2C2C2E"  # ✅ OSCURO
    )
    label_doc_valor.pack(pady=(0, 10), padx=15, anchor="w")
    
    def guardar_con_confirmacion():
        """Valida, confirma y guarda los cambios"""
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        ubicacion_sel = combo_ubicacion.get()
        
        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio", parent=ventana)
            entry_nombre.focus()
            return
        
        if not apellido:
            messagebox.showerror("Error", "El apellido es obligatorio", parent=ventana)
            entry_apellido.focus()
            return
        
        if ubicacion_sel == "Seleccione una ubicación":
            messagebox.showerror("Error", "Debe seleccionar una ubicación", parent=ventana)
            return
        
        nombre_valido, mensaje_nombre = ClienteBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana)
            entry_nombre.focus()
            return
        
        apellido_valido, mensaje_apellido = ClienteBL.validar_apellido(apellido)
        if not apellido_valido:
            messagebox.showerror("Error", mensaje_apellido, parent=ventana)
            entry_apellido.focus()
            return
        
        id_ubicacion = ubicaciones_dict.get(ubicacion_sel)
        if not id_ubicacion:
            messagebox.showerror("Error", "Ubicación inválida", parent=ventana)
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        respuesta = messagebox.askyesno(
            "Confirmar Actualización",
            f"¿Está seguro que desea guardar los cambios?\n\n"
            f"👤 Cliente: {nombre} {apellido}\n"
            f"📍 Ubicación: {ubicacion_sel}",
            parent=ventana
        )
        
        if not respuesta:
            return
        
        # Deshabilitar botones mientras se guarda
        btn_guardar.configure(text="⏳ Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana.update()
        
        try:
            exito, mensaje = ClienteBL.actualizar_cliente(
                id_cliente=cliente['id_cliente'],
                nombre=nombre,
                apellido=apellido,
                id_ubicacion=id_ubicacion,
                id_identidad=cliente['id_identidad']
            )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana)
                ventana.destroy()
                cargar_clientes(frame_lista, entry_buscar, label_contador)
            else:
                messagebox.showerror("❌ Error", mensaje, parent=ventana)
                btn_guardar.configure(text="💾 Guardar Cambios", state="normal")
                btn_cancelar.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar:\n{str(e)}", parent=ventana)
            btn_guardar.configure(text="💾 Guardar Cambios", state="normal")
            btn_cancelar.configure(state="normal")
            print(f"❌ Error al actualizar: {e}")
            import traceback
            traceback.print_exc()
    
    def cancelar_con_confirmacion():
        """Solicita confirmación antes de cancelar si hay cambios"""
        if cambios_realizados['hubo_cambios']:
            respuesta = messagebox.askyesno(
                "Confirmar Cancelación",
                "¿Está seguro que desea cancelar?\n\nSe perderán todos los cambios realizados.",
                parent=ventana
            )
            if respuesta:
                ventana.destroy()
        else:
            ventana.destroy()
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(10, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=cancelar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        height=50,
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        border_width=2,
        border_color=COLOR_ERROR,
        font=("Arial", 12, "bold"),
        corner_radius=10
    )
    btn_cancelar.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Guardar Cambios",
        command=guardar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        height=50,
        fg_color=COLOR_ADVERTENCIA,
        hover_color=COLOR_ADVERTENCIA_HOVER,
        font=("Arial", 12, "bold"),
        corner_radius=10
    )
    btn_guardar.pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    # Atajos de teclado
    entry_nombre.bind("<Return>", lambda e: entry_apellido.focus())
    entry_apellido.bind("<Return>", lambda e: guardar_con_confirmacion())
    ventana.bind("<Escape>", lambda e: cancelar_con_confirmacion())
    
    entry_nombre.focus()
    entry_nombre.select_range(0, 'end')
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
    y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
    ventana.geometry(f"+{x}+{y}")


def desactivar_cliente_confirm(cliente, frame_lista, entry_buscar=None, label_contador=None):
    nombre_completo = cliente['nombre_completo']
    id_cliente = cliente['id_cliente']
    
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar al cliente?\n\n"
        f"👤 {nombre_completo}\n\n"
        f"Esta acción marcará al cliente como inactivo."
    )
    
    if respuesta:
        exito, mensaje = ClienteBL.desactivar_cliente(id_cliente)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_clientes(frame_lista, entry_buscar, label_contador)
        else:
            messagebox.showerror("❌ Error", mensaje)