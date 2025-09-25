# FNOL (First Notice of Loss)

This project is a **First Notice of Loss (FNOL)** web application built with [Streamlit](https://streamlit.io/) and [FastAPI](https://fastapi.tiangolo.com/). It allows users to register, log in, and submit vehicle insurance claims by uploading vehicle images and entering policy details. The app uses AI (Gemini) to verify vehicle images and extract details.

---

## Features

### Core Functionality
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

### AI-Powered Features
- **Vehicle Image Verification**  
  Users are prompted to upload images of their vehicle from four angles: front, back, left, and right. The app leverages Gemini AI to analyze these images, extract vehicle details (make, model, year, type), and generate a damage report. This automated verification helps prevent fraud and ensures that the submitted details match the actual vehicle.

- **Damage Report Generation**  
  After image verification, the AI generates a detailed damage report based on the uploaded photos. This report is included in the summary and stored with the claim, providing insurers with immediate, objective evidence of the vehicle's condition at the time of claim.

- **OCR Document Processing**  
  The system includes OCR capabilities using pytesseract to extract text from images and documents, supporting various file formats including PDF, DOCX, and image files. [to be integrated]

### Claims Management
- **Complete Claims Lifecycle**  
  Full claims management system with status tracking (in-review, accepted, rejected), damage assessment, and approval workflows.

- **Document & Image Upload**  
  Support for uploading multiple claim images and supporting documents with organized file storage.

- **Insurable Assets Management**  
  Track and manage insurable assets linked to policies with comprehensive asset information.

### Technical Features
- **Database Integration**  
  All user, policy, vehicle, and claims data is stored in a robust SQLite database. This ensures data persistence, easy querying, and future scalability. The schema is designed to link users, policies, vehicles, and claims efficiently.

- **Role-Based Access Control (RBAC)**  
  Comprehensive RBAC system with three user types:
  - **Users:** Can manage their own policies and claims
  - **Agents:** Can view and manage multiple user accounts
  - **Admins:** Full system access with user management capabilities

- **RESTful API Architecture**  
  Complete FastAPI backend with endpoints for:
  - User management and authentication
  - Policy creation and management
  - Vehicle registration and verification
  - Claims processing and tracking
  - Asset management
  - File upload and retrieval

- **Modern, User-friendly Interface**  
  Built with Streamlit, the app provides a clean, responsive, and interactive web interface. Users are guided through each step, receive instant feedback, and can view summaries before submission.

- **Secure & Configurable**  
  Sensitive operations (like login and registration) are handled securely with JWT tokens and bcrypt password hashing. Configuration files allow for easy updates to paths, API keys, and database locations.

- **Flexible User Update**  
  Users can update any subset of their profile data. The backend supports partial updates using optional Pydantic fields. For example, you can update just the username via:

  ``` python
  { "username": "new_username" }
  ```

- **PDF Generation**  
  Automatic PDF generation of policy applications using HTML-to-PDF conversion with wkhtmltopdf.

- **File Processing Capabilities**  
  Support for multiple file formats including MSG, PDF, DOCX, and various image formats with text extraction capabilities.

---

## API Endpoints

### Authentication
- `POST /auth/token` - User login with JWT token generation
- `GET /auth/me` - Get current user information
- `POST /auth/logout` - User logout (clears cookies)

### User Management
- `GET /users/user_details` - Get user details (RBAC applied)
- `GET /users/user_details/{user_id}` - Get specific user by ID
- `GET /users/user_names` - Get all usernames (privileged users only)
- `POST /users/input_user_details` - Create new user
- `PUT /users/update_details` - Update user profile
- `PUT /users/update_user_details/{user_id}` - Admin update user
- `PUT /users/update_user_admin` - Admin update user with admin privileges
- `DELETE /users/user_details/{user_id}` - Delete user
- `GET /users/check_username/{username}` - Check username availability
- `GET /users/check_email/{email}` - Check email availability
- `GET /users/check_phone/{phone}` - Check phone number availability
- `POST /users/upload_pic` - Upload profile picture
- `GET /users/get_profile_pic/{user_id}` - Get user profile picture
- `POST /users/acknowledgement` - Create acknowledgement

### Policy Management
- `GET /policies/policy_details_all` - Get all policies list (RBAC applied)
- `GET /policies/policy_details` - Get specific policy by ID or number
- `GET /policies/policy_details/{policy_id}` - Get detailed policy information
- `GET /policies/policy_numbers/{user_id}` - Get policy numbers for user
- `POST /policies/policy_details` - Create new policy
- `PUT /policies/policy_details/{policy_id}` - Update policy
- `DELETE /policies/policy_details/{policy_id}` - Delete policy

### Vehicle Management
- `GET /vehicles/vehicle_details` - Get vehicles (RBAC applied)
- `GET /vehicles/vehicle_details/{vehicle_id}` - Get specific vehicle
- `POST /vehicles/vehicle_details` - Create vehicle record
- `PUT /vehicles/vehicle_details/{vehicle_id}` - Update vehicle
- `DELETE /vehicles/vehicle_details/{vehicle_id}` - Delete vehicle
- `POST /vehicles/upload_vehicle_images` - Upload vehicle images

### Claims Management
- `GET /claims/claim_details` - Get claims (RBAC applied)
- `GET /claims/claim_details/{claim_id}` - Get specific claim
- `POST /claims/claim_details` - Create new claim
- `PUT /claims/claim_details/{claim_id}` - Update claim
- `DELETE /claims/claim_details/{claim_id}` - Delete claim
- `POST /claims/upload_claim_images` - Upload claim images
- `POST /claims/upload_documents` - Upload claim documents
- `GET /claims/files` - Retrieve claim files

### Insurable Assets
- `GET /insurables/assets` - Get insurable assets (RBAC applied)
- `GET /insurables/get_id` - Get asset IDs by policy

### AI/ML Services
- `POST /llm/extract_vehicle_details` - Extract vehicle details from images
- `POST /llm/claim_validation` - Validate claims with damage assessment

---

## Folder Structure

```
challenge/
│
├── data/
│   ├── claims/                # Claim documents and images
│   ├── images/                # Uploaded vehicle images
│   │   ├── fourwheeler/
│   │   ├── threewheeler/
│   │   ├── twowheeler/
│   │   └── other/
│   ├── trail/                 # Test images
│   └── user/
│       ├── profile_pics/      # User profile pictures
│       └── policy.db          # SQLite database
│
├── src/
│   ├── app.py                 # Streamlit entry point
│   ├── main.py                # FastAPI entry point
│   │                          
│   ├── AI_ML/
│   │   ├── agents.py          # AI agents (Gemini integration)
│   │   └── damage_predictor.py # ML model prediction logic
│   │  
│   ├── database/
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── model.py           # ORM models
│   │   └── tables.py          # SQLite table helpers
│   │
│   ├── helpers/
│   │   ├── config.py          # Configuration and paths
│   │   ├── file_handlers.py   # File processing utilities
│   │   └── prompts.py         # AI prompts
│   │
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── claims.py          # Claims management endpoints
│   │   ├── insurables.py      # Insurable assets endpoints
│   │   ├── llmRoute.py        # AI/ML service endpoints
│   │   ├── policy.py          # Policy management endpoints
│   │   ├── user.py            # User management endpoints
│   │   └── vehicle.py         # Vehicle management endpoints
│   │
│   └── screens/
│       ├── home.py            # Home page
│       ├── login.py           # Login interface
│       ├── policies.py        # Policy management UI
│       ├── profile.py         # User profile management
│       └── registration.py    # User registration
│
├── vehicle_images_test/       # Test vehicle images
├── damage/                    # Damage assessment images
├── .env                       # Environment variables
├── .gitignore
├── requirements.txt           # Python dependencies
└── README.md
```

---

## Database Schemas

### Users Table
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

### Policies Table
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

### Vehicles Table
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

### Claims Table
| Column Name               | Data Type | Nullable | Primary Key | Foreign Key           | Extra Constraint                           |
| ------------------------- | --------- | -------- | ----------- | --------------------- | ------------------------------------------ |
| `claim_id`                | INTEGER   | No       | Yes         | –                     | AUTOINCREMENT                              |
| `policy_id`               | INTEGER   | No       | No          | `policies.policy_id`  | –                                          |
| `subject_id`              | INTEGER   | No       | No          | `insurables.id`       | –                                          |
| `claim_number`            | TEXT      | No       | No          | –                     | UNIQUE                                     |
| `damage_description_user` | TEXT      | No       | No          | –                     | –                                          |
| `damage_description_llm`  | TEXT      | No       | No          | –                     | –                                          |
| `severity_level`          | TEXT      | No       | No          | –                     | `IN ('Low', 'Moderate', 'High', 'Critical')` |
| `damage_percentage`       | REAL      | No       | No          | –                     | –                                          |
| `damage_image_path`       | TEXT      | Yes      | No          | –                     | –                                          |
| `date_of_incident`        | DATETIME  | No       | No          | –                     | –                                          |
| `location_of_incident`    | TEXT      | No       | No          | –                     | –                                          |
| `documents_path`          | TEXT      | Yes      | No          | –                     | –                                          |
| `fir_no`                  | TEXT      | Yes      | No          | –                     | –                                          |
| `claim_date`              | DATETIME  | Yes      | No          | –                     | –                                          |
| `remarks`                 | TEXT      | Yes      | No          | –                     | –                                          |
| `approvable_reason`       | TEXT      | Yes      | No          | –                     | –                                          |
| `requested_amount`        | REAL      | No       | No          | –                     | –                                          |
| `approvable_amount`       | REAL      | Yes      | No          | –                     | –                                          |
| `claim_status`            | TEXT      | No       | No          | –                     | `IN ('in-review', 'accepted', 'rejected')` |

### Insurables Table
| Column Name     | Data Type | Nullable | Primary Key | Foreign Key          | Extra Constraint |
| --------------- | --------- | -------- | ----------- | -------------------- | ---------------- |
| `id`            | INTEGER   | No       | Yes         | –                    | AUTOINCREMENT    |
| `policy_id`     | INTEGER   | No       | No          | `policies.policy_id` | –                |
| `type`          | TEXT      | No       | No          | –                    | –                |
| `policy_number` | TEXT      | No       | No          | –                    | –                |

---

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Gemini AI API Keys
gemini_API1=your_gemini_api_key_1
gemini_API2=your_gemini_api_key_2
gemini_API3=your_gemini_api_key_3
gemini_API4=your_gemini_api_key_4
gemini_API5=your_gemini_api_key_5
gemini_API6=your_gemini_api_key_6

# Admin Credentials
admin_username=admin
admin_password=admin123

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# File Paths
tesseract=path_to_tesseract_executable
wkhtlm=path_to_wkhtmltopdf_executable

# Database
DATABASE_URL=sqlite:///./data/user/policy.db
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Tesseract OCR
- wkhtmltopdf

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd challenge
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies**
   
   **For Windows:**
   - Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - Download and install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)
   
   **For Linux:**
   ```bash
   sudo apt-get install tesseract-ocr wkhtmltopdf
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the values with your API keys and system paths

5. **Initialize the database**
   ```bash
   cd src
   python main.py
   ```

6. **Run the applications**
   
   **Streamlit Frontend:**
   ```bash
   streamlit run src/app.py
   ```
   
   **FastAPI Backend:**
   ```bash
   uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
   ```

---

## Usage

### For End Users
1. Register as a new user or log in with existing credentials
2. Navigate to the Policies section
3. Fill in personal, policy, and vehicle details
4. Upload vehicle images (front, back, left, right)
5. Review the AI-generated damage report and summary
6. Submit your policy application
7. Track claims and manage your insurable assets

### For Agents/Admins
1. Log in with privileged credentials
2. Access user management features
3. Review and approve policy applications
4. Manage claims and process approvals
5. Generate reports and analytics

---

## API Documentation

Once the FastAPI server is running, visit:
- **Interactive API Docs:** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

---

## Security Features

- **JWT Authentication:** Secure token-based authentication
- **Password Hashing:** Bcrypt encryption for user passwords
- **Role-Based Access Control:** Three-tier user permission system
- **Input Validation:** Pydantic models for request/response validation
- **CORS Protection:** Configurable cross-origin resource sharing
- **SQL Injection Prevention:** SQLAlchemy ORM protection

---

## AI Integration

### Gemini AI Services
- **Vehicle Verification:** Automated vehicle detail extraction from images
- **Damage Assessment:** AI-powered damage analysis and reporting
- **OCR Processing:** Text extraction from documents and images

### Supported File Formats
- **Images:** PNG, JPG, JPEG, BMP, TIFF
- **Documents:** PDF, DOCX, MSG
- **Processing:** Text extraction, damage analysis, vehicle verification

---

## Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Ensure Tesseract is installed and path is set in `.env`

2. **wkhtmltopdf errors**
   - Install wkhtmltopdf and update path in configuration

3. **Database connection issues**
   - Check database file permissions
   - Ensure SQLite is properly installed

4. **API key errors**
   - Verify Gemini API keys are valid and active
   - Check rate limits and quotas

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend API framework
- [Google Gemini AI](https://ai.google.dev/gemini-api/docs) - AI services
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation