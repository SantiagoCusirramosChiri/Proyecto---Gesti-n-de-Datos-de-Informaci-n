# vista/registro.py
import customtkinter as ctk
from tkinter import messagebox
from logica.RegistroBL import RegistroBL

# Colores
COLOR_FONDO = "#0D0D0D"
COLOR_FONDO_SECUNDARIO = "#1A1A1A"
COLOR_ROJO_PRIMARY = "#DC143C"
COLOR_ROJO_HOVER = "#B71C1C"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"

def centrar_ventana(ventana_obj, ancho, alto):
    screen_width = ventana_obj.winfo_screenwidth()
    screen_height = ventana_obj.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana_obj.geometry(f"{ancho}x{alto}+{x}+{y}")

def crear_ventana_registro():
    """Crea y retorna la ventana de registro"""
    
    ventana = ctk.CTk()
    ventana.title("Registro de Empresa - IRONTOMB")
    ventana.geometry("500x700")
    ventana.resizable(False, False)
    ventana.configure(fg_color=COLOR_FONDO)
    centrar_ventana(ventana, 500, 700)

    # Frame principal
    frame_principal = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=20,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY
    )
    frame_principal.pack(pady=20, padx=30, fill="both", expand=True)

    # Título
    ctk.CTkLabel(
        frame_principal,
        text="🔥",
        font=("Arial Black", 60),
        text_color=COLOR_ROJO_PRIMARY
    ).pack(pady=(30, 10))

    ctk.CTkLabel(
        frame_principal,
        text="Registro de Empresa",
        font=("Arial Black", 28, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    ).pack(pady=(0, 10))

    ctk.CTkLabel(
        frame_principal,
        text="Complete los datos para registrarse",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    ).pack(pady=(0, 30))

    # Frame de inputs
    frame_inputs = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_inputs.pack(pady=10, padx=40, fill="both", expand=True)

    # Nombre de la empresa
    ctk.CTkLabel(
        frame_inputs,
        text="Nombre de la Empresa",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    ).pack(anchor="w", pady=(0, 5))

    entry_nombre = ctk.CTkEntry(
        frame_inputs,
        placeholder_text="Ej: Librería San Martín",
        width=350,
        height=45,
        font=("Arial", 13),
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        text_color=COLOR_TEXTO
    )
    entry_nombre.pack(pady=(0, 15))

    # Razón Social
    ctk.CTkLabel(
        frame_inputs,
        text="Razón Social",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    ).pack(anchor="w", pady=(0, 5))

    entry_razon = ctk.CTkEntry(
        frame_inputs,
        placeholder_text="Razón social completa",
        width=350,
        height=45,
        font=("Arial", 13),
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        text_color=COLOR_TEXTO
    )
    entry_razon.pack(pady=(0, 15))

    # RUC
    ctk.CTkLabel(
        frame_inputs,
        text="RUC (11 dígitos)",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    ).pack(anchor="w", pady=(0, 5))

    entry_ruc = ctk.CTkEntry(
        frame_inputs,
        placeholder_text="Ingrese el RUC de 11 dígitos",
        width=350,
        height=45,
        font=("Arial", 13),
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        text_color=COLOR_TEXTO
    )
    entry_ruc.pack(pady=(0, 20))

    # Función de registro
    def registrar():
        nombre = entry_nombre.get()
        razon = entry_razon.get()
        ruc = entry_ruc.get()

        btn_registrar.configure(text="Registrando...", state="disabled")
        ventana.update()

        try:
            exito, mensaje = RegistroBL.registrar_empresa(nombre, razon, ruc, 1)
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje, parent=ventana)
                ventana.destroy()
                
                # Volver al login
                from vista.login import crear_ventana_login
                ventana_login = crear_ventana_login()
                ventana_login.mainloop()
            else:
                btn_registrar.configure(text="REGISTRAR EMPRESA", state="normal")
                messagebox.showerror("❌ Error", mensaje, parent=ventana)
        except Exception as e:
            btn_registrar.configure(text="REGISTRAR EMPRESA", state="normal")
            messagebox.showerror("❌ Error", f"Error: {str(e)}", parent=ventana)

    # Botón registrar
    btn_registrar = ctk.CTkButton(
        frame_inputs,
        text="REGISTRAR EMPRESA",
        command=registrar,
        width=350,
        height=50,
        font=("Arial Black", 14, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        text_color=COLOR_TEXTO,
        corner_radius=10
    )
    btn_registrar.pack(pady=(0, 15))

    # Volver al login
    def volver_login():
        ventana.destroy()
        from vista.login import crear_ventana_login
        ventana_login = crear_ventana_login()
        ventana_login.mainloop()

    ctk.CTkButton(
        frame_inputs,
        text="← Volver al Login",
        command=volver_login,
        width=350,
        height=40,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        hover_color=COLOR_FONDO,
        text_color=COLOR_TEXTO_SECUNDARIO,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY,
        corner_radius=8
    ).pack()

    # Footer
    ctk.CTkLabel(
        ventana,
        text="© 2024 IRONtomb",
        font=("Arial", 9),
        text_color=COLOR_TEXTO_SECUNDARIO
    ).pack(side="bottom", pady=10)

    return ventana