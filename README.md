# AI Wiki Quiz Generator

This repository contains a small web application that scrapes Wikipedia articles, uses a generative LLM to produce multiple-choice quizzes, and stores generated quizzes in a database. It includes:

- `backend/` — FastAPI app (Python) with scraping, LLM integration, and storage.
- `frontend/` — React + Tailwind UI for generating quizzes and viewing history.

This README explains local setup, API endpoints, testing commands, and troubleshooting tips.

---

## Quick start (Windows / PowerShell)

Prerequisites
- Python 3.10+ (3.12 tested)
- Node.js 16+ & npm
- PostgreSQL (or change `DATABASE_URL` to a local SQLite URL for quick testing)
- An API key for the model provider used by `langchain_google_genai` (set `GEMINI_API_KEY`)

### 1) Backend: create & activate venv

```powershell
cd C:\Users\HP\Downloads\ai-quiz-generator-full\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2) (Optional) Install spaCy model used for NER

```powershell
python -m spacy download en_core_web_sm
```

### 3) Configure environment

Edit `backend/.env` and set the required values:

```
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+psycopg2://quiz_user:QuizUser123@localhost:5432/ai_quiz_db
MODEL_NAME=gemini-1.5-flash
CORS_ORIGINS=http://localhost:5173
```

### 4) Initialize DB (creates tables)

```powershell
python -c "from database import init_db; init_db()"
```

### 5) Start backend (development)

Run from the repository root (recommended):

```powershell
uvicorn backend.main:app --reload
```

> Note: running `uvicorn main:app` from inside `backend/` can cause relative import errors. Use the repo-root command above.

### 6) Frontend: install & run

```powershell
cd C:\Users\HP\Downloads\ai-quiz-generator-full\frontend
npm install
npm run dev
```

Open the dev server shown (usually http://localhost:5173).

---

## HTTP API Endpoints

Base URL: http://127.0.0.1:8000 (when running locally)

- POST /generate_quiz
  - Request JSON: `{ "url": "https://en.wikipedia.org/wiki/Alan_Turing" }`
  - Response: JSON quiz payload. Expected fields (the frontend normalizes small variations):
    - `title`, `summary`, `key_entities` (dict or list), `sections` (list)
    - `quiz` or `questions`: array of question objects
    - `related_topics`: array of strings

- GET /history
  - Returns an array of stored quiz payloads (each item contains `id`, `url`, `title`, `summary`, `key_entities`, `sections`, `quiz`, `related_topics`). Example item:

```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Turing was a British mathematician and...",
  "key_entities": {
    "people": ["Alan Turing"],
    "organizations": ["Bletchley Park"],
    "locations": ["United Kingdom"]
  },
  "sections": ["Early life","World War II","Legacy"],
  "quiz": [ /* question objects */ ],
  "related_topics": ["Cryptography","Enigma machine"]
}
```

- GET /quiz/{id}
  - Returns the saved quiz payload JSON for the given id.

---

## Frontend behavior and debugging

- The frontend attempts to normalize incoming quiz payloads (handles `quiz` vs `questions`, `key_entities` as dict vs list).
- If the UI shows "No quiz returned from the server", open DevTools → Network and inspect the `/generate_quiz` response body and console logs.

---

## Example curl commands

Generate a quiz:

```bash
curl -X POST 'http://127.0.0.1:8000/generate_quiz' -H 'Content-Type: application/json' -d '{"url":"https://en.wikipedia.org/wiki/Alan_Turing"}'
```

Get history:

```bash
curl 'http://127.0.0.1:8000/history'
```

Get quiz by id:

```bash
curl 'http://127.0.0.1:8000/quiz/1'
```

---

## Troubleshooting

- Import errors when running uvicorn from inside `backend/`:
  - Run `uvicorn backend.main:app --reload` from repo root to ensure package-relative imports work.

- `ModuleNotFoundError: No module named 'fastapi'`:
  - Activate the backend venv and install requirements: `python -m pip install -r requirements.txt`.

- LLM model errors (404 / model not found):
  - Ensure `MODEL_NAME` in `backend/.env` is valid for your account and the API version. Check your provider console or call ListModels.

- Empty or invalid quiz JSON:
  - The backend tries to parse the LLM output and store it. If the parser fails or the LLM returns unexpected JSON, check backend logs (uvicorn) for the error and paste the raw output here for help.

---

## Development tips

- To temporarily log raw LLM responses, add a `print()` or use the logging module in `backend/llm_quiz_generator.py` around the `chain.invoke(...)` call.
- To change the model quickly for testing, edit `backend/.env` `MODEL_NAME` and restart uvicorn.

---

If you want, I can add a small Postman collection or automated smoke-tests. Tell me how you'd like the README adjusted (shorter, more beginner-friendly, or include screenshots) and I'll update it.
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


