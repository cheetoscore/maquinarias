import streamlit as st
from database.connection import SessionLocal
from database.models import RegistroDiario, Proyectos, Equipos, Actividades, Operadores, Designación
from datetime import datetime

def registrar_actividades():
    st.title("Registro de Actividades de Equipos")

    # Conectar con la base de datos
    db = SessionLocal()

    # Selección de proyecto
    proyectos = db.query(Proyectos).all()
    proyecto_seleccionado = st.selectbox("Seleccionar Proyecto", [p.nombre_proyecto for p in proyectos])
    proyecto = next((p for p in proyectos if p.nombre_proyecto == proyecto_seleccionado), None)

    if not proyecto:
        st.error("No se encontró el proyecto seleccionado.")
        return

    # Consultar equipos asignados al proyecto a través de Designación
    designaciones = db.query(Designación).filter_by(id_proyecto=proyecto.id_proyecto).all()
    equipos_asignados = [d.id_equipo for d in designaciones]

    # Obtener los detalles de los equipos asignados
    equipos = db.query(Equipos).filter(Equipos.id_equipo.in_(equipos_asignados)).all()

    if not equipos:
        st.error("No hay equipos asignados a este proyecto.")
        return

    equipo_seleccionado = st.selectbox("Seleccionar Equipo", [e.nombre_equipo for e in equipos])

    # Manejo de error si el equipo no se encuentra
    equipo = next((e for e in equipos if e.nombre_equipo == equipo_seleccionado), None)
    if not equipo:
        st.error("No se encontró el equipo seleccionado.")
        return

    # Selección de actividad específica del proyecto
    actividades = db.query(Actividades).filter_by(id_proyecto=proyecto.id_proyecto).all()
    if not actividades:
        st.error("No hay actividades registradas para este proyecto.")
        return

    actividad_seleccionada = st.selectbox("Seleccionar Actividad", [a.nombre_actividad for a in actividades])

    # Datos adicionales
    horas_trabajadas = st.number_input("Horas Trabajadas", min_value=0.0)
    combustible = st.number_input("Combustible Asignado (L)", min_value=0.0)
    horómetro_inicial = st.number_input("Horómetro Inicial", min_value=0.0)
    horómetro_final = st.number_input("Horómetro Final", min_value=0.0)
    operador_seleccionado = st.selectbox("Seleccionar Operador", [o.name_operador for o in db.query(Operadores).all()])

    # Botón para registrar actividad
    if st.button("Registrar Actividad"):
        id_usuario = st.session_state["user_id"]
        actividad = next((a for a in actividades if a.nombre_actividad == actividad_seleccionada), None)
        operador = db.query(Operadores).filter_by(name_operador=operador_seleccionado).first()

        nuevo_registro = RegistroDiario(
            fecha=datetime.today().date(),
            id_proyecto=proyecto.id_proyecto,
            id_equipo=equipo.id_equipo,
            nombre_equipo=equipo.nombre_equipo,
            id_actividad=actividad.id_actividad,
            horas_trabajadas=horas_trabajadas,
            horómetro_inicial=horómetro_inicial,
            horómetro_final=horómetro_final,
            combustible=combustible,
            id_operador=operador.id_operador,
            name_operador=operador.name_operador,
            id_usuario=id_usuario
        )
        
        db.add(nuevo_registro)
        db.commit()
        st.success("Actividad registrada exitosamente")

    db.close()
