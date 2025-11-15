# tabla.py

import customtkinter as ctk
from vista.componentes.colores import (
    COLOR_FONDO_SECUNDARIO,
    COLOR_TABLA_HEADER,
    COLOR_TABLA_ROW_PAR,
    COLOR_TABLA_ROW_IMPAR,
    COLOR_TABLA_HOVER,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_ROJO_PRIMARY,
    COLOR_BORDE
)


class TablaCustom(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.columnas = []
        self.anchos_columnas = []
        self.filas = []
        self.fila_actual = 0
        
        self.frame_contenedor = ctk.CTkFrame(
            self,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=10,
            border_width=2,
            border_color=COLOR_BORDE
        )
        self.frame_contenedor.pack(fill="both", expand=True)
        
        self.frame_scroll = ctk.CTkScrollableFrame(
            self.frame_contenedor,
            fg_color=COLOR_FONDO_SECUNDARIO,
            corner_radius=0
        )
        self.frame_scroll.pack(fill="both", expand=True, padx=2, pady=2)
        
    # Configura nombres y anchos de las columnas
    def configurar_columnas(self, nombres_columnas: list, anchos: list = None):
        self.columnas = nombres_columnas
        
        if anchos is None:
            ancho_total = 800
            ancho_col = ancho_total // len(nombres_columnas)
            self.anchos_columnas = [ancho_col] * len(nombres_columnas)
        else:
            self.anchos_columnas = anchos
        
        self.frame_header = ctk.CTkFrame(
            self.frame_scroll,
            fg_color=COLOR_TABLA_HEADER,
            corner_radius=0
        )
        self.frame_header.pack(fill="x", pady=(0, 2))
        
        for i, (nombre, ancho) in enumerate(zip(self.columnas, self.anchos_columnas)):
            label = ctk.CTkLabel(
                self.frame_header,
                text=nombre,
                font=("Arial", 12, "bold"),
                text_color=COLOR_ROJO_PRIMARY,
                width=ancho,
                anchor="center"
            )
            label.pack(side="left", padx=2, pady=8)
    
    # Agrega una fila de datos a la tabla
    def agregar_fila(self, datos: list, color_personalizado: str = None):
        if color_personalizado:
            color_fila = color_personalizado
        else:
            color_fila = COLOR_TABLA_ROW_PAR if self.fila_actual % 2 == 0 else COLOR_TABLA_ROW_IMPAR
        
        frame_fila = ctk.CTkFrame(
            self.frame_scroll,
            fg_color=color_fila,
            corner_radius=0
        )
        frame_fila.pack(fill="x", pady=1)
        
        def on_enter(e):
            frame_fila.configure(fg_color=COLOR_TABLA_HOVER)
        
        def on_leave(e):
            frame_fila.configure(fg_color=color_fila)
        
        frame_fila.bind("<Enter>", on_enter)
        frame_fila.bind("<Leave>", on_leave)
        
        for i, (dato, ancho) in enumerate(zip(datos, self.anchos_columnas)):
            label = ctk.CTkLabel(
                frame_fila,
                text=str(dato),
                font=("Arial", 11),
                text_color=COLOR_TEXTO,
                width=ancho,
                anchor="center"
            )
            label.pack(side="left", padx=2, pady=6)
            
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
        
        self.filas.append(frame_fila)
        self.fila_actual += 1
        
        return frame_fila
    
    # Agrega botones de acción a una fila
    def agregar_botones_accion(self, frame_fila, botones: list):
        frame_botones = ctk.CTkFrame(
            frame_fila,
            fg_color="transparent"
        )
        frame_botones.pack(side="right", padx=5)
        
        for texto, comando in botones:
            btn = ctk.CTkButton(
                frame_botones,
                text=texto,
                command=comando,
                width=80,
                height=28,
                font=("Arial", 10),
                fg_color=COLOR_ROJO_PRIMARY,
                hover_color=COLOR_ROJO_PRIMARY,
                corner_radius=5
            )
            btn.pack(side="left", padx=2)
    
    # Elimina todas las filas de la tabla
    def limpiar(self):
        for fila in self.filas:
            fila.destroy()
        
        self.filas = []
        self.fila_actual = 0
    
    # Muestra mensaje cuando no hay datos
    def mostrar_vacio(self, mensaje: str = "No hay datos para mostrar"):
        self.limpiar()
        
        frame_vacio = ctk.CTkFrame(
            self.frame_scroll,
            fg_color="transparent"
        )
        frame_vacio.pack(fill="both", expand=True, pady=40)
        
        label_icono = ctk.CTkLabel(
            frame_vacio,
            text="📋",
            font=("Arial", 60)
        )
        label_icono.pack(pady=(20, 10))
        
        label_mensaje = ctk.CTkLabel(
            frame_vacio,
            text=mensaje,
            font=("Arial", 14),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        label_mensaje.pack()
    
    # Retorna la cantidad de filas en la tabla
    def obtener_cantidad_filas(self) -> int:
        return len(self.filas)


# Crea y retorna una tabla simple con datos
def crear_tabla_simple(parent, columnas: list, datos: list, anchos: list = None):
    tabla = TablaCustom(parent)
    tabla.pack(fill="both", expand=True, pady=10)
    
    tabla.configurar_columnas(columnas, anchos)
    
    if datos:
        for fila in datos:
            tabla.agregar_fila(fila)
    else:
        tabla.mostrar_vacio()
    
    return tabla