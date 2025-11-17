# inventario_movimientos.py

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
    COLOR_ERROR,
    COLOR_ADVERTENCIA,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra interfaz de historial de movimientos de inventario con búsqueda
def mostrar(frame_contenido, id_empresa):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="📊 Movimientos de Inventario",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_movimientos(frame_lista, entry_buscar),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_actualizar.pack(side="right", padx=5)
    
    frame_info = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", pady=(0, 15))
    
    label_info = ctk.CTkLabel(
        frame_info,
        text="ℹ️ Mostrando los últimos 100 movimientos de stock (Salidas por documentos emitidos)",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_info.pack(pady=10, padx=15)
    
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
        placeholder_text="Buscar por producto o tipo de documento...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_movimientos(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_movimientos(frame_lista, entry_buscar)


# Carga y muestra tabla de movimientos con filtro de búsqueda
def cargar_movimientos(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_movimientos_inventario()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="📊 No hay movimientos de inventario registrados",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID Doc', 'Tipo Doc', 'Fecha', 'Producto', 'Cantidad', 'Movimiento', 'Estado'],
            [80, 100, 100, 250, 100, 120, 100]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for movimiento in resultado:
            id_documento = movimiento[0]
            tipo_doc = movimiento[1]
            fecha = movimiento[2]
            producto = movimiento[3]
            cantidad = movimiento[4]
            estado = movimiento[5]
            tipo_movimiento = movimiento[6]
            
            if termino_busqueda:
                if (termino_busqueda not in producto.lower() and 
                    termino_busqueda not in tipo_doc.lower()):
                    continue
            
            if tipo_movimiento == 'SALIDA':
                movimiento_texto = f"➖ SALIDA ({cantidad})"
                color_mov = COLOR_ERROR
            else:
                movimiento_texto = f"➕ ENTRADA ({cantidad})"
                color_mov = COLOR_EXITO
            
            if estado == 'EMITIDO':
                estado_texto = "✅ Emitido"
            elif estado == 'PENDIENTE':
                estado_texto = "⏳ Pendiente"
            else:
                estado_texto = "❌ Anulado"
            
            frame_fila = tabla.agregar_fila([
                id_documento,
                tipo_doc,
                fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else str(fecha),
                producto,
                cantidad,
                movimiento_texto,
                estado_texto
            ])
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar movimientos:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Aplica filtro de búsqueda al listado de movimientos
def filtrar_movimientos(frame_lista, entry_buscar):
    cargar_movimientos(frame_lista, entry_buscar)