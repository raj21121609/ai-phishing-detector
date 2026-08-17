# PhishGuard AI

PhishGuard AI is an AI-powered email phishing detection web application. It analyzes email text, URLs, and sender information to provide a comprehensive phishing probability score and risk level explanation.

## Project Structure

- `frontend/`: React + Vite web interface.
- `backend/`: Django + Django REST Framework API.
- `ml/`: Machine learning models and training scripts.
- `docs/`: Project documentation.

## Tech Stack
- Frontend: React, Vite, Tailwind CSS, Axios, React Router
- Backend: Python, Django, DRF
- Database: PostgreSQL
- Machine Learning: scikit-learn, pandas, numpy, joblib

## Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy the `.env.example` file to `.env` inside the `backend` directory and configure the variables (ensure your PostgreSQL database is running).

5. **Run Migrations and Start Server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
