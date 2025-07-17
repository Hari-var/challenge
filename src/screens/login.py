import streamlit as st
import time
import streamlit_authenticator

import pickle
from pathlib import Path
from helpers.database import User  # Import User class

def login_page():
    """Login page for the Insurance Chatbot."""
    st.markdown("<h2 style='text-align: center;'>🔐 Login to Insurance Chatbot</h2>", unsafe_allow_html=True)
    
    # Center the login form using columns
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
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