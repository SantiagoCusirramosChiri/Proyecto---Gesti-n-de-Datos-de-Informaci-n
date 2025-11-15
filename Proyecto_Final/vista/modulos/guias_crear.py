# guias_crear.py

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from decimal import Decimal
from datos import procedimientos
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


# Muestra pantalla principal para crear guías de remisión
def mostrar(frame_contenido, id_empresa):
    if isinstance(id_empresa, (tuple, list)):
        for item in id_empresa:
            if isinstance(item, int):
                id_empresa = item
                break
        else:
            try:
                id_empresa = int(id_empresa[1]) if len(id_empresa) > 1 else int(id_empresa[0])
            except (ValueError, IndexError, TypeError):
                messagebox.showerror("Error", "ID de empresa inválido")
                return
    
    try:
        id_empresa = int(id_empresa)
    except (ValueError, TypeError):
        messagebox.showerror("Error", f"ID de empresa inválido: {id_empresa}")
        return
    
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    frame_principal = ctk.CTkFrame(frame_contenido, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="🚚 Crear Guías de Remisión",
        font=("Arial Black", 24, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 30))
    
    frame_info = ctk.CTkFrame(
        frame_principal,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15,
        border_width=2,
        border_color=COLOR_BORDE
    )
    frame_info.pack(fill="both", expand=True, padx=100, pady=50)
    
    label_icono = ctk.CTkLabel(
        frame_info,
        text="🚚",
        font=("Arial", 100)
    )
    label_icono.pack(pady=(50, 20))
    
    label_descripcion = ctk.CTkLabel(
        frame_info,
        text="Cree guías de remisión para documentos emitidos",
        font=("Arial", 16),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_descripcion.pack(pady=10)
    
    btn_nuevo = ctk.CTkButton(
        frame_info,
        text="➕ Nueva Guía de Remisión",
        command=lambda: abrir_formulario_guia(frame_principal, id_empresa),
        font=("Arial", 14, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        width=280,
        corner_radius=10
    )
    btn_nuevo.pack(pady=(30, 50))


# Abre ventana modal para crear guía de remisión
def abrir_formulario_guia(frame_principal, id_empresa):
    productos_guia = []
    
    ventana_form = ctk.CTkToplevel()
    ventana_form.title("Crear Nueva Guía de Remisión")
    ventana_form.geometry("900x950")
    ventana_form.resizable(False, False)
    ventana_form.grab_set()
    ventana_form.configure(fg_color=COLOR_FONDO)
    
    centrar_ventana(ventana_form, 900, 950)
    
    frame_form = ctk.CTkScrollableFrame(
        ventana_form,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=15
    )
    frame_form.pack(fill="both", expand=True, padx=20, pady=20)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="🚚 Crear Nueva Guía de Remisión",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(20, 30))
    
    frame_campos = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_campos.pack(fill="both", expand=True, padx=30)
    
    label_seccion1 = ctk.CTkLabel(
        frame_campos,
        text="📋 Datos de la Guía",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion1.pack(fill="x", pady=(0, 15))
    
    frame_row1 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row1.pack(fill="x", pady=(0, 15))
    
    frame_nro_guia = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_nro_guia.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_nro_guia = ctk.CTkLabel(
        frame_nro_guia,
        text="Nro. de Guía:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_nro_guia.pack(fill="x", pady=(0, 5))
    
    entry_nro_guia = ctk.CTkEntry(
        frame_nro_guia,
        placeholder_text="Ej: G001-00000001",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_nro_guia.pack(fill="x")
    
    frame_doc = ctk.CTkFrame(frame_row1, fg_color="transparent")
    frame_doc.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_doc = ctk.CTkLabel(
        frame_doc,
        text="Documento de Venta:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_doc.pack(fill="x", pady=(0, 5))
    
    documentos = procedimientos.obtener_documentos_emitidos(id_empresa)
    documentos_dict = {}
    documentos_lista = []
    
    if documentos:
        for doc in documentos:
            fecha_str = doc[2].strftime("%d/%m/%Y") if isinstance(doc[2], datetime) else str(doc[2])
            texto = f"Doc #{doc[0]} - {doc[1]} - {doc[3]} ({fecha_str})"
            documentos_dict[texto] = doc[0]
            documentos_lista.append(texto)
    
    combo_documento = ctk.CTkComboBox(
        frame_doc,
        values=documentos_lista if documentos_lista else ["No hay documentos emitidos disponibles"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        command=lambda e: cargar_productos_documento(combo_documento.get(), documentos_dict, frame_productos_lista, productos_guia)
    )
    combo_documento.pack(fill="x")
    if documentos_lista:
        combo_documento.set(documentos_lista[0])
    
    frame_row2 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row2.pack(fill="x", pady=(0, 15))
    
    frame_fecha_emision = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_fecha_emision.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_fecha_emision = ctk.CTkLabel(
        frame_fecha_emision,
        text="Fecha de Emisión:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_fecha_emision.pack(fill="x", pady=(0, 5))
    
    entry_fecha_emision = ctk.CTkEntry(
        frame_fecha_emision,
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_fecha_emision.pack(fill="x")
    entry_fecha_emision.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    frame_fecha_traslado = ctk.CTkFrame(frame_row2, fg_color="transparent")
    frame_fecha_traslado.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_fecha_traslado = ctk.CTkLabel(
        frame_fecha_traslado,
        text="Fecha Inicio Traslado:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_fecha_traslado.pack(fill="x", pady=(0, 5))
    
    entry_fecha_traslado = ctk.CTkEntry(
        frame_fecha_traslado,
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_fecha_traslado.pack(fill="x")
    entry_fecha_traslado.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    label_motivo = ctk.CTkLabel(
        frame_campos,
        text="Motivo de Traslado:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_motivo.pack(fill="x", pady=(0, 5))
    
    entry_motivo = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Ej: Venta, Traslado entre almacenes, Devolución",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_motivo.pack(fill="x", pady=(0, 15))
    
    frame_separador1 = ctk.CTkFrame(frame_campos, height=2, fg_color=COLOR_BORDE)
    frame_separador1.pack(fill="x", pady=20)
    
    label_seccion2 = ctk.CTkLabel(
        frame_campos,
        text="📍 Direcciones",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion2.pack(fill="x", pady=(0, 15))
    
    label_partida = ctk.CTkLabel(
        frame_campos,
        text="Dirección de Partida:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_partida.pack(fill="x", pady=(0, 5))
    
    entry_partida = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Dirección completa de origen",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_partida.pack(fill="x", pady=(0, 15))
    
    label_llegada = ctk.CTkLabel(
        frame_campos,
        text="Dirección de Llegada:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_llegada.pack(fill="x", pady=(0, 5))
    
    entry_llegada = ctk.CTkEntry(
        frame_campos,
        placeholder_text="Dirección completa de destino",
        height=40,
        font=("Arial", 12),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE
    )
    entry_llegada.pack(fill="x", pady=(0, 15))
    
    frame_separador2 = ctk.CTkFrame(frame_campos, height=2, fg_color=COLOR_BORDE)
    frame_separador2.pack(fill="x", pady=20)
    
    label_seccion3 = ctk.CTkLabel(
        frame_campos,
        text="🚛 Datos del Transporte",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion3.pack(fill="x", pady=(0, 15))
    
    frame_row3 = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_row3.pack(fill="x", pady=(0, 15))
    
    frame_conductor = ctk.CTkFrame(frame_row3, fg_color="transparent")
    frame_conductor.pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    label_conductor = ctk.CTkLabel(
        frame_conductor,
        text="Conductor:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_conductor.pack(fill="x", pady=(0, 5))
    
    conductores = procedimientos.obtener_conductores_combo()
    conductores_dict = {f"{c[1]} (Lic: {c[2]})": c[0] for c in conductores}
    conductores_lista = list(conductores_dict.keys())
    
    combo_conductor = ctk.CTkComboBox(
        frame_conductor,
        values=conductores_lista if conductores_lista else ["No hay conductores"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_conductor.pack(fill="x")
    if conductores_lista:
        combo_conductor.set(conductores_lista[0])
    
    frame_vehiculo = ctk.CTkFrame(frame_row3, fg_color="transparent")
    frame_vehiculo.pack(side="right", expand=True, fill="x", padx=(10, 0))
    
    label_vehiculo = ctk.CTkLabel(
        frame_vehiculo,
        text="Vehículo:",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_vehiculo.pack(fill="x", pady=(0, 5))
    
    vehiculos = procedimientos.obtener_vehiculos_combo()
    vehiculos_dict = {f"{v[1]} (Placa: {v[2]})": v[0] for v in vehiculos}
    vehiculos_lista = list(vehiculos_dict.keys())
    
    combo_vehiculo = ctk.CTkComboBox(
        frame_vehiculo,
        values=vehiculos_lista if vehiculos_lista else ["No hay vehículos"],
        height=40,
        font=("Arial", 11),
        fg_color=COLOR_FONDO_TERCIARIO,
        border_color=COLOR_BORDE,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER
    )
    combo_vehiculo.pack(fill="x")
    if vehiculos_lista:
        combo_vehiculo.set(vehiculos_lista[0])
    
    frame_separador3 = ctk.CTkFrame(frame_campos, height=2, fg_color=COLOR_BORDE)
    frame_separador3.pack(fill="x", pady=20)
    
    label_seccion4 = ctk.CTkLabel(
        frame_campos,
        text="📦 Productos a Trasladar",
        font=("Arial", 16, "bold"),
        text_color=COLOR_ROJO_PRIMARY,
        anchor="w"
    )
    label_seccion4.pack(fill="x", pady=(0, 15))
    
    frame_productos_lista = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_productos_lista.pack(fill="both", expand=True)
    
    if documentos_lista:
        cargar_productos_documento(
            documentos_lista[0], 
            documentos_dict, 
            frame_productos_lista, 
            productos_guia
        )
    
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.pack(fill="x", padx=30, pady=(20, 20))
    
    # Valida y guarda guía de remisión con sus detalles
    def guardar_guia():
        nro_guia = entry_nro_guia.get().strip()
        if not nro_guia:
            messagebox.showerror("Error", "Ingrese el número de guía", parent=ventana_form)
            return
        
        if procedimientos.verificar_guia_existe(nro_guia):
            messagebox.showerror("Error", "El número de guía ya existe", parent=ventana_form)
            return
        
        if not documentos_lista:
            messagebox.showerror("Error", "No hay documentos emitidos disponibles", parent=ventana_form)
            return
        
        if not conductores_lista or not vehiculos_lista:
            messagebox.showerror("Error", "Faltan datos de conductor o vehículo", parent=ventana_form)
            return
        
        motivo = entry_motivo.get().strip()
        partida = entry_partida.get().strip()
        llegada = entry_llegada.get().strip()
        
        if not motivo or not partida or not llegada:
            messagebox.showerror("Error", "Complete todos los campos requeridos", parent=ventana_form)
            return
        
        if len(productos_guia) == 0:
            messagebox.showerror("Error", "Debe seleccionar al menos un producto", parent=ventana_form)
            return
        
        try:
            fecha_emision = entry_fecha_emision.get()
            fecha_traslado = entry_fecha_traslado.get()
            id_doc_venta = documentos_dict[combo_documento.get()]
            id_conductor = conductores_dict[combo_conductor.get()]
            id_vehiculo = vehiculos_dict[combo_vehiculo.get()]
            
            id_empresa_int = id_empresa
            if isinstance(id_empresa_int, (tuple, list)):
                for item in id_empresa_int:
                    if isinstance(item, int):
                        id_empresa_int = item
                        break
                else:
                    try:
                        id_empresa_int = int(id_empresa_int[1]) if len(id_empresa_int) > 1 else int(id_empresa_int[0])
                    except (ValueError, IndexError, TypeError):
                        raise ValueError(f"ID de empresa inválido: {id_empresa}")
            
            id_empresa_int = int(id_empresa_int)
            
            id_guia = procedimientos.sp_insertar_encabezado_guia(
                id_doc_venta,
                nro_guia,
                fecha_emision,
                fecha_traslado,
                motivo,
                partida,
                llegada,
                id_conductor,
                id_vehiculo
            )
            
            for prod in productos_guia:
                id_producto = prod['id']
                descripcion = prod['nombre']
                unidad_medida = prod['unidad_medida']
                
                unidad_peso_bruto = "KG"
                peso_total_carga = 0.00
                modalidad_trans = "PRIVADO"
                transbordo_prog = "NO"
                categoriaM1_L = "NO"
                retorno_envases = "NO"
                vehiculo_vacio = "NO"
                
                procedimientos.sp_insertar_detalle_guia(
                    id_guia,
                    id_producto,
                    descripcion,
                    unidad_medida,
                    unidad_peso_bruto,
                    peso_total_carga,
                    modalidad_trans,
                    transbordo_prog,
                    categoriaM1_L,
                    retorno_envases,
                    vehiculo_vacio,
                    id_conductor,
                    id_vehiculo
                )
            
            messagebox.showinfo("✅ Éxito", 
                f"Guía N° {nro_guia} creada correctamente\n\nEstado: PENDIENTE",
                parent=ventana_form)
            
            ventana_form.destroy()
            
        except Exception as e:
            import traceback
            error_detallado = traceback.format_exc()
            print(f"❌ ERROR COMPLETO:\n{error_detallado}")
            messagebox.showerror("❌ Error", f"Error al crear guía:\n{str(e)}", parent=ventana_form)
    
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
        height=50,
        corner_radius=10
    )
    btn_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="💾 Crear Guía",
        command=guardar_guia,
        font=("Arial", 12, "bold"),
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        height=50,
        corner_radius=10
    )
    btn_guardar.pack(side="right", expand=True, fill="x", padx=(5, 0))


# Carga productos del documento seleccionado para la guía
def cargar_productos_documento(texto_documento, documentos_dict, frame_productos, productos_guia):
    for widget in frame_productos.winfo_children():
        widget.destroy()
    
    productos_guia.clear()
    
    if not texto_documento or texto_documento == "No hay documentos emitidos disponibles":
        label_vacio = ctk.CTkLabel(
            frame_productos,
            text="📦 Seleccione un documento para ver los productos",
            font=("Arial", 14),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_vacio.pack(pady=30)
        return
    
    try:
        id_documento = documentos_dict.get(texto_documento)
        if not id_documento:
            return
        
        productos = procedimientos.obtener_productos_documento(id_documento)
        
        if not productos:
            label_vacio = ctk.CTkLabel(
                frame_productos,
                text="📦 No hay productos en este documento",
                font=("Arial", 14),
                text_color=COLOR_TEXTO_SECUNDARIO
            )
            label_vacio.pack(pady=30)
            return
        
        frame_lista = ctk.CTkScrollableFrame(
            frame_productos,
            fg_color=COLOR_FONDO_TERCIARIO,
            corner_radius=10,
            height=200
        )
        frame_lista.pack(fill="both", expand=True)
        
        label_instruccion = ctk.CTkLabel(
            frame_lista,
            text="✓ Seleccione los productos que desea incluir en la guía:",
            font=("Arial", 11, "bold"),
            text_color=COLOR_TEXTO
        )
        label_instruccion.pack(pady=(10, 15), padx=10, anchor="w")
        
        for prod in productos:
            var_check = ctk.BooleanVar(value=True)
            
            frame_item = ctk.CTkFrame(
                frame_lista, 
                fg_color=COLOR_FONDO_SECUNDARIO, 
                corner_radius=8,
                border_width=1,
                border_color=COLOR_BORDE
            )
            frame_item.pack(fill="x", padx=10, pady=5)
            
            checkbox = ctk.CTkCheckBox(
                frame_item,
                text="",
                variable=var_check,
                command=lambda p=prod, v=var_check: toggle_producto(p, v, productos_guia),
                width=30,
                checkbox_width=25,
                checkbox_height=25,
                fg_color=COLOR_EXITO,
                hover_color=COLOR_EXITO_HOVER
            )
            checkbox.pack(side="left", padx=10, pady=10)
            
            label_info = ctk.CTkLabel(
                frame_item,
                text=f"{prod[1]} | Cantidad: {prod[2]} {prod[3]}",
                font=("Arial", 11),
                text_color=COLOR_TEXTO,
                anchor="w"
            )
            label_info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            productos_guia.append({
                'id': prod[0],
                'nombre': prod[1],
                'cantidad': prod[2],
                'unidad_medida': prod[3],
                'var': var_check
            })
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar productos:\n{str(e)}")


# Añade o quita producto de la lista de la guía
def toggle_producto(producto, var_check, productos_guia):
    id_prod = producto[0]
    
    if var_check.get():
        existe = any(p['id'] == id_prod for p in productos_guia)
        if not existe:
            productos_guia.append({
                'id': producto[0],
                'nombre': producto[1],
                'cantidad': producto[2],
                'unidad_medida': producto[3],
                'var': var_check
            })
    else:
        productos_guia[:] = [p for p in productos_guia if p['id'] != id_prod]


# Centra ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")