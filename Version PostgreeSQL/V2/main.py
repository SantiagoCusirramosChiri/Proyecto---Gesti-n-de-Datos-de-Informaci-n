# main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vista.postgres_config import abrir_config_postgres
from vista.login import abrir_login
from datos.conexion import ConexionDB

def probar_conexion_lolcito():
    """
    Intenta conectar con el usuario lolcito a la base de datos sistema_documentos.
    Retorna True si la conexión es exitosa y la BD existe con las tablas necesarias.
    """
    db = ConexionDB()
    
    try:
        # Intentar conectar
        db.conectar()
        
        if not db.engine:
            print("✗ No se pudo establecer conexión con la base de datos")
            return False
        
        # Validar que existan las tablas principales
        resultado = db.ejecutar("""
            SELECT COUNT(*) as total
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('mae_ubicacion', 'mae_cliente', 'mae_producto', 'trs_encabezado_documento')
        """)
        
        if resultado and resultado[0]['total'] >= 4:
            print("✓ Conexión exitosa con usuario 'lolcito' - Base de datos configurada correctamente")
            db.desconectar()
            return True
        else:
            print("✗ Base de datos existe pero faltan tablas - Se requiere reconfiguración")
            db.desconectar()
            return False
        
    except Exception as e:
        print(f"✗ Error al validar conexión: {e}")
        db.desconectar()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("INICIANDO SISTEMA DE DOCUMENTOS")
    print("="*60 + "\n")
    
    if probar_conexion_lolcito():
        # Si la conexión con lolcito es exitosa y las tablas existen, ir directo al login
        print("→ Redirigiendo al login...\n")
        abrir_login()
    else:
        # Si falla, abrir configuración de PostgreSQL
        print("→ Se requiere configuración inicial de PostgreSQL...\n")
        abrir_config_postgres()