import streamlit as st
import os
import pandas as pd
from pages.database import database

def display():


    st.title("⚙️ Admin Settings")

    # Header image
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = "assets\\"
        st.image(f"{image_path}Train-pana.png", use_column_width=True)

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🚂 Train Management", "🏢 Station Management", "👤 User Settings", "🔧 System Settings"])

    with tab1:
        st.subheader("Manage Trains")
        st.markdown("Add, update, or remove train records.")

        with st.expander("Add Train"):
            with st.form("Add Train Form"):
                train_name = st.text_input("Train Name")
                capacity = st.number_input("Capacity", min_value=1, max_value=1000, step=1)
                route = st.text_input("Route")
                status = st.selectbox("Status", ["Operational", "Under Maintenance"])
                submit = st.form_submit_button("Add Train")
                if submit:
                    st.success(f"Train {train_name} with capacity {capacity} added successfully!")

        with st.expander("Update Train Status"):
            train_id = st.number_input("Train ID to Update", min_value=1)
            new_status = st.selectbox("New Status", ["Operational", "Under Maintenance"])
            if st.button("Update Status"):
                st.success(f"Train ID {train_id} status updated to {new_status}!")

        with st.expander("View All Trains"):
            trains = database.get_trains()
            if trains:
                df_trains = pd.DataFrame(trains)
                st.dataframe(df_trains.style.set_properties(**{'text-align': 'center'}))
            else:
                st.info("No trains available at the moment.")

    with tab2:
        st.subheader("Manage Stations")
        st.markdown("Add, update, or remove station records.")

        with st.expander("Add Station"):
            with st.form("Add Station Form"):
                station_name = st.text_input("Station Name")
                location = st.text_input("Location")
                submit_station = st.form_submit_button("Add Station")
                if submit_station:
                    st.success(f"Station {station_name} at {location} added successfully!")

        with st.expander("View All Stations"):
            stations = database.get_stations()
            if stations:
                df_stations = pd.DataFrame(stations)
                st.dataframe(df_stations.style.set_properties(**{'text-align': 'center'}))
            else:
                st.info("No stations available at the moment.")

    with tab3:
        st.subheader("User Settings")
        st.markdown("Manage user accounts and roles.")

        with st.expander("Add User"):
            with st.form("Add User Form"):
                user_name = st.text_input("User Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["Admin", "User"])
                submit_user = st.form_submit_button("Add User")
                if submit_user:
                    st.success(f"User {user_name} added successfully with role {role}!")

        with st.expander("View All Users"):
            users = database.get_users()
            if users:
                df_users = pd.DataFrame(users)
                st.dataframe(df_users.style.set_properties(**{'text-align': 'center'}))
            else:
                st.info("No users available at the moment.")

    with tab4:
        st.subheader("System Settings")
        st.markdown("Configure system settings and preferences.")

        with st.container():
            st.markdown("### General Settings")
            theme = st.selectbox
