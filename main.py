import streamlit as st
from streamlit_option_menu import option_menu
from pages.userPages import userBookTicket, userContactUs, userHome, userViewTickets
from pages.onBoarding_and_authentication import login, signup, onboardingLogin
from pages.adminPages import adminGuide, adminHome, adminSettings
st.set_page_config(layout="wide")

def status_shower(email, username, status):
    text = f"""<button id="btn-message" class="button-message">
    <div class="content-avatar">
        <div class="status-user"></div>
        <div class="avatar">
            <svg class="user-img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12,12.5c-3.04,0-5.5,1.73-5.5,3.5s2.46,3.5,5.5,3.5,5.5-1.73,5.5-3.5-2.46-3.5-5.5-3.5Zm0-.5c1.66,0,3-1.34,3-3s-1.34-3-3-3-3,1.34-3,3,1.34,3,3,3Z"></path></svg>
        </div>
    </div>
    <div class="notice-content">
        <div class="username">{username}</div>
        <div class="lable-message">{status}<span class="number-message"></span></div>
        <div class="user-id">{email}</div>
    </div>
</button>"""
    if status == "Logged in":
        online_status = "#00da00"
    else:
        online_status = "#880808"

    css = f"""<style>
    #btn-message {{
        --text-color: rgb(255, 255, 255);
        --bg-color-sup: #5e5e5e;
        --bg-color: #000000;
        --bg-hover-color: #161616;
        --online-status: {online_status};
        --font-size: 16px;
        --btn-transition: all 0.2s ease-out;
    }}
    @media (prefers-color-scheme: dark) {{
        #btn-message {{
            --text-color: var(--text-color-dark);
            --bg-color-sup: var(--bg-color-sup-dark);
            --bg-color: var(--bg-color-dark);
            --bg-hover-color: var(--bg-hover-color-dark);
        }}
    }}

    @media (prefers-color-scheme: light) {{
        #btn-message {{
            --text-color: var(--text-color-light);
            --bg-color-sup: var(--bg-color-sup-light);
            --bg-color: var(--bg-color-light);
            --bg-hover-color: var(--bg-hover-color-light);
        }}
    }}

    .button-message {{
        display: flex;
        justify-content: center;
        align-items: center;
        font: 400 var(--font-size) Helvetica Neue, sans-serif;
        box-shadow: 0 0 2.17382px rgba(0,0,0,.049),0 1.75px 6.01034px rgba(0,0,0,.07),0 3.63px 14.4706px rgba(0,0,0,.091),0 22px 48px rgba(0,0,0,.14);
        background-color: var(--bg-color);
        border-radius: 68px;
        cursor: pointer;
        padding: 6px 10px 6px 6px;
        width: fit-content;
        height: 40px;
        border: 0;
        margin: 10px 10px 10px 60px;
        overflow: hidden;
        position: relative;
        transition: var(--btn-transition);
    }}

    .button-message:hover {{
        height: 48px;
        padding: 8px 20px 8px 8px;
        background-color: var(--bg-hover-color);
        transition: var(--btn-transition);
    }}

    .button-message:active {{
        transform: scale(0.99);
    }}

    .content-avatar {{
        width: 30px;
        height: 30px;
        margin: 0;
        transition: var(--btn-transition);
        position: relative;
    }}

    .button-message:hover .content-avatar {{
        width: 40px;
        height: 40px;
    }}

    .avatar {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        overflow: hidden;
        background-color: var(--bg-color-sup);
    }}

    .user-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .status-user {{
        position: absolute;
        width: 6px;
        height: 6px;
        right: 1px;
        bottom: 1px;
        border-radius: 50%;
        outline: solid 2px var(--bg-color);
        background-color: var({online_status});
        transition: var(--btn-transition);
        animation: active-status 2s ease-in-out infinite;
    }}

    .button-message:hover .status-user {{
        width: 10px;
        height: 10px;
        right: 1px;
        bottom: 1px;
        outline: solid 3px var(--bg-hover-color);
    }}

    .notice-content {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        padding-left: 8px;
        text-align: initial;
        color: var(--text-color);
    }}

    .username {{
        letter-spacing: -6px;
        height: 0;
        opacity: 0;
        transform: translateY(-20px);
        transition: var(--btn-transition);
    }}

    .user-id {{
        font-size: 12px;
        letter-spacing: -6px;
        height: 0;
        opacity: 0;
        transform: translateY(10px);
        transition: var(--btn-transition);
    }}

    .lable-message {{
        display: flex;
        align-items: center;
        opacity: 1;
        transform: scaleY(1);
        transition: var(--btn-transition);
    }}

    .button-message:hover .username {{
        height: auto;
        letter-spacing: normal;
        opacity: 1;
        transform: translateY(0);
        transition: var(--btn-transition);
    }}

    .button-message:hover .user-id {{
        height: auto;
        letter-spacing: normal;
        opacity: 1;
        transform: translateY(0);
        transition: var(--btn-transition);
    }}

    .button-message:hover .lable-message {{
        height: 0;
        transform: scaleY(0);
        transition: var(--btn-transition);
    }}

    .lable-message, .username {{
        font-weight: 600;
    }}

    .number-message {{
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-left: 8px;
        font-size: 12px;
        width: 16px;
        height: 16px;
        background-color: #c62828;
        color: #ffffff;
        border-radius: 50%;
        animation: notification 1s ease-in-out infinite alternate;
    }}

    @keyframes active-status {{
        from {{
            opacity: 0.4;
        }}
        to {{
            opacity: 1;
        }}
    }}

    @keyframes notification {{
        from {{
            transform: scale(1) translateY(0);
        }}
        to {{
            transform: scale(1.2) translateY(-2px);
        }}
    }}
    </style>"""

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(text, unsafe_allow_html=True)

def main():

    if not st.session_state.get('role', False):
        onboardingLogin.display()


    if st.session_state.role == 'user':
        if not st.session_state.get('user_logged_in', False):
            page = option_menu(menu_title=None, options=["Login", "Sign Up"], icons=["person", "person-plus"],
                               orientation="horizontal")
            if page == "Login":
                login.display()
            elif page == "Sign Up":
                signup.display()
        else:
            with st.sidebar:
                st.markdown("<h1 style='text-align: center;'>User Dashboard</h1>", unsafe_allow_html=True)
                selected = option_menu("Main Menu", ["Home", "Book Ticket", "View Tickets", "Contact Us"],
                                       icons=['house', 'ticket', 'list', 'envelope'],
                                       menu_icon="train-front", default_index=0)

                status_shower(st.session_state.email, st.session_state.username,
                              "Logged In" if st.session_state.logged_in else "Logged Out")

            if selected == "Home":
                userHome.display()
            elif selected == "Book Ticket":
                userBookTicket.display()
            elif selected == "View Tickets":
                userViewTickets.display()
            elif selected == "Contact Us":
                userContactUs.display()

    elif st.session_state.role == 'admin':
        if not st.session_state.get('user_logged_in', False):
            login.display()
        else:
            with st.sidebar:
                st.markdown("<h1 style='text-align: center;'>Admin Dashboard</h1>", unsafe_allow_html=True)

                selected = option_menu("Admin Menu", ["Home", "Manage Trains", "Manage Stations", "Settings","Guide"],
                                   icons=['house', 'train-front', 'pin-map', 'gear','book'],
                                   menu_icon="tools", default_index=0)
                status_shower(st.session_state.email, "Admin",
                              "Logged In" if st.session_state.user_logged_in else "Logged Out")

            if selected == "Home":
                adminHome.display()
            if selected == "Settings":
                adminSettings.display()
            if selected == "Guide":
                adminGuide.display()
            # Add appropriate functions for the admin menu items as needed


if __name__ == "__main__":
    main()
