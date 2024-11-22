from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Modelo para la tabla Usuarios
class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, nullable=False)
    contraseña = Column(String, nullable=False)
    dni_usuario = Column(String, unique=True, nullable=False)

    # Relación con Designación
    designaciones = relationship("Designación", back_populates="usuario")

# Modelo para la tabla Equipos
class Equipos(Base):
    __tablename__ = "equipos_db"

    id_equipo = Column(Integer, primary_key=True, index=True)
    nombre_equipo = Column(String, nullable=False)
    placa = Column(String, unique=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    serie = Column(String, unique=True, nullable=False)
    año_fabricación = Column(Integer, nullable=False)
    propietario = Column(String, nullable=False)
    precio_compra = Column(Float, nullable=False)

    # Relación con Designación
    designaciones = relationship("Designación", back_populates="equipo")

# Modelo para la tabla Proyectos
class Proyectos(Base):
    __tablename__ = "proyectos"

    id_proyecto = Column(Integer, primary_key=True, index=True)
    nombre_proyecto = Column(String, nullable=False)
    cliente = Column(String, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    ubicacion = Column(String, nullable=True)  # Nueva columna para la ubicación

    # Relación con Designación
    designaciones = relationship("Designación", back_populates="proyecto")

# Modelo para la tabla Designación
class Designación(Base):
    __tablename__ = "designación"

    id_designación = Column(Integer, primary_key=True, index=True)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id_proyecto"), nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos_db.id_equipo"), nullable=False)
    fecha_asignación = Column(Date, nullable=False)
    fecha_movimiento = Column(Date)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_registro = Column(TIMESTAMP, nullable=False)

    # Relaciones bidireccionales
    proyecto = relationship("Proyectos", back_populates="designaciones")
    equipo = relationship("Equipos", back_populates="designaciones")
    usuario = relationship("Usuarios", back_populates="designaciones")

# Modelo para la tabla Actividades
class Actividades(Base):
    __tablename__ = "actividades"

    id_actividad = Column(Integer, primary_key=True, index=True)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id_proyecto"), nullable=False)
    nombre_actividad = Column(String, nullable=False)
    descripción = Column(Text)

    proyecto = relationship("Proyectos")

# Modelo para la tabla Registro Diario
class RegistroDiario(Base):
    __tablename__ = "registro_diario"  # Cambiado el nombre a minúsculas

    id_registro = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id_proyecto"), nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipos_db.id_equipo"), nullable=False)
    nombre_equipo = Column(String, nullable=False)
    id_actividad = Column(Integer, ForeignKey("actividades.id_actividad"), nullable=False)
    horas_trabajadas = Column(Float, nullable=False)
    horómetro_inicial = Column(Float, nullable=False)
    horómetro_final = Column(Float, nullable=False)
    combustible = Column(Float)
    id_operador = Column(Integer, ForeignKey("operadores.id_operador"), nullable=False)
    name_operador = Column(String, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_registro = Column(TIMESTAMP, nullable=False)

    # Relaciones
    proyecto = relationship("Proyectos")
    equipo = relationship("Equipos")
    actividad = relationship("Actividades")
    operador = relationship("Operadores")
    usuario = relationship("Usuarios")

# Modelo para la tabla Operadores
class Operadores(Base):
    __tablename__ = "operadores"

    id_operador = Column(Integer, primary_key=True, index=True)
    name_operador = Column(String, nullable=False)

