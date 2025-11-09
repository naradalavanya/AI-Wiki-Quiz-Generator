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
DATABASE_URL=database_URL
MODEL_NAME=gemini-1.5-flash
CORS_ORIGINS=http://localhost:5173
```

### 4) Start backend (development)

Run from the repository root (recommended):

```powershell
uvicorn backend.main:app --reload
```

> Note: running `uvicorn main:app` from inside `backend/` can cause relative import errors. Use the repo-root command above.

### 5) Frontend: install & run

```powershell
cd frontend
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





Deployment Link: https://aiwikiquizgenerator22.netlify.app/
