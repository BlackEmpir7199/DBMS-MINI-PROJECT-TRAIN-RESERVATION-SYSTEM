import streamlit as st
from pages.database import database
import os
import pandas as pd

def display():
    # Page Title
    st.title("🚄 iTRS - Train Reservation System")

    # Centered Image
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        image_path = "assets\\"
        st.image(f"{image_path}Train-bro.png", use_column_width=True)

    # Display Available Trains
    st.subheader("🚂 Available Trains")
    trains = database.get_trains()
    if trains:
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

    # Admin Guide Section
    with st.expander("🔧 Admin Guide"):
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
            if connection is_connected():
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
    email = 'admin@example.com'
    password = 'securepassword'

    user = authenticate_user(table_name, email, password)
    if user:
        print("User authenticated successfully")
    else:
        print("Authentication failed")
    ''', language='python')

    # Train Management Explanation
    st.subheader("📊 Train Management")
    st.markdown("""
    Manage your trains efficiently through the following functionalities:

    - **Add Train**: You can add new train records by providing details such as train name, capacity, route, and status.
    - **Update Train Status**: Update the operational status of existing trains.
    - **View All Trains**: View all the trains currently available in the system.

    To manage trains, navigate to the Train Management section and select the desired action.
    """)

    # Station Management Explanation
    st.subheader("📍 Station Management")
    st.markdown("""
    Manage your stations seamlessly through the following functionalities:

    - **Add Station**: Add new station records by providing station name and location.
    - **Update Station**: Update details of existing stations.
    - **Delete Station**: Remove station records. Note that deleting a station will also delete all trains associated with that station.

    To manage stations, navigate to the Station Management section and select the desired action.
    """)

    # Security Considerations
    st.header("🔒 Security Considerations")
    st.markdown("""
    Ensure the security of your system by following these best practices:

    - **Parameterization**: Always use parameterized queries to prevent SQL injection.
    - **Sanitization**: Verify and sanitize user inputs, especially table names, to prevent SQL injection attacks.
    """)

    st.info("By following this guide, you should be able to authenticate users securely and effectively using the `authenticate_user` function, and manage trains and stations efficiently. If you encounter any issues, refer to the troubleshooting section or consult the MySQL and Python documentation for further assistance.")

