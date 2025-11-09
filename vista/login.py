# vista/login.py
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from logica.LoginBL import LoginBL
from vista.index import abrir_index

# ============================================================================
# CONFIGURACIÓN DE TEMA ROJO Y NEGRO
# ============================================================================
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# Colores personalizados
COLOR_FONDO = "#0D0D0D"
COLOR_FONDO_SECUNDARIO = "#1A1A1A"
COLOR_ROJO_PRIMARY = "#DC143C"
COLOR_ROJO_HOVER = "#B71C1C"
COLOR_ROJO_CLARO = "#FF4444"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"
COLOR_BORDE = "#DC143C"

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ============================================================================
# VENTANA DE LOGIN
# ============================================================================
ventana = ctk.CTk()
ventana.title("Inicio de sesión - IRONTOMB")
ventana.geometry("450x750")
ventana.resizable(False, False)
ventana.configure(fg_color=COLOR_FONDO)
centrar_ventana(ventana, 450, 750)

# ============================================================================
# FRAME PRINCIPAL CON EFECTO DE CONTENEDOR
# ============================================================================
frame_principal = ctk.CTkFrame(
    ventana,
    fg_color=COLOR_FONDO_SECUNDARIO,
    corner_radius=20,
    border_width=2,
    border_color=COLOR_ROJO_PRIMARY
)
frame_principal.pack(pady=20, padx=30, fill="both")

# ============================================================================
# LOGO / IMAGEN
# ============================================================================
try:
    imagen_logo = ctk.CTkImage(
        light_image=Image.open("recursos/simbolo.png"),
        dark_image=Image.open("recursos/simbolo.png"),
        size=(140, 140)
    )
    label_logo = ctk.CTkLabel(
        frame_principal,
        image=imagen_logo,
        text="",
        fg_color="transparent"
    )
    label_logo.pack(pady=(20, 5))
except Exception as e:
    print(f"No se pudo cargar la imagen: {e}")
    label_logo_alt = ctk.CTkLabel(
        frame_principal,
        text="🔥",
        font=("Arial Black", 80),
        text_color=COLOR_ROJO_PRIMARY,
        fg_color="transparent"
    )
    label_logo_alt.pack(pady=(20, 5))

# ============================================================================
# NOMBRE DE LA EMPRESA
# ============================================================================
label_titulo = ctk.CTkLabel(
    frame_principal,
    text="IRONtomb",
    font=("Arial Black", 32, "bold"),
    text_color=COLOR_ROJO_PRIMARY,
    fg_color="transparent"
)
label_titulo.pack(pady=(0, 5))

label_subtitulo = ctk.CTkLabel(
    frame_principal,
    text="Sistema de Gestión Empresarial",
    font=("Arial", 12),
    text_color=COLOR_TEXTO_SECUNDARIO,
    fg_color="transparent"
)
label_subtitulo.pack(pady=(0, 20))

# ============================================================================
# FRAME PARA CAMPOS DE ENTRADA
# ============================================================================
frame_inputs = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)
frame_inputs.pack(pady=10, padx=40)

# --- Campo Usuario ---
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

# --- Campo Contraseña (RUC) ---
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

# ============================================================================
# FUNCIÓN DE INICIO DE SESIÓN
# ============================================================================
def iniciar_sesion():
    usuario = entry_usuario.get()
    ruc = entry_contrasena.get()

    # Animación del botón
    btn_login.configure(text="Verificando...", state="disabled")
    ventana.update()

    try:
        # Usar LoginBL para validar (resultado es booleano)
        resultado = LoginBL.validar_login(usuario, ruc)
        
        if resultado:  # ← Cambio aquí: resultado es True/False directamente

            id_empresa = LoginBL.obtener_id_empresa(usuario, ruc)
            
            messagebox.showinfo(
                "✅ Éxito",
                f"¡Bienvenido {usuario}!",
                parent=ventana
            )
            ventana.destroy()
            abrir_index(usuario, id_empresa)
        else:
            btn_login.configure(text="INICIAR SESIÓN", state="normal")
            messagebox.showerror(
                "❌ Error de Autenticación",
                "Usuario o contraseña incorrectos",
                parent=ventana
            )
    except Exception as e:
        btn_login.configure(text="INICIAR SESIÓN", state="normal")
        messagebox.showerror(
            "❌ Error del Sistema",
            f"Ocurrió un error inesperado: {str(e)}",
            parent=ventana
        )

# ============================================================================
# BOTÓN DE INICIO DE SESIÓN
# ============================================================================
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
    corner_radius=10,
    border_width=0
)
btn_login.pack(pady=(15, 5))

# Bind Enter key para login rápido
entry_contrasena.bind("<Return>", lambda e: iniciar_sesion())
entry_usuario.bind("<Return>", lambda e: entry_contrasena.focus())

# ============================================================================
# FUNCIÓN DE REGISTRO
# ============================================================================
def mostrar_ventana_registro():
    """Abre la ventana de registro y oculta el login"""
    try:
        from vista.registro import abrir_registro
        ventana.withdraw()  # Ocultar ventana de login
        
        # Función callback para volver al login
        def volver_al_login():
            ventana.deiconify()  # Mostrar ventana de login nuevamente
        
        # Abrir ventana de registro con el callback
        abrir_registro(volver_al_login)
        
    except ImportError as e:
        messagebox.showerror(
            "❌ Error",
            "No se pudo cargar el módulo de registro.\nAsegúrate de que vista/registro.py existe.",
            parent=ventana
        )
        print(f"Error de importación: {e}")
    except Exception as e:
        messagebox.showerror(
            "❌ Error",
            f"Ocurrió un error al abrir el registro: {str(e)}",
            parent=ventana
        )
        print(f"Error al abrir registro: {e}")

# ============================================================================
# SECCIÓN DE REGISTRO
# ============================================================================
frame_registro = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)
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
    command=mostrar_ventana_registro,  # ← Corregido aquí
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

# ============================================================================
# FOOTER
# ============================================================================
label_footer = ctk.CTkLabel(
    ventana,
    text="© 2024 IRONtomb - Todos los derechos reservados",
    font=("Arial", 9),
    text_color=COLOR_TEXTO_SECUNDARIO
)
label_footer.pack(side="bottom", pady=10)

# ============================================================================
# INICIAR APLICACIÓN
# ============================================================================
ventana.mainloop()