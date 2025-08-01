# FNOL (First Notice of Loss)

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

- **Flexible User Update**
  Users can update any subset of their profile data. The backend supports partial updates using optional Pydantic fields. For example, you can update just the username via:

  ``` python
  { "username": "new_username" }
  ```

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
│   ├── main.py
│   │                          # FastAPI entry point
│   ├── AI_ML/
│   │   ├── agents.py                # AI agents (Gemini or others)
│   │   └── damage_predictor.py      # ML model prediction logic
│   │  
│   ├── database/
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── model.py           # ORM models
│   │   └── tables.py          # SQLite table helpers
|   |
│   ├── helpers/
│   │   ├── agents.py          # Gemini AI integration
│   │   ├── config.py          # Configs and paths
│   │   ├── file_handlers.py   # Image/file utilities
│   │   └── prompts.py  
│   │
│   ├── routers/
│   │   ├── auth.py                  # Auth-related endpoints
│   │   ├── claims.py                # Claim submission/review
│   │   ├── llmRoute.py              # AI routes (Gemini/ML)
│   │   ├── policy.py                # Policy endpoints
│   │   ├── user.py                  # User registration/login
│   │   └── vehicle.py               # Vehicle info endpoints
│   │
│   └── screens/
│       ├── home.py
│       ├── login.py
│       ├── policies.py
│       ├── profile.py
│       └── registration.py         # Registration page    
│
├── vehicle_images_test/       # Test images
├── damage/                    # Damage images
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Database Schemas



## Users Schema Table:  
| Column Name       | Data Type | Nullable | Primary Key | Unique | Default  | Constraints                     |
| ----------------- | --------- | -------- | ----------- | ------ | -------- | ------------------------------- |
| `user_id`         | INTEGER   | No       | Yes         | No     | –        | AUTOINCREMENT                   |
| `usertype`        | TEXT      | No       | No          | No     | `'user'` | `IN ('user', 'agent', 'admin')` |
| `username`        | TEXT      | No       | No          | Yes    | –        |                                 |
| `firstname`       | TEXT      | No       | No          | No     | –        |                                 |
| `middlename`      | TEXT      | Yes      | No          | No     | –        |                                 |
| `lastname`        | TEXT      | No       | No          | No     | –        |                                 |
| `hashed_password` | TEXT      | No       | No          | No     | –        |                                 |
| `dateofbirth`     | DATETIME  | No       | No          | No     | –        |                                 |
| `phone`           | TEXT      | Yes      | No          | No     | –        |                                 |
| `email`           | TEXT      | No       | No          | Yes    | –        |                                 |
| `address`         | TEXT      | Yes      | No          | No     | –        |                                 |



## Policies Schema Table: 
| Column Name              | Data Type | Nullable | Primary Key | Unique | Default | Constraints                             |
| ------------------------ | --------- | -------- | ----------- | ------ | ------- | --------------------------------------- |
| `policy_id`              | INTEGER   | No       | Yes         | No     | –       | AUTOINCREMENT                           |
| `policy_number`          | TEXT      | No       | No          | Yes    | –       |                                         |
| `policy_holder`          | TEXT      | No       | No          | No     | –       |                                         |
| `user_id`                | INTEGER   | Yes      | No          | No     | –       | FK → users.user\_id (ON DELETE CASCADE) |
| `start_date`             | TEXT      | No       | No          | No     | –       |                                         |
| `end_date`               | TEXT      | No       | No          | No     | –       |                                         |
| `premium`                | REAL      | No       | No          | No     | –       |                                         |
| `total_claimable_amount` | REAL      | No       | No          | No     | –       |                                         |
| `status`                 | TEXT      | No       | No          | No     | –       | `IN ('active', 'inactive', 'expired')`  |



## vehicles Schema Table: 
| Column Name        | Data Type | Nullable | Primary Key | Unique | Default | Constraints                                  |
| ------------------ | --------- | -------- | ----------- | ------ | ------- | -------------------------------------------- |
| `vehicle_id`       | INTEGER   | No       | Yes         | No     | –       | AUTOINCREMENT                                |
| `policy_id`        | INTEGER   | No       | No          | No     | –       | FK → policies.policy\_id (ON DELETE CASCADE) |
| `typeofvehicle`    | TEXT      | No       | No          | No     | –       |                                              |
| `image_path`       | TEXT      | Yes      | No          | No     | –       |                                              |
| `make`             | TEXT      | No       | No          | No     | –       |                                              |
| `model`            | TEXT      | No       | No          | No     | –       |                                              |
| `year_of_purchase` | INTEGER   | No       | No          | No     | –       |                                              |
| `chasis_no`        | TEXT      | No       | No          | No     | –       |                                              |
| `vehicle_no`       | TEXT      | No       | No          | No     | –       |                                              |
| `damage_report`    | TEXT      | Yes      | No          | No     | –       |                                              |


## Claims Schema Table:

| Column Name            | Data Type | Nullable | Primary Key | Foreign Key           | Extra Constraint                       |
| ---------------------- | --------- | -------- | ----------- | --------------------- | -------------------------------------- |
| `claim_id`             | INTEGER   | No       | Yes         | –                     | AUTOINCREMENT                          |
| `policy_id`            | INTEGER   | No       | No          | `policies.policy_id`  | –                                      |
| `vehicle_id`           | INTEGER   | No       | No          | `vehicles.vehicle_id` | –                                      |
| `claim_number`         | TEXT      | No       | No          | –                     | UNIQUE                                 |
| `damage_description_user`   | TEXT      | No       | No          | –                     | –                                      |
| `damage_description_llm`   | TEXT      | No       | No          | –                     | –  
| `severity_level`   | TEXT      | No       | No          | –                     | `IN ('Low', 'Moderate', 'High', 'Critical')`
| `damage_percentage`    | REAL      | No       | No          | –                     | –                                      |
| `damage_image_path`    | TEXT      | Yes      | No          | –                     | –                                      |
| `date_of_incident`     | DATETIME  | No       | No          | –                     | –                                      |
| `location_of_incident` | TEXT      | No       | No          | –                     | –                                      |
| `fir_no`               | TEXT      | Yes      | No          | –                     | –                                      |
| `claim_date`           | DATETIME  | Yes      | No          | –                     | –                                      |
| `requested_amount`     | REAL      | No       | No          | –                     | –                                      |
| `approvable_amount`      | REAL      | Yes      | No          | –                     | –                                      |
| `claim_status`         | TEXT      | No       | No          | –                     | `IN ('active', 'inactive', 'expired')` |





---

## Flowchart

See [`flow.mmd`](flow.mmd) for the full Mermaid flowchart.

![Flowchart](src/flowchart.png)

---

## How to Run

1. **Clone the repository**
    ```sh
    git clone <repo-url>
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
    uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
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

NONE

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini AI](https://ai.google.dev/gemini-api/docs)