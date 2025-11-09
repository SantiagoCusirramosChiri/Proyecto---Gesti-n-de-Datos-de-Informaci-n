import customtkinter as ctk

def abrir_index():
    ventana_index = ctk.CTk()
    ventana_index.title("Página de Inicio")
    ventana_index.state("zoomed")  # ventana completa
    ventana_index.geometry("800x600")  # tamaño inicial si no soporta zoomed

    label_bienvenida = ctk.CTkLabel(
        ventana_index,
        text="Bienvenido al sistema",
        font=("Arial Black", 32)
    )
    label_bienvenida.pack(pady=50)

    ventana_index.mainloop()
