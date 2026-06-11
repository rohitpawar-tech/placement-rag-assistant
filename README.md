
```markdown
# Placement Preparation RAG Assistant 🚀
An advanced Retrieval-Augmented Generation (RAG) platform designed to help students prepare for campus placements, technical interviews, and resume building.
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1-orange)](https://python.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
## 🌟 Features
*   **AI Chat Assistant:** Context-aware responses powered by Google Gemini and LangChain RAG.
*   **Document Management:** Upload PDFs, TXT, or DOCX files. The system automatically chunks, embeds, and indexes them using FAISS.

*   **Resume Analyzer:** ATS scoring, skill extraction, and improvement suggestions.
*   **Mock Interview System:** Generate HR and technical questions specific to target companies.
*   **Glassmorphism UI:** Modern, responsive frontend built with vanilla HTML/CSS and JavaScript.
*   **Production Ready:** Containerized with Docker and deployable on AWS or Render.

## 🛠 Tech Stack
**Backend:**
*   **Language:** Python
*   **Framework:** FastAPI
*   **AI Engine:** LangChain, Google Generative AI (Gemini)
*   **Vector Database:** FAISS
*   **Database:** PostgreSQL (Docker) / SQLite (Local)
*   **Auth:** JWT (JSON Web Tokens), Passlib
**Frontend:**
*   **Core:** HTML5, CSS3, Vanilla JavaScript
*   **Style:** Glassmorphism UI, Responsive Design
**DevOps:**
*   **Containerization:** Docker, Docker Compose
*   **Reverse Proxy:** Nginx
## 📸 Project Structure



```text
placement-rag-assistant/
├── backend/
│   ├── app/
│   │   ├── api/         # API Endpoints (Auth, Chat, Docs)
│   │   ├── core/        # Config, Database, Security
│   │   ├── models/      # SQLAlchemy Models
│   │   ├── services/    # RAG Logic, Resume Service
│   │   └── main.py      # Application Entry Point
│   ├── uploads/         # User Uploaded Documents
│   ├── vector_db/       # FAISS Indices
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Single Page App
│   └── assets/          # Images/Icons
├── docker-compose.yml
└── .env                 # Environment Variables
```
## 🚀 Installation & Setup

### Option 1: Docker (Recommended for Production)
This is the easiest way to run the full stack (Backend + Database) without dependency issues.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rohitpawar-tech/placement-rag-assistant.git
    cd placement-rag-assistant/backend
    ```
2.  **Create Environment Variables:**
    Create a file named `.env` in the `backend` folder with the following content:
    ```ini
    GOOGLE_API_KEY=your_google_gemini_api_key_here
    DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/placement_db
    SECRET_KEY=your-secret-key
    ```
    3.  **Update `.env` for SQLite:**
    ```ini
    DATABASE_URL=sqlite+aiosqlite:///./placement.db
    GOOGLE_API_KEY=your_google_gemini_api_key_here

3.  **Run Docker Compose:**
    ```bash
    docker-compose up --build
    ```
4.  **Access the Application:**
    *   Frontend: `http://localhost:5500`
    *   Backend API Docs: `http://localhost:8000/docs`
### Option 2: Local Development (Python)

If you prefer to run the backend directly on your machine:

1.  **Install Dependencies:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
    2.  **Fix Known Dependency Issues (Windows Only):**
    If you encounter errors related to `greenlet` or `bcrypt`, run these fixes:
    ```bash
    pip install "bcrypt<4.0.0"
    pip install aiosqlite
    ```
    


    ```

4.  **Create a User:**
    Run the user creation script to enable login:
    ```bash
    python -c "from app.core.database import SessionLocal; from app.models.models import User; from app.core.security import get_password_hash; db = SessionLocal(); u = User(full_name='Demo', email='demo@user.com', password_hash=get_password_hash('password')); db.add(u); db.commit(); print('User Created!'); db.close()"
    ```


