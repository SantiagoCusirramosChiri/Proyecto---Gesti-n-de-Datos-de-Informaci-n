# vista/modulos/documentos_listar.py

import customtkinter as ctk
from tkinter import messagebox
from logica.DocumentoBL import DocumentoBL
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_ADVERTENCIA
)


def mostrar(contenedor, id_empresa):
    """Muestra interfaz principal de gestión de documentos"""
    for widget in contenedor.winfo_children():
        widget.destroy()
    
    # Header
    frame_header = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_header.pack(fill="x", padx=20, pady=(20, 10))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="📄 Gestión de Documentos",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_refrescar = ctk.CTkButton(
        frame_header,
        text="🔄 Refrescar",
        command=lambda: cargar_documentos(frame_tabla, id_empresa, combo_filtro.get()),
        width=120,
        height=35,
        font=("Arial", 11, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        corner_radius=8
    )
    btn_refrescar.pack(side="right", padx=5)
    
    # Filtros
    frame_filtros = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_SECUNDARIO, corner_radius=10)
    frame_filtros.pack(fill="x", padx=20, pady=10)
    
    label_filtro = ctk.CTkLabel(
        frame_filtros,
        text="Filtrar por estado:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO
    )
    label_filtro.pack(side="left", padx=(15, 10), pady=10)
    
    combo_filtro = ctk.CTkComboBox(
        frame_filtros,
        values=["TODOS", "PENDIENTE", "EMITIDO", "ANULADO"],
        width=150,
        height=35,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        command=lambda e: cargar_documentos(frame_tabla, id_empresa, combo_filtro.get())
    )
    combo_filtro.set("TODOS")
    combo_filtro.pack(side="left", padx=10, pady=10)
    
    # Tabla
    frame_tabla = ctk.CTkScrollableFrame(
        contenedor,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10
    )
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    cargar_documentos(frame_tabla, id_empresa, "TODOS")


def cargar_documentos(frame_tabla, id_empresa, filtro="TODOS"):
    """Carga y muestra documentos de la empresa con filtro opcional"""
    for widget in frame_tabla.winfo_children():
        widget.destroy()
    
    try:
        documentos = DocumentoBL.obtener_documentos_empresa(id_empresa, filtro)
        
        if not documentos:
            label_vacio = ctk.CTkLabel(
                frame_tabla,
                text="📭 No hay documentos registrados",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=50)
            return
        
        # Cabecera
        frame_cabecera = ctk.CTkFrame(
            frame_tabla, 
            fg_color=COLOR_ROJO_PRIMARY, 
            corner_radius=8,
            height=45
        )
        frame_cabecera.pack(fill="x", padx=5, pady=(5, 10))
        frame_cabecera.pack_propagate(False)
        
        headers = [
            ("ID", 50),
            ("Tipo", 80),
            ("Fecha", 100),
            ("Cliente", 150),
            ("Forma Pago", 120),
            ("Moneda", 80),
            ("Estado", 90),
            ("Acciones", 180)
        ]
        
        x_pos = 10
        for header, width in headers:
            label = ctk.CTkLabel(
                frame_cabecera,
                text=header,
                font=("Arial", 11, "bold"),
                text_color="white",
                anchor="w",
                width=width
            )
            label.place(x=x_pos, rely=0.5, anchor="w")
            x_pos += width + 10
        
        # Filas
        for doc in documentos:
            crear_fila_documento(frame_tabla, doc, id_empresa)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar documentos:\n{str(e)}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def crear_fila_documento(frame_tabla, doc, id_empresa):
    """Crea una fila de documento en la tabla"""
    frame_fila = ctk.CTkFrame(
        frame_tabla,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=8,
        border_width=1,
        border_color=COLOR_BORDE,
        height=50
    )
    frame_fila.pack(fill="x", padx=5, pady=3)
    frame_fila.pack_propagate(False)
    
    # Color de estado
    emoji, color_tipo = DocumentoBL.formatear_estado_badge(doc['estado_doc'])
    
    if color_tipo == "success":
        color_estado = COLOR_EXITO
    elif color_tipo == "error":
        color_estado = COLOR_ROJO_PRIMARY
    else:
        color_estado = COLOR_ADVERTENCIA
    
    # Datos
    cliente_truncado = doc['cliente'][:20] + "..." if len(doc['cliente']) > 20 else doc['cliente']
    
    datos = [
        (str(doc['id_documento']), 50),
        (doc['tipo_doc'], 80),
        (doc['fecha_formateada'], 100),
        (cliente_truncado, 150),
        (doc['forma_pago'], 120),
        (doc['moneda'], 80),
    ]
    
    x_pos = 10
    for dato, width in datos:
        label = ctk.CTkLabel(
            frame_fila,
            text=dato,
            font=("Arial", 10),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=width
        )
        label.place(x=x_pos, rely=0.5, anchor="w")
        x_pos += width + 10
    
    # Badge de estado
    label_estado = ctk.CTkLabel(
        frame_fila,
        text=doc['estado_doc'],
        font=("Arial", 10, "bold"),
        text_color="white",
        fg_color=color_estado,
        corner_radius=5,
        width=80,
        height=25
    )
    label_estado.place(x=x_pos, rely=0.5, anchor="w")
    x_pos += 90 + 10
    
    # Botones de acción
    x_btn = x_pos
    
    # Botón Ver
    btn_ver = ctk.CTkButton(
        frame_fila,
        text="👁️",
        command=lambda: ver_detalle(doc),
        width=35,
        height=30,
        font=("Arial", 12),
        fg_color=COLOR_FONDO,
        hover_color=COLOR_BORDE,
        corner_radius=5
    )
    btn_ver.place(x=x_btn, rely=0.5, anchor="w")
    x_btn += 40
    
    # Botones solo para documentos pendientes
    if doc['estado_doc'] == "PENDIENTE":
        # Botón Emitir
        btn_emitir = ctk.CTkButton(
            frame_fila,
            text="✅",
            command=lambda: emitir_documento(doc['id_documento'], frame_tabla, id_empresa),
            width=35,
            height=30,
            font=("Arial", 12),
            fg_color=COLOR_EXITO,
            hover_color="#28a745",
            corner_radius=5
        )
        btn_emitir.place(x=x_btn, rely=0.5, anchor="w")
        x_btn += 40
        
        # Botón Anular
        btn_anular = ctk.CTkButton(
            frame_fila,
            text="❌",
            command=lambda: anular_documento(doc['id_documento'], frame_tabla, id_empresa),
            width=35,
            height=30,
            font=("Arial", 12),
            fg_color=COLOR_ROJO_PRIMARY,
            hover_color=COLOR_ROJO_HOVER,
            corner_radius=5
        )
        btn_anular.place(x=x_btn, rely=0.5, anchor="w")


def ver_detalle(documento):
    """Muestra ventana modal con detalle completo del documento"""
    ventana = ctk.CTkToplevel()
    ventana.title(f"Detalle Documento #{documento['id_documento']}")
    ventana.geometry("750x600")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)
    ventana.grab_set()
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 750) // 2
    y = (ventana.winfo_screenheight() - 600) // 2
    ventana.geometry(f"750x600+{x}+{y}")
    
    frame_principal = ctk.CTkScrollableFrame(
        ventana, 
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text=f"📄 Documento #{documento['id_documento']} - {documento['tipo_doc']}",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(10, 20))
    
    # Información del documento
    frame_info = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", padx=10, pady=10)
    
    # Color de estado
    emoji, color_tipo = DocumentoBL.formatear_estado_badge(documento['estado_doc'])
    
    if color_tipo == "success":
        color_badge = COLOR_EXITO
    elif color_tipo == "error":
        color_badge = COLOR_ROJO_PRIMARY
    else:
        color_badge = COLOR_ADVERTENCIA
    
    info = [
        ("📅 Fecha:", documento['fecha_formateada']),
        ("👤 Cliente:", documento['cliente']),
        ("💳 Forma de Pago:", documento['forma_pago']),
        ("💰 Moneda:", documento['moneda']),
    ]
    
    for label, valor in info:
        frame_item = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_item.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(
            frame_item,
            text=label,
            font=("Arial", 12, "bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=150
        ).pack(side="left")
        
        ctk.CTkLabel(
            frame_item,
            text=valor,
            font=("Arial", 12),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
    
    # Estado
    frame_estado = ctk.CTkFrame(frame_info, fg_color="transparent")
    frame_estado.pack(fill="x", padx=15, pady=8)
    
    ctk.CTkLabel(
        frame_estado,
        text="🏷️ Estado:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w",
        width=150
    ).pack(side="left")
    
    ctk.CTkLabel(
        frame_estado,
        text=f"{emoji} {documento['estado_doc']}",
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color=color_badge,
        corner_radius=5,
        width=120,
        height=30
    ).pack(side="left", padx=5)
    
    # Separador
    frame_sep = ctk.CTkFrame(frame_principal, height=2, fg_color=COLOR_BORDE)
    frame_sep.pack(fill="x", padx=10, pady=15)
    
    # Productos
    label_productos = ctk.CTkLabel(
        frame_principal,
        text="🛒 Productos",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_productos.pack(pady=(5, 10))
    
    frame_detalle = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_detalle.pack(fill="both", expand=True, padx=10, pady=10)
    
    try:
        detalles = DocumentoBL.obtener_detalle_documento(documento['id_documento'])
        
        if detalles:
            # Cabecera de productos
            frame_header = ctk.CTkFrame(
                frame_detalle, 
                fg_color=COLOR_ROJO_PRIMARY,
                corner_radius=8,
                height=40
            )
            frame_header.pack(fill="x", padx=10, pady=(10, 5))
            frame_header.pack_propagate(False)
            
            headers_prod = [
                ("Producto", 250),
                ("Cant.", 60),
                ("Subtotal", 90),
                ("IGV", 80),
                ("Total", 90)
            ]
            
            x_pos = 10
            for header, width in headers_prod:
                ctk.CTkLabel(
                    frame_header,
                    text=header,
                    font=("Arial", 11, "bold"),
                    text_color="white",
                    anchor="w",
                    width=width
                ).place(x=x_pos, rely=0.5, anchor="w")
                x_pos += width + 5
            
            # Lista de productos
            frame_lista = ctk.CTkScrollableFrame(
                frame_detalle,
                fg_color="transparent",
                height=200
            )
            frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
            
            for det in detalles:
                frame_item = ctk.CTkFrame(
                    frame_lista, 
                    fg_color=COLOR_FONDO_SECUNDARIO,
                    corner_radius=5,
                    height=40,
                    border_width=1,
                    border_color=COLOR_BORDE
                )
                frame_item.pack(fill="x", pady=3)
                frame_item.pack_propagate(False)
                
                producto_truncado = det['producto'][:35] + "..." if len(det['producto']) > 35 else det['producto']
                
                valores = [
                    (producto_truncado, 250),
                    (str(det['cantidad']), 60),
                    (f"S/ {det['subtotal']:.2f}", 90),
                    (f"S/ {det['igv']:.2f}", 80),
                    (f"S/ {det['importe']:.2f}", 90)
                ]
                
                x_pos = 10
                for valor, width in valores:
                    ctk.CTkLabel(
                        frame_item,
                        text=valor,
                        font=("Arial", 10),
                        text_color=COLOR_TEXTO,
                        anchor="w",
                        width=width
                    ).place(x=x_pos, rely=0.5, anchor="w")
                    x_pos += width + 5
            
            # Total
            total_general = DocumentoBL.calcular_total_documento(detalles)
            
            frame_total = ctk.CTkFrame(
                frame_detalle, 
                fg_color=COLOR_EXITO, 
                corner_radius=8,
                height=50
            )
            frame_total.pack(fill="x", padx=10, pady=(10, 10))
            frame_total.pack_propagate(False)
            
            ctk.CTkLabel(
                frame_total,
                text=f"💵 TOTAL GENERAL: S/ {total_general:.2f}",
                font=("Arial Black", 16, "bold"),
                text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(
                frame_detalle,
                text="📦 No hay productos en este documento",
                font=("Arial", 12),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).pack(pady=30)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar detalle:\n{str(e)}", parent=ventana)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Botón cerrar
    btn_cerrar = ctk.CTkButton(
        frame_principal,
        text="✖️ Cerrar",
        command=ventana.destroy,
        width=200,
        height=40,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        corner_radius=8
    )
    btn_cerrar.pack(pady=(10, 15))
    
    # Atajo
    ventana.bind("<Escape>", lambda e: ventana.destroy())


def emitir_documento(id_documento, frame_tabla, id_empresa):
    """Cambia estado de documento a EMITIDO y descuenta stock"""
    respuesta = messagebox.askyesno(
        "⚠️ Confirmar Emisión",
        f"¿Está seguro de EMITIR el documento #{id_documento}?\n\n"
        "Esta acción:\n"
        "• Descontará el stock de los productos\n"
        "• No podrá ser modificada posteriormente\n\n"
        "¿Desea continuar?",
        icon='warning'
    )
    
    if respuesta:
        try:
            exito, mensaje = DocumentoBL.actualizar_estado_documento(id_documento, "EMITIDO")
            
            if exito:
                messagebox.showinfo(
                    "✅ Éxito", 
                    f"{mensaje}\n\nEl stock ha sido actualizado."
                )
                cargar_documentos(frame_tabla, id_empresa, "TODOS")
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al emitir documento:\n{str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


def anular_documento(id_documento, frame_tabla, id_empresa):
    """Cambia estado de documento a ANULADO"""
    respuesta = messagebox.askyesno(
        "⚠️ Confirmar Anulación",
        f"¿Está seguro de ANULAR el documento #{id_documento}?\n\n"
        "⚠️ ADVERTENCIA:\n"
        "• Esta acción no se puede deshacer\n"
        "• El documento quedará marcado como anulado\n\n"
        "¿Desea continuar?",
        icon='warning'
    )
    
    if respuesta:
        try:
            exito, mensaje = DocumentoBL.actualizar_estado_documento(id_documento, "ANULADO")
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                cargar_documentos(frame_tabla, id_empresa, "TODOS")
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al anular documento:\n{str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()