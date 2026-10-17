import pandas as pd
import sqlite3
import os

def ini_base_datos(rutas_csv, ruta_db="tiendas.db"):
    
    print("Iniciando ingesta de datos")
    
    conexion = sqlite3.connect(ruta_db)
    
    for nombre_tabla, ruta_archivo in rutas_csv.items():
        if os.path.exists(ruta_archivo):
            df = pd.read_csv(ruta_archivo)
            
            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            print(f" Tabla '{nombre_tabla}' cargada exitosamente con {len(df)} registros.")
        else:
            print(f" Archivo no encontrado: {ruta_archivo}")
    
    conexion.close()
    print(f"Base de datos estructurada lista en: {ruta_db}")

if __name__ == "__main__":
    
    archivos_datos = {
        "tiendas": "datos/tiendas.csv",
        "catologo_productos": "datos/catalogo_productos.csv",
        "ventas": "datos/ventas.csv",
        "inventario": "datos/inventario.csv",
        "tickets_mesa_servicio": "datos/tickets_mesa_servicio.csv"
    }
    
    ini_base_datos(archivos_datos)