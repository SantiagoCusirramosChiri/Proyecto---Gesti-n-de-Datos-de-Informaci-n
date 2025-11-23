# vista/modulos/inventario_movimientos.py

import customtkinter as ctk
from tkinter import messagebox
from logica.MovimientoBL import MovimientoBL
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_ADVERTENCIA,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_INFO,
    COLOR_INFO_HOVER
)


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de historial de movimientos de inventario con búsqueda"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ============= HEADER =============
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="📊 Movimientos de Inventario",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    label_contador = ctk.CTkLabel(
        frame_header,
        text="",
        font=("Arial", 12, "bold"),
        text_color="#000000"
    )
    label_contador.pack(side="left", padx=20)
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_movimientos(frame_lista, entry_buscar, label_contador),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_INFO,
        hover_color=COLOR_INFO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_actualizar.pack(side="right", padx=5)
    
    # ============= INFO BANNER =============
    frame_info = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="x", pady=(0, 15))
    
    label_info = ctk.CTkLabel(
        frame_info,
        text="ℹ️ Mostrando los últimos 100 movimientos de stock (Salidas por documentos emitidos)",
        font=("Arial", 11),
        text_color="#666666"
    )
    label_info.pack(pady=12, padx=15)
    
    # ============= BARRA DE BÚSQUEDA =============
    frame_busqueda = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=10,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_busqueda.pack(fill="x", pady=(0, 15))
    
    frame_busqueda_inner = ctk.CTkFrame(frame_busqueda, fg_color="transparent")
    frame_busqueda_inner.pack(fill="x", padx=15, pady=12)
    
    label_buscar = ctk.CTkLabel(
        frame_busqueda_inner,
        text="🔍 Buscar:",
        font=("Arial", 12, "bold"),
        text_color="#000000"
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda_inner,
        placeholder_text="Buscar por producto o tipo de documento...",
        width=450,
        height=38,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#000000"
    )
    entry_buscar.pack(side="left", fill="x", expand=True)
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_movimientos(frame_lista, entry_buscar, label_contador))
    
    btn_limpiar = ctk.CTkButton(
        frame_busqueda_inner,
        text="✖️",
        command=lambda: limpiar_busqueda(entry_buscar, frame_lista, label_contador),
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        width=40,
        height=38,
        corner_radius=8,
        border_width=2,
        border_color=COLOR_BORDE
    )
    btn_limpiar.pack(side="left", padx=(10, 0))
    
    # ============= TABLA DE MOVIMIENTOS =============
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_movimientos(frame_lista, entry_buscar, label_contador)


def cargar_movimientos(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de movimientos con filtro de búsqueda"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get().strip() if entry_buscar else ""
        
        if termino_busqueda:
            movimientos = MovimientoBL.buscar_movimientos(termino_busqueda)
        else:
            movimientos = MovimientoBL.obtener_movimientos_inventario()
        
        # ============= ACTUALIZAR CONTADOR =============
        if label_contador:
            if movimientos:
                total = len(movimientos)
                entradas = sum(1 for m in movimientos if m['tipo_movimiento'] == 'ENTRADA')
                salidas = sum(1 for m in movimientos if m['tipo_movimiento'] == 'SALIDA')
                
                texto = f"({total} movimiento{'s' if total != 1 else ''}"
                if entradas > 0:
                    texto += f" • {entradas} entrada{'s' if entradas != 1 else ''}"
                if salidas > 0:
                    texto += f" • {salidas} salida{'s' if salidas != 1 else ''}"
                texto += ")"
                
                label_contador.configure(text=texto)
            else:
                label_contador.configure(text="(0 movimientos)")
        
        # ============= MENSAJE VACÍO =============
        if not movimientos or len(movimientos) == 0:
            frame_vacio = ctk.CTkFrame(
                frame_lista,
                fg_color=COLOR_FONDO_SECUNDARIO,
                corner_radius=15,
                border_width=1,
                border_color=COLOR_BORDE
            )
            frame_vacio.pack(fill="both", expand=True, padx=50, pady=50)
            
            icono = "🔍" if termino_busqueda else "📊"
            mensaje = "No se encontraron resultados" if termino_busqueda else "No hay movimientos de inventario registrados"
            
            label_icono = ctk.CTkLabel(
                frame_vacio,
                text=icono,
                font=("Arial", 80)
            )
            label_icono.pack(pady=(50, 20))
            
            label_mensaje = ctk.CTkLabel(
                frame_vacio,
                text=mensaje,
                font=("Arial", 16),
                text_color="#666666"
            )
            label_mensaje.pack(pady=(0, 20))
            
            if termino_busqueda:
                label_sugerencia = ctk.CTkLabel(
                    frame_vacio,
                    text=f"Búsqueda: '{termino_busqueda}'",
                    font=("Arial", 12),
                    text_color=COLOR_TEXTO_SECUNDARIO
                )
                label_sugerencia.pack(pady=(0, 50))
            else:
                label_placeholder = ctk.CTkLabel(
                    frame_vacio,
                    text="",
                    height=20
                )
                label_placeholder.pack(pady=(0, 50))
            
            return
        
        # ============= TABLA DE DATOS =============
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID Doc', 'Tipo Doc', 'Fecha', 'Producto', 'Cantidad', 'Movimiento', 'Estado'],
            [80, 100, 100, 250, 100, 120, 100]
        )
        
        for movimiento in movimientos:
            movimiento_texto, _ = MovimientoBL.formatear_tipo_movimiento(
                movimiento['tipo_movimiento'],
                movimiento['cantidad']
            )
            
            estado_texto = MovimientoBL.formatear_estado(movimiento['estado'])
            
            frame_fila = tabla.agregar_fila([
                movimiento['id_documento'],
                movimiento['tipo_doc'],
                movimiento['fecha_formateada'],
                movimiento['producto'],
                movimiento['cantidad'],
                movimiento_texto,
                estado_texto
            ])
            
    except Exception as e:
        frame_error = ctk.CTkFrame(
            frame_lista,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_ERROR
        )
        frame_error.pack(fill="both", expand=True, padx=50, pady=50)
        
        label_icono_error = ctk.CTkLabel(
            frame_error,
            text="❌",
            font=("Arial", 80)
        )
        label_icono_error.pack(pady=(50, 20))
        
        label_error = ctk.CTkLabel(
            frame_error,
            text="Error al cargar movimientos",
            font=("Arial", 16, "bold"),
            text_color=COLOR_ERROR
        )
        label_error.pack(pady=(0, 10))
        
        label_detalle = ctk.CTkLabel(
            frame_error,
            text=str(e),
            font=("Arial", 12),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_detalle.pack(pady=(0, 50), padx=30)
        
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_movimientos(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de movimientos"""
    cargar_movimientos(frame_lista, entry_buscar, label_contador)


def limpiar_busqueda(entry_buscar, frame_lista, label_contador):
    """Limpia el campo de búsqueda y recarga todos los movimientos"""
    entry_buscar.delete(0, 'end')
    cargar_movimientos(frame_lista, entry_buscar, label_contador)