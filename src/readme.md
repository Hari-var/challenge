# FNOL (First Notice of Loss) Streamlit App

This project is a **First Notice of Loss (FNOL)** web application built with [Streamlit](https://streamlit.io/) and [FastAPI](https://fastapi.tiangolo.com/). It allows users to register, log in, and submit vehicle insurance claims by uploading vehicle images and entering policy details. The app uses AI (Gemini) to verify vehicle images and extract details.

---

## Features

- **User Registration & Login**  
  Users can securely create an account and log in with their credentials. The system supports different user roles (user, agent, admin), allowing for role-based access and future extensibility. Registration ensures that only authorized users can submit claims, and login sessions are managed securely.

- **Personal Info Autofill**  
  When a user logs in, their personal details (such as name, date of birth, email, phone, and address) are automatically fetched from the database and pre-filled in the claim form. This reduces manual entry, minimizes errors, and speeds up the claim process.

- **Multi-step Policy Creation**  
  The claim submission process is broken down into clear, guided steps:
  - **Personal Info:** Review and confirm your personal details.
  - **Policy Info:** Enter or review policy-specific information such as policy period, premium, and status.
  - **Vehicle Info:** Provide vehicle details and upload required images.
  - **Summary & Submission:** Review all entered information, including a damage report, before final submission. This step-by-step approach ensures completeness and clarity for both users and insurers.

- **Vehicle Image Verification**  
  Users are prompted to upload images of their vehicle from four angles: front, back, left, and right. The app leverages Gemini AI to analyze these images, extract vehicle details (make, model, year, type), and generate a damage report. This automated verification helps prevent fraud and ensures that the submitted details match the actual vehicle.

- **Damage Report Generation**  
  After image verification, the AI generates a detailed damage report based on the uploaded photos. This report is included in the summary and stored with the claim, providing insurers with immediate, objective evidence of the vehicle's condition at the time of claim.

- **Database Integration**  
  All user, policy, and vehicle data is stored in a robust SQLite database. This ensures data persistence, easy querying, and future scalability. The schema is designed to link users, policies, and vehicles efficiently, supporting both individual and organizational workflows.

- **Admin/Agent Support**  
  The system is designed to be extendable for admin and agent dashboards. Admins and agents can be given special access to review, approve, or manage claims, making the platform suitable for real-world insurance operations.

- **Modern, User-friendly Interface**  
  Built with Streamlit, the app provides a clean, responsive, and interactive web interface. Users are guided through each step, receive instant feedback, and can view summaries before submission.

- **Secure & Configurable**  
  Sensitive operations (like login and registration) are handled securely. Configuration files allow for easy updates to paths, API keys, and database locations.

---

## Folder Structure

```
challenge/
│
├── data/
│   ├── images/                # Uploaded vehicle images
│   └── user/
│       └── policy.db          # SQLite database
│
├── src/
│   ├── app.py                 # Streamlit entry point
│   ├── main.py                # FastAPI entry point
│   ├── database/
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── model.py           # ORM models
│   │   └── tables.py          # SQLite table helpers
│   ├── helpers/
│   │   ├── agents.py          # Gemini AI integration
│   │   ├── config.py          # Configs and paths
│   │   └── file_handlers.py   # Image/file utilities
│   └── screens/
│       ├── login.py           # Login page
│       ├── policies.py        # Policy creation workflow
│       └── registration.py    # Registration page
│
├── vehicle_images_test/       # Test images
└── README.md
```

---

## Database Schema

```
--------------------------------------------------------
Schema for table: users
(0, 'user_id', 'INTEGER', 0, None, 1)
(1, 'usertype', 'TEXT', 1, "'user'", 0)
(2, 'username', 'TEXT', 1, None, 0)
(3, 'firstname', 'TEXT', 1, None, 0)
(4, 'middlename', 'TEXT', 0, None, 0)
(5, 'lastname', 'TEXT', 1, None, 0)
(6, 'password', 'TEXT', 1, None, 0)
(7, 'dateofbirth', 'Date', 0, None, 0)
(8, 'phone', 'TEXT', 0, None, 0)
(9, 'email', 'TEXT', 1, None, 0)
(10, 'address', 'TEXT', 0, None, 0)

--------------------------------------------------------
Schema for table: policies
(0, 'policy_id', 'INTEGER', 0, None, 1)
(1, 'policy_number', 'TEXT', 1, None, 0)
(2, 'policy_holder', 'TEXT', 1, None, 0)
(3, 'user_id', 'INTEGER', 0, None, 0)
(4, 'start_date', 'TEXT', 1, None, 0)
(5, 'end_date', 'TEXT', 1, None, 0)
(6, 'premium', 'REAL', 1, None, 0)
(7, 'status', 'TEXT', 1, None, 0)

--------------------------------------------------------
Schema for table: vehicles
(0, 'vehicle_id', 'INTEGER', 0, None, 1)
(1, 'policy_id', 'INTEGER', 1, None, 0)
(2, 'typeofvehicle', 'TEXT', 1, None, 0)
(3, 'image_path', 'TEXT', 0, None, 0)
(4, 'make', 'TEXT', 1, None, 0)
(5, 'model', 'TEXT', 1, None, 0)
(6, 'year_of_purchase', 'INTEGER', 1, None, 0)
(7, 'damage_report', 'TEXT', 0, None, 0)
--------------------------------------------------------
```

---

## Flowchart

See [`src/flow.mmd`](src/flow.mmd) for the full Mermaid flowchart.

![Flowchart](src/flowchart.png)

---

## How to Run

1. **Clone the repository**
    ```sh
    git clone <your-repo-url>
    cd challenge
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**
    - Set your Gemini API key:
      ```sh
      export gemini_API6=your_gemini_api_key
      ```
      Or set it in your system environment variables.

4. **Run the Streamlit app**
    ```sh
    streamlit run src/app.py
    ```

5. **(Optional) Run the FastAPI backend**
    ```sh
    uvicorn src.main:app --reload
    ```

---

## Usage

- Register as a new user or log in.
- Fill in your personal, policy, and vehicle details.
- Upload vehicle images (front, back, left, right).
- The app verifies your vehicle using AI and shows a summary.
- Submit your application.

---

## Customization

- **AI Model:**  
  The Gemini AI logic is in `src/helpers/agents.py`. You can swap or extend this for other models.

- **Database:**  
  The schema is defined in `src/database/model.py` and `src/database/tables.py`.

- **UI:**  
  Modify `src/screens/policies.py` and `src/screens/form3.html` for custom forms and summary layouts.

---

## License

MIT License

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini AI](https://ai.google.dev/gemini-api/docs)