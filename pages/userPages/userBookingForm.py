import streamlit as st
from pages.database import database
def display_booking_form(train,date_of_travel):
    st.title("Enter Passenger Details")

    st.write("You selected the following train:")
    st.subheader(
        f"Train ID: {train['train_id']}, Train Name: {train['name']}, Departure: {train['departure_time']}, Arrival: {train['arrival_time']}")

    st.header("Passenger Details")

    # Initialize with 6 passenger fields
    passenger_fields = [
        {'name': '', 'age': '', 'sex': ''}
        for _ in range(6)
    ]

    for i, passenger in enumerate(passenger_fields):
        st.markdown(f"**Passenger {i + 1}**")
        col1, col2, col3 = st.columns(3)  # Create 3 columns for layout
        with col1:
            name = st.text_input("Name", key=f"name_{i}", value=passenger['name'])
        with col2:
            age = st.text_input("Age", key=f"age_{i}", value=passenger['age'])
        with col3:
            sex = st.selectbox("Sex", ["Male", "Female", "Other"], key=f"sex_{i}",
                               index=0 if passenger['sex'] == 'Male' else 1 if passenger['sex'] == 'Female' else 2)

            # Update passenger_fields list
            passenger_fields[i] = {'name': name, 'age': age, 'sex': sex}

    # Filter out empty fields
    passenger_fields = [passenger for passenger in passenger_fields if all(passenger.values())]
    if st.button("Submit"):
        if passenger_fields:
            # Book tickets using the database function
            booking_id = book_tickets(train['train_id'], st.session_state['email'], date_of_travel, passenger_fields)
            if booking_id:
                st.success(f"Tickets booked successfully! Your booking ID is {booking_id}.")
        else:
            st.error("Please fill in at least one passenger's details.")


def get_station_names():
    stations = database.get_stations()
    return [station['name'] for station in stations]


def book_tickets(train_id, user_mail, date_of_travel, passengers):
    # Assuming this function is implemented in the database module to book tickets
    booking_id = database.book_ticket(train_id, user_mail, date_of_travel)
    for passenger in passengers:
        database.add_passenger(booking_id, passenger['name'], passenger['age'], passenger['sex'])
    return booking_id