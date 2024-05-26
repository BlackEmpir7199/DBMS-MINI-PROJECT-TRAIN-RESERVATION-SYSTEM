import streamlit as st
from streamlit_option_menu import option_menu
from pages.database import database
from datetime import datetime, time

def display():
    st.title("🚆 Manage Trains")

    selected = option_menu("Manage Trains", ["View", "Add", "Update", "Delete"],
                           orientation='horizontal', icons=["eye", "plus-square", "arrow-clockwise", "trash"])

    trains = database.get_trains()  # Assuming get_trains returns a list of dicts
    stations = database.get_stations()  # Get stations for dropdowns

    if selected == "View":
        st.subheader("View Trains",divider='red')
        if trains:
            with st.container():
                st.dataframe(trains, width=1000)
        else:
            st.info("No trains available.")

    elif selected == "Add":
        st.subheader("Add Train",divider='red')
        if 'add_train_name' not in st.session_state:
            st.session_state.add_train_name = ""
        train_name = st.text_input("Train Name", key="add_train_name")
        from_station = st.selectbox("From Station", [station['name'] for station in stations], key="add_from_station")
        to_station = st.selectbox("To Station", [station['name'] for station in stations], key="add_to_station")
        departure_time = st.time_input("Departure Time", key="add_departure_time")
        arrival_time = st.time_input("Arrival Time", key="add_arrival_time")
        total_seats = st.number_input("Total Seats", min_value=1, key="add_total_seats")
        available_seats = st.number_input("Available Seats", min_value=0, max_value=total_seats, key="add_available_seats")
        if st.button("Add"):
            from_station_id = next(station['station_id'] for station in stations if station['name'] == from_station)
            to_station_id = next(station['station_id'] for station in stations if station['name'] == to_station)
            database.add_train(train_name, from_station_id, to_station_id, departure_time, arrival_time, total_seats, available_seats)
            st.success(f"Train '{train_name}' added successfully!")
            st.session_state.add_train_name = ""
            st.session_state.add_departure_time = time(0, 0)
            st.session_state.add_arrival_time = time(0, 0)
            st.session_state.add_total_seats = 1
            st.session_state.add_available_seats = 0


    elif selected == "Update":
        st.subheader("Update Train",divider='red')
        train_to_update = st.selectbox("Select Train to Update", [train['name'] for train in trains])
        train = next(train for train in trains if train['name'] == train_to_update)

        def convert_to_time(delta):
            return (datetime.min + delta).time()

        departure_time = convert_to_time(train['departure_time'])
        arrival_time = convert_to_time(train['arrival_time'])

        new_train_name = st.text_input("New Train Name", value=train['name'], key="update_train_name")
        new_from_station = st.selectbox("New From Station", [station['name'] for station in stations], index=[station['name'] for station in stations].index(train['from_station']), key="update_from_station")
        new_to_station = st.selectbox("New To Station", [station['name'] for station in stations], index=[station['name'] for station in stations].index(train['to_station']), key="update_to_station")
        new_departure_time = st.time_input("New Departure Time", value=departure_time, key="update_departure_time")
        new_arrival_time = st.time_input("New Arrival Time", value=arrival_time, key="update_arrival_time")
        new_total_seats = st.number_input("New Total Seats", min_value=1, value=train['total_seats'], key="update_total_seats")
        new_available_seats = st.number_input("New Available Seats", min_value=0, max_value=new_total_seats, value=train['available_seats'], key="update_available_seats")
        if st.button("Update"):
            new_from_station_id = next(station['station_id'] for station in stations if station['name'] == new_from_station)
            new_to_station_id = next(station['station_id'] for station in stations if station['name'] == new_to_station)
            database.update_train(train['train_id'], new_train_name, new_from_station_id, new_to_station_id, new_departure_time, new_arrival_time, new_total_seats, new_available_seats)
            st.success(f"Train '{train_to_update}' updated successfully!")


    elif selected == "Delete":
        st.subheader("Delete Train",divider='red')
        train_to_delete = st.selectbox("Select Train to Delete", [train['name'] for train in trains])
        if st.button("Delete"):
            try:
                with st.experimental_dialog("Delete station"):
                    database.delete_train(train_to_delete)
                    st.success(f"Train '{train_to_delete}' deleted successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")

