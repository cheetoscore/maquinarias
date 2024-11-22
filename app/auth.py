import streamlit as st
from database.connection import SessionLocal
from database.models import Usuarios

def login():
    st.title("Inicio de Sesión")

    # Inputs de usuario y contraseña
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    # Botón de inicio de sesión
    if st.button("Iniciar Sesión"):
        # Conectar con la base de datos
        db = SessionLocal()
        # Buscar usuario en la base de datos
        user = db.query(Usuarios).filter_by(nombre_usuario=usuario, contraseña=contraseña).first()
        db.close()

        # Verificar credenciales
        if user:
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = user.id_usuario
            st.success("Inicio de sesión exitoso")
        else:
            st.error("Usuario o contraseña incorrectos")
