import streamlit as st
# Streamlit UI
def display():
    st.title("Admin Guide for User Authentication and System Setup")

    st.header("Overview")
    st.markdown("""
    The `authenticate_user` function is designed to authenticate users by verifying their email and password against the records in the specified table. This guide provides instructions on how to set up, use, and troubleshoot the function, as well as how to set up and manage trains, stations, and other settings in the system.
    """)

    st.header("Setup Instructions")
    st.subheader("1. Install Required Python Libraries")
    st.code("pip install mysql-connector-python streamlit", language="bash")

    st.subheader("2. Database Configuration")
    st.markdown("""
    Ensure your MySQL database is set up correctly. Follow these steps to create the necessary tables:

    1. **Open MySQL Workbench**: Download and install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
    2. **Connect to MySQL Server**: Open MySQL Workbench and connect to your MySQL server.
    3. **Create Database**: Create a new database if it doesn't exist:
    """)
    st.code("CREATE DATABASE your_database;", language="sql")
    st.markdown("""
    4. **Create Tables**: Create the required tables (e.g., `admins`, `users`, `trains`, `stations`) with appropriate columns. Here is an example:
    """)
    st.code('''
    USE your_database;

    CREATE TABLE admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE trains (
        id INT AUTO_INCREMENT PRIMARY KEY,
        train_name VARCHAR(255) NOT NULL,
        capacity INT NOT NULL
    );

    CREATE TABLE stations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        station_name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL
    );
    ''', language='sql')

    st.header("Function Definition")
    st.markdown("Here is the `authenticate_user` function with table name sanitization:")

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
        # Allowed tables list
        allowed_tables = ['admins', 'users']  # Add all allowed table names here

        if table not in allowed_tables:
            st.error("Invalid table name")
            return None

        connection = create_connection()
        if connection is None:
            st.error("Failed to create connection to the database")
            return None

        cursor = connection.cursor()
        try:
            # Properly include the table name in the query
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

    st.header("Usage Instructions")
    st.subheader("1. Define User Credentials and Table")
    st.markdown(
        "Specify the table, user email, and password you want to authenticate. Ensure the table name is in the allowed tables list.")
    st.code('''
    table_name = 'admins'
    email = 'rakhul@gmail.com'
    password = 'rakhul2005'
    ''', language='python')

    st.subheader("2. Call the Function")
    st.markdown("Call the `authenticate_user` function with the specified parameters:")
    st.code('''
    user = authenticate_user(table_name, email, password)
    if user:
        print("User authenticated successfully")
    else:
        print("Authentication failed")
    ''', language='python')

    st.header("Example Script")
    st.markdown("Here is a full example script to authenticate a user:")
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
            print(f"The error '{e}' occurred")
            return None

    def authenticate_user(table, usermail, password):
        # Allowed tables list
        allowed_tables = ['admins', 'users']  # Add all allowed table names here

        if table not in allowed_tables:
            raise ValueError("Invalid table name")

        connection = create_connection()
        if connection is None:
            raise ConnectionError("Failed to create connection to the database")

        cursor = connection.cursor()
        try:
            # Properly include the table name in the query
            query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
            cursor.execute(query, (usermail, password))
            user = cursor.fetchone()
            print(user)
            return user
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            connection.close()

    # Example usage
    table_name = 'admins'
    email = 'rakhul@gmail.com'
    password = 'rakhul2005'

    user = authenticate_user(table_name, email, password)
    if user:
        print("User authenticated successfully")
    else:
        print("Authentication failed")
    ''', language='python')

    st.header("Managing Trains, Stations, and Settings")
    st.markdown(
        "You can manage trains, stations, and other settings using similar functions. Here is an example of how you can add a train:")
    st.code('''
    def add_train(train_name, capacity):
        connection = create_connection()
        if connection is None:
            st.error("Failed to create connection to the database")
            return None

        cursor = connection.cursor()
        try:
            query = "INSERT INTO trains (train_name, capacity) VALUES (%s, %s)"
            cursor.execute(query, (train_name, capacity))
            connection.commit()
            st.success("Train added successfully")
        except Error as e:
            st.error(f"The error '{e}' occurred")
        finally:
            cursor.close()
            connection.close()

    # Example usage
    add_train("Express", 200)
    ''', language='python')

    st.header("Troubleshooting")
    st.markdown("""
    - **Connection Issues**: Ensure your database connection parameters (host, database, user, password) are correct.
    - **Invalid Table Name**: Ensure the table name is in the allowed tables list.
    - **SQL Errors**: Check the console output for any SQL errors and ensure your table structure matches the expected format.
    """)

    st.header("Security Considerations")
    st.markdown("""
    - **Parameterization**: Always use parameterized queries to prevent SQL injection.
    - **Sanitization**: Verify and sanitize user inputs, especially table names, to prevent SQL injection attacks.
    """)

    st.info(
        "By following this guide, you should be able to authenticate users securely and effectively using the `authenticate_user` function, and manage trains and stations. If you encounter any issues, refer to the troubleshooting section or consult the MySQL and Python documentation for further assistance.")

