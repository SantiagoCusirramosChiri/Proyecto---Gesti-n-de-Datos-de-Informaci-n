# buscar_archivo_problematico.py
import os
import glob

# Buscar en todas las versiones de PostgreSQL
postgres_base_dir = r"C:\Program Files\PostgreSQL"

print("Buscando archivos .conf con encoding incorrecto...\n")

archivos_conf = []
# Buscar en todas las versiones de PostgreSQL
if os.path.exists(postgres_base_dir):
    for version_dir in os.listdir(postgres_base_dir):
        full_version_path = os.path.join(postgres_base_dir, version_dir)
        if os.path.isdir(full_version_path):
            for root, dirs, files in os.walk(full_version_path):
                for file in files:
                    if file.endswith(('.conf', '.conf.sample')):
                        archivos_conf.append(os.path.join(root, file))
else:
    print("✗ No se encontró el directorio de PostgreSQL")
    exit(1)

for archivo in archivos_conf:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if len(contenido) > 85:
                print(f"✓ UTF-8 OK: {archivo}")
    except UnicodeDecodeError as e:
        print(f"⚠️ ERROR en posición {e.start}: {archivo}")
        print(f"   Bytes problemáticos: {e.object[e.start:e.start+10]}")
        
        # Intentar leer con cp1252
        try:
            with open(archivo, 'r', encoding='cp1252') as f:
                contenido = f.read()
                if 'ó' in contenido[:100] or 'ñ' in contenido[:100]:
                    print(f"   → Contiene caracteres Latin-1 (ó, ñ, etc.)")
                    print(f"   → Primeros 100 chars: {contenido[:100]}")
        except:
            pass
        print()