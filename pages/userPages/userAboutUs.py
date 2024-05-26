import streamlit as st


def display():
    st.title("About Us")
    st.markdown("---")

    st.header("Our Team")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.subheader("Rakhul",divider='red')
            if st.button("Know More About Rakhul"):
                with st.expander("Details"):
                    st.markdown("""
                    **Student at Rajalakshmi Engineering College, II Year - CSE**

                    Second-year Computer Science and Engineering student at Rajalakshmi Engineering College. Talented developer with a keen eye for detail and a passion for learning. Expertise in various technologies and the ability to quickly adapt to new challenges have been invaluable to the team's success. Significant contributions have been made to both the front-end and back-end connections of the project. 
                    """)
                st.balloons()

    with col2:
        with st.container():
            st.subheader("Sabarish",divider='red')
            if st.button("Know More About Sabarish"):
                with st.expander("Details"):
                    st.markdown("""
                    **Student at Rajalakshmi Engineering College, II Year - CSE**

                    Second-year Computer Science and Engineering student at Rajalakshmi Engineering College. Skilled in backend development, database normalization, and problem-solving. Strong analytical thinker with a passion for coding and creating efficient systems. Contributions have been pivotal in enhancing system performance and reliability, demonstrating dedication and diligence in every project undertaken.
                    """)
                st.snow()

    st.markdown("---")
    st.header("Project Stack")
    st.markdown("""
    Our project leverages a combination of powerful technologies to deliver an efficient and user-friendly train reservation system. Here's a look at the technology stack we used:
    """)

    with st.expander("Streamlit"):
        st.markdown("""
        - **Streamlit**: An open-source app framework used to create the front-end interface. Streamlit allows for quick and easy development of interactive web applications.
        """)

    with st.expander("MySQL"):
        st.markdown("""
        - **MySQL**: A reliable and scalable relational database management system used for storing and managing data. MySQL's robust features enable us to handle complex queries and transactions efficiently.
        """)

    st.markdown("""
    Our team has worked diligently to integrate these technologies seamlessly, ensuring a smooth and enjoyable user experience. We are proud of what we have achieved and look forward to continuing to improve and expand our system.
    """)

