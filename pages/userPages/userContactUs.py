import streamlit as st

def display():
    # Title and Subtitle
    st.title("📞 Contact Us")
    st.subheader("We're here to help!")
    # Add an image/banner
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.image('assets//train-pana.png', width=450)

    # Contact Information
    st.markdown("""
        <style>
        .contact-info {
            font-size: 20px;
            margin-bottom: 25px;
        }
        .contact-icon {
            font-size: 22px;
            margin-right: 10px;
        }
        </style>
        <div class="contact-info">
            <p><span class="contact-icon">📧</span>Email: <a href="mailto:support@trainbookingsystem.com">support@trainbookingsystem.com</a></p>
            <p><span class="contact-icon">📞</span>Phone: +1 234 567 890</p>
            <p><span class="contact-icon">🏢</span>Address: 123 Train St, Booking City, Country</p>
        </div>
    """, unsafe_allow_html=True)

    # Contact Form
    st.markdown("### Send Us a Message")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            st.success("Thank you for reaching out to us! We'll get back to you soon.")

    # Social Media Links
    st.markdown("""
        <style>
        .social-media {
            font-size: 25px;
        }
        .social-media a {
            margin: 0 15px;
        }
        </style>
        <div class="social-media">
            <a href="https://facebook.com" target="_blank">🌐 Facebook</a>
            <a href="https://twitter.com" target="_blank">🌐 Twitter</a>
            <a href="https://linkedin.com" target="_blank">🌐 LinkedIn</a>
            <a href="https://instagram.com" target="_blank">🌐 Instagram</a>
        </div>
    """, unsafe_allow_html=True)

    # Add a decorative line
    st.markdown("<hr style='border: 1px solid #f0f0f0;'>", unsafe_allow_html=True)

# Call the function to display the page
