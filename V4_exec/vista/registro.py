# registro.py

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


# Muestra la ventana de registro de nuevas empresas
def abrir_registro(volver_al_login_callback):
    ventana_registro = ctk.CTkToplevel()
    ventana_registro.title("Registro de Empresa - IRONtomb")
    ventana_registro.geometry("900x600")
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
    
    frame_form = ctk.CTkFrame(frame_derecho, fg_color="transparent")
    frame_form.pack(fill="both", expand=True, padx=40, pady=40)
    
    label_titulo = ctk.CTkLabel(
        frame_form,
        text="Crear Cuenta",
        font=("Arial Black", 28, "bold"),
        text_color="white"
    )
    label_titulo.pack(pady=(0, 10))
    
    label_subtitulo_form = ctk.CTkLabel(
        frame_form,
        text="Completa los datos de tu empresa",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_subtitulo_form.pack(pady=(0, 30))
    
    label_nombre = ctk.CTkLabel(
        frame_form,
        text="Nombre de la Empresa",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_nombre.pack(fill="x", pady=(0, 5))
    
    entry_nombre = ctk.CTkEntry(
        frame_form,
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
    
    label_razon_social = ctk.CTkLabel(
        frame_form,
        text="Razón Social",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_razon_social.pack(fill="x", pady=(0, 5))
    
    entry_razon_social = ctk.CTkEntry(
        frame_form,
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
    
    label_ruc = ctk.CTkLabel(
        frame_form,
        text="RUC (11 dígitos)",
        font=("Arial", 11, "bold"),
        text_color="#b0b0b0",
        anchor="w"
    )
    label_ruc.pack(fill="x", pady=(0, 5))
    
    entry_ruc = ctk.CTkEntry(
        frame_form,
        placeholder_text="20123456789",
        height=45,
        border_width=0,
        corner_radius=10,
        fg_color=COLOR_FONDO_TERCIARIO,
        text_color="white",
        placeholder_text_color="#6a6a6a",
        font=("Arial", 12)
    )
    entry_ruc.pack(fill="x", pady=(0, 25))
    
    def registrar():
        nombre = entry_nombre.get().strip()
        razon_social = entry_razon_social.get().strip()
        ruc = entry_ruc.get().strip()
        
        if not nombre or not razon_social or not ruc:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if len(ruc) != 11 or not ruc.isdigit():
            messagebox.showerror("Error", "El RUC debe tener exactamente 11 dígitos numéricos")
            return
        
        btn_registrar.configure(text="Registrando...", state="disabled")
        ventana_registro.update()
        
        try:
            exito, mensaje = RegistroBL.registrar_empresa(nombre, razon_social, ruc, id_ubicacion=1)
            
            btn_registrar.configure(text="Registrar Empresa", state="normal")
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                ventana_registro.destroy()
                volver_al_login_callback()
            else:
                messagebox.showerror("❌ Error", mensaje)
        
        except Exception as e:
            btn_registrar.configure(text="Registrar Empresa", state="normal")
            messagebox.showerror("❌ Error", f"Error del sistema: {str(e)}")
    
    btn_registrar = ctk.CTkButton(
        frame_form,
        text="Registrar Empresa",
        command=registrar,
        height=45,
        corner_radius=10,
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        text_color="white",
        font=("Arial", 13, "bold")
    )
    btn_registrar.pack(fill="x", pady=(0, 15))
    
    entry_ruc.bind("<Return>", lambda e: registrar())
    
    frame_volver = ctk.CTkFrame(frame_form, fg_color="transparent")
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