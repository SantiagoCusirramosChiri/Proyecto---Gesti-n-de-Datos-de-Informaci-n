import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
from logica.RegistroBL import RegistroBL
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_EXITO,
    COLOR_EXITO_HOVER,
    COLOR_ERROR,
    COLOR_ERROR_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)


def abrir_registro(volver_al_login_callback):
    cambios_realizados = {'hubo_cambios': False}
    
    ventana_registro = ctk.CTkToplevel()
    ventana_registro.title("Registro de Empresa - IRONtomb")
    ventana_registro.geometry("900x750")
    ventana_registro.resizable(False, False)
    ventana_registro.grab_set()
    ventana_registro.configure(fg_color="#1a1a1a")
    
    frame_principal = ctk.CTkFrame(ventana_registro, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=40, pady=40)
    
    frame_izquierdo = ctk.CTkFrame(frame_principal, fg_color=COLOR_ROJO_PRIMARY, corner_radius=20)
    frame_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 20))
    
    try:
        ruta_logo = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "recursos",
            "simbolo.png"
        )
        if os.path.exists(ruta_logo):
            imagen_logo = ctk.CTkImage(
                light_image=Image.open(ruta_logo),
                dark_image=Image.open(ruta_logo),
                size=(180, 180)
            )
            label_logo = ctk.CTkLabel(frame_izquierdo, image=imagen_logo, text="")
            label_logo.pack(pady=(80, 30))
    except:
        label_logo_alt = ctk.CTkLabel(
            frame_izquierdo,
            text="🔥",
            font=("Arial Black", 100)
        )
        label_logo_alt.pack(pady=(80, 30))
    
    label_bienvenida = ctk.CTkLabel(
        frame_izquierdo,
        text="Únete a\nIRONtomb",
        font=("Arial Black", 32, "bold"),
        text_color="white",
        justify="center"
    )
    label_bienvenida.pack(pady=20)
    
    label_subtitulo = ctk.CTkLabel(
        frame_izquierdo,
        text="Gestiona tu empresa de manera\neficiente y profesional",
        font=("Arial", 14),
        text_color="#ffdddd",
        justify="center"
    )
    label_subtitulo.pack(pady=10)
    frame_derecho = ctk.CTkFrame(frame_principal, fg_color=COLOR_FONDO_SECUNDARIO, corner_radius=20)
    frame_derecho.pack(side="right", fill="both", expand=True)
    
    frame_scroll = ctk.CTkScrollableFrame(frame_derecho, fg_color="transparent")
    frame_scroll.pack(fill="both", expand=True, padx=40, pady=40)
    
    label_titulo = ctk.CTkLabel(
        frame_scroll,
        text="Crear Cuenta",
        font=("Arial Black", 28, "bold"),
        text_color="white"
    )
    label_titulo.pack(pady=(0, 10))
    
    label_subtitulo_form = ctk.CTkLabel(
        frame_scroll,
        text="Completa los datos de tu empresa",
        font=("Arial", 12),
        text_color="#cccccc"
    )
    label_subtitulo_form.pack(pady=(0, 30))
    def registrar_cambio(event=None):
        """Marca que hubo cambios en el formulario"""
        cambios_realizados['hubo_cambios'] = True

    label_nombre = ctk.CTkLabel(
        frame_scroll,
        text="Nombre de la Empresa *",
        font=("Arial", 11, "bold"),
        text_color="#1a1a1a",
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="Ej: Transportes SAC",
        placeholder_text_color="#2C2C2E",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="#1a1a1a",
        font=("Arial", 12)
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    entry_nombre.bind("<KeyRelease>", registrar_cambio)
    
    label_razon_social = ctk.CTkLabel(
        frame_scroll,
        text="Razón Social *",
        font=("Arial", 11, "bold"),
        text_color="#1a1a1a",
        anchor="w"
    )
    label_razon_social.pack(fill="x", pady=(0, 5))
    
    entry_razon_social = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="Razón social completa",
        placeholder_text_color="#2C2C2E",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="#1a1a1a",
        font=("Arial", 12)
    )
    entry_razon_social.pack(fill="x", pady=(0, 15))
    entry_razon_social.bind("<KeyRelease>", registrar_cambio)
    
    label_ruc = ctk.CTkLabel(
        frame_scroll,
        text="RUC (11 dígitos) *",
        font=("Arial", 11, "bold"),
        text_color="#1a1a1a",
        anchor="w"
    )
    label_ruc.pack(fill="x", pady=(0, 5))
    
    entry_ruc = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="20123456789",
        placeholder_text_color="#2C2C2E",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="#1a1a1a",
        font=("Arial", 12)
    )
    entry_ruc.pack(fill="x", pady=(0, 15))
    entry_ruc.bind("<KeyRelease>", registrar_cambio)
    
    label_ubicacion = ctk.CTkLabel(
        frame_scroll,
        text="Ubicación *",
        font=("Arial", 11, "bold"),
        text_color="#1a1a1a",
        anchor="w"
    )
    label_ubicacion.pack(fill="x", pady=(0, 5))
    
    frame_ubicacion = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_ubicacion.pack(fill="x", pady=(0, 15))
    
    frame_ubicacion.grid_columnconfigure(0, weight=1)  
    frame_ubicacion.grid_columnconfigure(1, weight=0) 
    
    ubicaciones = RegistroBL.obtener_ubicaciones_activas()
    ubicaciones_dict = {}
    ubicaciones_lista = []
    
    if ubicaciones and len(ubicaciones) > 0:
        ubicaciones_dict = {ub['descripcion']: ub['id_ubicacion'] for ub in ubicaciones}
        ubicaciones_lista = list(ubicaciones_dict.keys())
    
    combo_ubicacion = ctk.CTkComboBox(
    frame_ubicacion,
    values=ubicaciones_lista if ubicaciones_lista else ["Sin ubicaciones"],
    height=45,
    corner_radius=10,
    fg_color=COLOR_FONDO_TERCIARIO,  
    button_color=COLOR_ROJO_PRIMARY,  
    button_hover_color=COLOR_ROJO_HOVER,  
    dropdown_fg_color="#FFFFFF",  
    dropdown_hover_color=COLOR_ROJO_PRIMARY,  
    dropdown_text_color="#1a1a1a",  
    text_color="#1a1a1a",  
    font=("Arial", 12),
    state="readonly"
    )
    combo_ubicacion.set("Seleccione una ubicación")
    combo_ubicacion.grid(row=0, column=0, sticky="ew", padx=(0, 10))
    
    def abrir_nueva_ubicacion():
        """Abre ventana para crear nueva ubicación"""
        cambios_ubicacion = {'hubo_cambios': False}
        
        ventana_ubi = ctk.CTkToplevel(ventana_registro)
        ventana_ubi.title("Nueva Ubicación")
        ventana_ubi.geometry("500x350")
        ventana_ubi.resizable(False, False)
        ventana_ubi.grab_set()
        ventana_ubi.configure(fg_color=COLOR_FONDO)
        
        ventana_ubi.update_idletasks()
        x = (ventana_ubi.winfo_screenwidth() // 2) - (500 // 2)
        y = (ventana_ubi.winfo_screenheight() // 2) - (350 // 2)
        ventana_ubi.geometry(f"500x350+{x}+{y}")
        
        frame_ubi = ctk.CTkFrame(
            ventana_ubi,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDE
        )
        frame_ubi.pack(fill="both", expand=True, padx=20, pady=20)
        
        label_ubi_titulo = ctk.CTkLabel(
            frame_ubi,
            text="📍 Nueva Ubicación",
            font=("Arial Black", 20, "bold"),
            text_color=COLOR_EXITO
        )
        label_ubi_titulo.pack(pady=(20, 30))
        
        frame_campos_ubi = ctk.CTkFrame(frame_ubi, fg_color="transparent")
        frame_campos_ubi.pack(fill="both", expand=True, padx=30)
        
        label_ubi_desc = ctk.CTkLabel(
            frame_campos_ubi,
            text="Descripción de la Ubicación *",
            font=("Arial", 11, "bold"),
            text_color="#1a1a1a",
            anchor="w"
        )
        label_ubi_desc.pack(fill="x", pady=(0, 5))
        
        entry_ubi_desc = ctk.CTkEntry(
            frame_campos_ubi,
            placeholder_text="Ej: Av. Principal 123, Lima - Perú",
            placeholder_text_color="#2C2C2E",
            height=45,
            fg_color=COLOR_FONDO_TERCIARIO,
            text_color="#1a1a1a",
            font=("Arial", 12)
        )
        entry_ubi_desc.pack(fill="x", pady=(0, 10))
        entry_ubi_desc.bind("<KeyRelease>", lambda e: cambios_ubicacion.update({'hubo_cambios': True}))
        
        # Ayuda
        frame_ayuda_ubi = ctk.CTkFrame(
            frame_campos_ubi,
            fg_color=COLOR_FONDO_TERCIARIO,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_BORDE
        )
        frame_ayuda_ubi.pack(fill="x", pady=(0, 20))
        
        label_ayuda_ubi = ctk.CTkLabel(
            frame_ayuda_ubi,
            text="💡 Mínimo 10 caracteres, máximo 100.",
            font=("Arial", 10),
            text_color="#666666",
            anchor="w",
            justify="left"
        )
        label_ayuda_ubi.pack(fill="x", padx=12, pady=10)
        
        def guardar_ubicacion_con_confirmacion():
            descripcion = entry_ubi_desc.get().strip()
            
            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria", parent=ventana_ubi)
                entry_ubi_desc.focus()
                return
            
            if len(descripcion) < 10:
                messagebox.showerror("Error", "La descripción debe tener al menos 10 caracteres", parent=ventana_ubi)
                entry_ubi_desc.focus()
                return
            
            respuesta = messagebox.askyesno(
                "Confirmar Registro",
                f"¿Está seguro que desea registrar esta ubicación?\n\n"
                f"📍 Ubicación: {descripcion}",
                parent=ventana_ubi
            )
            
            if not respuesta:
                return
            
            btn_guardar_ubi.configure(text="⏳ Guardando...", state="disabled")
            btn_cancelar_ubi.configure(state="disabled")
            ventana_ubi.update()
            
            try:
                exito, mensaje, id_ubicacion = RegistroBL.insertar_ubicacion(descripcion)
                
                if exito:
                    messagebox.showinfo("✅ Éxito", mensaje, parent=ventana_ubi)
                    
                    ubicaciones_nuevas = RegistroBL.obtener_ubicaciones_activas()
                    
                    if ubicaciones_nuevas:
                        ubicaciones_dict.clear()
                        ubicaciones_dict.update({ub['descripcion']: ub['id_ubicacion'] for ub in ubicaciones_nuevas})
                        
                        nuevas_descripciones = list(ubicaciones_dict.keys())
                        combo_ubicacion.configure(values=nuevas_descripciones)
                        combo_ubicacion.set(descripcion)
                    
                    ventana_ubi.destroy()
                else:
                    messagebox.showerror("❌ Error", mensaje, parent=ventana_ubi)
                    btn_guardar_ubi.configure(text="💾 Guardar", state="normal")
                    btn_cancelar_ubi.configure(state="normal")
            
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana_ubi)
                btn_guardar_ubi.configure(text="💾 Guardar", state="normal")
                btn_cancelar_ubi.configure(state="normal")
        
        def cancelar_ubicacion_con_confirmacion():
            if cambios_ubicacion['hubo_cambios']:
                respuesta = messagebox.askyesno(
                    "Confirmar Cancelación",
                    "¿Está seguro que desea cancelar?\n\nSe perderán todos los cambios realizados.",
                    parent=ventana_ubi
                )
                if respuesta:
                    ventana_ubi.destroy()
            else:
                ventana_ubi.destroy()
        
        # Botones
        frame_botones_ubi = ctk.CTkFrame(frame_ubi, fg_color="transparent")
        frame_botones_ubi.pack(fill="x", padx=30, pady=(0, 20))
        
        btn_cancelar_ubi = ctk.CTkButton(
            frame_botones_ubi,
            text="❌ Cancelar",
            command=cancelar_ubicacion_con_confirmacion,
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            hover_color=COLOR_FONDO_TERCIARIO,
            text_color=COLOR_ERROR,
            border_width=2,
            border_color=COLOR_ERROR,
            height=45,
            corner_radius=10
        )
        btn_cancelar_ubi.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        btn_guardar_ubi = ctk.CTkButton(
            frame_botones_ubi,
            text="💾 Guardar",
            command=guardar_ubicacion_con_confirmacion,
            height=45,
            fg_color=COLOR_EXITO,
            hover_color=COLOR_EXITO_HOVER,
            font=("Arial", 12, "bold"),
            corner_radius=10,
            text_color="white"
        )
        btn_guardar_ubi.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        entry_ubi_desc.bind("<Return>", lambda e: guardar_ubicacion_con_confirmacion())
        ventana_ubi.bind("<Escape>", lambda e: cancelar_ubicacion_con_confirmacion())
        entry_ubi_desc.focus()
    
    btn_nueva_ubicacion = ctk.CTkButton(
        frame_ubicacion,
        text="+ Nueva",
        command=abrir_nueva_ubicacion,
        width=100,
        height=45,
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        font=("Arial", 11, "bold"),
        text_color="white"
    )
    btn_nueva_ubicacion.grid(row=0, column=1, sticky="e") 
    
    def registrar_con_confirmacion():
        nombre = entry_nombre.get().strip()
        razon_social = entry_razon_social.get().strip()
        ruc = entry_ruc.get().strip()
        
        # Validaciones
        if not nombre or not razon_social or not ruc:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if combo_ubicacion.get() == "Seleccione una ubicación" or combo_ubicacion.get() == "Sin ubicaciones":
            messagebox.showerror("Error", "Debe seleccionar una ubicación válida")
            return
        
        ubicacion_seleccionada = combo_ubicacion.get()
        id_ubicacion = ubicaciones_dict.get(ubicacion_seleccionada)
        
        if not id_ubicacion:
            messagebox.showerror("Error", "Ubicación inválida")
            return
        
        ruc_valido, mensaje_ruc = RegistroBL.validar_ruc(ruc)
        if not ruc_valido:
            messagebox.showerror("Error", mensaje_ruc)
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Registro",
            f"¿Está seguro que desea registrar esta empresa?\n\n"
            f"🏢 Nombre: {nombre}\n"
            f"📄 Razón Social: {razon_social}\n"
            f"🆔 RUC: {ruc}\n"
            f"📍 Ubicación: {ubicacion_seleccionada}"
        )
        
        if not respuesta:
            return
        btn_registrar.configure(text="⏳ Registrando...", state="disabled")
        btn_volver.configure(state="disabled")
        ventana_registro.update()
        
        try:
            exito, mensaje, id_empresa = RegistroBL.registrar_empresa(
                nombre, razon_social, ruc, id_ubicacion
            )
            
            if exito:
                messagebox.showinfo(
                    "✅ Éxito", 
                    f"{mensaje}\n\nID de Empresa: {id_empresa}\n\nAhora puedes iniciar sesión con este ID."
                )
                ventana_registro.destroy()
                volver_al_login_callback()
            else:
                messagebox.showerror("❌ Error", mensaje)
                btn_registrar.configure(text="✅ Registrar Empresa", state="normal")
                btn_volver.configure(state="normal")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error: {str(e)}")
            btn_registrar.configure(text="✅ Registrar Empresa", state="normal")
            btn_volver.configure(state="normal")
            import traceback
            traceback.print_exc()

    def volver_con_confirmacion():
        """Solicita confirmación antes de volver si hay cambios"""
        if cambios_realizados['hubo_cambios']:
            respuesta = messagebox.askyesno(
                "Confirmar Cancelación",
                "¿Está seguro que desea volver?\n\nSe perderán todos los cambios realizados."
            )
            if respuesta:
                ventana_registro.destroy()
                volver_al_login_callback()
        else:
            ventana_registro.destroy()
            volver_al_login_callback()
    
    btn_registrar = ctk.CTkButton(
        frame_scroll,
        text="✅ Registrar Empresa",
        command=registrar_con_confirmacion,
        height=45,
        corner_radius=10,
        fg_color=COLOR_EXITO,
        hover_color=COLOR_EXITO_HOVER,
        text_color="white",
        font=("Arial", 13, "bold")
    )
    btn_registrar.pack(fill="x", pady=(10, 15))
    
    entry_ruc.bind("<Return>", lambda e: registrar_con_confirmacion())
    
    frame_volver = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_volver.pack(fill="x")
    
    label_ya_tienes = ctk.CTkLabel(
        frame_volver,
        text="¿Ya tienes cuenta?",
        font=("Arial", 11),
        text_color="#cccccc"
    )
    label_ya_tienes.pack(side="left")
    
    btn_volver = ctk.CTkButton(
        frame_volver,
        text="Iniciar Sesión",
        command=volver_con_confirmacion,
        width=100,
        height=25,
        corner_radius=5,
        fg_color="transparent",
        hover_color=COLOR_FONDO_TERCIARIO,
        text_color=COLOR_ROJO_PRIMARY,
        font=("Arial", 11, "bold"),
        border_width=0
    )
    btn_volver.pack(side="left", padx=5)
    
    ventana_registro.bind("<Escape>", lambda e: volver_con_confirmacion())
    
    ventana_registro.update_idletasks()
    x = (ventana_registro.winfo_screenwidth() // 2) - (ventana_registro.winfo_width() // 2)
    y = (ventana_registro.winfo_screenheight() // 2) - (ventana_registro.winfo_height() // 2)
    ventana_registro.geometry(f"+{x}+{y}")
    
    return ventana_registro