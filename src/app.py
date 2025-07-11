import streamlit as st

def main():
    st.title("ValueMomentum Insurance")
    st.write("Welcome to the ValueMomentum Insurance app!")

    # sidebar with policies page and home page
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Policies"])