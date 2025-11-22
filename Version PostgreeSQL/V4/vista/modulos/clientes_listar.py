# vista/modulos/clientes_listar.py

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
        text_color=COLOR_TEXTO_SECUNDARIO
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
        border_color=COLOR_BORDE,
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_clientes(frame_lista, entry_buscar, label_contador))
    
    # Tabla más grande - ocupa más espacio vertical
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent", height=600)
    frame_lista.pack(fill="both", expand=True, pady=(0, 10))
    
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
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=100)
            return
        
        tabla = TablaCustom(frame_lista)
        tabla.pack(fill="both", expand=True)
        
        tabla.configurar_columnas(
            ['ID', 'Nombre', 'Apellido', 'Tipo Doc', 'N° Doc', 'Ubicación', 'Acciones'],
            [50, 150, 150, 80, 100, 250, 220]
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
            
            # Botones con colores correctos usando la nueva funcionalidad de tabla.py
            botones = [
                ('✏️ Editar', lambda c=cliente: abrir_ventana_edicion(c, frame_lista, entry_buscar, label_contador), 
                 COLOR_ADVERTENCIA, COLOR_ADVERTENCIA_HOVER),
                ('🗑️ Desactivar', lambda c=cliente: desactivar_cliente_confirm(c, frame_lista, entry_buscar, label_contador),
                 COLOR_ERROR, COLOR_ERROR_HOVER)
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
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_clientes(frame_lista, entry_buscar, label_contador=None):
    cargar_clientes(frame_lista, entry_buscar, label_contador)


def abrir_ventana_edicion(cliente, frame_lista, entry_buscar=None, label_contador=None):
    
    ventana = ctk.CTkToplevel()
    ventana.title("✏️ Editar Cliente")
    ventana.geometry("500x600")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.configure(fg_color=COLOR_FONDO_SECUNDARIO)
    
    # Variable para detectar si hubo cambios
    cambios_realizados = {'hubo_cambios': False}
    
    frame_form = ctk.CTkScrollableFrame(ventana, fg_color="transparent")
    frame_form.pack(fill="both", expand=True, padx=30, pady=30)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text=f"✏️ Editar Cliente",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ADVERTENCIA
    )
    label_titulo.pack(pady=(0, 10))
    
    label_id = ctk.CTkLabel(
        frame_form,
        text=f"ID: {cliente['id_cliente']}",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_id.pack(pady=(0, 30))
    
    label_nombre = ctk.CTkLabel(
        frame_form,
        text="Nombre *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_form,
        placeholder_text="Nombre del cliente",
        height=45,
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        font=("Arial", 13),
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO
    )
    entry_nombre.insert(0, cliente['nombre'])
    entry_nombre.pack(fill="x", pady=(0, 15))
    
    label_apellido = ctk.CTkLabel(
        frame_form,
        text="Apellido *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO_SECUNDARIO,
        anchor="w"
    )
    label_apellido.pack(fill="x", pady=(0, 5))
    
    entry_apellido = ctk.CTkEntry(
        frame_form,
        placeholder_text="Apellido del cliente",
        height=45,
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        font=("Arial", 13),
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO
    )
    entry_apellido.insert(0, cliente['apellido'])
    entry_apellido.pack(fill="x", pady=(0, 15))
    
    label_ubicacion = ctk.CTkLabel(
        frame_form,
        text="Ubicación *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO_SECUNDARIO,
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
        frame_form,
        values=ubicaciones_lista if ubicaciones_lista else ["Sin ubicaciones"],
        height=45,
        fg_color=COLOR_FONDO_TERCIARIO,
        button_color=COLOR_ADVERTENCIA,
        button_hover_color=COLOR_ADVERTENCIA_HOVER,
        border_color=COLOR_BORDE,
        font=("Arial", 13),
        text_color=COLOR_TEXTO,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        dropdown_text_color=COLOR_TEXTO,
        state="readonly"
    )
    
    ubicacion_actual = cliente['ubicacion']
    if ubicacion_actual in ubicaciones_lista:
        combo_ubicacion.set(ubicacion_actual)
    else:
        combo_ubicacion.set("Seleccione una ubicación")
    
    combo_ubicacion.pack(fill="x", pady=(0, 15))
    
    frame_doc_info = ctk.CTkFrame(frame_form, fg_color=COLOR_FONDO_TERCIARIO, corner_radius=10)
    frame_doc_info.pack(fill="x", pady=(0, 20))
    
    label_doc_titulo = ctk.CTkLabel(
        frame_doc_info,
        text="📄 Documento de Identidad (no editable)",
        font=("Arial", 11, "bold"),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_doc_titulo.pack(pady=(10, 5), padx=15, anchor="w")
    
    label_doc_valor = ctk.CTkLabel(
        frame_doc_info,
        text=f"{cliente['tipo_identificacion']}: {cliente['codigo_documento']}",
        font=("Arial", 13),
        text_color=COLOR_TEXTO
    )
    label_doc_valor.pack(pady=(0, 10), padx=15, anchor="w")
    
    # Detectar cambios en los campos
    def marcar_cambio(*args):
        cambios_realizados['hubo_cambios'] = True
    
    entry_nombre.bind("<KeyRelease>", marcar_cambio)
    entry_apellido.bind("<KeyRelease>", marcar_cambio)
    combo_ubicacion.bind("<<ComboboxSelected>>", marcar_cambio)
    
    def cancelar_con_confirmacion():
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
    
    def guardar_cambios():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        ubicacion_sel = combo_ubicacion.get()
        
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
        
        # Confirmación antes de guardar
        respuesta = messagebox.askyesno(
            "Confirmar Cambios",
            "¿Está seguro que desea guardar los cambios realizados?",
            parent=ventana
        )
        
        if not respuesta:
            return
        
        btn_guardar.configure(text="Guardando...", state="disabled")
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
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", pady=(20, 0))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=cancelar_con_confirmacion,
        height=50,
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        border_width=2,
        border_color=COLOR_ERROR,
        font=("Arial", 14, "bold"),
        corner_radius=10
    )
    btn_cancelar.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Guardar Cambios",
        command=guardar_cambios,
        height=50,
        fg_color=COLOR_ADVERTENCIA,
        hover_color=COLOR_ADVERTENCIA_HOVER,
        font=("Arial", 14, "bold"),
        corner_radius=10
    )
    btn_guardar.pack(side="right", fill="x", expand=True, padx=(10, 0))
    
    entry_nombre.bind("<Return>", lambda e: entry_apellido.focus())
    entry_apellido.bind("<Return>", lambda e: guardar_cambios())
    ventana.bind("<Escape>", lambda e: cancelar_con_confirmacion())
    
    entry_nombre.focus()
    entry_nombre.select_range(0, 'end')
    
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
    y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
    ventana.geometry(f"+{x}+{y}")


def desactivar_cliente_confirm(cliente, frame_lista, entry_buscar=None, label_contador=None):
    nombre_completo = cliente['nombre_completo']
    id_cliente = cliente['id_cliente']
    
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar al cliente?\n\n{nombre_completo}\n\nEsta acción marcará al cliente como inactivo."
    )
    
    if respuesta:
        exito, mensaje = ClienteBL.desactivar_cliente(id_cliente)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_clientes(frame_lista, entry_buscar, label_contador)
        else:
            messagebox.showerror("❌ Error", mensaje)