import streamlit as st
import database


def display():
    st.title("Login")
    usermail = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = database.authenticate_user(usermail, password)
        if user:
            st.success("Logged in successfully!")
            # Set session state variable to indicate user is logged in
            if 'email' not in st.session_state:
                st.session_state['email'] = usermail
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = True

            st.experimental_rerun()

            # Redirect to main page or perform further actions
        else:
            st.error("Invalid username or password")
