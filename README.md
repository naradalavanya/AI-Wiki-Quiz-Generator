# AI Wiki Quiz Generator

Python **FastAPI** backend + **LangChain + Gemini** + **BeautifulSoup** + **SQLAlchemy (PostgreSQL)** and **React + Tailwind** frontend.

## Run

### Backend (Windows-friendly)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
# Edit .env (GEMINI_API_KEY & DATABASE_URL)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```powershell
cd frontend
npm i
# echo VITE_API_BASE_URL=http://localhost:8000 > .env
npm run dev
```

Open http://localhost:5173
