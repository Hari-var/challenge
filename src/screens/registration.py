import streamlit as st
from database.tables import User
import datetime

def registration_page():
    st.title("User Registration")

    with st.form("registration_form"):
        # usertype = st.selectbox("User Type", ["user", "admin", "developer"])
        username = st.text_input("Username *")
        firstname = st.text_input("First Name *")
        middlename = st.text_input("Middle Name")
        lastname = st.text_input("Last Name *")
        password = st.text_input("Password *", type="password")
        dateofbirth = st.date_input(
            "Date of Birth",
            value=datetime.date(2000, 1, 1),  # default to year 2000
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today()
        )
        phone = st.text_input("Phone")
        email = st.text_input("Email *")
        address = st.text_area("Address *")
        submit = st.form_submit_button("Register")

        if submit:
            if not username or not firstname or not lastname or not password or not email or not address:
                st.error("Please fill all required fields.")
            else:
                user_obj = User()
                # try:
                user_obj.add(
                    # usertype='user',  # Default to 'user' if not provided
                    username=username,
                    firstname=firstname,
                    middlename=middlename,
                    lastname=lastname,
                    password=password,
                    dateofbirth=dateofbirth,
                    phone=phone,
                    email=email,
                    address=address
                )
                st.success("Registration successful!")
                # except Exception as e:
                #     st.error(f"Registration failed: {e}")

if __name__ == "__main__":
    registration_page()