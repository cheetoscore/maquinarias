import streamlit as st
from sqlalchemy import func
from sqlalchemy.orm import aliased
from database.connection import SessionLocal
from database.models import Equipos, Proyectos, Designación
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import folium
from streamlit_folium import st_folium
import re


# Función para convertir coordenadas de formato DMS a decimales
def dms_to_decimal(dms):
    pattern = r"(\d+)°(\d+)'([\d.]+)\"?([NSEW])"
    matches = re.findall(pattern, dms)
    if not matches:
        return None, None
    coords = []
    for degrees, minutes, seconds, direction in matches:
        decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if direction in "SW":
            decimal = -decimal
        coords.append(decimal)
    return coords[0], coords[1]  # Retorna latitud y longitud


def registrar_movimientos():
    st.title("Registro de Movimientos de Equipos")

    # Conexión a la base de datos
    db = SessionLocal()

    # Subconsulta para obtener el último registro (considerando fecha_movimiento y fecha_asignación)
    latest_movements = (
        db.query(
            Designación.id_equipo,
            func.max(func.coalesce(Designación.fecha_movimiento, Designación.fecha_asignación)).label("ultima_fecha")
        )
        .group_by(Designación.id_equipo)
        .subquery()
    )

    # Consulta principal para obtener los detalles de los equipos, movimientos y proyectos
    equipos_alias = aliased(Equipos)
    movimientos = (
        db.query(
            equipos_alias.id_equipo,
            equipos_alias.nombre_equipo,
            equipos_alias.modelo,
            Proyectos.nombre_proyecto,
            Proyectos.ubicacion,
            latest_movements.c.ultima_fecha
        )
        .join(latest_movements, equipos_alias.id_equipo == latest_movements.c.id_equipo)
        .join(
            Designación,
            (Designación.id_equipo == latest_movements.c.id_equipo) &
            (func.coalesce(Designación.fecha_movimiento, Designación.fecha_asignación) == latest_movements.c.ultima_fecha)
        )
        .join(Proyectos, Proyectos.id_proyecto == Designación.id_proyecto)
        .all()
    )

    # Convertir los datos en un formato que Streamlit pueda mostrar como tabla
    data = [
        {
            "ID Equipo": movimiento.id_equipo,
            "Nombre Equipo": movimiento.nombre_equipo,
            "Modelo": movimiento.modelo,
            "Nombre Proyecto": movimiento.nombre_proyecto,
            "Ubicación": movimiento.ubicacion,
            "Fecha Movimiento": movimiento.ultima_fecha,
        }
        for movimiento in movimientos
    ]

    # Convertir las ubicaciones a coordenadas decimales
    for row in data:
        if row["Ubicación"]:
            lat, lon = dms_to_decimal(row["Ubicación"])
            row["Latitud"] = lat
            row["Longitud"] = lon

    # Mostrar tabla dinámica con Ag-Grid
    st.subheader("Posición Actual de los Equipos")
    if data:
        # Convertir los datos a un DataFrame
        df = pd.DataFrame(data)

        # Configuración de Ag-Grid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Paginación
        gb.configure_side_bar()  # Barra lateral con filtros avanzados
        gb.configure_default_column(
            filter=True,
            sortable=True,
            resizable=True,
            filter_params={'newRowsAction': 'keep'},
        )
        gb.configure_selection("single")  # Selección de una fila

        # Ajustar opciones de la grilla
        gb.configure_grid_options(domLayout='normal')

        grid_options = gb.build()

        # Renderizar Ag-Grid con altura ajustada
        AgGrid(
            df,
            gridOptions=grid_options,
            enable_enterprise_modules=False,
            theme="streamlit",
            update_mode="MODEL_CHANGED",
            allow_unsafe_jscode=True,
            height=500,
            fit_columns_on_grid_load=True,
        )

        # Crear un diccionario para agrupar equipos por proyecto/ubicación
        proyectos_equipos = {}
        for _, row in df.iterrows():
            key = (row["Nombre Proyecto"], row["Ubicación"], row["Latitud"], row["Longitud"])
            if key not in proyectos_equipos:
                proyectos_equipos[key] = []
            proyectos_equipos[key].append(row["Nombre Equipo"])

        # Mostrar mapa interactivo con ubicaciones
        st.subheader("Mapa de Ubicaciones de Proyectos")
        m = folium.Map(location=[-12.0464, -77.0428], zoom_start=6)  # Ubicación inicial: Perú
        for (proyecto, ubicacion, lat, lon), equipos in proyectos_equipos.items():
            if pd.notnull(lat) and pd.notnull(lon):
                popup_content = f"<strong>{proyecto}</strong><br><br>Equipos:<ul>"
                popup_content += "".join([f"<li>{equipo}</li>" for equipo in equipos])
                popup_content += "</ul>"

                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=proyecto,
                ).add_to(m)

        # Mostrar el mapa en Streamlit
        st_folium(
             m,
             width=1000,  # Ancho del mapa (ajustar al ancho de la pantalla)
             height=700,  # Altura del mapa
        )

    else:
        st.warning("No hay movimientos registrados.")

    db.close()


    st.markdown("---")  # Línea divisoria

    # Formulario para registrar una nueva designación
    st.subheader("Formulario de Designación de Equipos")

    # Selección de proyecto
    proyectos = db.query(Proyectos).all()
    if not proyectos:
        st.error("No hay proyectos registrados.")
        db.close()
        return

    proyecto_seleccionado = st.selectbox("Seleccionar Proyecto", [p.nombre_proyecto for p in proyectos], key="proyecto")

    # Selección de equipo
    equipos = db.query(Equipos).all()
    if not equipos:
        st.error("No hay equipos registrados.")
        db.close()
        return

    equipo_seleccionado = st.selectbox("Seleccionar Equipo", [e.nombre_equipo for e in equipos], key="equipo")

    # Fecha de asignación
    fecha_asignacion = st.date_input("Fecha de Asignación", key="fecha_asignacion")

    # Botón para registrar la designación
    if st.button("Registrar Designación", key="registrar_designacion"):
        proyecto = next((p for p in proyectos if p.nombre_proyecto == proyecto_seleccionado), None)
        equipo = next((e for e in equipos if e.nombre_equipo == equipo_seleccionado), None)

        if proyecto and equipo:
            nueva_designacion = Designación(
                id_proyecto=proyecto.id_proyecto,
                id_equipo=equipo.id_equipo,
                fecha_asignación=fecha_asignacion,
                id_usuario=st.session_state.get("user_id", 1)  # Cambia esto por la lógica de sesión
            )
            db.add(nueva_designacion)
            db.commit()
            st.success(f"Equipo '{equipo_seleccionado}' asignado al proyecto '{proyecto_seleccionado}'.")
        else:
            st.error("Error al registrar la designación. Verifique los datos seleccionados.")

    # Cerrar la conexión a la base de datos
    db.close()
