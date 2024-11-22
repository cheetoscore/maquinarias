from .connection import engine
from .models import Base, Usuarios, Equipos, Proyectos, Operadores
from sqlalchemy.orm import Session

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Insertar datos iniciales
def seed_data():
    with Session(engine) as session:
        # Usuarios de prueba
        usuario = Usuarios(nombre_usuario="admin", contraseña="admin123", dni_usuario="12345678")
        session.add(usuario)

        # Equipos de prueba
        equipo = Equipos(
            nombre_equipo="Excavadora CAT 320D",
            placa="XYZ123",
            marca="Caterpillar",
            modelo="320D",
            serie="SN123456",
            año_fabricación=2020,
            propietario="Empresa A",
            precio_compra=250000.0
        )
        session.add(equipo)

        # Proyectos de prueba
        proyecto = Proyectos(
            nombre_proyecto="Construcción de Puente",
            cliente="Cliente ABC",
            fecha_inicio="2024-01-01",
            fecha_fin="2024-12-31"
        )
        session.add(proyecto)

        # Operadores de prueba
        operador = Operadores(name_operador="Operador 1")
        session.add(operador)

        session.commit()

if __name__ == "__main__":
    seed_data()
