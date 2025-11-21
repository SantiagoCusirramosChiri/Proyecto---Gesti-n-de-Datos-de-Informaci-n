# vista/modulos/guias_listar.py

import customtkinter as ctk
from tkinter import messagebox
from logica.GuiaBL import GuiaBL
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
    """Muestra interfaz principal de gestión de guías"""
    for widget in contenedor.winfo_children():
        widget.destroy()
    
    # Header
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
        command=lambda: cargar_guias(frame_tabla, id_empresa, combo_filtro.get()),
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
        command=lambda e: cargar_guias(frame_tabla, id_empresa, combo_filtro.get())
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
    
    cargar_guias(frame_tabla, id_empresa, "TODOS")


def cargar_guias(frame_tabla, id_empresa, filtro="TODOS"):
    """Carga y muestra guías de la empresa con filtro opcional"""
    for widget in frame_tabla.winfo_children():
        widget.destroy()
    
    try:
        guias = GuiaBL.obtener_guias_empresa(id_empresa, filtro)
        
        if not guias:
            label_vacio = ctk.CTkLabel(
                frame_tabla,
                text="📭 No hay guías de remisión registradas",
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
            ("N° Guía", 100),
            ("F. Emisión", 90),
            ("F. Traslado", 90),
            ("Motivo", 100),
            ("Origen", 120),
            ("Destino", 120),
            ("Conductor", 110),
            ("Estado", 80),
            ("Acciones", 150)
        ]
        
        x_pos = 10
        for header, width in headers:
            label = ctk.CTkLabel(
                frame_cabecera,
                text=header,
                font=("Arial", 10, "bold"),
                text_color="white",
                anchor="w",
                width=width
            )
            label.place(x=x_pos, rely=0.5, anchor="w")
            x_pos += width + 5
        
        # Filas
        for guia in guias:
            crear_fila_guia(frame_tabla, guia, id_empresa)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar guías:\n{str(e)}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def crear_fila_guia(frame_tabla, guia, id_empresa):
    """Crea una fila de guía en la tabla"""
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
    emoji, color_tipo = GuiaBL.formatear_estado_badge(guia['estado_guia'])
    
    if color_tipo == "success":
        color_estado = COLOR_EXITO
    elif color_tipo == "error":
        color_estado = COLOR_ROJO_PRIMARY
    else:
        color_estado = COLOR_ADVERTENCIA
    
    # Truncar textos largos
    motivo = guia.get('motivo_traslado', 'N/A')[:15] + "..." if len(guia.get('motivo_traslado', '')) > 15 else guia.get('motivo_traslado', 'N/A')
    origen = guia['punto_partida'][:17] + "..." if len(guia['punto_partida']) > 17 else guia['punto_partida']
    destino = guia['punto_llegada'][:17] + "..." if len(guia['punto_llegada']) > 17 else guia['punto_llegada']
    conductor = guia['conductor'][:15] + "..." if len(guia['conductor']) > 15 else guia['conductor']
    
    # Datos
    datos = [
        (guia['nro_guia'], 100),
        (guia['fecha_emision_formateada'], 90),
        (guia['fecha_traslado_formateada'], 90),
        (motivo, 100),
        (origen, 120),
        (destino, 120),
        (conductor, 110),
    ]
    
    x_pos = 10
    for dato, width in datos:
        label = ctk.CTkLabel(
            frame_fila,
            text=dato,
            font=("Arial", 9),
            text_color=COLOR_TEXTO,
            anchor="w",
            width=width
        )
        label.place(x=x_pos, rely=0.5, anchor="w")
        x_pos += width + 5
    
    # Badge de estado
    label_estado = ctk.CTkLabel(
        frame_fila,
        text=guia['estado_guia'],
        font=("Arial", 9, "bold"),
        text_color="white",
        fg_color=color_estado,
        corner_radius=5,
        width=70,
        height=25
    )
    label_estado.place(x=x_pos, rely=0.5, anchor="w")
    x_pos += 80 + 5
    
    # Botones de acción
    x_btn = x_pos
    
    # Botón Ver
    btn_ver = ctk.CTkButton(
        frame_fila,
        text="👁️",
        command=lambda: ver_detalle(guia),
        width=35,
        height=30,
        font=("Arial", 12),
        fg_color=COLOR_FONDO,
        hover_color=COLOR_BORDE,
        corner_radius=5
    )
    btn_ver.place(x=x_btn, rely=0.5, anchor="w")
    x_btn += 40
    
    # Botones solo para guías pendientes
    if guia['estado_guia'] == "PENDIENTE":
        # Botón Emitir
        btn_emitir = ctk.CTkButton(
            frame_fila,
            text="✅",
            command=lambda: emitir_guia(guia['id_guia'], frame_tabla, id_empresa),
            width=30,
            height=30,
            font=("Arial", 12),
            fg_color=COLOR_EXITO,
            hover_color="#28a745",
            corner_radius=5
        )
        btn_emitir.place(x=x_btn, rely=0.5, anchor="w")
        x_btn += 35
        
        # Botón Anular
        btn_anular = ctk.CTkButton(
            frame_fila,
            text="❌",
            command=lambda: anular_guia(guia['id_guia'], frame_tabla, id_empresa),
            width=30,
            height=30,
            font=("Arial", 12),
            fg_color=COLOR_ROJO_PRIMARY,
            hover_color=COLOR_ROJO_HOVER,
            corner_radius=5
        )
        btn_anular.place(x=x_btn, rely=0.5, anchor="w")


def ver_detalle(guia):
    """Muestra ventana modal con detalle completo de la guía"""
    ventana = ctk.CTkToplevel()
    ventana.title(f"Detalle Guía {guia['nro_guia']}")
    ventana.geometry("750x750")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)
    ventana.grab_set()
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - 750) // 2
    y = (ventana.winfo_screenheight() - 750) // 2
    ventana.geometry(f"750x750+{x}+{y}")
    
    frame_principal = ctk.CTkScrollableFrame(
        ventana, 
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text=f"🚚 Guía de Remisión {guia['nro_guia']}",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(10, 20))
    
    # Información de la guía
    frame_info = ctk.CTkFrame(
        frame_principal, 
        fg_color=COLOR_FONDO_TERCIARIO, 
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", padx=10, pady=10)
    
    # Color de estado
    emoji, color_tipo = GuiaBL.formatear_estado_badge(guia['estado_guia'])
    
    if color_tipo == "success":
        color_badge = COLOR_EXITO
    elif color_tipo == "error":
        color_badge = COLOR_ROJO_PRIMARY
    else:
        color_badge = COLOR_ADVERTENCIA
    
    info = [
        ("📅 Fecha Emisión:", guia['fecha_emision_formateada']),
        ("🗓️ Fecha Traslado:", guia['fecha_traslado_formateada']),
        ("📝 Motivo:", guia.get('motivo_traslado', 'N/A')),
        ("📍 Dirección Partida:", guia['punto_partida']),
        ("📍 Dirección Llegada:", guia['punto_llegada']),
        ("👤 Conductor:", guia['conductor']),
        ("🚗 Vehículo:", guia['vehiculo']),
        ("📄 Doc. Relacionado:", guia['documento_relacionado']),
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
            width=180
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
        width=180
    ).pack(side="left")
    
    ctk.CTkLabel(
        frame_estado,
        text=f"{emoji} {guia['estado_guia']}",
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
        text="📦 Detalle de Productos",
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
        detalles = GuiaBL.obtener_detalle_guia(guia['id_guia'])
        
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
                ("Producto", 220),
                ("Descripción", 200),
                ("Unidad", 80),
                ("Peso (kg)", 80),
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
                    height=50,
                    border_width=1,
                    border_color=COLOR_BORDE
                )
                frame_item.pack(fill="x", pady=3)
                frame_item.pack_propagate(False)
                
                producto_truncado = det['producto'][:30] + "..." if len(det['producto']) > 30 else det['producto']
                descripcion_truncada = det['descripcion'][:27] + "..." if len(det['descripcion']) > 27 else det['descripcion']
                
                valores = [
                    (producto_truncado, 220),
                    (descripcion_truncada, 200),
                    (det['unidad_medida'], 80),
                    (f"{det['peso_total']:.2f}", 80),
                    (det['modalidad'], 100)
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


def emitir_guia(id_guia, frame_tabla, id_empresa):
    """Cambia estado de guía a EMITIDO"""
    respuesta = messagebox.askyesno(
        "⚠️ Confirmar Emisión",
        f"¿Está seguro de EMITIR la guía #{id_guia}?\n\n"
        "Esta acción no podrá ser modificada posteriormente.\n\n"
        "¿Desea continuar?",
        icon='warning'
    )
    
    if respuesta:
        try:
            exito, mensaje = GuiaBL.actualizar_estado_guia(id_guia, "EMITIDO")
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                cargar_guias(frame_tabla, id_empresa, "TODOS")
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al emitir guía:\n{str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


def anular_guia(id_guia, frame_tabla, id_empresa):
    """Cambia estado de guía a ANULADO"""
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
            exito, mensaje = GuiaBL.actualizar_estado_guia(id_guia, "ANULADO")
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                cargar_guias(frame_tabla, id_empresa, "TODOS")
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al anular guía:\n{str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()