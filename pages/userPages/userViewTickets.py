import streamlit as st
from pages.database import database

def display():
    st.title("🎟️ View and Manage Your Tickets")
    st.markdown("## Welcome to your ticket dashboard!")
    st.caption(f"**Logged in as:** {st.session_state.email}")

    search_query = st.text_input("🔍 Search Tickets", help="Search by Booking ID or Train ID",
                                 placeholder="Enter Booking ID or Train ID")

    tickets = database.get_tickets(st.session_state.email)

    if search_query:
        tickets = [ticket for ticket in tickets if
                   search_query.lower() in str(ticket['booking_id']).lower() or search_query.lower() in str(
                       ticket['train_id']).lower()]

    if tickets:
        st.markdown(f"### Found {len(tickets)} ticket(s):")
        for ticket in tickets:
            with st.expander(f"📄 **Booking ID:** {ticket['booking_id']}", expanded=True):
                st.write(f"**Train ID:** {ticket['train_id']}")
                st.write(f"**Date of Travel:** {ticket['date_of_travel']}")
                st.write(f"**Name:** {ticket['name']}")
                st.write(f"**Email:** {st.session_state.email}")

                passengers = database.get_passengers_by_booking_id(ticket['booking_id'])

                if passengers:
                    st.markdown("#### Passengers:")
                    for passenger in passengers:
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        col1.write(f"**Name:** {passenger['name']}")
                        col2.write(f"**Age:** {passenger['age']}")
                        col3.write(f"**Sex:** {passenger['sex']}")
                        with col4:
                            if st.button("❌ Delete Passenger", key=f"delete_passenger_{passenger['passenger_id']}"):
                                database.delete_passenger(passenger['passenger_id'])
                                st.success(f"Passenger {passenger['name']} deleted.")
                                st.rerun()  # Refresh the page to show updated passengers

                if st.button("🗑️ Delete Booking", key=f"delete_booking_{ticket['booking_id']}"):
                    database.delete_ticket(ticket['booking_id'])
                    st.success(f"Booking ID {ticket['booking_id']} deleted.")
                    st.rerun()  # Refresh the page to show updated tickets
    else:
        st.warning("No tickets found. Please check your search query or book a new ticket.")
