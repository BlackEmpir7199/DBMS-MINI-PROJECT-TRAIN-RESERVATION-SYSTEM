import streamlit as st

# Declare the main function for onboarding as user and admin
def display():
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    # Show the logo and ask what kind of login
    st.header("iRTS - Railway Reservation System", divider='red')
    col1, col2 = st.columns([1, 1])
    with col1:
        container = st.container()
        with container:
            cola, colb, colc = st.columns([1, 2, 1])
            with colb:
                st.markdown("<h3 style='text-align: center;'>User</h3>", unsafe_allow_html=True)
                image_path = "assets\\"
                st.image(f"{image_path}Mobile inbox-pana.png", use_column_width=True)
                if st.button("Enter", key='user'):
                    st.session_state['role'] = 'user'
                    st.rerun()

    with col2:
        container = st.container()
        with container:
            cola, colb, colc = st.columns([1, 2, 1])
            with colb:
                st.markdown("<h3 style='text-align: center;'>Admin</h3>", unsafe_allow_html=True)
                image_path = "assets\\"
                st.image(f"{image_path}Server-cuate.png", use_column_width=True)
                if st.button("Enter", key='admin'):
                    st.session_state['role'] = 'admin'
                    st.rerun()

