import streamlit as st
import pandas as pd
from pages.database import database

def display():
    st.title("⚙️ Admin Settings")

    # Header image
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        image_path = "assets//"
        st.image(f"{image_path}Train-pana.png", use_column_width=True)

    # Tabs for different sections
    tab1, tab2 = st.tabs(["👤 User Settings", "🔧 System Settings"])

    with tab1:
        st.subheader("👤 User Settings")
        st.markdown("Manage user accounts and roles with ease.")

        st.divider()

        with st.expander("Add User", expanded=True):
            with st.form("Add User Form"):
                user_name = st.text_input("User Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["Admin", "User"])
                submit_user = st.form_submit_button("Add User")
                if submit_user:
                    if role == "User":
                        try:
                            database.register_user(user_name, email, password)
                            st.success(f"User {user_name} added successfully with role {role}!")
                        except Exception as e:
                            st.error(f"Error in adding user: {e}")
                    if role == "Admin":
                        try:
                            database.register_admin(user_name, email, password)
                            st.success(f"User {user_name} added successfully with role {role}!")
                        except Exception as e:
                            st.error(f"Error in adding user: {e}")

        st.divider()

        with st.expander("View All Users", expanded=True):
            users = database.get_users()
            if users:
                df_users = pd.DataFrame(users)
                st.dataframe(df_users.style.set_properties(**{'text-align': 'center'}))
            else:
                st.info("No users available at the moment.")

    with tab2:
        st.subheader("🔧 System Settings")
        st.markdown("Configure system settings and preferences.")
        st.divider()
        st.write("Logout of the system")
        if st.button("Logout", key="logout"):
            st.session_state.role = None
            st.session_state.user_logged_in = None
            st.session_state.email = None
            st.session_state.username = None
            st.session_state.logged_in = None
            st.rerun()


    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;color:gray;font-size:small;">© 2024 Train Reservation System. All rights reserved.</p>',
        unsafe_allow_html=True,
    )

