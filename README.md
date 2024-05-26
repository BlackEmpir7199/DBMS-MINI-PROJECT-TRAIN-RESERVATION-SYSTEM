# User Authentication and System Setup Guide

Welcome to the User Authentication and System Setup guide for managing trains, stations, and user authentication in your application. This guide provides detailed instructions on setting up, using, and troubleshooting the authentication function and managing various aspects of your system.

## Overview

The `authenticate_user` function is a crucial component designed to authenticate users by validating their email and password against records stored in a MySQL database. Additionally, this guide covers instructions on setting up and managing trains, stations, and other settings within your system.

## Setup Instructions

### 1. Install Required Python Libraries

Ensure you have the necessary Python libraries installed by running the following command:

```bash
pip install -r requirements.txt
```

### 2. Database Configuration

Set up your MySQL database and create the required tables by following these steps:

1. **Open MySQL Workbench**: Download and install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
2. **Connect to MySQL Server**: Open MySQL Workbench and connect to your MySQL server.
3. **Create Database**: If not already created, create a new database:
   
    ```sql
    CREATE DATABASE your_database;
    ```
4. **Create Tables**: Create the necessary tables (e.g., `admins`, `users`, `trains`, `stations`) with appropriate columns. See the example provided in the guide for table structure.

    ```sql
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
    ```
## Function Definition

The `create_connection` function to establish database connectivity. Below is the function definition along with table name sanitization to ensure security and effectiveness.

```python
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
```

## Usage Instructions

Follow these steps to utilize the `authenticate_user` function:

1. Define User Credentials and Table:
   ```python
   table_name = 'admins'
   email = 'example@gmail.com'
   password = 'password123'
   ```

2. Call the Function:
   ```python
   user = authenticate_user(table_name, email, password)
   if user:
       print("User authenticated successfully")
   else:
       print("Authentication failed")
   ```

## Example Script

An example script is provided to demonstrate the usage of the authentication function along with other functionalities like registering users and admins.

```python
import mysql.connector
from mysql.connector import Error
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
```

## Managing Trains, Stations, and Settings

You can manage trains, stations, and other settings using functions provided in the guide. Example functions include adding trains, booking tickets, and updating stations.

```python
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
```
## Troubleshooting

If you encounter any issues, consider the following troubleshooting steps:

- **Connection Issues**: Verify database connection parameters.
- **Invalid Table Name**: Ensure the table name is correct and in the allowed list.
- **SQL Errors**: Check console output for SQL errors and verify table structure.

## Security Considerations

To ensure security, follow these best practices:

- **Parameterization**: Always use parameterized queries to prevent SQL injection.
- **Sanitization**: Verify and sanitize user inputs, especially table names, to prevent SQL injection attacks.

By following this guide, you should be able to securely authenticate users and effectively manage various aspects of your system. For further assistance, refer to the troubleshooting section or consult MySQL and Python documentation.

---

Feel free to customize this guide to fit your specific application requirements. Happy coding! 🚀
