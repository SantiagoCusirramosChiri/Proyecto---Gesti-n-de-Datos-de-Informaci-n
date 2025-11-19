# main.py
"""
Punto de entrada principal del sistema IRONtomb
Inicia la aplicación con la ventana de login
"""
import customtkinter as ctk

def main():
    """Función principal que inicia el sistema"""
    # Configuración global de CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Importar y ejecutar el login
    import vista.login as login_module
    
    # Si tu login.py tiene 'ventana' como variable global
    if hasattr(login_module, 'ventana'):
        login_module.ventana.mainloop()
    # Si tu login.py tiene la función crear_ventana_login
    elif hasattr(login_module, 'crear_ventana_login'):
        ventana_login = login_module.crear_ventana_login()
        ventana_login.mainloop()
    else:
        print("Error: No se encontró la ventana de login")
        print("Asegúrate de que login.py tenga 'ventana' o 'crear_ventana_login()'")

if __name__ == "__main__":
    main()