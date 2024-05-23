import mysql.connector
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
        if params:
            query = query % params
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def execute_read_query_without_session(query, params=()):
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
    stations = execute_read_query(query)
    return stations
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
    trains = execute_read_query_without_session(query, params)
    return trains

def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_read_query(query, (email,))
    return user[0] if user else None
def get_userid_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_read_query(query, (email,))
    return user[0]['user_id'] if user else None

def get_username_by_email(table, email):
    query = f"SELECT * FROM {table} WHERE email = '%s'"
    user = execute_read_query(query, (email))
    return user[0]['name'] if user else None


def create_user(name, email):
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    user_id = execute_query(query, (name, email))
    return user_id

def book_ticket(train_id, user_id, date_of_travel):
    query = "CALL book_ticket(%s, %s, %s)"
    params = (train_id, user_id, date_of_travel)
    booking_id = execute_query(query, params)
    return booking_id

def add_passenger(booking_id, name, age, sex):
    query = "INSERT INTO passengers (booking_id, name, age, sex) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (booking_id, name, age, sex))

def get_tickets(email):
    query = """
    SELECT b.booking_id, b.train_id, b.date_of_travel, u.name
    FROM bookings b
    JOIN users u ON b.user_id = u.user_id
    WHERE u.email = %s
    """
    params = (email,)
    tickets = execute_read_query(query, params)
    return tickets
