import streamlit as st
from app.auth import login
from app.registro_movimientos import registrar_movimientos
from app.registro_actividades import registrar_actividades
from app.visualizacion_datos import visualizar_datos

# Configuración de la página
st.set_page_config(page_title="Gestión de Equipos de Línea Amarilla", layout="wide")

# Verificar si el usuario está autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Menú de navegación
menu = st.sidebar.selectbox(
    "Menú Principal",
    ["Inicio de Sesión", "Registro de Movimientos de Equipos", "Registro de Actividades de Equipos", "Visualización de Datos"]
)

# Lógica de navegación basada en el menú seleccionado
if menu == "Inicio de Sesión":
    login()
elif st.session_state["authenticated"]:
    if menu == "Registro de Movimientos de Equipos":
        registrar_movimientos()
    elif menu == "Registro de Actividades de Equipos":
        registrar_actividades()
    elif menu == "Visualización de Datos":
        visualizar_datos()
else:
    st.warning("Por favor, inicie sesión primero para acceder a las funciones.")
