import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

# Configuración de la base de datos
db_url = "postgresql://neondb_owner:stWF2aPT6rXz@ep-white-fire-a4iyo3s3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
table_name = "equipos_db"

# Ruta del archivo Excel
excel_file_path = r"C:\Users\fgara\Downloads\equipos_db.xlsx"

# Leer el archivo Excel
try:
    data = pd.read_excel(excel_file_path, engine="openpyxl")
    print("Archivo Excel leído exitosamente.")
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    exit()

# Limpiar y preparar los datos
try:
    data["placa"] = data["placa"].fillna("SIN_PLACA").astype(str)  # Convertir NaN a 'SIN_PLACA'
    data["año_fabricación"] = data["año_fabricación"].fillna(0).astype(int)  # Asegurar enteros
    data["precio_compra"] = data["precio_compra"].fillna(0.0).astype(float)  # Asegurar flotantes
    print("Datos limpiados correctamente.")
except Exception as e:
    print(f"Error al limpiar los datos: {e}")
    exit()

# Crear conexión a la base de datos y reflejar la tabla
try:
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)  # Reflejar las tablas existentes en la base de datos
    table = metadata.tables.get(table_name)  # Obtener la tabla como objeto SQLAlchemy

    if table is None:
        raise ValueError(f"La tabla '{table_name}' no existe en la base de datos.")

    # Realizar el UPSERT
    with engine.begin() as connection:  # Usar begin() para commit automático
        for _, row in data.iterrows():
            stmt = insert(table).values(row.to_dict())
            stmt = stmt.on_conflict_do_update(
                index_elements=["placa"],  # Clave para detectar conflictos
                set_={
                    "nombre_equipo": stmt.excluded.nombre_equipo,
                    "marca": stmt.excluded.marca,
                    "modelo": stmt.excluded.modelo,
                    "serie": stmt.excluded.serie,
                    "año_fabricación": stmt.excluded.año_fabricación,
                    "propietario": stmt.excluded.propietario,
                    "precio_compra": stmt.excluded.precio_compra,
                },
            )
            connection.execute(stmt)
    print("Datos cargados o actualizados exitosamente en la base de datos.")
except Exception as e:
    print(f"Error al cargar los datos en la base de datos: {e}")
