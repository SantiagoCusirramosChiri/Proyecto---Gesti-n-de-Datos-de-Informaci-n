# vista/modulos/maestro_monedas.py

import customtkinter as ctk
from tkinter import messagebox
from logica.MonedaBL import MonedaBL
from vista.componentes.tabla import TablaCustom
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE,
    COLOR_INFO,
    COLOR_INFO_HOVER
)


def mostrar(frame_contenido, id_empresa):
    """Muestra interfaz de gestión de monedas con búsqueda"""
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    frame_header = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_header.pack(fill="x", pady=(0, 20))
    
    label_titulo = ctk.CTkLabel(
        frame_header,
        text="💰 Gestión de Monedas",
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
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Moneda",
        command=lambda: abrir_formulario_moneda(frame_principal, id_empresa, None, frame_lista, entry_buscar, label_contador),
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
        command=lambda: cargar_monedas(frame_lista, entry_buscar, label_contador),
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
        placeholder_text="Buscar por código ISO o nombre...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_monedas(frame_lista, entry_buscar, label_contador))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_monedas(frame_lista, entry_buscar, label_contador)


def cargar_monedas(frame_lista, entry_buscar=None, label_contador=None):
    """Carga y muestra tabla de monedas activas"""
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        termino_busqueda = entry_buscar.get() if entry_buscar else ""
        
        if termino_busqueda:
            monedas = MonedaBL.buscar_monedas(termino_busqueda)
        else:
            monedas = MonedaBL.obtener_monedas_activas()
        
        if label_contador:
            total = len(monedas) if monedas else 0
            label_contador.configure(text=f"({total} monedas)")
        
        if not monedas or len(monedas) == 0:
            mensaje = "🔍 No se encontraron resultados" if termino_busqueda else "💰 No hay monedas registradas"
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
            ['ID', 'Código ISO', 'Nombre', 'Estado', 'Acciones'],
            [60, 150, 250, 100, 250]
        )
        
        for moneda in monedas:
            estado = "✅ Activo" if moneda['activo'] else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([
                moneda['id_moneda'],
                moneda['codigo_iso'],
                moneda['nombre'],
                estado
            ])
            
            botones = [
                ('✏️ Editar', lambda m=moneda, fl=frame_lista, eb=entry_buscar, lc=label_contador: 
                    editar_moneda(m, fl, eb, lc)),
                ('🗑️ Desactivar', lambda m=moneda, fl=frame_lista, eb=entry_buscar, lc=label_contador: 
                    desactivar_moneda_confirm(m, fl, eb, lc))
            ]
            
            tabla.agregar_botones_accion(frame_fila, botones)
            
    except Exception as e:
        label_error = ctk.CTkLabel(
            frame_lista,
            text=f"❌ Error al cargar monedas:\n{str(e)}",
            font=("Arial", 14),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_error.pack(pady=50)
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def filtrar_monedas(frame_lista, entry_buscar, label_contador=None):
    """Aplica filtro de búsqueda al listado de monedas"""
    cargar_monedas(frame_lista, entry_buscar, label_contador)


def abrir_formulario_moneda(frame_principal, id_empresa, moneda_editar=None, frame_lista=None, entry_buscar=None, label_contador=None):
    """Abre ventana modal con formulario para crear o editar moneda"""
    es_edicion = moneda_editar is not None
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Editar Moneda" if es_edicion else "Registrar Moneda")
    ventana_form.geometry("500x450")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 450)
    
    frame_form = ctk.CTkFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=1,
        border_color=COLOR_BORDE
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="✏️ Editar Moneda" if es_edicion else "➕ Registrar Moneda",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY if es_edicion else COLOR_EXITO
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_codigo = ctk.CTkLabel(
        frame_campos,
        text="Código ISO (3 caracteres) *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_codigo.pack(fill="x", pady=(0, 5))
    
    entry_codigo = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: PEN, USD, EUR",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_codigo.pack(fill="x", pady=(0, 20))
    
    label_nombre = ctk.CTkLabel(
        frame_campos,
        text="Nombre de la Moneda *",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Soles, Dólares, Euros",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nombre.pack(fill="x", pady=(0, 30))
    
    if es_edicion:
        entry_codigo.insert(0, moneda_editar['codigo_iso'])
        entry_nombre.insert(0, moneda_editar['nombre'])
    
    def guardar():
        """Valida y guarda la moneda"""
        codigo_iso = entry_codigo.get().strip().upper()
        nombre = entry_nombre.get().strip()
        
        codigo_valido, mensaje_codigo = MonedaBL.validar_codigo_iso(codigo_iso)
        if not codigo_valido:
            messagebox.showerror("Error", mensaje_codigo, parent=ventana_form)
            entry_codigo.focus()
            return
        
        nombre_valido, mensaje_nombre = MonedaBL.validar_nombre(nombre)
        if not nombre_valido:
            messagebox.showerror("Error", mensaje_nombre, parent=ventana_form)
            entry_nombre.focus()
            return
        
        btn_guardar.configure(text="Guardando...", state="disabled")
        btn_cancelar.configure(state="disabled")
        ventana_form.update()
        
        try:
            if es_edicion:
                exito, mensaje = MonedaBL.actualizar_moneda(
                    id_moneda=moneda_editar['id_moneda'],
                    codigo_iso=codigo_iso,
                    nombre=nombre
                )
            else:
                exito, mensaje, id_moneda = MonedaBL.insertar_moneda(
                    codigo_iso=codigo_iso,
                    nombre=nombre
                )
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_form)
                ventana_form.destroy()
                
                if frame_lista:
                    cargar_monedas(frame_lista, entry_buscar, label_contador)
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
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana_form.destroy,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ERROR,
        border_width=2,
        border_color=COLOR_ERROR,
        height=40,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Guardar",
        command=guardar,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=40,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    entry_codigo.bind("<Return>", lambda e: entry_nombre.focus())
    entry_nombre.bind("<Return>", lambda e: guardar())
    ventana_form.bind("<Escape>", lambda e: ventana_form.destroy())
    
    entry_codigo.focus()


def editar_moneda(moneda, frame_lista, entry_buscar=None, label_contador=None):
    """Abre formulario de edición con datos de la moneda seleccionada"""
    frame_principal = frame_lista.master
    abrir_formulario_moneda(frame_principal, None, moneda, frame_lista, entry_buscar, label_contador)


def desactivar_moneda_confirm(moneda, frame_lista, entry_buscar=None, label_contador=None):
    """Desactiva moneda tras confirmación del usuario"""
    nombre = moneda['nombre']
    id_moneda = moneda['id_moneda']
    
    respuesta = messagebox.askyesno(
        "Confirmar Desactivación",
        f"¿Está seguro de desactivar la moneda?\n\n{nombre}\n\nEsta acción marcará la moneda como inactiva."
    )
    
    if respuesta:
        exito, mensaje = MonedaBL.desactivar_moneda(id_moneda)
        
        if exito:
            messagebox.showinfo("✅ Éxito", mensaje)
            cargar_monedas(frame_lista, entry_buscar, label_contador)
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