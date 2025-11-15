# guias_listar.py

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


# Muestra interfaz principal de gestión de guías con filtros
def mostrar(contenedor, id_empresa):
    for widget in contenedor.winfo_children():
        widget.destroy()
    
    frame_header = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_header.pack(fill="x", padx=20, pady=(20, 10))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="🚚 Gestión de Guías de Remisión",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_refrescar = ctk.CTkButton(
        frame_header,
        text="🔄 Refrescar",
        command=lambda: cargar_guias(frame_tabla, id_empresa),
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
        command=lambda e: filtrar_guias(frame_tabla, id_empresa, combo_filtro.get())
    )
    combo_filtro.set("TODOS")
    combo_filtro.pack(side="left", padx=10, pady=10)
    
    frame_tabla = ctk.CTkScrollableFrame(
        contenedor,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10
    )
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    cargar_guias(frame_tabla, id_empresa)


# Carga y muestra listado de guías con filtro de estado
def cargar_guias(frame_tabla, id_empresa, filtro="TODOS"):
    for widget in frame_tabla.winfo_children():
        widget.destroy()
    
    try:
        guias = procedimientos.obtener_guias_empresa(id_empresa)
        
        if filtro != "TODOS":
            guias = [guia for guia in guias if guia[9] == filtro]
        
        if not guias:
            label_vacio = ctk.CTkLabel(
                frame_tabla,
                text="📭 No hay guías de remisión registradas",
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
            ("Nro. Guía", 130),
            ("Doc. Venta", 90),
            ("Fecha Emisión", 110),
            ("Fecha Traslado", 115),
            ("Conductor", 130),
            ("Vehículo", 130),
            ("Estado", 90),
            ("Acciones", 150)
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
            x_pos += width + 5
        
        for guia in guias:
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
            
            if guia[9] == "EMITIDO":
                color_estado = COLOR_EXITO
            elif guia[9] == "ANULADO":
                color_estado = COLOR_ROJO_PRIMARY
            else:
                color_estado = COLOR_ADVERTENCIA
            
            fecha_emision = guia[2].strftime("%d/%m/%Y") if isinstance(guia[2], datetime) else str(guia[2])
            fecha_traslado = guia[3].strftime("%d/%m/%Y") if isinstance(guia[3], datetime) else str(guia[3])
            
            datos = [
                (str(guia[0]), 50),
                (guia[1], 130),
                (f"{guia[10]} #{guia[11]}", 90),
                (fecha_emision, 110),
                (fecha_traslado, 115),
                (guia[7][:15] + "..." if len(guia[7]) > 15 else guia[7], 130),
                (guia[8][:15] + "..." if len(guia[8]) > 15 else guia[8], 130),
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
                x_pos += width + 5
            
            label_estado = ctk.CTkLabel(
                frame_fila,
                text=guia[9],
                font=("Arial", 10, "bold"),
                text_color="white",
                fg_color=color_estado,
                corner_radius=5,
                width=80,
                height=25
            )
            label_estado.place(x=x_pos, rely=0.5, anchor="w")
            x_pos += 90 + 5
            
            x_btn = x_pos
            
            btn_ver = ctk.CTkButton(
                frame_fila,
                text="👁️",
                command=lambda g=guia: ver_detalle(g),
                width=35,
                height=30,
                font=("Arial", 12),
                fg_color=COLOR_FONDO,
                hover_color=COLOR_BORDE,
                corner_radius=5
            )
            btn_ver.place(x=x_btn, rely=0.5, anchor="w")
            x_btn += 40
            
            if guia[9] == "PENDIENTE":
                btn_emitir = ctk.CTkButton(
                    frame_fila,
                    text="✅",
                    command=lambda id_guia=guia[0]: emitir_guia(id_guia, frame_tabla, id_empresa),
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
                    command=lambda id_guia=guia[0]: anular_guia(id_guia, frame_tabla, id_empresa),
                    width=35,
                    height=30,
                    font=("Arial", 12),
                    fg_color=COLOR_ROJO_PRIMARY,
                    hover_color=COLOR_ROJO_HOVER,
                    corner_radius=5
                )
                btn_anular.place(x=x_btn, rely=0.5, anchor="w")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar guías:\n{str(e)}")


# Aplica filtro de estado a la lista de guías
def filtrar_guias(frame_tabla, id_empresa, filtro):
    cargar_guias(frame_tabla, id_empresa, filtro)


# Abre ventana modal con información detallada de la guía
def ver_detalle(guia):
    ventana = ctk.CTkToplevel()
    ventana.title(f"Detalle Guía de Remisión {guia[1]}")
    ventana.geometry("800x700")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)
    ventana.grab_set()
    
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 800) // 2
    y = (ventana.winfo_screenheight() - 700) // 2
    ventana.geometry(f"800x700+{x}+{y}")
    
    frame_principal = ctk.CTkScrollableFrame(
        ventana, 
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text=f"🚚 Guía de Remisión: {guia[1]}",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(10, 20))
    
    if guia[9] == "EMITIDO":
        color_badge = COLOR_EXITO
    elif guia[9] == "ANULADO":
        color_badge = COLOR_ROJO_PRIMARY
    else:
        color_badge = COLOR_ADVERTENCIA
    
    label_seccion1 = ctk.CTkLabel(
        frame_principal,
        text="📋 Información General",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion1.pack(fill="x", padx=10, pady=(5, 10))
    
    frame_info1 = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info1.pack(fill="x", padx=10, pady=10)
    
    fecha_emision = guia[2].strftime("%d/%m/%Y") if isinstance(guia[2], datetime) else str(guia[2])
    fecha_traslado = guia[3].strftime("%d/%m/%Y") if isinstance(guia[3], datetime) else str(guia[3])
    
    info1 = [
        ("🔢 ID Guía:", str(guia[0])),
        ("📄 Nro. Guía:", guia[1]),
        ("📋 Doc. Venta:", f"{guia[10]} #{guia[11]}"),
        ("📅 Fecha Emisión:", fecha_emision),
        ("🚀 Fecha Inicio Traslado:", fecha_traslado),
        ("📝 Motivo Traslado:", guia[4]),
    ]
    
    for label, valor in info1:
        frame_item = ctk.CTkFrame(frame_info1, fg_color="transparent")
        frame_item.pack(fill="x", padx=15, pady=6)
        
        ctk.CTkLabel(
            frame_item,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=180
        ).pack(side="left")
        
        ctk.CTkLabel(
            frame_item,
            text=valor,
            font=("Arial", 11),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
    
    frame_estado = ctk.CTkFrame(frame_info1, fg_color="transparent")
    frame_estado.pack(fill="x", padx=15, pady=6)
    
    ctk.CTkLabel(
        frame_estado,
        text="🏷️ Estado:",
        font=("Arial", 11, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w",
        width=180
    ).pack(side="left")
    
    ctk.CTkLabel(
        frame_estado,
        text=guia[9],
        font=("Arial", 11, "bold"),
        text_color="white",
        fg_color=color_badge,
        corner_radius=5,
        width=100,
        height=28
    ).pack(side="left", padx=5)
    
    label_seccion2 = ctk.CTkLabel(
        frame_principal,
        text="📍 Direcciones",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion2.pack(fill="x", padx=10, pady=(15, 10))
    
    frame_info2 = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info2.pack(fill="x", padx=10, pady=10)
    
    info2 = [
        ("📤 Dirección de Partida:", guia[5]),
        ("📥 Dirección de Llegada:", guia[6]),
    ]
    
    for label, valor in info2:
        frame_item = ctk.CTkFrame(frame_info2, fg_color="transparent")
        frame_item.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(
            frame_item,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=180
        ).pack(side="left", anchor="n", pady=2)
        
        ctk.CTkLabel(
            frame_item,
            text=valor,
            font=("Arial", 11),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w",
            wraplength=500,
            justify="left"
        ).pack(side="left", fill="x", expand=True)
    
    label_seccion3 = ctk.CTkLabel(
        frame_principal,
        text="🚛 Datos del Transporte",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion3.pack(fill="x", padx=10, pady=(15, 10))
    
    frame_info3 = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info3.pack(fill="x", padx=10, pady=10)
    
    info3 = [
        ("👨‍✈️ Conductor:", guia[7]),
        ("🚙 Vehículo:", guia[8]),
    ]
    
    for label, valor in info3:
        frame_item = ctk.CTkFrame(frame_info3, fg_color="transparent")
        frame_item.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(
            frame_item,
            text=label,
            font=("Arial", 11, "bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=180
        ).pack(side="left")
        
        ctk.CTkLabel(
            frame_item,
            text=valor,
            font=("Arial", 11),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
    
    frame_sep = ctk.CTkFrame(frame_principal, height=2, fg_color=COLOR_BORDE)
    frame_sep.pack(fill="x", padx=10, pady=15)
    
    label_productos = ctk.CTkLabel(
        frame_principal,
        text="📦 Productos a Trasladar",
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
        detalles = procedimientos.obtener_detalle_guia(guia[0])
        
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
                ("Producto", 200),
                ("Descripción", 200),
                ("Unidad", 80),
                ("Peso (Kg)", 90),
                ("Modalidad", 100)
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
                height=150
            )
            frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
            
            for det in detalles:
                frame_item = ctk.CTkFrame(
                    frame_lista, 
                    fg_color=COLOR_FONDO_SECUNDARIO,
                    corner_radius=5,
                    height=45,
                    border_width=1,
                    border_color=COLOR_BORDE
                )
                frame_item.pack(fill="x", pady=3)
                frame_item.pack_propagate(False)
                
                valores = [
                    (det[0][:28] + "..." if len(det[0]) > 28 else det[0], 200),
                    (det[1][:28] + "..." if len(det[1]) > 28 else det[1], 200),
                    (det[2], 80),
                    (f"{det[3]:.2f}" if det[3] else "0.00", 90),
                    (det[4], 100)
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
        else:
            ctk.CTkLabel(
                frame_detalle,
                text="📦 No hay productos en esta guía",
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


# Cambia estado de guía a EMITIDO tras confirmación
def emitir_guia(id_guia, frame_tabla, id_empresa):
    respuesta = messagebox.askyesno(
        "⚠️ Confirmar Emisión",
        f"¿Está seguro de EMITIR la guía #{id_guia}?\n\n"
        "Esta acción:\n"
        "• Confirmará el traslado de mercancías\n"
        "• No podrá ser modificada posteriormente\n\n"
        "¿Desea continuar?",
        icon='warning'
    )
    
    if respuesta:
        try:
            procedimientos.actualizar_estado_guia(id_guia, "EMITIDO")
            messagebox.showinfo(
                "✅ Éxito", 
                f"Guía #{id_guia} emitida correctamente\n\nEl traslado ha sido confirmado."
            )
            cargar_guias(frame_tabla, id_empresa)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al emitir guía:\n{str(e)}")


# Cambia estado de guía a ANULADO tras confirmación
def anular_guia(id_guia, frame_tabla, id_empresa):
    respuesta = messagebox.askyesno(
        "⚠️ Confirmar Anulación",
        f"¿Está seguro de ANULAR la guía #{id_guia}?\n\n"
        "⚠️ ADVERTENCIA:\n"
        "• Esta acción no se puede deshacer\n"
        "• La guía quedará marcada como anulada\n\n"
        "¿Desea continuar?",
        icon='warning'
    )
    
    if respuesta:
        try:
            procedimientos.actualizar_estado_guia(id_guia, "ANULADO")
            messagebox.showinfo(
                "✅ Éxito", 
                f"Guía #{id_guia} anulada correctamente"
            )
            cargar_guias(frame_tabla, id_empresa)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al anular guía:\n{str(e)}")