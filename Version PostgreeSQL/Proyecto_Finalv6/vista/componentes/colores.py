
COLOR_FONDO = "#F5F5F7"                    
COLOR_FONDO_SECUNDARIO = "#FFFFFF"         
COLOR_FONDO_TERCIARIO = "#E8E8EA"         


COLOR_ROJO_PRIMARY = "#E85D75"             
COLOR_ROJO_HOVER = "#D14D64"                
COLOR_ROJO_CLARO = "#FFA5B8"                


COLOR_TEXTO = "#2C2C2E"                     
COLOR_TEXTO_SECUNDARIO = "#000000"         
COLOR_TEXTO_TERCIARIO = "#000000"          

COLOR_BORDE = "#D1D1D6"                     
COLOR_BORDE_SECUNDARIO = "#E5E5EA"         

COLOR_EXITO = "#52C27C"                     
COLOR_EXITO_HOVER = "#3FB068"               

COLOR_ADVERTENCIA = "#FFB84D"               
COLOR_ADVERTENCIA_HOVER = "#F5A623"        

COLOR_INFO = "#4A7BA7"                      
COLOR_INFO_HOVER = "#3A6B8F"                

COLOR_ERROR = "#E85D75"                    
COLOR_ERROR_HOVER = "#D14D64"               

COLOR_TABLA_HEADER = "#F5F5F7"            
COLOR_TABLA_ROW_PAR = "#FFFFFF"            
COLOR_TABLA_ROW_IMPAR = "#F8F8F9"          
COLOR_TABLA_HOVER = "#E8E8EA"              

COLOR_PENDIENTE = "#FFB84D"               
COLOR_EMITIDO = "#52C27C"                  
COLOR_ANULADO = "#E85D75"                   

def obtener_color_estado(estado: str) -> str:
    """Retorna el color según el estado de la guía"""
    estados = {
        'PENDIENTE': COLOR_PENDIENTE,
        'EMITIDO': COLOR_EMITIDO,
        'ANULADO': COLOR_ANULADO
    }
    return estados.get(estado.upper(), COLOR_TEXTO_SECUNDARIO)


def obtener_color_stock(stock: int, stock_minimo: int = 25) -> str:
    """Retorna el color según el nivel de stock"""
    if stock <= 0:
        return COLOR_ERROR
    elif stock <= stock_minimo:
        return COLOR_ADVERTENCIA
    else:
        return COLOR_EXITO

