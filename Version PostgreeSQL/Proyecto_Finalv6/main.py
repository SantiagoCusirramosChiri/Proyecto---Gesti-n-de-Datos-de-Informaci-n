# main.py 

import sys
import os

if sys.platform == 'win32':
    
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vista.postgres_config import abrir_config_postgres
from vista.login import abrir_login
from datos.conexion import ConexionDB

def verificar_usuario_existe():
    try:
        db = ConexionDB()
        db.conectar()
        
        if db.engine:
            db.desconectar()
            return True
        return False
    except:
        return False

def probar_conexion_lolcito():
    db = ConexionDB()
    
    try:
        db.conectar()
        
        if not db.engine:
            print("✗ No se pudo establecer conexión con la base de datos")
            return False
        
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
    if not verificar_usuario_existe():
        print("⚠ Usuario 'lolcito' no existe")
        print("→ Se requiere configuración inicial de PostgreSQL...\n")
    
        config_exitosa = abrir_config_postgres()
        
        if config_exitosa:
            print("\n→ Redirigiendo al login...\n")
            abrir_login()
        else:
            print("\n→ Configuración cancelada o fallida. Saliendo...\n")
            
    elif probar_conexion_lolcito():
        print("→ Redirigiendo al login...\n")
        abrir_login()
    else:
        print("→ Se requiere configuración de la base de datos...\n")
        config_exitosa = abrir_config_postgres()
        
        if config_exitosa:
            print("\n→ Redirigiendo al login...\n")
            abrir_login()
        else:
            print("\n→ Configuración cancelada o fallida. Saliendo...\n")