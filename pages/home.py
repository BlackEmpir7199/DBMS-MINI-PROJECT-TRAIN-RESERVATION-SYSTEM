import streamlit as st
from PIL import Image
import database
import os
def display():
    st.title("Train Ticket Booking System")
    # Get the absolute path to the image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, '..', 'assets', 'train1.jpg')

    # Load and display the image
    st.image(image_path, use_column_width=True)

    st.header("Search for Trains")

    stations = database.get_stations()
    station_names = [station['name'] for station in stations]

    from_station = st.selectbox("From", station_names)
    to_station = st.selectbox("To", station_names)
    date_of_travel = st.date_input("Date of Travel")

    if st.button("Search Trains"):
        trains = database.search_trains(from_station, to_station, date_of_travel)
        if trains:
            st.write("Available Trains:")
            for train in trains:
                st.write(
                    f"Train ID: {train['train_id']}, Train Name: {train['name']}, Departure: {train['departure_time']}, Arrival: {train['arrival_time']}")
                if st.button(f"Book Train {train['train_id']}", key=train['train_id']):
                    st.session_state['selected_train'] = train['train_id']
                    st.session_state['date_of_travel'] = date_of_travel
                    st.experimental_rerun()

        else:
            st.write("No trains available for the selected route and date.")

    st.header("About Us")
    st.write("""
    Welcome to the Train Ticket Booking System. Our aim is to provide a seamless and user-friendly experience for booking train tickets. 
    With our platform, you can easily search for trains, view available tickets, and book your journey with just a few clicks.
    """)

    st.header("Contact Us")
    st.write("For inquiries, please email us at support@trainbookingsystem.com.")
