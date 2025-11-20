# vista/postgres_config.py

import customtkinter as ctk
from tkinter import messagebox
from logica.PostgresAuthBL import PostgresAuthBL
from vista.login import abrir_login
from vista.componentes.colores import (
    COLOR_FONDO,
    COLOR_FONDO_SECUNDARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_ROJO_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def centrar_ventana(ventana, ancho, alto):
    """Centra una ventana en la pantalla"""
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def abrir_config_postgres():
    """
    Muestra la ventana de configuración de PostgreSQL.
    Si la autenticación es exitosa y los scripts se ejecutan, abre automáticamente el login.
    """
    ventana = ctk.CTk()
    ventana.title("Configuración PostgreSQL - IRONTOMB")
    ventana.geometry("900x900")
    ventana.resizable(False, False)
    ventana.configure(fg_color=COLOR_FONDO)
    centrar_ventana(ventana, 500, 500)

    frame_principal = ctk.CTkFrame(
        ventana,
        fg_color=COLOR_FONDO_SECUNDARIO,
        corner_radius=20,
        border_width=2,
        border_color=COLOR_ROJO_PRIMARY
    )
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    # Ícono de base de datos
    label_icono = ctk.CTkLabel(
        frame_principal,
        text="🗄️",
        font=("Arial Black", 60)
    )
    label_icono.pack(pady=(30, 10))

    # Título
    label_titulo = ctk.CTkLabel(
        frame_principal,
        text="Configuración PostgreSQL",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 5))

    # Subtítulo
    label_subtitulo = ctk.CTkLabel(
        frame_principal,
        text="Ingrese usuario y contraseña de PostgreSQL",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_subtitulo.pack(pady=(0, 30))

    # Frame para el input
    frame_input = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_input.pack(pady=10, padx=30)

    # Label y Entry para usuario
    label_user = ctk.CTkLabel(
        frame_input,
        text="Usuario PostgreSQL",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_user.pack(anchor="w", pady=(0, 5))

    entry_user = ctk.CTkEntry(
        frame_input,
        placeholder_text="postgres",
        width=300,
        height=45,
        font=("Arial", 13),
        fg_color=COLOR_FONDO,
        border_color=COLOR_ROJO_PRIMARY,
        border_width=2,
        placeholder_text_color=COLOR_TEXTO_SECUNDARIO,
        text_color=COLOR_TEXTO
    )
    entry_user.pack(pady=(0, 15))
    entry_user.focus()

    # Label y Entry para contraseña
    label_password = ctk.CTkLabel(
        frame_input,
        text="Contraseña PostgreSQL",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_password.pack(anchor="w", pady=(0, 5))

    entry_password = ctk.CTkEntry(
        frame_input,
        placeholder_text="●●●●●●●●",
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
    entry_password.pack(pady=(0, 10))

    # Checkbox para mostrar contraseña
    var_mostrar = ctk.BooleanVar()
    
    def toggle_password():
        entry_password.configure(show="" if var_mostrar.get() else "●")
    
    check_mostrar = ctk.CTkCheckBox(
        frame_input,
        text="Mostrar contraseña",
        variable=var_mostrar,
        command=toggle_password,
        font=("Arial", 10),
        text_color=COLOR_TEXTO_SECUNDARIO,
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        border_color=COLOR_ROJO_PRIMARY
    )
    check_mostrar.pack(anchor="w", pady=(0, 20))

    # Función de validación y ejecución de scripts
    def validar_y_abrir_login():
        user = entry_user.get()
        password = entry_password.get()

        if not user or not password:
            messagebox.showerror("Error", "Debe ingresar usuario y contraseña", parent=ventana)
            return

        btn_confirmar.configure(text="Validando...", state="disabled")
        ventana.update()

        try:
            exito, mensaje = PostgresAuthBL.validar_usuario_password_postgres(user, password)

            if exito:
                messagebox.showinfo(
                    "✅ Éxito",
                    "PostgreSQL configurado correctamente",
                    parent=ventana
                )
                ventana.destroy()
                abrir_login()
            else:
                btn_confirmar.configure(text="CONFIRMAR", state="normal")
                messagebox.showerror("❌ Error", mensaje, parent=ventana)
                entry_password.delete(0, "end")
                entry_password.focus()
                
        except Exception as e:
            btn_confirmar.configure(text="CONFIRMAR", state="normal")
            messagebox.showerror("❌ Error", f"Error al validar: {str(e)}", parent=ventana)

    # Botón de confirmar
    btn_confirmar = ctk.CTkButton(
        frame_input,
        text="CONFIRMAR",
        command=validar_y_abrir_login,
        width=300,
        height=50,
        font=("Arial Black", 14, "bold"),
        fg_color=COLOR_ROJO_PRIMARY,
        hover_color=COLOR_ROJO_HOVER,
        text_color=COLOR_TEXTO,
        corner_radius=10
    )
    btn_confirmar.pack(pady=(5, 10))

    # Bind Enter key
    entry_password.bind("<Return>", lambda e: validar_y_abrir_login())

    # Footer
    label_footer = ctk.CTkLabel(
        frame_principal,
        text="Este usuario y contraseña se usarán para\nconectar y ejecutar scripts en la base de datos",
        font=("Arial", 9),
        text_color=COLOR_TEXTO_SECUNDARIO,
        justify="center"
    )
    label_footer.pack(side="bottom", pady=15)

    ventana.mainloop()
