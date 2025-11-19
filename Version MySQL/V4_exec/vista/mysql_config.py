# vista/mysql_config.py

import customtkinter as ctk
from tkinter import messagebox
from logica.MySQLAuthBL import MySQLAuthBL
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


def abrir_config_mysql():
    """
    Muestra la ventana de configuración de MySQL
    Si la autenticación es exitosa, abre automáticamente el login
    """
    ventana = ctk.CTk()
    ventana.title("Configuración MySQL - IRONTOMB")
    ventana.geometry("400x400")
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
        text="Configuración MySQL",
        font=("Arial Black", 22, "bold"),
        text_color=COLOR_ROJO_PRIMARY
    )
    label_titulo.pack(pady=(0, 5))

    # Subtítulo
    label_subtitulo = ctk.CTkLabel(
        frame_principal,
        text="Ingrese la contraseña de root",
        font=("Arial", 11),
        text_color=COLOR_TEXTO_SECUNDARIO
    )
    label_subtitulo.pack(pady=(0, 30))

    # Frame para el input
    frame_input = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_input.pack(pady=10, padx=30)

    # Label de contraseña
    label_password = ctk.CTkLabel(
        frame_input,
        text="Contraseña MySQL",
        font=("Arial", 12, "bold"),
        text_color=COLOR_TEXTO,
        anchor="w"
    )
    label_password.pack(anchor="w", pady=(0, 5))

    # Entry de contraseña
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
    entry_password.focus()

    # Checkbox para mostrar contraseña
    var_mostrar = ctk.BooleanVar()
    
    def toggle_password():
        if var_mostrar.get():
            entry_password.configure(show="")
        else:
            entry_password.configure(show="●")
    
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

    def validar_y_abrir_login():
        password = entry_password.get()

        if not password:
            messagebox.showerror("Error", "Debe ingresar la contraseña", parent=ventana)
            return

        btn_confirmar.configure(text="Validando...", state="disabled")
        ventana.update()

        try:
            # Validar contraseña usando la capa de lógica
            exito, mensaje = MySQLAuthBL.validar_password_mysql(password)
            
            if exito:
                messagebox.showinfo(
                    "✅ Éxito",
                    "Conexión MySQL configurada correctamente",
                    parent=ventana
                )
                
                # Cerrar ventana de configuración
                ventana.destroy()
                
                # Abrir el login (la vista decide qué hacer después)
                abrir_login()
                
            else:
                btn_confirmar.configure(text="CONFIRMAR", state="normal")
                messagebox.showerror(
                    "❌ Error",
                    mensaje,
                    parent=ventana
                )
                entry_password.delete(0, "end")
                entry_password.focus()
                
        except Exception as e:
            btn_confirmar.configure(text="CONFIRMAR", state="normal")
            messagebox.showerror(
                "❌ Error",
                f"Error al validar: {str(e)}",
                parent=ventana
            )

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
        text="Esta contraseña se usará para todas\nlas conexiones a la base de datos",
        font=("Arial", 9),
        text_color=COLOR_TEXTO_SECUNDARIO,
        justify="center"
    )
    label_footer.pack(side="bottom", pady=15)

    ventana.mainloop()
