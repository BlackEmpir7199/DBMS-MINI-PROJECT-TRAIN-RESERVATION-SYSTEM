import streamlit as st
from streamlit_option_menu import option_menu
from pages.database import database


def display():
    st.title("🚉 Manage Stations")

    selected = option_menu("Manage Stations", ["View", "Add", "Update", "Delete"],
                           orientation='horizontal', icons=["eye", "plus-square", "arrow-clockwise", "trash"])

    stations = database.get_stations()  # Assuming get_stations returns a list of dicts

    if selected == "View":
        st.subheader("View Stations",divider='red')
        if stations:
            with st.container():
                st.dataframe(stations, width=1000)
        else:
            st.info("No stations available.")

    elif selected == "Add":
        st.subheader("Add Station",divider='red')
        if 'add_station' not in st.session_state:
            st.session_state.add_station = ""
        station_name = st.text_input("Station Name", key="add_station")
        if st.button("Add"):
            if any(station['name'] == station_name for station in stations):
                st.error("The station already exists.")
            else:
                database.add_station(station_name)  # Assuming add_station is a function in database module
                st.success(f"Station '{station_name}' added successfully!")
                st.experimental_rerun()

    elif selected == "Update":
        st.subheader("Update Station",divider='red')
        station_to_update = st.selectbox("Select Station to Update", [station['name'] for station in stations])
        new_station_name = st.text_input("New Station Name", key="update_station_name")
        if st.button("Update"):
            if any(station['name'] == new_station_name for station in stations):
                st.error("The new station name already exists.")
            else:
                database.update_station(station_to_update, new_station_name)  # Assuming update_station is a function in database module
                st.success(f"Station '{station_to_update}' updated to '{new_station_name}' successfully!")
                st.experimental_rerun()

    elif selected == "Delete":
        st.subheader("Delete Station",divider='red')
        station_to_delete = st.selectbox("Select Station to Delete", [station['name'] for station in stations])
        if st.button("Delete"):
                    try:
                        database.delete_trains_by_station(station_to_delete)  # Assuming delete_trains_by_station is a function in database module
                        database.delete_station(station_to_delete)  # Assuming delete_station is a function in database module
                        st.success(f"Station '{station_to_delete}' and all associated trains deleted successfully!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")


