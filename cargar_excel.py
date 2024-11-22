import pandas as pd
from sqlalchemy import create_engine

# Ruta del archivo Excel
excel_path = r"C:\Users\fgara\OneDrive\Documentos\actividades_7.xlsx"

# Conexión a la base de datos PostgreSQL
db_url = "postgresql://neondb_owner:stWF2aPT6rXz@ep-white-fire-a4iyo3s3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Cargar los datos desde Excel
try:
    data = pd.read_excel(excel_path)
    print("Archivo Excel cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el archivo Excel: {e}")
    exit()

# Verificar el formato de los datos
print("Primeras filas de los datos:")
print(data.head())

# Eliminar filas con valores nulos en 'nombre_actividad'
try:
    data.dropna(subset=['nombre_actividad'], inplace=True)
    print("Filas con valores nulos en 'nombre_actividad' eliminadas.")
except Exception as e:
    print(f"Error al procesar las filas con valores nulos: {e}")
    exit()

# Normalizar los nombres de las columnas para que coincidan con la base de datos
column_mapping = {
    'id_actividad': 'id_actividad',
    'id_proyecto': 'id_proyecto',
    'nombre_actividad': 'nombre_actividad',
    'descripcíon': 'descripción'  # Cambiar para que coincida con la base de datos
}
data.rename(columns=column_mapping, inplace=True)

# Crear conexión a PostgreSQL usando SQLAlchemy
try:
    engine = create_engine(db_url)
    print("Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit()

# Cargar los datos en la tabla 'actividades'
try:
    data.to_sql('actividades', con=engine, if_exists='append', index=False)
    print("Datos cargados exitosamente en la tabla 'actividades'.")
except Exception as e:
    print(f"Error al cargar los datos en la base de datos: {e}")
