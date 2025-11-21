# vista/registro.py - CORREGIDO (sin error de scope)

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
from logica.RegistroBL import RegistroBL
from vista.componentes.colores import (
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO
)


def abrir_registro(volver_al_login_callback):
    """Muestra la ventana de registro de nuevas empresas"""
    ventana_registro = ctk.CTkToplevel()
    ventana_registro.title("Registro de Empresa - IRONtomb")
    ventana_registro.geometry("900x750")
    ventana_registro.resizable(False, False)
    ventana_registro.grab_set()
    ventana_registro.configure(fg_color="#1a1a1a")
    
    frame_principal = ctk.CTkFrame(ventana_registro, fg_color="transparent")
    frame_principal.pack(fill="both", expand=True, padx=40, pady=40)
    
    # LADO IZQUIERDO
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
    
    # LADO DERECHO
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
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_subtitulo_form.pack(pady=(0, 30))
    
    # Nombre
    label_nombre = ctk.CTkLabel(
        frame_scroll,
        text="Nombre de la Empresa *",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="Ej: Transportes SAC",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="white",
        placeholder_text_color="#6a6a6a",
        font=("Arial", 12)
    )
    entry_nombre.pack(fill="x", pady=(0, 15))
    
    # Razón Social
    label_razon_social = ctk.CTkLabel(
        frame_scroll,
        text="Razón Social *",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_razon_social.pack(fill="x", pady=(0, 5))
    
    entry_razon_social = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="Razón social completa",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="white",
        placeholder_text_color="#6a6a6a",
        font=("Arial", 12)
    )
    entry_razon_social.pack(fill="x", pady=(0, 15))
    
    # RUC
    label_ruc = ctk.CTkLabel(
        frame_scroll,
        text="RUC (11 dígitos) *",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_ruc.pack(fill="x", pady=(0, 5))
    
    entry_ruc = ctk.CTkEntry(
        frame_scroll,
        placeholder_text="20123456789",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="white",
        placeholder_text_color="#6a6a6a",
        font=("Arial", 12)
    )
    entry_ruc.pack(fill="x", pady=(0, 15))
    
    # Ubicación
    label_ubicacion = ctk.CTkLabel(
        frame_scroll,
        text="Ubicación *",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_ubicacion.pack(fill="x", pady=(0, 5))
    
    frame_ubicacion = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_ubicacion.pack(fill="x", pady=(0, 15))
    
    # Cargar ubicaciones iniciales
    ubicaciones = RegistroBL.obtener_ubicaciones_activas()
    ubicaciones_dict = {}
    ubicaciones_lista = []
    
    if ubicaciones and len(ubicaciones) > 0:
        ubicaciones_dict = {ub['descripcion']: ub['id_ubicacion'] for ub in ubicaciones}
        ubicaciones_lista = list(ubicaciones_dict.keys())
    
    # ComboBox
    combo_ubicacion = ctk.CTkComboBox(
        frame_ubicacion,
        values=ubicaciones_lista if ubicaciones_lista else ["Sin ubicaciones"],
        height=45,
        width=300,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        button_color=COLOR_ROJO_PRIMARY,
        button_hover_color=COLOR_ROJO_HOVER,
        dropdown_fg_color=COLOR_FONDO_TERCIARIO,
        text_color="white",
        font=("Arial", 12),
        state="readonly"
    )
    combo_ubicacion.set("Seleccione una ubicación")
    combo_ubicacion.pack(side="left", fill="x", expand=True)
    
    def abrir_nueva_ubicacion():
        """Abre ventana para crear nueva ubicación"""
        ventana_ubi = ctk.CTkToplevel(ventana_registro)
        ventana_ubi.title("Nueva Ubicación")
        ventana_ubi.geometry("400x250")
        ventana_ubi.resizable(False, False)
        ventana_ubi.grab_set()
        ventana_ubi.configure(fg_color=COLOR_FONDO_SECUNDARIO)
        
        frame_ubi = ctk.CTkFrame(ventana_ubi, fg_color="transparent")
        frame_ubi.pack(fill="both", expand=True, padx=30, pady=30)
        
        label_ubi_titulo = ctk.CTkLabel(
            frame_ubi,
            text="📍 Nueva Ubicación",
            font=("Arial Black", 20, "bold"),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_ubi_titulo.pack(pady=(0, 20))
        
        label_ubi_desc = ctk.CTkLabel(
            frame_ubi,
            text="Descripción *",
            font=("Arial", 11, "bold"),
            text_color="#b0b0b0",
            anchor="w"
        )
        label_ubi_desc.pack(fill="x", pady=(0, 5))
        
        entry_ubi_desc = ctk.CTkEntry(
            frame_ubi,
            placeholder_text="Ej: Lima - Perú",
            height=45,
            fg_color=COLOR_FONDO_TERCIARIO,
            text_color="white",
            font=("Arial", 12)
        )
        entry_ubi_desc.pack(fill="x", pady=(0, 20))
        
        def guardar_ubicacion():
            descripcion = entry_ubi_desc.get().strip()
            
            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria", parent=ventana_ubi)
                return
            
            exito, mensaje, id_ubicacion = RegistroBL.insertar_ubicacion(descripcion)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=ventana_ubi)
                
                # Recargar ubicaciones
                ubicaciones_nuevas = RegistroBL.obtener_ubicaciones_activas()
                
                if ubicaciones_nuevas:
                    # Actualizar diccionario y lista
                    ubicaciones_dict.clear()
                    ubicaciones_dict.update({ub['descripcion']: ub['id_ubicacion'] for ub in ubicaciones_nuevas})
                    
                    nuevas_descripciones = list(ubicaciones_dict.keys())
                    
                    # Actualizar combo
                    combo_ubicacion.configure(values=nuevas_descripciones)
                    combo_ubicacion.set(descripcion)
                
                ventana_ubi.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=ventana_ubi)
        
        btn_guardar_ubi = ctk.CTkButton(
            frame_ubi,
            text="Guardar Ubicación",
            command=guardar_ubicacion,
            height=45,
            fg_color=COLOR_ROJO_PRIMARY,
            hover_color=COLOR_ROJO_HOVER,
            font=("Arial", 13, "bold")
        )
        btn_guardar_ubi.pack(fill="x")
        
        entry_ubi_desc.bind("<Return>", lambda e: guardar_ubicacion())
    
    btn_nueva_ubicacion = ctk.CTkButton(
        frame_ubicacion,
        text="+ Nueva",
        command=abrir_nueva_ubicacion,
        width=100,
        height=45,
        fg_color=COLOR_FONDO_TERCIARIO,
        hover_color=COLOR_ROJO_HOVER,
        font=("Arial", 11, "bold")
    )
    btn_nueva_ubicacion.pack(side="right", padx=(10, 0))
    
    def registrar():
        """Registrar la empresa"""
        nombre = entry_nombre.get().strip()
        razon_social = entry_razon_social.get().strip()
        ruc = entry_ruc.get().strip()
        
        if not nombre or not razon_social or not ruc:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if combo_ubicacion.get() == "Seleccione una ubicación":
            messagebox.showerror("Error", "Debe seleccionar una ubicación")
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
        
        btn_registrar.configure(text="Registrando...", state="disabled")
        ventana_registro.update()
        
        try:
            exito, mensaje, id_empresa = RegistroBL.registrar_empresa(
                nombre, razon_social, ruc, id_ubicacion
            )
            
            btn_registrar.configure(text="Registrar Empresa", state="normal")
            
            if exito:
                messagebox.showinfo(
                    "✅ Éxito", 
                    f"{mensaje}\n\nID: {id_empresa}\n\nAhora puedes iniciar sesión."
                )
                ventana_registro.destroy()
                volver_al_login_callback()
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            btn_registrar.configure(text="Registrar Empresa", state="normal")
            messagebox.showerror("❌ Error", f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    btn_registrar = ctk.CTkButton(
        frame_scroll,
        text="Registrar Empresa",
        command=registrar,
        height=45,
        corner_radius=10,
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        text_color="white",
        font=("Arial", 13, "bold")
    )
    btn_registrar.pack(fill="x", pady=(10, 15))
    
    entry_ruc.bind("<Return>", lambda e: registrar())
    
    # Volver
    frame_volver = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_volver.pack(fill="x")
    
    label_ya_tienes = ctk.CTkLabel(
        frame_volver,
        text="¿Ya tienes cuenta?",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_ya_tienes.pack(side="left")
    
    btn_volver = ctk.CTkButton(
        frame_volver,
        text="Iniciar Sesión",
        command=lambda: [ventana_registro.destroy(), volver_al_login_callback()],
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
    
    ventana_registro.update_idletasks()
    x = (ventana_registro.winfo_screenwidth() // 2) - (ventana_registro.winfo_width() // 2)
    y = (ventana_registro.winfo_screenheight() // 2) - (ventana_registro.winfo_height() // 2)
    ventana_registro.geometry(f"+{x}+{y}")
    
    return ventana_registro