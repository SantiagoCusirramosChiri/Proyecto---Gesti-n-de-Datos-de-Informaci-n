# clientes_listar.py

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
    COLOR_EXITO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra la interfaz principal de listado de clientes
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
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_clientes(frame_lista, entry_buscar),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
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
        text_color=COLOR_TEXTO
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda,
        placeholder_text="Buscar por nombre, apellido o documento...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_clientes(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_clientes(frame_lista, entry_buscar)


# Carga y muestra todos los clientes activos en la tabla
def cargar_clientes(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_clientes_activos()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="👥 No hay clientes registrados",
                font=("Arial", 16),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Nombre', 'Apellido', 'Tipo Doc', 'N° Doc', 'Ubicación', 'Acciones'],
            [50, 150, 150, 80, 100, 250, 200]
        )
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for cliente in resultado:
            id_cliente = cliente[0]
            nombre = cliente[1]
            apellido = cliente[2]
            ubicacion = cliente[3]
            tipo_doc = cliente[4]
            codigo_doc = cliente[5]
            
            if termino_busqueda:
                if (termino_busqueda not in nombre.lower() and 
                    termino_busqueda not in apellido.lower() and 
                    termino_busqueda not in codigo_doc.lower()):
                    continue
            
            frame_fila = tabla.agregar_fila([id_cliente, nombre, apellido, tipo_doc, codigo_doc, ubicacion])
            
            botones = [
                ('✏️ Editar', lambda c=cliente: editar_cliente(frame_lista, c)),
                ('🗑️ Desactivar', lambda id=id_cliente, n=f"{nombre} {apellido}": desactivar_cliente_confirm(id, n, frame_lista, entry_buscar))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar clientes:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)


# Filtra clientes según término de búsqueda
def filtrar_clientes(frame_lista, entry_buscar):
    cargar_clientes(frame_lista, entry_buscar)


# Abre formulario de registro/edición de cliente
def abrir_formulario_cliente(frame_principal, id_empresa, cliente_editar=None):
    from vista.modulos import clientes_registrar
    clientes_registrar.abrir_formulario(frame_principal, id_empresa, cliente_editar, cargar_clientes)


# Prepara edición de cliente seleccionado
def editar_cliente(frame_lista, cliente):
    frame_principal = frame_lista.master
    abrir_formulario_cliente(frame_principal, None, cliente)


# Confirma y ejecuta desactivación de cliente
def desactivar_cliente_confirm(id_cliente, nombre_completo, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar al cliente:\n{nombre_completo}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_cliente(id_cliente)
            messagebox.showinfo("✅ Éxito", "Cliente desactivado correctamente")
            cargar_clientes(frame_lista, entry_buscar)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al desactivar: {str(e)}")