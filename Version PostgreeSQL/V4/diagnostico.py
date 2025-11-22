# buscar_archivo_problematico.py
import os
import glob

postgres_dir = r"C:\Program Files\PostgreSQL\18"

print("Buscando archivos .conf con encoding incorrecto...\n")

archivos_conf = []
for root, dirs, files in os.walk(postgres_dir):
    for file in files:
        if file.endswith(('.conf', '.conf.sample')):
            archivos_conf.append(os.path.join(root, file))

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