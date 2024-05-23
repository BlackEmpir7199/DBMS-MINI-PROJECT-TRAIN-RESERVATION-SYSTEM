import streamlit as st
from pages.database import database
import os
import pandas as pd

def display():
    # Page Title
    st.title("🚄 iTRS - Train Reservation System")

    # Columns for layout
    col1, col2, col3 = st.columns([0.4, 0.45, 0.4])

    with col2:
        # Display image
        image_path = "assets\\"
        st.image(f"{image_path}Train-bro.png", use_column_width=True)

    # Fetch and display trains
    trains = database.get_trains()
    if trains:
        st.subheader("🚂 Available Trains")
        df_trains = pd.DataFrame(trains)
        st.dataframe(df_trains.style.highlight_max(axis=0))
    else:
        st.info("No trains available at the moment.")

    # Help Guide Section
    st.subheader("📚 Help Guide For Administration")
    st.markdown("Navigate to **Guide** in the main menu to get a fully administered guide for help.")
    st.markdown("### Quick Tips")
    st.markdown("""
    - **Setup Instructions**: Follow the steps to set up your database and environment.
    - **Managing Trains**: Add, update, or delete train records.
    - **User Authentication**: Securely authenticate users.
    """)

    # Interactive Button
    if st.button("View Admin Guide"):
        st.markdown("## Admin Guide")
        st.markdown("""
        The `authenticate_user` function is designed to authenticate users by verifying their email and password against the records in the specified table. 
        This guide provides instructions on how to set up, use, and troubleshoot the function.
        """)

        st.markdown("### Function Definition")
        st.code('''
        import mysql.connector
        from mysql.connector import Error

        def create_connection():
            try:
                connection = mysql.connector.connect(
                    host='your_host',
                    database='your_database',
                    user='your_user',
                    password='your_password'
                )
                if connection.is_connected():
                    return connection
            except Error as e:
                st.error(f"The error '{e}' occurred")
                return None

        def authenticate_user(table, usermail, password):
            allowed_tables = ['admins', 'users']
            if table not in allowed_tables:
                st.error("Invalid table name")
                return None

            connection = create_connection()
            if connection is None:
                st.error("Failed to create connection to the database")
                return None

            cursor = connection.cursor()
            try:
                query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
                cursor.execute(query, (usermail, password))
                user = cursor.fetchone()
                return user
            except Error as e:
                st.error(f"The error '{e}' occurred")
            finally:
                cursor.close()
                connection.close()
        ''', language='python')

        st.markdown("### Example Usage")
        st.code('''
        table_name = 'admins'
        email = 'rakhul@gmail.com'
        password = 'rakhul2005'

        user = authenticate_user(table_name, email, password)
        if user:
            print("User authenticated successfully")
        else:
            print("Authentication failed")
        ''', language='python')

    st.subheader("📊 Train Management")
    st.markdown("Manage your trains, stations, and settings seamlessly with our user-friendly interface.")

    # Example train management section
    if st.button("Add Train"):
        with st.form("Add Train Form"):
            train_name = st.text_input("Train Name")
            capacity = st.number_input("Capacity", min_value=1, max_value=1000, step=1)
            route = st.text_input("Route")
            status = st.selectbox("Status", ["Operational", "Under Maintenance"])
            submit = st.form_submit_button("Add Train")
            if submit:
                st.success(f"Train {train_name} with capacity {capacity} added successfully!")

    if st.button("Update Train Status"):
        train_id = st.number_input("Train ID to Update", min_value=1)
        new_status = st.selectbox("New Status", ["Operational", "Under Maintenance"])
        if st.button("Update Status"):
            st.success(f"Train ID {train_id} status updated to {new_status}!")

    st.subheader("📍 Station Management")
    if st.button("Add Station"):
        with st.form("Add Station Form"):
            station_name = st.text_input("Station Name")
            location = st.text_input("Location")
            submit_station = st.form_submit_button("Add Station")
            if submit_station:
                st.success(f"Station {station_name} at {location} added successfully!")

    st.header("🔒 Security Considerations")
    st.markdown("""
    - **Parameterization**: Always use parameterized queries to prevent SQL injection.
    - **Sanitization**: Verify and sanitize user inputs, especially table names, to prevent SQL injection attacks.
    """)

    st.info("By following this guide, you should be able to authenticate users securely and effectively using the `authenticate_user` function, and manage trains and stations efficiently. If you encounter any issues, refer to the troubleshooting section or consult the MySQL and Python documentation for further assistance.")

if __name__ == "__main__":
    display()
