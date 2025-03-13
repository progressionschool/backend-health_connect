# Health Connect API

A FastAPI-based backend for Health Connect application that manages doctors, appointments, and user interactions.

## Features

- 🔐 **User Authentication**
  - Signup with email verification
  - JWT-based authentication
  - Secure password handling

- 👨‍⚕️ **Doctor Management**
  - List all doctors
  - Filter doctors by department
  - Detailed doctor profiles
  - Department-wise categorization

- 📅 **Appointment System**
  - Book appointments with doctors
  - View user appointments
  - Appointment history

- 📝 **Contact System**
  - Submit contact forms
  - Store and retrieve messages

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- SQLite Database

## API Endpoints

### Authentication
- POST `/auth/signup` - User registration
- POST `/auth/verify-email` - Email verification
- POST `/auth/login` - User login

### Doctors
- GET `/doctors` - Get all doctors
- GET `/doctors/{doctor_id}` - Get specific doctor
- GET `/doctors/deptt` - Get all departments
- GET `/doctors/deptt/{deptt_name}` - Get doctors by department
- POST `/doctors` - Create new doctor

### Users & Appointments
- GET `/users/{user_id}` - Get user details with appointments
- POST `/appointments` - Create new appointment

### Contact
- POST `/contact/get_in_touch` - Submit contact form
- GET `/contact/messages` - Get all messages

## Setup Instructions

### Using Traditional pip (Option 1)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/progressionschool/backend-health_connect.git
   cd backend-health_connect
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Using UV - Fast Python Package Installer (Option 2)

1. **Install UV**
   ```bash
   # Using pip
   pip install uv

   # Or using curl (Unix/MacOS)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/progressionschool/backend-health_connect.git
   cd backend-health_connect
   ```

3. **Create and Activate Virtual Environment with UV**
   ```bash
   uv venv
   source .venv/bin/activate  # Unix/MacOS
   # or
   .venv\Scripts\activate     # Windows
   ```

4. **Install Dependencies with UV**
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## API Security

- All endpoints (except login and signup) require JWT authentication
- Tokens must be included in the Authorization header
- Format: `Authorization: Bearer your_token_here`

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Why UV?

UV offers several advantages over traditional pip:

- 🚀 **Faster Installation**: Up to 10-100x faster than pip
- 🔒 **Reliable Builds**: Deterministic builds across different machines
- 💻 **Cross-Platform**: Works on Windows, macOS, and Linux
- 🔄 **Cache Optimization**: Smart caching for faster subsequent installs
- 🛡️ **Security**: Built-in security features and checks




