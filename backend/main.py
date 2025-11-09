import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import SessionLocal, init_db, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz_payload


app = FastAPI(title="AI Wiki Quiz Generator", version="1.0")

origins_env = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow frontend hosted anywhere
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
        title, summary, sections, key_entities, cleaned_text = scrape_wikipedia(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scrape failed: {e}")

    try:
        quiz_dict = generate_quiz_payload(
            title=title,
            summary=summary,
            sections=sections,
            key_entities=key_entities,
            article_text=cleaned_text,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    session = SessionLocal()
    try:
        record = Quiz(
            url=req.url,
            title=title,
            scraped_content=cleaned_text,
            full_quiz_data=json.dumps(quiz_dict, ensure_ascii=False),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
    finally:
        session.close()

    return quiz_dict

@app.get("/history")
def history():
    """Return history items including the saved quiz payload for each record.

    Each item will include: id, url, title, summary, key_entities (dict),
    sections (list), quiz (list of questions) and related_topics.
    """
    session = SessionLocal()
    try:
        rows = session.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        result = []
        for r in rows:
            try:
                payload = json.loads(r.full_quiz_data)
            except Exception:
                payload = {}

            # Normalize fields, prefer values from payload when available
            summary = payload.get("summary") or payload.get("summary_text") or ""
            key_entities = payload.get("key_entities") or payload.get("keyEntities") or {}
            sections = payload.get("sections") or []
            quiz_list = payload.get("quiz") or payload.get("questions") or []
            related = payload.get("related_topics") or payload.get("relatedTopics") or payload.get("related") or []

            # compute epoch ms for easier client-side rendering
            date_ms = None
            if getattr(r, "date_generated", None) is not None:
                try:
                    date_ms = int(r.date_generated.timestamp() * 1000)
                except Exception:
                    date_ms = None

            result.append({
                "id": r.id,
                "url": r.url,
                "title": payload.get("title", r.title),
                "summary": summary,
                "key_entities": key_entities,
                "sections": sections,
                "quiz": quiz_list,
                "related_topics": related,
                # include timestamp so frontend can show when the quiz was generated
                "date_generated": (r.date_generated.isoformat() if getattr(r, 'date_generated', None) is not None else None),
                "date_generated_ms": date_ms,
            })

        return result
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
