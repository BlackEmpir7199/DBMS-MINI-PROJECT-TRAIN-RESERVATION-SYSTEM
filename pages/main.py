import streamlit as st
from streamlit_option_menu import option_menu
import home
import book_ticket
import view_tickets
import contact_us
import login, signup

#MAIN FUNCTION
def main():

    # Check if the user is logged in
    if not st.session_state.get('logged_in', False):
        # Display login/signup form
        st.sidebar.title("Login / Sign Up")
        page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
        if page == "Login":
            login.display()
        elif page == "Sign Up":
            signup.display()
    else:
        # Display main navigation
        with st.sidebar:

            selected = option_menu("Main Menu", ["Home", "Book Ticket", "View Tickets", "Contact Us"],
                                   icons=['house', 'ticket', 'list', 'envelope'],
                                   menu_icon="cast", default_index=0)

        # Display the selected page
        if selected == "Home":
            home.display()
        elif selected == "Book Ticket":
            book_ticket.display()
        elif selected == "View Tickets":
            view_tickets.display()
        elif selected == "Contact Us":
            contact_us.display()

if __name__ == "__main__":
    main()
