from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a la base de datos
DATABASE_URL = "postgresql://neondb_owner:stWF2aPT6rXz@ep-white-fire-a4iyo3s3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
