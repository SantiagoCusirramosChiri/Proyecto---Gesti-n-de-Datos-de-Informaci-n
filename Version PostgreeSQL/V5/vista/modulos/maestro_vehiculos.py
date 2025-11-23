# vista/modulos/maestro_vehiculos.py

import customtkinter as ctk
from tkinter import messagebox
from logica.VehiculoBL import VehiculoBL
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
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_INFO,
    COLOR_INFO_HOVER
)


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de gestión de vehículos con búsqueda"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ============= HEADER =============
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="🚗 Gestión de Vehículos",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(side="left")
    
    label_contador = ctk.CTkLabel(
        frame_header,
        text="",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E"  # ✅ OSCURO
    )
    label_contador.pack(side="left", padx=20)
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nuevo Vehículo",
        command=lambda: abrir_formulario_vehiculo(frame_principal, id_empresa, None, frame_lista, entry_buscar, label_contador),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_nuevo.pack(side="right", padx=5)
    
    btn_actualizar = ctk.CTkButton(
        frame_header,
        text="🔄 Actualizar",
        command=lambda: cargar_vehiculos(frame_lista, entry_buscar, label_contador),
        font=("Arial", 13, "bold"),
        fg_color=COLOR_INFO,
        hover_color=COLOR_INFO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_actualizar.pack(side="right", padx=5)
    
    # ============= BARRA DE BÚSQUEDA =============
    frame_busqueda = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_busqueda.pack(fill="x", pady=(0, 15))
    
    label_buscar = ctk.CTkLabel(
        frame_busqueda,
        text="🔍 Buscar:",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E"  # ✅ OSCURO
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ctk.CTkEntry(
        frame_busqueda,
        placeholder_text="Buscar por descripción o placa...",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"  # ✅ OSCURO
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_vehiculos(frame_lista, entry_buscar, label_contador))
    
    # ============= LISTA DE VEHÍCULOS =============
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_vehiculos(frame_lista, entry_buscar, label_contador)


def cargar_vehiculos(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de vehículos activos"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            vehiculos = VehiculoBL.buscar_vehiculos(termino_busqueda)
        else:
            vehiculos = VehiculoBL.obtener_vehiculos_activos()
        
        if label_contador:
            total = len(vehiculos) if vehiculos else 0
            label_contador.configure(text=f"({total} vehículo{'s' if total != 1 else ''})")
        
        if not vehiculos or len(vehiculos) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "🚗 No hay vehículos registrados"
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
            ['ID', 'Descripción', 'Placa', 'Estado', 'Acciones'],
            [60, 300, 120, 100, 250]
        )
        
        for vehiculo in vehiculos:
            estado = "✅ Activo" if vehiculo['activo'] else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([
                vehiculo['id_vehiculo'],
                vehiculo['descripcion'],
                vehiculo['placa'],
                estado
            ])
            
            def crear_funcion_editar(v):
                return lambda: editar_vehiculo(v, frame_lista, entry_buscar, label_contador)
            
            def crear_funcion_desactivar(v):
                return lambda: desactivar_vehiculo_confirm(v, frame_lista, entry_buscar, label_contador)
            
            # ✅ BOTONES CON COLORES CORRECTOS
            botones = [
                ('✏️ Editar', crear_funcion_editar(vehiculo), COLOR_ADVERTENCIA, COLOR_ADVERTENCIA_HOVER),  # AMARILLO
                ('🗑️ Desactivar', crear_funcion_desactivar(vehiculo), COLOR_ERROR, COLOR_ERROR_HOVER)  # ROJO
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar vehículos:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ERROR
        )
        label_error.pack(pady=50)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_vehiculos(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de vehículos"""
    cargar_vehiculos(frame_lista, entry_buscar, label_contador)


def abrir_formulario_vehiculo(frame_principal, id_empresa, vehiculo_editar=None, frame_lista=None, entry_buscar=None, label_contador=None):
    """Abre ventana modal con formulario para crear o editar vehículo"""
    es_edicion = vehiculo_editar is not None
    
    # ============= CONTROL DE CAMBIOS =============
    cambios_realizados = {'hubo_cambios': False}
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Vehículo" if es_edicion else "Registrar Vehículo")
    ventana_form.geometry("500x540")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 540)
    
    frame_form = ctk.CTkFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ============= TÍTULO =============
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="✏️ Editar Vehículo" if es_edicion else "➕ Registrar Vehículo",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ADVERTENCIA if es_edicion else COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    # ============= CAMPOS DEL FORMULARIO =============
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    # ============= FUNCIÓN PARA REGISTRAR CAMBIOS =============
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True
    
    # Campo: Descripción
    label_descripcion = ctk.CTkLabel(
        frame_campos,
        text="Descripción del Vehículo *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_descripcion.pack(fill="x", pady=(0, 5))
    
    entry_descripcion = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Camioneta Toyota Hilux Blanca",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_descripcion.pack(fill="x", pady=(0, 20))
    entry_descripcion.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Campo: Placa
    label_placa = ctk.CTkLabel(
        frame_campos,
        text="Placa (6-8 caracteres) *",
        font=("Arial", 12, "bold"),
        text_color="#2C2C2E",  # ✅ OSCURO
        anchor="w"
    )
    label_placa.pack(fill="x", pady=(0, 5))
    
    entry_placa = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: ABC-123 o ABC1234",
        placeholder_text_color="#2C2C2E",  # ✅ PLACEHOLDER OSCURO
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        text_color="#2C2C2E"
    )
    entry_placa.pack(fill="x", pady=(0, 10))
    entry_placa.bind("<KeyRelease>", registrar_cambio)  # ✅ Detecta cambios
    
    # Ayuda
    frame_ayuda = ctk.CTkFrame(
        frame_campos,
        fg_color=COLOR_FONDO_TERCIARIO,
        corner_radius=8,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_ayuda.pack(fill="x", pady=(0, 30))
    
    label_ayuda = ctk.CTkLabel(
        frame_ayuda,
        text="💡 La placa se convertirá a mayúsculas automáticamente.\nFormato: 6-8 caracteres (letras y números).",
        font=("Arial", 10),
        text_color="#666666",
        anchor="w",
        justify="left"
    )
    label_ayuda.pack(fill="x", padx=12, pady=10)
    
    # Cargar datos si es edición
    if es_edicion:
        entry_descripcion.insert(0, vehiculo_editar['descripcion'])
        entry_placa.insert(0, vehiculo_editar['placa'])
        cambios_realizados['hubo_cambios'] = False  # Resetear después de cargar
    
    # ============= FUNCIÓN GUARDAR CON CONFIRMACIÓN =============
    def guardar_con_confirmacion():
        """Valida, confirma y guarda el vehículo"""
        descripcion = entry_descripcion.get().strip()
        placa = entry_placa.get().strip()
        
        # Validaciones
        descripcion_valida, mensaje_desc = VehiculoBL.validar_descripcion(descripcion)
        if not descripcion_valida:
            messagebox.showerror("Error", mensaje_desc, parent=ventana_form)
            entry_descripcion.focus()
            return
        
        placa_valida, mensaje_placa = VehiculoBL.validar_placa(placa)
        if not placa_valida:
            messagebox.showerror("Error", mensaje_placa, parent=ventana_form)
            entry_placa.focus()
            return
        
        # ✅ CONFIRMACIÓN ANTES DE GUARDAR
        if es_edicion:
            respuesta = messagebox.askyesno(
                "Confirmar Actualización",
                f"¿Está seguro que desea actualizar este vehículo?\n\n"
                f"🚗 Vehículo: {descripcion}\n"
                f"🚙 Placa: {placa.upper()}",
                parent=ventana_form
            )
        else:
            respuesta = messagebox.askyesno(
                "Confirmar Registro",
                f"¿Está seguro que desea registrar este vehículo?\n\n"
                f"🚗 Vehículo: {descripcion}\n"
                f"🚙 Placa: {placa.upper()}",
                parent=ventana_form
            )
        
        if not respuesta:
            return
        
        # Deshabilitar botones mientras se guarda
        btn_guardar.configure(text="⏳ Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if es_edicion:
                exito, mensaje = VehiculoBL.actualizar_vehiculo(
                    id_vehiculo=vehiculo_editar['id_vehiculo'],
                    descripcion=descripcion,
                    placa=placa
                )
            else:
                exito, mensaje, id_vehiculo = VehiculoBL.insertar_vehiculo(
                    descripcion=descripcion,
                    placa=placa
                )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
                ventana_form.destroy()
                
                if frame_lista:
                    cargar_vehiculos(frame_lista, entry_buscar, label_contador)
            else:
                messagebox.showerror("❌ Error", mensaje, parent=ventana_form)
                btn_guardar.configure(text="💾 Guardar", state="normal")
                btn_cancelar.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana_form)
            btn_guardar.configure(text="💾 Guardar", state="normal")
            btn_cancelar.configure(state="normal")
            print(f"❌ Error al guardar: {e}")
            import traceback
            traceback.print_exc()
    
    # ============= FUNCIÓN CANCELAR CON CONFIRMACIÓN =============
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
    
    # ============= BOTONES =============
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=cancelar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
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
        text="💾 Guardar",
        command=guardar_con_confirmacion,  # ✅ CON CONFIRMACIÓN
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO if not es_edicion else COLOR_ADVERTENCIA,  # ✅ Verde o Amarillo
        hover_color=COLOR_EXITO_HOVER if not es_edicion else COLOR_ADVERTENCIA_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    # Atajos de teclado
    entry_descripcion.bind("<Return>", lambda e: entry_placa.focus())
    entry_placa.bind("<Return>", lambda e: guardar_con_confirmacion())
    ventana_form.bind("<Escape>", lambda e: cancelar_con_confirmacion())
    
    entry_descripcion.focus()


def editar_vehiculo(vehiculo, frame_lista, entry_buscar=None, label_contador=None):
    """Abre formulario de edición con datos del vehículo seleccionado"""
    frame_principal = frame_lista.master
    abrir_formulario_vehiculo(frame_principal, None, vehiculo, frame_lista, entry_buscar, label_contador)


def desactivar_vehiculo_confirm(vehiculo, frame_lista, entry_buscar=None, label_contador=None):
    """Desactiva vehículo tras confirmación del usuario"""
    descripcion = vehiculo['descripcion']
    id_vehiculo = vehiculo['id_vehiculo']
    placa = vehiculo['placa']
    
    # ✅ CONFIRMACIÓN CON FORMATO MEJORADO
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar este vehículo?\n\n"
        f"🚗 {descripcion}\n"
        f"🚙 Placa: {placa}\n\n"
        f"Esta acción marcará el vehículo como inactivo."
    )
    
    if respuesta:
        exito, mensaje = VehiculoBL.desactivar_vehiculo(id_vehiculo)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_vehiculos(frame_lista, entry_buscar, label_contador)
        else:
            messagebox.showerror("❌ Error", mensaje)


def centrar_ventana(ventana, ancho, alto):
    """Centra ventana en la pantalla"""
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")