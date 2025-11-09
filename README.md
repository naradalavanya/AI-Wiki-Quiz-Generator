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
uvicorn main:app --reload 
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```


