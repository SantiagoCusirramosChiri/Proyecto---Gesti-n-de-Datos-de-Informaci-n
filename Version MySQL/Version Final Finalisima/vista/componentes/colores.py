# colores.py

#Principales

# Fondos

COLOR_FONDO = "#0D0D0D"                   
COLOR_FONDO_SECUNDARIO = "#1A1A1A"       
COLOR_FONDO_TERCIARIO = "#242424"         

# Rojos 

COLOR_ROJO_PRIMARY = "#DC143C"            
COLOR_ROJO_HOVER = "#B71C1C"              
COLOR_ROJO_CLARO = "#FF4444"              

# Textos

COLOR_TEXTO = "#FFFFFF"                   
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"     
COLOR_TEXTO_TERCIARIO = "#8A8A8A"        

# Bordes

COLOR_BORDE = "#DC143C"                   
COLOR_BORDE_SECUNDARIO = "#333333"       

#Estados

# Éxito

COLOR_EXITO = "#28A745"                 
COLOR_EXITO_HOVER = "#218838"             

# Error

COLOR_ERROR = "#DC143C"                  
COLOR_ERROR_HOVER = "#B71C1C"            

# Advertencia

COLOR_ADVERTENCIA = "#FFC107"             
COLOR_ADVERTENCIA_HOVER = "#E0A800"      

# Información

COLOR_INFO = "#17A2B8"                    
COLOR_INFO_HOVER = "#138496"          

#Tablas

COLOR_TABLA_HEADER = "#1A1A1A"            
COLOR_TABLA_ROW_PAR = "#0D0D0D"            
COLOR_TABLA_ROW_IMPAR = "#1A1A1A"          
COLOR_TABLA_HOVER = "#242424"             

#Estados Guía

COLOR_PENDIENTE = "#FFC107"                
COLOR_EMITIDO = "#28A745"                  
COLOR_ANULADO = "#DC143C"                 

#Getters

def obtener_color_estado(estado: str) -> str:

    estados = {
        'PENDIENTE': COLOR_PENDIENTE,
        'EMITIDO': COLOR_EMITIDO,
        'ANULADO': COLOR_ANULADO
    }
    return estados.get(estado.upper(), COLOR_TEXTO_SECUNDARIO)


def obtener_color_stock(stock: int, stock_minimo: int = 25) -> str:

    if stock <= 0:
        return COLOR_ERROR
    elif stock <= stock_minimo:
        return COLOR_ADVERTENCIA
    else:
        return COLOR_EXITO