import streamlit as st
import database
from datetime import datetime

def display():
    st.title("Book a Train Ticket")

    # Search and filter options
    st.sidebar.title("Search and Filter")
    from_station_names = [station['name'] for station in database.get_stations()]
    from_station = st.sidebar.selectbox("From Station", from_station_names, index=0)

    to_station_names = [station['name'] for station in database.get_stations()]
    to_station = st.sidebar.selectbox("To Station", to_station_names, index=1)

    date_of_travel = st.sidebar.date_input("Date of Travel", min_value=datetime.today())

    # Display available trains based on search and filter options
    trains = database.search_trains(from_station, to_station, date_of_travel)
    if trains:
        st.subheader("Available Trains")
        for train in trains:
            st.write(
                f"Train ID: {train['train_id']}, From: {from_station}, To: {to_station}, Departure Time: {train['departure_time']}, Arrival Time: {train['arrival_time']}")

        # Select train for booking
        selected_train = st.selectbox("Select Train", [train['train_id'] for train in trains])

        # Store selected train and date of travel in session state
        st.session_state.selected_train = selected_train
        st.session_state.date_of_travel = date_of_travel

        # Booking form
        st.subheader("Book Ticket")
        with st.form("booking_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            submit_button = st.form_submit_button(label='Book Ticket')

            if submit_button:
                if not name or not email:
                    st.error("Name and email are required.")
                else:
                    user = database.get_user_by_email(email)
                    if not user:
                        user_id = database.create_user(name, email)
                    else:
                        user_id = user['user_id']

                    booking_id = database.book_ticket(user_id, selected_train, date_of_travel)
                    if booking_id:
                        st.success(f"Ticket booked successfully! Your booking ID is {booking_id}.")
                    else:
                        st.error("Failed to book ticket. Please try again.")
    else:
        st.error("No trains available for the selected route and date.")

if __name__ == "__main__":
    display()
