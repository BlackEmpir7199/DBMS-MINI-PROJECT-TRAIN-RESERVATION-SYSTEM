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
    st.code("pip install requirements.txt", language="bash")

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
    
CREATE TABLE `stations` (
  `station_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`station_id`)
);

CREATE TABLE `users` (
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE `admins` (
  `email` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `username` (`name`)
);

CREATE TABLE `trains` (
  `train_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `from_station` int DEFAULT NULL,
  `to_station` int DEFAULT NULL,
  `departure_time` time NOT NULL,
  `arrival_time` time NOT NULL,
  `total_seats` int NOT NULL,
  `available_seats` int NOT NULL,
  PRIMARY KEY (`train_id`),
  KEY `from_station` (`from_station`),
  KEY `to_station` (`to_station`),
  CONSTRAINT `trains_ibfk_1` FOREIGN KEY (`from_station`) REFERENCES `stations` (`station_id`),
  CONSTRAINT `trains_ibfk_2` FOREIGN KEY (`to_station`) REFERENCES `stations` (`station_id`)
);

CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int DEFAULT NULL,
  `date_of_travel` date NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `train_id` (`train_id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`)
);

CREATE TABLE `passengers` (
  `passenger_id` int NOT NULL AUTO_INCREMENT,
  `booking_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`passenger_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `passengers_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`)
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
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
        cursor.execute(query, (usermail, password))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def register_user(username, usermail, password):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO users (name ,email , password) VALUES (%s ,%s, %s)"
        cursor.execute(query, (username, usermail, password))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()

def register_admin(username, usermail, password):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO admins (name ,email , password) VALUES (%s ,%s, %s)"
        cursor.execute(query, (username, usermail, password))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
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
    def book_ticket(train_id, email, date_of_travel):
    query = "INSERT INTO bookings (train_id, email, date_of_travel) VALUES (%s, %s, %s)"
    params = (train_id, email, date_of_travel)
    booking_id = execute_query(query, params)
    return booking_id


def add_passenger(booking_id, name, age, sex):
    query = "INSERT INTO passengers (booking_id, name, age, sex) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (booking_id, name, age, sex))


def get_tickets(email):
    query = """
    SELECT b.booking_id, b.train_id, b.date_of_travel, u.name
    FROM bookings b
    JOIN users u ON b.email = u.email
    WHERE u.email = %s
    """
    params = (email,)
    tickets = execute_read_query(query, params)
    return tickets


def delete_ticket(booking_id):
    # First, delete all passengers associated with the booking
    delete_passengers_by_booking_id(booking_id)

    # Then, delete the booking from the 'bookings' table
    query = "DELETE FROM bookings WHERE booking_id = %s"
    execute_query(query, (booking_id,))


def delete_passengers_by_booking_id(booking_id):
    query = "DELETE FROM passengers WHERE booking_id = %s"
    execute_query(query, (booking_id,))


def get_passengers_by_booking_id(booking_id):
    query = "SELECT * FROM passengers WHERE booking_id = %s"
    return execute_read_query(query, (booking_id,))


def delete_passenger(passenger_id):
    query = "DELETE FROM passengers WHERE passenger_id = %s"
    execute_query(query, (passenger_id,))


def get_trains():
    query = """
    SELECT t.train_id, t.name, s1.name AS from_station, s2.name AS to_station, t.departure_time, t.arrival_time, t.total_seats, t.available_seats
    FROM trains t
    JOIN stations s1 ON t.from_station = s1.station_id
    JOIN stations s2 ON t.to_station = s2.station_id
    """
    return execute_read_query(query)


def add_train(name, from_station, to_station, departure_time, arrival_time, total_seats, available_seats):
    query = """
    INSERT INTO trains (name, from_station, to_station, departure_time, arrival_time, total_seats, available_seats)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (name, from_station, to_station, departure_time, arrival_time, total_seats, available_seats))


def update_train(train_id, name, from_station, to_station, departure_time, arrival_time, total_seats, available_seats):
    query = """
    UPDATE trains
    SET name = %s, from_station = %s, to_station = %s, departure_time = %s, arrival_time = %s, total_seats = %s, available_seats = %s
    WHERE train_id = %s
    """
    return execute_query(query, (name, from_station, to_station, departure_time, arrival_time, total_seats, available_seats, train_id))

def get_trains():
    query = "SELECT * FROM trains"
    trains = execute_read_query(query)
    return trains

def get_stations():
    query = "SELECT * FROM stations"
    return execute_read_query(query)


def add_station(station_name):
    query = "INSERT INTO stations (name) VALUES (%s)"
    return execute_query(query, (station_name,))


def update_station(old_name, new_name):
    query = "UPDATE stations SET name = %s WHERE name = %s"
    return execute_query(query, (new_name, old_name))


def delete_station(station_name):
    query = "DELETE FROM stations WHERE name = %s"
    return execute_query(query, (station_name,))


def get_trains_by_station(station_name):
    query = """
    SELECT t.* 
    FROM trains t
    JOIN stations s ON t.from_station = s.station_id OR t.to_station = s.station_id
    WHERE s.name = %s
    """
    return execute_read_query(query, (station_name,))


def update_train_station(train_id, new_station_name):
    new_station_id_query = "SELECT station_id FROM stations WHERE name = %s"
    new_station_id = execute_read_query(new_station_id_query, (new_station_name,))[0]['station_id']
    query = "UPDATE trains SET from_station = %s WHERE train_id = %s"
    return execute_query(query, (new_station_id, train_id))


def search_trains(from_station, to_station, date_of_travel):
    query = """
    SELECT * FROM trains 
    WHERE from_station IN (SELECT station_id FROM stations WHERE name = %s) 
    AND to_station IN (SELECT station_id FROM stations WHERE name = %s)
    """
    params = (from_station, to_station)
    trains = execute_read_query(query, params)
    return trains

def delete_train(train_name):
    query = "DELETE FROM trains WHERE name = %s"
    return execute_query(query, (train_name,))


def delete_trains_by_station(station_name):
    query = """
    DELETE FROM trains 
    WHERE from_station = (SELECT station_if from stations where name=%s)
    OR to_station = (SELECT station_id from stations where name=%s)
    """
    execute_query(query, (station_name, station_name))

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

