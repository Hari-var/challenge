import streamlit as st
import time
from screens.policies import new_policy_page
from database.tables import User
from screens.login import login_page

def main_page():
    

    # sidebar with policies page and home page
    st.sidebar.title("Navigation")
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    st.session_state.page = st.sidebar.selectbox("Go to", ["Home", "Policies"], index=["Home", "Policies"].index(st.session_state['page']))
    if st.button("create new policy"):
        st.session_state.page = "Policies"
        

    page = st.session_state['page']
    
    if page == "Home":
        st.title("ValueMomentum Insurance")
        st.write("Welcome to the ValueMomentum Insurance app!")
    elif page == "Policies":
        new_policy_page()

if __name__ == "__main__": 
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if st.session_state['logged_in']:
        main_page()  # Show the main page if logged in
    else:
        login_page()