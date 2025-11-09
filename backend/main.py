import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import SessionLocal, init_db, Quiz
from backend.scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz_payload


app = FastAPI(title="AI Wiki Quiz Generator", version="1.0")

origins_env = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
init_db()

class GenerateQuizRequest(BaseModel):
    url: str

class HistoryItem(BaseModel):
    id: int
    url: str
    title: str
    date_generated: str

@app.post("/generate_quiz")
def generate_quiz(req: GenerateQuizRequest):
    try:
        title, cleaned_text = scrape_wikipedia(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scrape failed: {e}")

    try:
        quiz_dict = generate_quiz_payload(title=title, article_text=cleaned_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    session = SessionLocal()
    try:
        record = Quiz(
            url=req.url,
            title=quiz_dict.get("title", title) or title,
            scraped_content=cleaned_text,
            full_quiz_data=json.dumps(quiz_dict, ensure_ascii=False),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
    finally:
        session.close()

    return quiz_dict

@app.get("/history", response_model=List[HistoryItem])
def history():
    session = SessionLocal()
    try:
        rows = session.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        return [
            HistoryItem(
                id=r.id,
                url=r.url,
                title=r.title,
                date_generated=r.date_generated.isoformat(),
            )
            for r in rows
        ]
    finally:
        session.close()

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    session = SessionLocal()
    try:
        row = session.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Quiz not found")
        try:
            payload = json.loads(row.full_quiz_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Stored quiz JSON invalid: {e}")
        return payload
    finally:
        session.close()
