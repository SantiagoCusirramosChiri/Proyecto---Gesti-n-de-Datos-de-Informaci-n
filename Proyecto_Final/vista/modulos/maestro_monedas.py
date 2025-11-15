# maestro_monedas.py

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


# Muestra interfaz de gestión de monedas con búsqueda
def mostrar(frame_contenido, id_empresa):
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
    
    btn_nuevo = ctk.CTkButton(
        frame_header,
        text="➕ Nueva Moneda",
        command=lambda: abrir_formulario_moneda(frame_principal, id_empresa),
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
        command=lambda: cargar_monedas(frame_lista, entry_buscar),
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
        placeholder_text="Buscar por código ISO o nombre...",
        width=400,
        height=35,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_buscar.pack(side="left")
    entry_buscar.bind("<KeyRelease>", lambda e: filtrar_monedas(frame_lista, entry_buscar))
    
    frame_lista = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_lista.pack(fill="both", expand=True)
    
    cargar_monedas(frame_lista, entry_buscar)


# Carga y muestra tabla de monedas activas
def cargar_monedas(frame_lista, entry_buscar=None):
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        resultado = procedimientos.obtener_monedas_activas()
        
        if not resultado or len(resultado) == 0:
            label_vacio = ctk.CTkLabel(
                frame_lista,
                text="💰 No hay monedas registradas",
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
        
        termino_busqueda = entry_buscar.get().lower() if entry_buscar else ""
        
        for moneda in resultado:
            id_moneda = moneda[0]
            codigo_iso = moneda[1]
            nombre = moneda[2]
            activo = moneda[3]
            
            if termino_busqueda:
                if termino_busqueda not in codigo_iso.lower() and termino_busqueda not in nombre.lower():
                    continue
            
            estado = "✅ Activo" if activo else "❌ Inactivo"
            
            frame_fila = tabla.agregar_fila([id_moneda, codigo_iso, nombre, estado])
            
            botones = [
                ('✏️ Editar', lambda m=moneda: editar_moneda(frame_lista, m)),
                ('🗑️ Desactivar', lambda id=id_moneda, n=nombre: desactivar_moneda(id, n, frame_lista, entry_buscar))
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


# Aplica filtro de búsqueda al listado de monedas
def filtrar_monedas(frame_lista, entry_buscar):
    cargar_monedas(frame_lista, entry_buscar)


# Abre ventana modal con formulario para crear o editar moneda
def abrir_formulario_moneda(frame_principal, id_empresa, moneda_editar=None):
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Registrar Moneda" if not moneda_editar else "Editar Moneda")
    ventana_form.geometry("500x450")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 500, 450)
    
    frame_form = ctk.CTkFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="➕ Registrar Moneda" if not moneda_editar else "✏️ Editar Moneda",
        font=("Arial Black", 20, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=40)
    
    label_codigo = ctk.CTkLabel(
        frame_campos,
        text="Código ISO (3 caracteres):",
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
        text="Nombre de la Moneda:",
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
    
    if moneda_editar:
        entry_codigo.insert(0, moneda_editar[1])
        entry_nombre.insert(0, moneda_editar[2])
    
    def guardar():
        codigo_iso = entry_codigo.get().strip().upper()
        nombre = entry_nombre.get().strip()
        
        if not codigo_iso or not nombre:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana_form)
            return
        
        if len(codigo_iso) != 3:
            messagebox.showerror("Error", "El código ISO debe tener exactamente 3 caracteres", parent=ventana_form)
            return
        
        if not codigo_iso.isalpha():
            messagebox.showerror("Error", "El código ISO solo debe contener letras", parent=ventana_form)
            return
        
        try:
            if moneda_editar:
                procedimientos.actualizar_moneda(moneda_editar[0], codigo_iso, nombre)
                messagebox.showinfo("✅ Éxito", "Moneda actualizada correctamente", parent=ventana_form)
            else:
                procedimientos.sp_insertar_moneda(codigo_iso, nombre)
                messagebox.showinfo("✅ Éxito", "Moneda registrada correctamente", parent=ventana_form)
            
            ventana_form.destroy()
            
            frame_lista = frame_principal.winfo_children()[-1]
            cargar_monedas(frame_lista)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar: {str(e)}", parent=ventana_form)
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=40, pady=(0, 20))
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ Cancelar",
        command=ventana_form.destroy,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO,
        text_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY,
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


# Abre formulario de edición con datos de la moneda seleccionada
def editar_moneda(frame_lista, moneda):
    frame_principal = frame_lista.master
    abrir_formulario_moneda(frame_principal, None, moneda)


# Desactiva moneda tras confirmación del usuario
def desactivar_moneda(id_moneda, nombre, frame_lista, entry_buscar):
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro de desactivar la moneda:\n{nombre}?"
    )
    
    if respuesta:
        try:
            procedimientos.desactivar_moneda(id_moneda)
            messagebox.showinfo("✅ Éxito", "Moneda desactivada correctamente")
            cargar_monedas(frame_lista, entry_buscar)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al desactivar: {str(e)}")


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")