import streamlit as st
import database

def display():
    st.title("View Tickets")
    st.write(st.session_state.email)
    tickets = database.get_tickets(st.session_state.email)
    if tickets:
        for ticket in tickets:
            st.write(f"Booking ID: {ticket['booking_id']}, Train ID: {ticket['train_id']}, Date: {ticket['date_of_travel']}, Name: {ticket['name']}")
    else:
        st.write("No tickets found.")
