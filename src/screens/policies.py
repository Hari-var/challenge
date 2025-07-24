import streamlit as st
import datetime
import os
import base64
import time
from PIL import Image
from json import loads

from database.tables import Policy, Vehicle
from database.tables import User

from AI_ML.agents import verify_vehicle_images
from helpers.file_handlers import Load, Extract
from helpers.prompts import vehicle_details_extract_prompt as prompt


import streamlit.components.v1 as components

def clear_policy_session_state():
    keys_to_clear = [
        'add_policy_step',
        'active_tab',
        'policy_info',
        'vehicle_info'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# def verify_vehicle_images(front, back, left, right,make,model,type,year):
#     front= Image.open(front)  
#     back = Image.open(back)
#     left = Image.open(left)
#     right = Image.open(right)
#     ex=Extract()
#   # Replace with the appropriate response value
#     response = gemini_ai(front, back, left, right, prompt)
#     verify = ex.extract_code(response)
#     # print(verify) 
#     result = loads(verify)
#     year_range = list(map(int,result['Manufacturing_year_range'].split('-')))
#     year_validity = False
#     if len(year_range) == 2:
#         year_validity = year_range[0] <= int(year) <= year_range[1]
#     else:
#         year_validity = year_range[0] <= int(year)

#     if result['make'].lower() == make.lower() and result['model'].lower() == model.lower() and result['vehicle_type'].lower()==type.lower() and year_validity:
#         return [True, result]
#     else:
#         st.error("Vehicle details are not valid!")
#         # print("result['make'].lower() == make.lower()", result['make'].lower(), make.lower())
#         # print("result['model'].lower() == model.lower()", result['model'].lower(), model.lower())
#         # print("result['vehicle_type'].lower() == type.lower()", result['vehicle_type'].lower(), type.lower())
#         # print("year_validity", year_validity, year_range, year)
#         return [False,result]
#     # print(result, type(result)) # or simply print(response) to see the whole structure
    
    

def personal_info_autofill():
    st.header("Policy Holder Information")
    with st.form("personal_info_form"):
        policy_holder = st.text_input("Policy Holder Name *", value=st.session_state.personal_info.get("policy_holder", ""), disabled=True)
        dateofbirth = st.text_input("Date of Birth *", value=str(st.session_state.personal_info.get("dateofbirth", "")), disabled=True)
        email = st.text_input("Email *", value=st.session_state.personal_info.get("email", ""), disabled=True)
        phone = st.text_input("Phone Number *", value=st.session_state.personal_info.get("phone", ""), disabled=True)
        address = st.text_area("Address *", value=st.session_state.personal_info.get("address", ""), disabled=True)
        next1 = st.form_submit_button("Submit")
        error = ""
        if next1:
            # Basic validation
            if not policy_holder or not email or not phone or not address:
                error = "Please fill all required fields."
            elif "@" not in email or "." not in email:
                error = "Please enter a valid email address."
            elif len(str(phone)) < 7:
                error = "Please enter a valid phone number."
            else:
                st.session_state.personal_info = {
                    "policy_holder": policy_holder,
                    "dateofbirth": dateofbirth,
                    "email": email,
                    "phone": phone,
                    "address": address,
                }
                st.session_state.add_policy_step = max(st.session_state.add_policy_step, 1)
                st.session_state.active_tab = 1
                st.rerun()  # Switch to Policy Info tab
                  # Switch to Policy Info tab
        if error:
            st.error(error)

def policy_info_tab():
    st.header("Policy Details")
    if st.session_state.add_policy_step >= 1:
        with st.form("policy_info_form"):
            start_date = st.date_input("Start Date *", value=st.session_state.policy_info.get("start_date", datetime.date.today()))
            end_date = st.date_input("End Date *", value=st.session_state.policy_info.get("end_date", datetime.date.today() + datetime.timedelta(days=365)))
            premium = st.number_input("Premium Amount *", min_value=0.0, value=st.session_state.policy_info.get("premium", 0.0))
            status = st.selectbox("Status *", ["active", "inactive"], index=0 if st.session_state.policy_info.get("status", "active") == "active" else 1)
            next2 = st.form_submit_button("Submit")
            error = ""
    
            if next2:
                if end_date <= start_date:
                    error = "End date must be after start date."
                elif premium <= 0:
                    error = "Premium must be greater than zero."
                else:
                    st.session_state.policy_info = {
                        "start_date": start_date,
                        "end_date": end_date,
                        "premium": premium,
                        "status": status,
                    }
                    st.session_state.add_policy_step = max(st.session_state.add_policy_step, 2)
                    st.session_state.active_tab = 2
                    st.write(st.session_state.active_tab)
                    # st.rerun()
            if error:
                st.error(error)
    else:
        st.info("Please complete Personal Info first.")

def vehicle_info_tab():
    st.header("Vehicle Information")
    if st.session_state.add_policy_step >= 2:
        with st.form("vehicle_info_form"):
            typeofvehicle = st.selectbox("Type of Vehicle *", ["fourwheeler", "threewheeler", "twowheeler", "other"], index=0)
            make = st.text_input("Vehicle Make *", value=st.session_state.vehicle_info.get("make", ""))
            model = st.text_input("Vehicle Model *", value=st.session_state.vehicle_info.get("model", ""))
            year_of_purchase = st.number_input("Year of Purchase *", min_value=1900, max_value=datetime.date.today().year, value=st.session_state.vehicle_info.get("year_of_purchase", datetime.date.today().year))
            chasis_no = st.text_input("Chassis Number", value=st.session_state.vehicle_info.get("chasis_no", ""))
            vehicle_number = st.text_input("Vehicle Number", value=st.session_state.vehicle_info.get("vehicle_number", "")) 
            image_front = st.file_uploader("Upload Front Image", type=["png", "jpg", "jpeg"])
            image_back = st.file_uploader("Upload Back Image", type=["png", "jpg", "jpeg"])
            image_left = st.file_uploader("Upload Left Image", type=["png", "jpg", "jpeg"])
            image_right = st.file_uploader("Upload Right Image", type=["png", "jpg", "jpeg"])
            next3 = st.form_submit_button("Submit")
            error = ""
            if next3:
                if not make or not model:
                    error = "Please fill all required fields."
                else:
                    folder_name = f"{make}_{model}_{year_of_purchase}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    image_paths = Load().save_vehicle_images(image_front, image_back, image_left, image_right, folder_name, typeofvehicle=typeofvehicle)
                    
                    verification_result = verify_vehicle_images(
                        image_paths.get("front", ""),
                        image_paths.get("back", ""),
                        image_paths.get("left", ""),
                        image_paths.get("right", ""),
                        make,
                        model,
                        typeofvehicle,
                        int(year_of_purchase)
                    )
                    if verification_result[0]:
                        st.session_state.vehicle_info = {
                          "make": make,
                          "model": model,
                          "year_of_purchase": year_of_purchase,
                          "typeofvehicle": typeofvehicle,
                          "image_main_folder": image_paths.get("main_folder", ""),
                          "image_front_path": image_paths.get("front", ""),
                          "image_back_path": image_paths.get("back", ""),
                          "image_left_path": image_paths.get("left", ""),
                          "image_right_path": image_paths.get("right", ""),
                          "damages": verification_result[1]['damages'] ,
                        }
                        
                        st.session_state.add_policy_step = max(st.session_state.add_policy_step, 3)
                        st.session_state.active_tab = 3
                        st.success("Vehicle details are valid!")
                        st.info(f"DAMAGE REPORT:\n\t{st.session_state.vehicle_info.get('damages', '')}")
                        # st.write(st.session_state.add_policy_step)
                        st.rerun()
                    else:
                        error = "Vehicle verification failed. Please check the images and details."
            
            if error:
                st.error(error)
    else:
        st.info("Please complete Policy Info first.")

def summary_tab():
    st.header("Review & Submit")
    if st.session_state.add_policy_step >= 3:
        personal = st.session_state.personal_info
        policy = st.session_state.policy_info
        vehicle = st.session_state.vehicle_info
        today = datetime.date.today().strftime("%Y-%m-%d")

        def get_image_tag(image_path, label):
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    b64_img = base64.b64encode(img_file.read()).decode()
                    return f"<div style='margin-bottom:10px'><strong>{label}:</strong><br><img src='data:image/jpeg;base64,{b64_img}' alt='{label}' style='width:200px;border:1px solid #aaa;border-radius:8px;'/></div>"
            return ""

        image_tags = ""
        image_tags += get_image_tag(vehicle.get("image_front_path", ""), "Front")
        image_tags += get_image_tag(vehicle.get("image_back_path", ""), "Back")
        image_tags += get_image_tag(vehicle.get("image_left_path", ""), "Left")
        image_tags += get_image_tag(vehicle.get("image_right_path", ""), "Right")

        # HTML template with dynamic values
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Insurance Policy Application</title>
          <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; color: #333; }}
            .header {{ background-color: #444; color: white; padding: 20px; text-align: left; font-size: 22px; font-weight: bold; }}
            .sub-header {{ margin-top: 10px; font-size: 14px; }}
            .container {{ background-color: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h2 {{ font-size: 16px; color: #555; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-top: 30px; }}
            .form-row {{ display: flex; flex-wrap: wrap; margin: 10px 0; }}
            .form-group {{ width: 45%; margin-right: 5%; margin-bottom: 15px; }}
            .form-group label {{ display: block; font-weight: bold; margin-bottom: 5px; }}
            .form-group input, .form-group textarea {{ width: 100%; padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; background-color: #f3f3f3; }}
            .form-group textarea {{ resize: vertical; }}
            .full-width {{ width: 100%; }}
            .vehicle-images {{ margin-top: 20px; display: flex; gap: 20px; flex-wrap: wrap; }}
            .vehicle-images div {{ text-align: center; }}
            .footer {{ margin-top: 40px; font-size: 12px; color: #777; border-top: 1px solid #ccc; padding-top: 10px; text-align: center; }}
          </style>
        </head>
        <body>
          <div class="header">
            Insurance Policy Application
          </div>
          <div class="container">
            <p>Dear Insurance Team,</p>
            <p>I would like to register my vehicle insurance policy. Below is my personal, policy, and vehicle information for your records.</p>
            <h2>Personal Information</h2>
            <div class="form-row">
              <div class="form-group">
                <label>Policy Holder Name</label>
                <input type="text" value="{personal.get('policy_holder','')}" readonly>
              </div>
              <div class="form-group">
                <label>Date of Birth</label>
                <input type="text" value="{personal.get('dateofbirth','')}" readonly>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Email</label>
                <input type="email" value="{personal.get('email','')}" readonly>
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input type="text" value="{personal.get('phone','')}" readonly>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group full-width">
                <label>Address</label>
                <textarea rows="2" readonly>{personal.get('address','')}</textarea>
              </div>
            </div>
            <h2>Policy Information</h2>
            <div class="form-row">
              <div class="form-group">
                <label>Policy Start Date</label>
                <input type="text" value="{policy.get('start_date','')}" readonly>
              </div>
              <div class="form-group">
                <label>Policy End Date</label>
                <input type="text" value="{policy.get('end_date','')}" readonly>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Premium Amount</label>
                <input type="text" value="₹{policy.get('premium','')}" readonly>
              </div>
              <div class="form-group">
                <label>Status</label>
                <input type="text" value="{policy.get('status','').capitalize()}" readonly>
              </div>
            </div>
            <h2>Vehicle Information</h2>
            <div class="form-row">
              <div class="form-group">
                <label>Make</label>
                <input type="text" value="{vehicle.get('make','')}" readonly>
              </div>
              <div class="form-group">
                <label>Model</label>
                <input type="text" value="{vehicle.get('model','')}" readonly>
              </div>
              <div class="form-group">
                <label>Type of Vehicle</label>
                <input type="text" value="{vehicle.get('typeofvehicle','')}" readonly>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Year of Purchase</label>
                <input type="text" value="{vehicle.get('year_of_purchase','')}" readonly>
              </div>
              <div class="form-group full-width">
                <label>Damage Report</label>
                <textarea rows="2" readonly>{vehicle.get('damages','')}</textarea>
              </div>
            </div>
            <div class="vehicle-images">
              {image_tags}
            </div>
            <div class="form-row">
              <div class="form-group full-width">
                <label>Submission Date</label>
                <input type="text" value="{today}" readonly>
              </div>
            </div>
            <p>Thank you for considering my application. I look forward to your positive response.</p>
            <p>Best regards,<br>{personal.get('policy_holder','')}</p>
          </div>
          <div class="footer">
            &copy; {today.split('-')[0]} Insurance Company. All rights reserved.
          </div>
        </body>
        </html>
        """

        components.html(html, height=800, scrolling=True)

        # File download button
        from helpers.file_handlers import Transform

        pdf_buffer = Transform().html_to_pdf(html)
        if isinstance(pdf_buffer, str):
            st.error(pdf_buffer)
        else:
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="insurance_policy_application.pdf",
                mime="application/pdf",
            )

        # Submit button
        submit = st.button("Submit Application")
        if submit:
            # Save policy and vehicle details to DB
            policy_obj = Policy()
            vehicle_obj = Vehicle()
            # Add policy with user_id as foreign key
            policy_obj.add(
                policy_holder=personal.get("policy_holder"),
                start_date=policy.get("start_date"),
                end_date=policy.get("end_date"),
                premium=policy.get("premium"),
                status=policy.get("status"),
                typeofvehicle=vehicle.get("typeofvehicle"),
                user_id=st.session_state.get("user_id"),  # Pass user_id
            )

            policy_id = policy_obj.get_id()  # Get the last inserted policy ID
            # Add vehicle
            vehicle_obj.add(
                policy_id=policy_id,
                typeofvehicle=vehicle.get("typeofvehicle"),
                image_path=vehicle.get("image_main_folder"),
                make=vehicle.get("make"),
                model=vehicle.get("model"),
                year_of_purchase=vehicle.get("year_of_purchase"),
            )
            st.success("Application submitted successfully!")
            time.sleep(2)
            clear_policy_session_state()
            st.session_state.page = "Home"
            st.session_state.add_policy_step = 1
            st.session_state.active_tab = 1
            st.rerun()

    else:
        st.info("Please complete Vehicle Info first.")

def new_policy_page():
    st.title("Add New Insurance Policy")
    st.markdown("Please complete all steps to add a new policy. Fields marked * are required.")

    # --- State Initialization ---
    if "add_policy_step" not in st.session_state:
        st.session_state.add_policy_step = 1
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 1
    if "personal_info" not in st.session_state:
        st.session_state.personal_info = {}
    if "policy_info" not in st.session_state:
        st.session_state.policy_info = {}
    if "vehicle_info" not in st.session_state:
        st.session_state.vehicle_info = {}

    tabs = st.tabs(["Personal Info", "Policy Info", "Vehicle Info", "Summary"])

    # Autofill personal info if user is logged in and not already filled
    user_id = st.session_state.get('user_id')
    if user_id and not st.session_state.personal_info:
        
        user_obj = User()
        user = user_obj.get_by_id(user_id)
        if user:
            st.session_state.personal_info = {
                "policy_holder": f"{user[3]} {user[4] or ''} {user[5]}".strip(),
                "dateofbirth": user[7],  # You can calculate from dateofbirth if needed
                "email": user[9],
                "phone": user[8],
                "address": user[10],
            }

    # --- Personal Info Tab ---
    with tabs[0]:
        personal_info_autofill()
        
    # --- Policy Info Tab ---
    with tabs[1]:
        policy_info_tab()

    # --- Vehicle Info Tab ---
    with tabs[2]:
        vehicle_info_tab()

    # --- Summary Tab ---
    with tabs[3]:
        summary_tab()  
   
if __name__ == "__main__":
  new_policy_page()