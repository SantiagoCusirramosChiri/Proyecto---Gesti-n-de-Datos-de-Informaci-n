# vista/postgres_config.py - CORREGIDO

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from logica.PostgresAuthBL import PostgresAuthBL

class VentanaConfigPostgres:
    """
    Ventana de configuración inicial de PostgreSQL.
    """
    
    def __init__(self):
        self.ventana = ttk.Window(themename="superhero")
        self.ventana.title("Configuración PostgreSQL")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)
        
        # Variable para saber si la configuración fue exitosa
        self.configuracion_exitosa = False
        
        # Centrar ventana
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (400 // 2)
        self.ventana.geometry(f"500x400+{x}+{y}")
        
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        frame_principal = ttk.Frame(self.ventana, padding=30)
        frame_principal.pack(fill=BOTH, expand=YES)
        
        # Título
        titulo = ttk.Label(
            frame_principal,
            text="Configuración Inicial de PostgreSQL",
            font=("Segoe UI", 16, "bold"),
            bootstyle="inverse-primary"
        )
        titulo.pack(pady=(0, 20))
        
        # Descripción
        descripcion = ttk.Label(
            frame_principal,
            text="Para continuar, necesitas configurar la base de datos.\n"
                 "Ingresa la contraseña del usuario administrador 'postgres'.",
            font=("Segoe UI", 10),
            justify=CENTER,
            wraplength=400
        )
        descripcion.pack(pady=(0, 30))
        
        # Frame para credenciales
        frame_credenciales = ttk.Frame(frame_principal)
        frame_credenciales.pack(fill=X, pady=10)
        
        # Label y Entry para contraseña
        ttk.Label(
            frame_credenciales,
            text="Contraseña de postgres:",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=(0, 5))
        
        self.entry_password = ttk.Entry(
            frame_credenciales,
            font=("Segoe UI", 11),
            show="•",
            width=40
        )
        self.entry_password.pack(fill=X)
        self.entry_password.focus()
        
        # Bind Enter key
        self.entry_password.bind("<Return>", lambda e: self.iniciar_configuracion())
        
        # Frame para mensajes
        self.frame_mensajes = ttk.Frame(frame_principal)
        self.frame_mensajes.pack(fill=BOTH, expand=YES, pady=20)
        
        self.label_mensaje = ttk.Label(
            self.frame_mensajes,
            text="",
            font=("Segoe UI", 9),
            wraplength=400,
            justify=LEFT
        )
        self.label_mensaje.pack()
        
        # Barra de progreso
        self.progressbar = ttk.Progressbar(
            frame_principal,
            mode='indeterminate',
            bootstyle="success-striped"
        )
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(side=BOTTOM, pady=(20, 0))
        
        self.btn_configurar = ttk.Button(
            frame_botones,
            text="Configurar Base de Datos",
            command=self.iniciar_configuracion,
            bootstyle="success",
            width=25
        )
        self.btn_configurar.pack(side=LEFT, padx=5)
        
        self.btn_cancelar = ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.cancelar,
            bootstyle="secondary",
            width=15
        )
        self.btn_cancelar.pack(side=LEFT, padx=5)
        
    def mostrar_mensaje(self, mensaje, tipo="info"):
        """Muestra un mensaje en la interfaz"""
        colores = {
            "info": "primary",
            "success": "success",
            "error": "danger",
            "warning": "warning"
        }
        
        self.label_mensaje.config(
            text=mensaje,
            bootstyle=colores.get(tipo, "primary")
        )
        self.ventana.update()
        
    def iniciar_configuracion(self):
        """Inicia el proceso de configuración"""
        password = self.entry_password.get().strip()
        
        if not password:
            self.mostrar_mensaje("⚠ Por favor, ingresa la contraseña de postgres", "warning")
            return
        
        # Deshabilitar botones
        self.btn_configurar.config(state=DISABLED)
        self.btn_cancelar.config(state=DISABLED)
        self.entry_password.config(state=DISABLED)
        
        # Mostrar progreso
        self.progressbar.pack(fill=X, pady=10)
        self.progressbar.start(10)
        
        # Ejecutar configuración
        self.mostrar_mensaje("⏳ Iniciando configuración...", "info")
        self.ventana.update()
        
        # Llamar a la lógica de negocio
        bl = PostgresAuthBL()
        exito, mensaje = bl.configurar_postgresql_completo(password)
        
        # Detener progreso
        self.progressbar.stop()
        self.progressbar.pack_forget()
        
        if exito:
            self.configuracion_exitosa = True  # ✅ Marcar como exitoso
            
            self.mostrar_mensaje(
                "✓ Configuración completada exitosamente.\n"
                "Ahora serás redirigido al login.",
                "success"
            )
            
            # Cerrar ventana automáticamente después de 2 segundos
            self.ventana.after(2000, self.cerrar_ventana)
            
            # Cambiar botón a "Continuar"
            self.btn_configurar.pack_forget()
            self.btn_cancelar.config(
                state=NORMAL, 
                text="Continuar",
                command=self.cerrar_ventana,
                bootstyle="success"
            )
        else:
            self.mostrar_mensaje(f"✗ Error: {mensaje}", "error")
            
            # Re-habilitar botones
            self.btn_configurar.config(state=NORMAL)
            self.btn_cancelar.config(state=NORMAL)
            self.entry_password.config(state=NORMAL)
    
    def cancelar(self):
        """Cancela y cierra la ventana sin marcar como exitoso"""
        self.configuracion_exitosa = False
        self.ventana.quit()
        self.ventana.destroy()
    
    def cerrar_ventana(self):
        """Cierra la ventana (se llama cuando la configuración fue exitosa)"""
        self.ventana.quit()
        self.ventana.destroy()
            
    def ejecutar(self):
        """Muestra la ventana y retorna True si la configuración fue exitosa"""
        self.ventana.mainloop()
        return self.configuracion_exitosa  # ✅ Retornar si fue exitoso


def abrir_config_postgres():
    """Función para abrir la ventana de configuración"""
    ventana = VentanaConfigPostgres()
    return ventana.ejecutar()  # ✅ Retornar resultado


if __name__ == "__main__":
    resultado = abrir_config_postgres()
    print(f"Configuración exitosa: {resultado}")