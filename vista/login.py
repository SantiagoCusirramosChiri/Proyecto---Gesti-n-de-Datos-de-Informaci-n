# vista/login.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from logica.LoginBL import LoginBL
from vista.index import abrir_index
from vista.registro import abrir_registro  # Importamos la función de registro

# Configuración de CustomTkinter
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

def abrir_login():
    """Función para abrir la ventana de login (para poder volver desde registro)"""
    
    # --- Ventana de login ---
    ventana = ctk.CTk()
    ventana.title("Inicio de sesión - IRONtomb")
    ventana.geometry("400x500")
    ventana.resizable(False, False)
    
    # --- Logo / Imagen ---
    try:
        imagen_logo = ctk.CTkImage(
            light_image=Image.open("recursos/simbolo.png"),
            dark_image=Image.open("recursos/simbolo.png"),
            size=(120, 120)
        )
        label_logo = ctk.CTkLabel(ventana, image=imagen_logo, text="")
        label_logo.pack(pady=(30, 10))
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
    
    # --- Nombre de la empresa ---
    label_titulo = ctk.CTkLabel(ventana, text="IRONtomb", font=("Arial Black", 24))
    label_titulo.pack(pady=(0, 30))
    
    # --- Campos de usuario y contraseña ---
    entry_usuario = ctk.CTkEntry(ventana, placeholder_text="Nombre de usuario", width=250)
    entry_usuario.pack(pady=10)
    
    entry_contrasena = ctk.CTkEntry(ventana, placeholder_text="Contraseña", width=250, show="*")
    entry_contrasena.pack(pady=10)
    
    # --- Función de inicio de sesión ---
    def iniciar_sesion():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        
        # Validación de campos vacíos
        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña")
            return
        
        # Validación de login usando la capa de negocio
        if LoginBL.validar_login(usuario, contrasena):
            ventana.destroy()  # Cerramos la ventana de login
            abrir_index()      # Abrimos ventana principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    # --- Botón de inicio de sesión ---
    btn_login = ctk.CTkButton(ventana, text="Iniciar sesión", command=iniciar_sesion, width=200)
    btn_login.pack(pady=20)
    
    # --- Registro ---
    label_registro = ctk.CTkLabel(ventana, text="¿No tienes cuenta?")
    label_registro.pack()
    
    # Función para abrir registro
    def abrir_ventana_registro():
        ventana.withdraw()  # Oculta la ventana de login
        abrir_registro(lambda: ventana.deiconify())  # Callback para volver
    
    btn_registro = ctk.CTkButton(
        ventana,
        text="Registrarse",
        command=abrir_ventana_registro,
        fg_color="transparent",
        text_color="#00BFFF",
        hover_color="#004C99"
    )
    btn_registro.pack(pady=10)
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
    y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
    ventana.geometry(f"+{x}+{y}")
    
    ventana.mainloop()

# Para mantener compatibilidad con el main.py existente
ventana = None

if __name__ == "__main__":
    abrir_login()