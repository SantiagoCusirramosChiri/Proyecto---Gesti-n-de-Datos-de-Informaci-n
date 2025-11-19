# login.py

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
from logica.LoginBL import LoginBL
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_FONDO_TERCIARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_ROJO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_BORDE
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Centra una ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# Muestra la ventana de inicio de sesión del sistema
def abrir_login():
    ventana = ctk.CTk()
    ventana.title("Inicio de sesión - IRONTOMB")
    ventana.geometry("450x750")
    ventana.resizable(False, False)
    ventana.configure(fg_color=COLOR_FONDO)
    centrar_ventana(ventana, 450, 750)

    frame_principal = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=20,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY
    )
    frame_principal.pack(pady=20, padx=30, fill="both", expand=True)

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
                size=(140, 140)
            )
            label_logo = ctk.CTkLabel(frame_principal, image=imagen_logo, text="")
            label_logo.pack(pady=(20, 5))
    except Exception as e:
        label_logo_alt = ctk.CTkLabel(
            frame_principal,
            text="🔥",
            font=("Arial Black", 80),
            text_color=COLOR_ROJO_PRIMARY
        )
        label_logo_alt.pack(pady=(20, 5))

    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="IRONtomb",
        font=("Arial Black", 32, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 5))

    label_subtitulo = ctk.CTkLabel(
        frame_principal,
        text="Sistema de Gestión Empresarial",
        font=("Arial", 12),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_subtitulo.pack(pady=(0, 20))

    frame_inputs = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_inputs.pack(pady=10, padx=40)

    label_usuario = ctk.CTkLabel(
        frame_inputs,
        text="Usuario",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_usuario.pack(anchor="w", pady=(0, 5))

    entry_usuario = ctk.CTkEntry(
        frame_inputs,
        placeholder_text="Nombre de la empresa",
        width=300,
        height=45,
        font=("Arial", 13),
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO,
        text_color=COLOR_TEXTO
    )
    entry_usuario.pack(pady=(0, 15))

    label_contrasena = ctk.CTkLabel(
        frame_inputs,
        text="RUC (11 dígitos)",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_contrasena.pack(anchor="w", pady=(0, 5))

    entry_contrasena = ctk.CTkEntry(
        frame_inputs,
        placeholder_text="Ingrese el RUC de 11 dígitos",
        width=300,
        height=45,
        font=("Arial", 13),
        show="●",
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO,
        text_color=COLOR_TEXTO
    )
    entry_contrasena.pack(pady=(0, 10))

    def iniciar_sesion():
        usuario = entry_usuario.get().strip()
        ruc = entry_contrasena.get().strip()

        if not usuario or not ruc:
            messagebox.showerror("Error", "Complete todos los campos", parent=ventana)
            return

        btn_login.configure(text="Verificando...", state="disabled")
        ventana.update()

        try:
            resultado = LoginBL.validar_login(usuario, ruc)
            
            if resultado:
                id_empresa = LoginBL.obtener_id_empresa(usuario, ruc)
                
                ventana.withdraw()
                
                try:
                    from vista.index import abrir_index
                    abrir_index(usuario, id_empresa)
                    ventana.destroy()
                except Exception as e:
                    ventana.deiconify()
                    btn_login.configure(text="INICIAR SESIÓN", state="normal")
                    messagebox.showerror("❌ Error", f"Error al abrir sistema: {str(e)}", parent=ventana)
            else:
                btn_login.configure(text="INICIAR SESIÓN", state="normal")
                messagebox.showerror(
                    "❌ Error",
                    "Usuario o RUC incorrectos",
                    parent=ventana
                )
        except Exception as e:
            if ventana.winfo_exists():
                btn_login.configure(text="INICIAR SESIÓN", state="normal")
                messagebox.showerror("❌ Error", f"Error del sistema: {str(e)}", parent=ventana)

    btn_login = ctk.CTkButton(
        frame_inputs,
        text="INICIAR SESIÓN",
        command=iniciar_sesion,
        width=300,
        height=50,
        font=("Arial Black", 14, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        text_color=COLOR_TEXTO,
        corner_radius=10
    )
    btn_login.pack(pady=(15, 5))

    entry_contrasena.bind("<Return>", lambda e: iniciar_sesion())
    entry_usuario.bind("<Return>", lambda e: entry_contrasena.focus())

    def mostrar_ventana_registro():
        try:
            from vista.registro import abrir_registro
            ventana.withdraw()
            
            def volver_al_login():
                ventana.deiconify()
            
            abrir_registro(volver_al_login)
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir registro: {e}", parent=ventana)

    frame_registro = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_registro.pack(pady=(10, 20))

    label_registro = ctk.CTkLabel(
        frame_registro,
        text="¿No tienes cuenta?",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_registro.pack()

    btn_registro = ctk.CTkButton(
        frame_registro,
        text="REGISTRARSE AHORA",
        command=mostrar_ventana_registro,
        width=200,
        height=35,
        font=("Arial", 12, "bold"),
        fg_color="transparent",
        text_color=COLOR_ROJO_CLARO,
        hover_color=COLOR_FONDO,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY,
        corner_radius=8
    )
    btn_registro.pack(pady=5)

    label_footer = ctk.CTkLabel(
        ventana,
        text="© 2024 IRONtomb - Todos los derechos reservados",
        font=("Arial", 9),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_footer.pack(side="bottom", pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    abrir_login()