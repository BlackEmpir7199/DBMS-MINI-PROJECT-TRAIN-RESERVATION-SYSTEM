import mysql.connector
import streamlit
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_DATABASE')
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

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

def execute_query(query, params=()):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(query, params=()):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()


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


def get_users():
    query = "SELECT * FROM users"
    users = execute_read_query(query)
    return users


def get_trains():
    query = "SELECT * FROM trains"
    trains = execute_read_query(query)
    return trains


def search_trains(from_station, to_station, date_of_travel):
    query = """
    SELECT * FROM trains 
    WHERE from_station IN (SELECT station_id FROM stations WHERE name = %s) 
    AND to_station IN (SELECT station_id FROM stations WHERE name = %s)
    """
    params = (from_station, to_station)
    trains = execute_read_query(query, params)
    return trains


def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_read_query(query, (email,))
    return user[0] if user else None


def get_username_by_email(table, email):
    query = f"SELECT * FROM {table} WHERE email = %s"
    user = execute_read_query(query, (email,))
    return user[0]['name'] if user else None


def create_user(name, email):
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    user_id = execute_query(query, (name, email))
    return user_id


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
