import streamlit as st
import pandas as pd
from pages.database import database
from pages.userPages import userBookingForm

def display():
    st.title("Book Train Tickets")
    st.write(st.session_state.email)
    # Search filter
    st.subheader("Search Filter")
    col1, col2, col3 = st.columns(3)
    with col1:
        from_station = st.selectbox("From", options=userBookingForm.get_station_names(), index=0)

    with col2:
        to_station = st.selectbox("To", options=userBookingForm.get_station_names(), index=0)

    with col3:
        date_of_travel = st.date_input("Date of Travel")

    # Fetch trains based on search filter
    trains = database.search_trains(from_station, to_station, date_of_travel)

    # Display filtered trains in a table
    if trains:
        st.subheader("Available Trains")
        df_trains = pd.DataFrame(trains)
        st.dataframe(df_trains)

        # Book button for each train
        for index, row in df_trains.iterrows():
            userBookingForm.display_booking_form(row,date_of_travel)
    else:
        st.error("No trains available for the selected route and date.")


