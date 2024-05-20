import streamlit as st
import database

def display():
    st.title("Sign Up")
    username = st.text_input("Username")
    usermail = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password == confirm_password:
            if database.register_user(username,usermail, password):
                st.success("Sign up successful!")
                # Redirect to login page or perform further actions
            else:
                st.error("Failed to register user")
        else:
            st.error("Passwords do not match")
