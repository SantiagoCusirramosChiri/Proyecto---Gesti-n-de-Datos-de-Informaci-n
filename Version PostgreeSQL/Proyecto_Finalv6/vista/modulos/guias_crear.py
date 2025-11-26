
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from logica.GuiaBL import GuiaBL
from logica.DocumentoBL import DocumentoBL
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


def mostrar(frame_contenido, id_empresa):
    id_valido, mensaje, id_empresa_norm = DocumentoBL.validar_id_empresa(id_empresa)
    if not id_valido:
        messagebox.showerror("Error", mensaje)
        return
    
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="🚚 Crear Guías de Remisión",
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
        text="🚚",
        font=("Arial", 100)
    )
    label_icono.pack(pady=(50, 20))
    
    label_descripcion = ctk.CTkLabel(
        frame_info,
        text="Cree guías de remisión para documentos emitidos",
        font=("Arial", 16),
        text_color="#666666"
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nueva Guía de Remisión",
        command=lambda: abrir_formulario_guia(frame_principal, id_empresa_norm),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=280,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


def abrir_formulario_guia(frame_principal, id_empresa):
    productos_guia = []
    
    # ============= CONTROL DE CAMBIOS =============
    cambios_realizados = {'hubo_cambios': False}
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Crear Nueva Guía de Remisión")
    ventana_form.geometry("900x950")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 900, 950)
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="🚚 Crear Nueva Guía de Remisión",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=30)
    
    frame_campos.productos_frame = None
    frame_campos.cambios_realizados = cambios_realizados
    
    crear_seccion_datos_guia(frame_campos, id_empresa, productos_guia)
    
    entry_partida, entry_llegada = crear_seccion_direcciones(frame_campos)
    
    combo_conductor, combo_vehiculo, conductores_dict, vehiculos_dict = crear_seccion_transporte(frame_campos)
    
    frame_productos_lista = crear_seccion_productos(frame_campos)
    frame_campos.productos_frame = frame_productos_lista
    
    if hasattr(frame_campos, 'documentos_lista') and frame_campos.documentos_lista:
        cargar_productos_documento(
            frame_campos.documentos_lista[0],
            frame_campos.documentos_dict,
            frame_productos_lista,
            productos_guia
        )
    
    #  guarda con confirmacion 
    def guardar_con_confirmacion():
        """Valida, confirma y guarda la guía"""
        nro_guia = frame_campos.entry_nro_guia.get().strip()
        
        if not frame_campos.documentos_lista:
            messagebox.showerror("Error", "No hay documentos emitidos disponibles", parent=ventana_form)
            return
        
        valido_nro, msg_nro = GuiaBL.validar_numero_guia(nro_guia)
        if not valido_nro:
            messagebox.showerror("Error", msg_nro, parent=ventana_form)
            frame_campos.entry_nro_guia.focus()
            return
        
        productos_seleccionados = [p for p in productos_guia if p['var'].get()]
        
        if len(productos_seleccionados) == 0:
            messagebox.showerror("Error", "Debe seleccionar al menos un producto", parent=ventana_form)
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        texto_documento = frame_campos.combo_documento.get()
        total_productos = len(productos_seleccionados)
        
        respuesta = messagebox.askyesno(
            "Confirmar Creación",
            f"¿Está seguro que desea crear esta guía de remisión?\n\n"
            f"🚚 Nro. Guía: {nro_guia}\n"
            f"📄 Documento: {texto_documento}\n"
            f"📦 Productos: {total_productos}",
            parent=ventana_form
        )
        
        if not respuesta:
            return
        
        guardar_guia_completa(
            frame_campos, entry_partida, entry_llegada,
            combo_conductor, combo_vehiculo, conductores_dict, vehiculos_dict,
            productos_guia, id_empresa, ventana_form
        )
    
    # cancela con confirmacion
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
    
    # botn
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=30, pady=(20, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=cancelar_con_confirmacion,
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
        text="💾 Crear Guía",
        command=guardar_con_confirmacion,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    ventana_form.bind("<Escape>", lambda e: cancelar_con_confirmacion())


def crear_seccion_datos_guia(frame_campos, id_empresa, productos_guia):
    # cambias registrar
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        frame_campos.cambios_realizados['hubo_cambios'] = True
    
    label_seccion1 = ctk.CTkLabel(
        frame_campos,
        text="📋 Datos de la Guía",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion1.pack(fill="x", pady=(0, 15))
    
    frame_row1 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row1.pack(fill="x", pady=(0, 15))
    
    # Nro de Guía
    frame_nro_guia = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_nro_guia.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_nro_guia = ctk.CTkLabel(
        frame_nro_guia,
        text="Nro. de Guía *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_nro_guia.pack(fill="x", pady=(0, 5))
    
    entry_nro_guia = ctk.CTkEntry(
        frame_nro_guia,
        placeholder_text="Ej: G001-00000001",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_nro_guia.pack(fill="x")
    entry_nro_guia.bind("<KeyRelease>", registrar_cambio)
    
    # Documento de Venta
    frame_doc = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_doc.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_doc = ctk.CTkLabel(
        frame_doc,
        text="Documento de Venta *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_doc.pack(fill="x", pady=(0, 5))
    
    documentos = GuiaBL.obtener_documentos_emitidos(id_empresa)
    documentos_dict = {}
    documentos_lista = []
    
    if documentos:
        documentos_dict = {f"{d[1]} #{d[0]}": d[0] for d in documentos}
        documentos_lista = list(documentos_dict.keys())
    
    def on_documento_change(e):
        registrar_cambio()
        if frame_campos.productos_frame:
            cargar_productos_documento(
                combo_documento.get(),
                documentos_dict,
                frame_campos.productos_frame,
                productos_guia
            )
    
    combo_documento = ctk.CTkComboBox(
        frame_doc,
        values=documentos_lista if documentos_lista else ["No hay documentos emitidos disponibles"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E",
        command=on_documento_change
    )
    combo_documento.pack(fill="x")
    if documentos_lista:
        combo_documento.set(documentos_lista[0])
    
    frame_campos.entry_nro_guia = entry_nro_guia
    frame_campos.combo_documento = combo_documento
    frame_campos.documentos_dict = documentos_dict
    frame_campos.documentos_lista = documentos_lista
    
    # Fechas
    frame_row2 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row2.pack(fill="x", pady=(0, 15))
    
    # Fecha Emisión
    frame_fecha_em = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_fecha_em.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_fecha_em = ctk.CTkLabel(
        frame_fecha_em,
        text="Fecha de Emisión *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_fecha_em.pack(fill="x", pady=(0, 5))
    
    entry_fecha_emision = ctk.CTkEntry(
        frame_fecha_em,
        placeholder_text="YYYY-MM-DD",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_fecha_emision.pack(fill="x")
    entry_fecha_emision.insert(0, datetime.now().strftime('%Y-%m-%d'))
    entry_fecha_emision.bind("<KeyRelease>", registrar_cambio)
    
    # Fecha Traslado
    frame_fecha_tr = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_fecha_tr.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_fecha_tr = ctk.CTkLabel(
        frame_fecha_tr,
        text="Fecha de Traslado *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_fecha_tr.pack(fill="x", pady=(0, 5))
    
    entry_fecha_traslado = ctk.CTkEntry(
        frame_fecha_tr,
        placeholder_text="YYYY-MM-DD",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_fecha_traslado.pack(fill="x")
    entry_fecha_traslado.insert(0, datetime.now().strftime('%Y-%m-%d'))
    entry_fecha_traslado.bind("<KeyRelease>", registrar_cambio)
    
    frame_campos.entry_fecha_emision = entry_fecha_emision
    frame_campos.entry_fecha_traslado = entry_fecha_traslado
    
    # Motivo
    label_motivo = ctk.CTkLabel(
        frame_campos,
        text="Motivo de Traslado *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_motivo.pack(fill="x", pady=(10, 5))
    
    entry_motivo = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Venta, Traslado entre locales, etc.",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_motivo.pack(fill="x", pady=(0, 15))
    entry_motivo.bind("<KeyRelease>", registrar_cambio)
    
    frame_campos.entry_motivo = entry_motivo


def crear_seccion_direcciones(frame_campos):
    def registrar_cambio(event=None):
        frame_campos.cambios_realizados['hubo_cambios'] = True
    
    label_seccion2 = ctk.CTkLabel(
        frame_campos,
        text="📍 Direcciones",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion2.pack(fill="x", pady=(20, 15))
    
    # Punto de Partida
    label_partida = ctk.CTkLabel(
        frame_campos,
        text="Punto de Partida *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_partida.pack(fill="x", pady=(0, 5))
    
    entry_partida = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Dirección completa de origen",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_partida.pack(fill="x", pady=(0, 15))
    entry_partida.bind("<KeyRelease>", registrar_cambio)
    
    # Punto de Llegada
    label_llegada = ctk.CTkLabel(
        frame_campos,
        text="Punto de Llegada *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_llegada.pack(fill="x", pady=(0, 5))
    
    entry_llegada = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Dirección completa de destino",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_llegada.pack(fill="x", pady=(0, 15))
    entry_llegada.bind("<KeyRelease>", registrar_cambio)
    
    return entry_partida, entry_llegada


def crear_seccion_transporte(frame_campos):
    def registrar_cambio(event=None):
        frame_campos.cambios_realizados['hubo_cambios'] = True
    
    label_seccion3 = ctk.CTkLabel(
        frame_campos,
        text="🚛 Transporte",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion3.pack(fill="x", pady=(20, 15))
    
    frame_row3 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row3.pack(fill="x", pady=(0, 15))
    
    # Conductor
    frame_conductor = ctk.CTkFrame(frame_row3, fg_color="transparent")
    frame_conductor.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_conductor = ctk.CTkLabel(
        frame_conductor,
        text="Conductor *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_conductor.pack(fill="x", pady=(0, 5))
    
    conductores = GuiaBL.obtener_conductores_combo()
    conductores_dict = {c[1]: c[0] for c in conductores}
    conductores_lista = list(conductores_dict.keys())
    
    combo_conductor = ctk.CTkComboBox(
        frame_conductor,
        values=conductores_lista if conductores_lista else ["No hay conductores"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_conductor.pack(fill="x")
    if conductores_lista:
        combo_conductor.set(conductores_lista[0])
    combo_conductor.bind("<<ComboboxSelected>>", registrar_cambio)
    
    # Vehículo
    frame_vehiculo = ctk.CTkFrame(frame_row3, fg_color="transparent")
    frame_vehiculo.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_vehiculo = ctk.CTkLabel(
        frame_vehiculo,
        text="Vehículo *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_vehiculo.pack(fill="x", pady=(0, 5))
    
    vehiculos = GuiaBL.obtener_vehiculos_combo()
    vehiculos_dict = {v[1]: v[0] for v in vehiculos}
    vehiculos_lista = list(vehiculos_dict.keys())
    
    combo_vehiculo = ctk.CTkComboBox(
        frame_vehiculo,
        values=vehiculos_lista if vehiculos_lista else ["No hay vehículos"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E",  # ✅ OSCURO
        button_color=COLOR_EXITO,
        button_hover_color=COLOR_EXITO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color="#2C2C2E"
    )
    combo_vehiculo.pack(fill="x")
    if vehiculos_lista:
        combo_vehiculo.set(vehiculos_lista[0])
    combo_vehiculo.bind("<<ComboboxSelected>>", registrar_cambio)
    
    return combo_conductor, combo_vehiculo, conductores_dict, vehiculos_dict


def crear_seccion_productos(frame_campos):
    label_seccion4 = ctk.CTkLabel(
        frame_campos,
        text="📦 Productos del Documento",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion4.pack(fill="x", pady=(20, 15))
    
    frame_productos_lista = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_productos_lista.pack(fill="both", expand=True)
    
    return frame_productos_lista


def cargar_productos_documento(texto_documento, documentos_dict, frame_productos, productos_guia):
    for widget in frame_productos.winfo_children():
        widget.destroy()
    
    productos_guia.clear()
    
    if not texto_documento or texto_documento == "No hay documentos emitidos disponibles":
        label_vacio = ctk.CTkLabel(
            frame_productos,
            text="📦 Seleccione un documento para ver los productos",
            font=("Arial", 14),
            text_color="#666666"
        )
        label_vacio.pack(pady=30)
        return
    
    try:
        id_documento = documentos_dict.get(texto_documento)
        if not id_documento:
            return
        
        productos = GuiaBL.obtener_productos_documento(id_documento)
        
        if not productos:
            label_vacio = ctk.CTkLabel(
                frame_productos,
                text="📦 No hay productos en este documento",
                font=("Arial", 14),
                text_color="#666666"
            )
            label_vacio.pack(pady=30)
            return
        
        frame_lista = ctk.CTkScrollableFrame(
            frame_productos,
            fg_color=COLOR_FONDO_TERCIARIO,
            corner_radius=10,
            height=200
        )
        frame_lista.pack(fill="both", expand=True)
        
        label_instruccion = ctk.CTkLabel(
            frame_lista,
            text="✓ Seleccione los productos que desea incluir en la guía:",
            font=("Arial", 11, "bold"),
            text_color="#2C2C2E"  # ✅ OSCURO
        )
        label_instruccion.pack(pady=(10, 15), padx=10, anchor="w")
        
        for prod in productos:
            var_check = ctk.BooleanVar(value=True)
            
            frame_item = ctk.CTkFrame(
                frame_lista, 
                fg_color=COLOR_FONDO_SECUNDARIO, 
                corner_radius=8,
                border_width=1,
                border_color=COLOR_BORDE
            )
            frame_item.pack(fill="x", padx=10, pady=5)
            
            checkbox = ctk.CTkCheckBox(
                frame_item,
                text="",
                variable=var_check,
                command=lambda p=prod, v=var_check: toggle_producto(p, v, productos_guia),
                width=30,
                checkbox_width=25,
                checkbox_height=25,
                fg_color=COLOR_EXITO,
                hover_color=COLOR_EXITO_HOVER
            )
            checkbox.pack(side="left", padx=10, pady=10)
            
            label_info = ctk.CTkLabel(
                frame_item,
                text=f"{prod[1]} | Cantidad: {prod[2]} {prod[3]}",
                font=("Arial", 11),
                text_color="#2C2C2E",  # ✅ OSCURO
                anchor="w"
            )
            label_info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            productos_guia.append({
                'id': prod[0],
                'nombre': prod[1],
                'cantidad': prod[2],
                'unidad_medida': prod[3],
                'var': var_check
            })
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar productos:\n{str(e)}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def toggle_producto(producto, var_check, productos_guia):
    id_prod = producto[0]
    
    if var_check.get():
        existe = any(p['id'] == id_prod for p in productos_guia)
        if not existe:
            productos_guia.append({
                'id': producto[0],
                'nombre': producto[1],
                'cantidad': producto[2],
                'unidad_medida': producto[3],
                'var': var_check
            })
    else:
        productos_guia[:] = [p for p in productos_guia if p['id'] != id_prod]


def guardar_guia_completa(frame_campos, entry_partida, entry_llegada, combo_conductor,
                          combo_vehiculo, conductores_dict, vehiculos_dict,
                          productos_guia, id_empresa, ventana_form):
    nro_guia = frame_campos.entry_nro_guia.get().strip()
    fecha_emision = frame_campos.entry_fecha_emision.get()
    fecha_traslado = frame_campos.entry_fecha_traslado.get()
    motivo = frame_campos.entry_motivo.get().strip()
    dir_partida = entry_partida.get().strip()
    dir_llegada = entry_llegada.get().strip()
    
    if not frame_campos.documentos_lista:
        messagebox.showerror("Error", "No hay documentos emitidos disponibles", parent=ventana_form)
        return
    
    valido_nro, msg_nro = GuiaBL.validar_numero_guia(nro_guia)
    if not valido_nro:
        messagebox.showerror("Error", msg_nro, parent=ventana_form)
        frame_campos.entry_nro_guia.focus()
        return
    
    if GuiaBL.verificar_guia_existe(nro_guia):
        messagebox.showerror("Error", f"El número de guía {nro_guia} ya existe", parent=ventana_form)
        frame_campos.entry_nro_guia.focus()
        return
    
    if not motivo:
        messagebox.showerror("Error", "El motivo de traslado es obligatorio", parent=ventana_form)
        frame_campos.entry_motivo.focus()
        return
    
    if not dir_partida:
        messagebox.showerror("Error", "La dirección de partida es obligatoria", parent=ventana_form)
        entry_partida.focus()
        return
    
    if not dir_llegada:
        messagebox.showerror("Error", "La dirección de llegada es obligatoria", parent=ventana_form)
        entry_llegada.focus()
        return
    
    valido_fecha, msg_fecha = GuiaBL.validar_fecha_traslado(fecha_emision, fecha_traslado)
    if not valido_fecha:
        messagebox.showerror("Error", msg_fecha, parent=ventana_form)
        frame_campos.entry_fecha_traslado.focus()
        return
    
    productos_seleccionados = [p for p in productos_guia if p['var'].get()]
    
    if len(productos_seleccionados) == 0:
        messagebox.showerror("Error", "Debe seleccionar al menos un producto", parent=ventana_form)
        return
    
    try:
        texto_documento = frame_campos.combo_documento.get()
        id_doc_venta = frame_campos.documentos_dict[texto_documento]
        
        texto_conductor = combo_conductor.get()
        id_conductor = conductores_dict[texto_conductor]
        
        texto_vehiculo = combo_vehiculo.get()
        id_vehiculo = vehiculos_dict[texto_vehiculo]
        
        exito, mensaje, id_guia = GuiaBL.crear_guia_completa(
            id_doc_venta=id_doc_venta,
            nro_guia=nro_guia,
            fecha_emision=fecha_emision,
            fecha_traslado=fecha_traslado,
            motivo=motivo,
            dir_partida=dir_partida,
            dir_llegada=dir_llegada,
            id_conductor=id_conductor,
            id_vehiculo=id_vehiculo,
            productos=productos_seleccionados
        )
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
            ventana_form.destroy()
        else:
            messagebox.showerror("❌ Error", mensaje, parent=ventana_form)
        
    except KeyError as e:
        messagebox.showerror("Error", f"Error al obtener datos: {str(e)}", parent=ventana_form)
        print(f"❌ KeyError: {e}")
        import traceback
        traceback.print_exc()
    
    except Exception as e:
        messagebox.showerror("❌ Error", f"Error al crear guía:\n{str(e)}", parent=ventana_form)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")