import streamlit as st
from database.connection import SessionLocal
from database.models import RegistroDiario
from datetime import datetime
import pandas as pd

def visualizar_datos():
    st.title("Visualización de Datos")

    # Conectar con la base de datos
    db = SessionLocal()
    id_usuario = st.session_state["user_id"]

    # Filtro de período
    fecha_inicio = st.date_input("Fecha de Inicio", datetime.now())
    fecha_fin = st.date_input("Fecha de Fin", datetime.now())

    # Consulta de registros del usuario autenticado en el rango de fechas
    registros = db.query(RegistroDiario).filter(
        RegistroDiario.id_usuario == id_usuario,
        RegistroDiario.fecha >= fecha_inicio,
        RegistroDiario.fecha <= fecha_fin
    ).all()

    # Convertir a DataFrame para mostrar en tabla
    datos = [
        {
            "Fecha": registro.fecha,
            "Proyecto": registro.id_proyecto,
            "Equipo": registro.nombre_equipo,
            "Actividad": registro.id_actividad,
            "Horas Trabajadas": registro.horas_trabajadas,
            "Combustible": registro.combustible,
            "Operador": registro.name_operador
        }
        for registro in registros
    ]

    df = pd.DataFrame(datos)
    st.dataframe(df)

    db.close()
