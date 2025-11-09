# vista/registro.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from logica.RegistroBL import RegistroBL

def abrir_registro(volver_al_login_callback):
    """Abre la ventana de registro"""
    
    # --- Ventana de registro ---
    ventana_registro = ctk.CTkToplevel()
    ventana_registro.title("Registro de Empresa - IRONtomb")
    ventana_registro.geometry("450x550")
    ventana_registro.resizable(False, False)
    ventana_registro.grab_set()  # Hace la ventana modal
    
    # --- Logo / Imagen ---
    try:
        imagen_logo = ctk.CTkImage(
            light_image=Image.open("recursos/simbolo.png"),
            dark_image=Image.open("recursos/simbolo.png"),
            size=(100, 100)
        )
        label_logo = ctk.CTkLabel(ventana_registro, image=imagen_logo, text="")
        label_logo.pack(pady=(20, 10))
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
    
    # --- Título ---
    label_titulo = ctk.CTkLabel(ventana_registro, text="Registro de Empresa", font=("Arial Black", 20))
    label_titulo.pack(pady=(0, 20))
    
    # --- Frame para los campos ---
    frame_campos = ctk.CTkFrame(ventana_registro)
    frame_campos.pack(pady=10, padx=20, fill="both", expand=True)
    
    # --- Campos de registro ---
    label_nombre = ctk.CTkLabel(frame_campos, text="Nombre de la Empresa:", font=("Arial", 12))
    label_nombre.pack(pady=(15, 5))
    entry_nombre = ctk.CTkEntry(frame_campos, placeholder_text="Ingrese nombre", width=300)
    entry_nombre.pack(pady=5)
    
    label_razon_social = ctk.CTkLabel(frame_campos, text="Razón Social:", font=("Arial", 12))
    label_razon_social.pack(pady=(15, 5))
    entry_razon_social = ctk.CTkEntry(frame_campos, placeholder_text="Ingrese razón social", width=300)
    entry_razon_social.pack(pady=5)
    
    label_ruc = ctk.CTkLabel(frame_campos, text="RUC (11 dígitos):", font=("Arial", 12))
    label_ruc.pack(pady=(15, 5))
    entry_ruc = ctk.CTkEntry(frame_campos, placeholder_text="Ingrese RUC", width=300)
    entry_ruc.pack(pady=5)
    
    # --- Función de registro ---
    def registrar():
        nombre = entry_nombre.get().strip()
        razon_social = entry_razon_social.get().strip()
        ruc = entry_ruc.get().strip()
        
        # Validación de campos vacíos
        if not nombre or not razon_social or not ruc:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validación de RUC
        if len(ruc) != 11 or not ruc.isdigit():
            messagebox.showerror("Error", "El RUC debe tener exactamente 11 dígitos numéricos")
            return
        
        # Intentar registro
        exito, mensaje = RegistroBL.registrar_empresa(nombre, razon_social, ruc)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana_registro.destroy()
            volver_al_login_callback()
        else:
            messagebox.showerror("Error en registro", mensaje)
    
    # --- Botón de registro ---
    btn_registrar = ctk.CTkButton(
        frame_campos, 
        text="Registrar Empresa", 
        command=registrar, 
        width=200,
        fg_color="#2E8B57",
        hover_color="#3CB371"
    )
    btn_registrar.pack(pady=20)
    
    # --- Botón para volver al login ---
    btn_volver = ctk.CTkButton(
        frame_campos,
        text="Volver al Login",
        command=ventana_registro.destroy,
        width=150,
        fg_color="transparent",
        text_color="#00BFFF",
        hover_color="#004C99"
    )
    btn_volver.pack(pady=10)
    
    # Centrar la ventana
    ventana_registro.update_idletasks()
    x = (ventana_registro.winfo_screenwidth() // 2) - (ventana_registro.winfo_width() // 2)
    y = (ventana_registro.winfo_screenheight() // 2) - (ventana_registro.winfo_height() // 2)
    ventana_registro.geometry(f"+{x}+{y}")
    
    return ventana_registro