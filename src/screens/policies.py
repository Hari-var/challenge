from database import (
    get_all_policies,
    add_policy,
    get_policy_by_id,
    get_policies_by_holder,
    update_policy,
    add_vehicle,  # <-- import this
)
import datetime
import streamlit as st
import os

def policies_page():
    st.title("Policies")

    # --- Search Bar ---
    search = st.text_input("Search by Policy Holder Name or Policy Number")

    # --- State Initialization ---
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False
    if "edit_policy_id" not in st.session_state:
        st.session_state.edit_policy_id = None
    if "view_policy_id" not in st.session_state:
        st.session_state.view_policy_id = None

    # --- Add New Policy Button ---
    if st.button("Add New Policy"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.session_state.view_policy_id = None

    # --- Add Policy Form ---
    if st.session_state.show_add_form:
        with st.form("add_policy_form", clear_on_submit=True):
            # Policy details
            policy_holder = st.text_input("Policy Holder Name")
            start_date = st.date_input("Start Date", datetime.date.today())
            end_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=365))
            premium = st.number_input("Premium", min_value=0.0)
            status = st.selectbox("Status", ["active", "inactive"])

            st.markdown("#### Vehicle Details")
            # Vehicle details
            make = st.text_input("Vehicle Make")
            model = st.text_input("Vehicle Model")
            year_of_purchase = st.number_input("Year of Purchase", min_value=1900, max_value=datetime.date.today().year, value=datetime.date.today().year)
            image_file = st.file_uploader("Upload Vehicle Image", type=["png", "jpg", "jpeg"])

            submitted = st.form_submit_button("Submit")
            if submitted:
                # Save image to local folder and get path
                image_path = ""
                if image_file:
                    image_folder = "vehicle_images"
                    os.makedirs(image_folder, exist_ok=True)
                    image_path = os.path.join(image_folder, image_file.name)
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                # Add policy and vehicle
                policy_id, policy_number = add_policy(
                    policy_holder,
                    str(start_date),
                    str(end_date),
                    premium,
                    status,
                )
                add_vehicle(
                    policy_id,
                    image_path,
                    make,
                    model,
                    year_of_purchase,
                )
                st.success(f"Policy {policy_number} and vehicle added successfully!")
                st.session_state.show_add_form = False
                st.rerun()

    # --- Retrieve and Filter Policies ---
    policies = get_all_policies()
    if search:
        policies = [
            p for p in policies
            if search.lower() in str(p[2]).lower() or search.lower() in str(p[1]).lower()
        ]

    # --- Display Policies Table ---
    if policies and not st.session_state.show_add_form and not st.session_state.show_edit_form and not st.session_state.view_policy_id:
        import pandas as pd
        df = pd.DataFrame(
            policies,
            columns=[
                "Policy ID", "Policy Number", "Policy Holder", "Start Date",
                "End Date", "Premium", "Status"
            ]
        )
        st.dataframe(df, use_container_width=True)

        # --- Clickable Row ---
        selected_id = st.number_input("Enter Policy ID to View/Edit", min_value=1, step=1)
        if st.button("View Policy"):
            st.session_state.view_policy_id = selected_id

    # --- View Policy ---
    if st.session_state.view_policy_id and not st.session_state.show_edit_form:
        policy = get_policy_by_id(st.session_state.view_policy_id)
        if policy:
            st.subheader(f"Policy: {policy[2]} ({policy[1]})")
            st.write(f"Start Date: {policy[3]}")
            st.write(f"End Date: {policy[4]}")
            st.write(f"Premium: {policy[5]}")
            st.write(f"Status: {policy[6]}")
            if st.button("Edit Policy"):
                st.session_state.show_edit_form = True
        else:
            st.warning("Policy not found.")
            st.session_state.view_policy_id = None

        if st.button("Back to Policies"):
            st.session_state.view_policy_id = None
            st.session_state.show_edit_form = False
            st.session_state.edit_policy_id = None
            st.rerun()

    # --- Edit Policy Form ---
    if st.session_state.show_edit_form and st.session_state.view_policy_id:
        policy = get_policy_by_id(st.session_state.view_policy_id)
        if policy:
            with st.form("edit_policy_form", clear_on_submit=True):
                new_holder = st.text_input("Policy Holder Name", value=policy[2])
                new_start = st.date_input("Start Date", value=datetime.datetime.strptime(policy[3], "%Y-%m-%d"))
                new_end = st.date_input("End Date", value=datetime.datetime.strptime(policy[4], "%Y-%m-%d"))
                new_premium = st.number_input("Premium", min_value=0.0, value=policy[5])
                new_status = st.selectbox("Status", ["active", "inactive"], index=0 if policy[6]=="active" else 1)
                save = st.form_submit_button("Save Changes")
                if save:
                    update_policy(
                        policy[0],
                        new_holder,
                        str(new_start),
                        str(new_end),
                        new_premium,
                        new_status,
                    )
                    st.success("Policy updated!")
                    st.session_state.show_edit_form = False
                    st.session_state.view_policy_id = None
                    st.rerun()
            if st.button("Cancel Edit"):
                st.session_state.show_edit_form = False
                st.rerun()
        else:
            st.warning("Policy not found.")
            st.session_state.show_edit_form = False
            st.session_state.view_policy_id = None

    if not policies:
        st.info("No policies found.")

policies_page()