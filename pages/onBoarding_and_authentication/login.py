import streamlit as st
from pages.database import database

def display():
    st.title(f"Login as {st.session_state.role}")
    if st.session_state.role == "user":
        table = "users"
    else:
        table = "admins"
    usermail = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = database.authenticate_user(table, usermail, password)
        if user:
            st.success("Logged in successfully!")
            st.session_state.email = usermail
            st.session_state.logged_in = True
            st.session_state.username = database.get_username_by_email(table, usermail)
            st.session_state.user_logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")
