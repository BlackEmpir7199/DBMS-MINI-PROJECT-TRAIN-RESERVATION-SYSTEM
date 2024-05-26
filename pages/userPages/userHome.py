import streamlit as st
from pages.database import database
import os
import pandas as pd


def display():

    # Title with icon
    st.title("🚄 iTRS - Train Reservation System")

    # Centered image with columns
    col1, col2, col3 = st.columns([0.4, 0.45, 0.4])
    with col2:
        image_path = "assets\\"
        st.image(f"{image_path}Train-bro.png", use_column_width=True)

    # Fetch and display trains in a table
    trains = database.get_trains()
    if trains:
        st.subheader("🚂 Available Trains")
        df_trains = pd.DataFrame(trains)
        st.dataframe(df_trains.style.set_properties(**{'text-align': 'center'}))
    else:
        st.info("No trains available at the moment.")

    # Book Tickets Section
    st.subheader("🎟️ Book Tickets")
    st.markdown(
        "Book tickets for your journey by navigating to the **Book Tickets** page using the main menu in the sidebar.")
    st.markdown("---")

    # About Us Section
    st.header("📖 About Us")
    st.write("""
        Welcome to the Train Ticket Booking System. Our aim is to provide a seamless and user-friendly experience for booking train tickets. 
        With our platform, you can easily search for trains, view available tickets, and book your journey with just a few clicks.
        """)
    st.markdown("---")

    # Contact Us Section
    st.header("📞 Contact Us")
    st.write(
        "For inquiries, please email us at [support@trainbookingsystem.com](mailto:support@trainbookingsystem.com).")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>© 2024 iTRS - Train Reservation System. All rights reserved.</p>",
                unsafe_allow_html=True)


if __name__ == "__main__":
    display()
