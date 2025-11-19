# documentos_listar.py

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from datos import procedimientos
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


# Muestra interfaz principal de gestión de documentos
def mostrar(contenedor, id_empresa):
    for widget in contenedor.winfo_children():
        widget.destroy()
    
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
        command=lambda: cargar_documentos(frame_tabla, id_empresa),
        width=120,
        height=35,
        font=("Arial", 11, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        corner_radius=8
    )
    btn_refrescar.pack(side="right", padx=5)
    
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
        command=lambda e: filtrar_documentos(frame_tabla, id_empresa, combo_filtro.get())
    )
    combo_filtro.set("TODOS")
    combo_filtro.pack(side="left", padx=10, pady=10)
    
    frame_tabla = ctk.CTkScrollableFrame(
        contenedor,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10
    )
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    cargar_documentos(frame_tabla, id_empresa)


# Carga y muestra documentos de la empresa con filtro opcional
def cargar_documentos(frame_tabla, id_empresa, filtro="TODOS"):
    for widget in frame_tabla.winfo_children():
        widget.destroy()
    
    try:
        documentos = procedimientos.obtener_documentos_empresa(id_empresa)
        
        if filtro != "TODOS":
            documentos = [doc for doc in documentos if doc[6] == filtro]
        
        if not documentos:
            label_vacio = ctk.CTkLabel(
                frame_tabla,
                text="📭 No hay documentos registrados",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=50)
            return
        
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
        
        for doc in documentos:
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
            
            if doc[6] == "EMITIDO":
                color_estado = COLOR_EXITO
            elif doc[6] == "ANULADO":
                color_estado = COLOR_ROJO_PRIMARY
            else:
                color_estado = COLOR_ADVERTENCIA
            
            fecha_str = doc[2].strftime("%d/%m/%Y") if isinstance(doc[2], datetime) else str(doc[2])
            
            datos = [
                (str(doc[0]), 50),
                (doc[1], 80),
                (fecha_str, 100),
                (doc[3][:20] + "..." if len(doc[3]) > 20 else doc[3], 150),
                (doc[4], 120),
                (doc[5], 80),
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
            
            label_estado = ctk.CTkLabel(
                frame_fila,
                text=doc[6],
                font=("Arial", 10, "bold"),
                text_color="white",
                fg_color=color_estado,
                corner_radius=5,
                width=80,
                height=25
            )
            label_estado.place(x=x_pos, rely=0.5, anchor="w")
            x_pos += 90 + 10
            
            x_btn = x_pos
            
            btn_ver = ctk.CTkButton(
                frame_fila,
                text="👁️",
                command=lambda d=doc: ver_detalle(d),
                width=35,
                height=30,
                font=("Arial", 12),
                fg_color=COLOR_FONDO,
                hover_color=COLOR_BORDE,
                corner_radius=5
            )
            btn_ver.place(x=x_btn, rely=0.5, anchor="w")
            x_btn += 40
            
            if doc[6] == "PENDIENTE":
                btn_emitir = ctk.CTkButton(
                    frame_fila,
                    text="✅",
                    command=lambda id_doc=doc[0]: emitir_documento(id_doc, frame_tabla, id_empresa),
                    width=35,
                    height=30,
                    font=("Arial", 12),
                    fg_color=COLOR_EXITO,
                    hover_color="#28a745",
                    corner_radius=5
                )
                btn_emitir.place(x=x_btn, rely=0.5, anchor="w")
                x_btn += 40
                
                btn_anular = ctk.CTkButton(
                    frame_fila,
                    text="❌",
                    command=lambda id_doc=doc[0]: anular_documento(id_doc, frame_tabla, id_empresa),
                    width=35,
                    height=30,
                    font=("Arial", 12),
                    fg_color=COLOR_ROJO_PRIMARY,
                    hover_color=COLOR_ROJO_HOVER,
                    corner_radius=5
                )
                btn_anular.place(x=x_btn, rely=0.5, anchor="w")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar documentos:\n{str(e)}")


# Filtra documentos según estado seleccionado
def filtrar_documentos(frame_tabla, id_empresa, filtro):
    cargar_documentos(frame_tabla, id_empresa, filtro)


# Muestra ventana modal con detalle completo del documento
def ver_detalle(documento):
    ventana = ctk.CTkToplevel()
    ventana.title(f"Detalle Documento #{documento[0]}")
    ventana.geometry("750x600")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)
    ventana.grab_set()
    
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
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text=f"📄 Documento #{documento[0]} - {documento[1]}",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(10, 20))
    
    frame_info = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", padx=10, pady=10)
    
    if documento[6] == "EMITIDO":
        color_badge = COLOR_EXITO
    elif documento[6] == "ANULADO":
        color_badge = COLOR_ROJO_PRIMARY
    else:
        color_badge = COLOR_ADVERTENCIA
    
    info = [
        ("📅 Fecha:", documento[2].strftime("%d/%m/%Y") if isinstance(documento[2], datetime) else str(documento[2])),
        ("👤 Cliente:", documento[3]),
        ("💳 Forma de Pago:", documento[4]),
        ("💰 Moneda:", documento[5]),
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
        text=documento[6],
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color=color_badge,
        corner_radius=5,
        width=100,
        height=30
    ).pack(side="left", padx=5)
    
    frame_sep = ctk.CTkFrame(frame_principal, height=2, fg_color=COLOR_BORDE)
    frame_sep.pack(fill="x", padx=10, pady=15)
    
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
        detalles = procedimientos.obtener_detalle_documento(documento[0])
        
        if detalles:
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
            
            frame_lista = ctk.CTkScrollableFrame(
                frame_detalle,
                fg_color="transparent",
                height=200
            )
            frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
            
            total_general = 0
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
                
                valores = [
                    (det[0][:35] + "..." if len(det[0]) > 35 else det[0], 250),
                    (str(det[1]), 60),
                    (f"S/ {det[2]:.2f}", 90),
                    (f"S/ {det[3]:.2f}", 80),
                    (f"S/ {det[4]:.2f}", 90)
                ]
                
                total_general += det[4]
                
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


# Cambia estado de documento a EMITIDO y descuenta stock
def emitir_documento(id_documento, frame_tabla, id_empresa):
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
            procedimientos.actualizar_estado_documento(id_documento, "EMITIDO")
            messagebox.showinfo(
                "✅ Éxito", 
                f"Documento #{id_documento} emitido correctamente\n\nEl stock ha sido actualizado."
            )
            cargar_documentos(frame_tabla, id_empresa)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al emitir documento:\n{str(e)}")


# Cambia estado de documento a ANULADO
def anular_documento(id_documento, frame_tabla, id_empresa):
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
            procedimientos.actualizar_estado_documento(id_documento, "ANULADO")
            messagebox.showinfo(
                "✅ Éxito", 
                f"Documento #{id_documento} anulado correctamente"
            )
            cargar_documentos(frame_tabla, id_empresa)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al anular documento:\n{str(e)}")