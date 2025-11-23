# colores.py - VERSIÓN FINAL CON MODO CLARO Y SISTEMA DE COLORES DIFERENCIADOS

# ============================================================================
# FONDOS CLAROS
# ============================================================================

COLOR_FONDO = "#F5F5F7"                     # Gris muy claro casi blanco
COLOR_FONDO_SECUNDARIO = "#FFFFFF"          # Blanco puro para frames
COLOR_FONDO_TERCIARIO = "#E8E8EA"          # Gris perla para botones

# ============================================================================
# ROJOS (MARCA PRINCIPAL)
# ============================================================================

COLOR_ROJO_PRIMARY = "#E85D75"              # Rojo coral suave (principal)
COLOR_ROJO_HOVER = "#D14D64"                # Rojo más saturado (hover)
COLOR_ROJO_CLARO = "#FFA5B8"                # Rosa pastel (acentos)

# ============================================================================
# TEXTOS
# ============================================================================

COLOR_TEXTO = "#2C2C2E"                     # Gris muy oscuro (casi negro)
COLOR_TEXTO_SECUNDARIO = "#000000"          # Gris medio
COLOR_TEXTO_TERCIARIO = "#000000"          # Gris claro

# ============================================================================
# BORDES
# ============================================================================

COLOR_BORDE = "#D1D1D6"                     # Gris claro suave
COLOR_BORDE_SECUNDARIO = "#E5E5EA"         # Gris muy claro

# ============================================================================
# BOTONES DE ACCIÓN (Sistema de identidad visual)
# ============================================================================

# VERDE - Para acciones de CREACIÓN (Nuevo, Guardar nuevo, Insertar)
COLOR_EXITO = "#52C27C"                     # Verde menta suave
COLOR_EXITO_HOVER = "#3FB068"               # Verde más saturado

# AMARILLO/NARANJA - Para acciones de EDICIÓN (Editar, Modificar, Actualizar registro)
COLOR_ADVERTENCIA = "#FFB84D"               # Naranja pastel suave
COLOR_ADVERTENCIA_HOVER = "#F5A623"        # Naranja más saturado

# AZUL - Para acciones de CONSULTA/ACTUALIZACIÓN (Refrescar, Actualizar lista, Ver)
COLOR_INFO = "#4A7BA7"                      # Azul medio oscuro
COLOR_INFO_HOVER = "#3A6B8F"                # Azul más oscuro

# ROJO - Para acciones DESTRUCTIVAS (Eliminar, Desactivar, Cancelar destructivo)
COLOR_ERROR = "#E85D75"                     # Rojo coral (usa el mismo de la marca)
COLOR_ERROR_HOVER = "#D14D64"               # Rojo más oscuro

# ============================================================================
# TABLAS
# ============================================================================

COLOR_TABLA_HEADER = "#F5F5F7"              # Igual al fondo
COLOR_TABLA_ROW_PAR = "#FFFFFF"             # Blanco
COLOR_TABLA_ROW_IMPAR = "#F8F8F9"          # Gris muy muy claro
COLOR_TABLA_HOVER = "#E8E8EA"               # Gris perla

# ============================================================================
# ESTADOS DE GUÍAS
# ============================================================================

COLOR_PENDIENTE = "#FFB84D"                 # Naranja pastel
COLOR_EMITIDO = "#52C27C"                   # Verde menta
COLOR_ANULADO = "#E85D75"                   # Rojo coral

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

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

