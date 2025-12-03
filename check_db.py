import sqlite3

conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()

# Ver todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()

print("=== TABLAS EN LA BASE DE DATOS ===")
for tabla in tablas:
    print(f"\n📋 Tabla: {tabla[0]}")
    
    # Ver estructura de cada tabla
    cursor.execute(f"PRAGMA table_info({tabla[0]})")
    columnas = cursor.fetchall()
    
    print("  Columnas:")
    for col in columnas:
        print(f"    - {col[1]} ({col[2]})")

conn.close()
