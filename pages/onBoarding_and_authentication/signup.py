import streamlit as st
from pages.database import database

def display():
    st.title(f"Sign Up as {st.session_state.role}")
    username = st.text_input("Username")
    usermail = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password == confirm_password:
            if database.register_user(username, usermail, password):
                st.success("Sign up successful!")
                st.session_state.email = usermail
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_logged_in = True
                st.rerun()
            else:
                st.error("Failed to register user")
        else:
            st.error("Passwords do not match")
