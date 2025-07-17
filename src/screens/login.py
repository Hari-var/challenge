import streamlit as st
import time
from database.tables import User
from screens.registration import registration_page

def login_page():
    """Login page for the Insurance Chatbot."""
    st.markdown("<h2 style='text-align: center;'>🔐 Login to Insurance Chatbot</h2>", unsafe_allow_html=True)
    
    # Center the login form using columns
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
        # If ?register=1 in URL, show registration page
        query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
        if query_params.get("register", ["0"])[0] == "1":
            registration_page()
            return

        with st.form("login_form"):
            # Input fields for username and password
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password") 
            # Login button
            submitted = st.form_submit_button("Login")
            if submitted:
                user_obj = User()
                # Query user by username
                users = user_obj.get_all()
                user = None
                for u in users:
                    # users table: user_id, usertype, username, firstname, middlename, lastname, password, dateofbirth, phone, email, address
                    if u[2] == username:
                        user = u
                        break
                if user and user[6] == password:
                    st.session_state['logged_in'] = True  # Update login state
                    st.session_state['user_id'] = user[0]  # Store user_id for later use
                    st.success("Login successful! Redirecting...")
                    time.sleep(0.6)
                    st.rerun()  # Redirect to the main page
                else:
                    st.error("Invalid credentials. Please try again.")

        # Display the hyperlink
        st.markdown(
            "<p style='text-align:center;'>Not a user? <a href='?register=1'>Create account</a></p>",
            unsafe_allow_html=True
        )
