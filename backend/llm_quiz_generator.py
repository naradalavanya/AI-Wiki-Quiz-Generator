import os
from typing import Dict, List
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from models import QuizOutput

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")  # MUST match your Render model name
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")


llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0.5,
)

parser = JsonOutputParser(pydantic_object=QuizOutput)
format_instructions = parser.get_format_instructions()

SYSTEM_PROMPT = """
You are an expert exam content creator.
Given clean article text, generate *only* the quiz and suggested related topics.
Do NOT rewrite title, summary, or entities.
Your quiz should contain:
- 5 to 10 multiple-choice questions
- Each question has 4 options (A, B, C, D) only
- One correct answer that exactly matches one of the options
- A short explanation (1–2 sentences)
- A difficulty level: easy / medium / hard

Then return 5–10 related Wikipedia topics (just titles, not links).
Return only JSON following the provided schema.
"""

USER_PROMPT = """
Title: {title}

Summary: {summary}

Key Entities:
{key_entities}

Sections:
{sections}

Clean Article Text:
{article_text}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", USER_PROMPT),
])

chain = prompt | llm | parser

def compress_text(text, max_chars=4000):
    """Trim extremely long article text before sending to LLM."""
    text = text.strip()
    if len(text) > max_chars:
        return text[:max_chars]  # take only relevant part
    return text

def generate_quiz_payload(title: str, summary: str, sections: List[str], key_entities: Dict, article_text: str) -> Dict:
    """Generate quiz part only; attach metadata outside."""
    article_text = compress_text(article_text)
    try:
        result = chain.invoke({
            "title": title,
            "summary": summary,
            "sections": sections,
            "key_entities": key_entities,
            "article_text": article_text,
            "format_instructions": format_instructions,
        })
        # `result` may be a pydantic model (with .dict()) or a plain dict-like object.
        if hasattr(result, "dict"):
            data = result.dict()
        elif isinstance(result, dict):
            data = result
        else:
            # fallback: try attribute access to build a dict
            data = {
                "title": getattr(result, "title", title),
                "summary": getattr(result, "summary", summary),
                "sections": getattr(result, "sections", sections),
                "key_entities": getattr(result, "key_entities", key_entities),
                "questions": getattr(result, "questions", None),
                "related_topics": getattr(result, "related_topics", None),
            }

        # Normalize fields expected by the frontend
        questions = data.get("questions") or data.get("quiz") or []
        related = data.get("related_topics") or data.get("relatedTopics") or []

        # Flatten key_entities (dict -> list) so frontend can join/display easily
        ke = data.get("key_entities") or key_entities or {}
        if isinstance(ke, dict):
            flattened_ke = []
            for v in ke.values():
                if isinstance(v, (list, tuple)):
                    flattened_ke.extend(v)
                elif v:
                    flattened_ke.append(v)
            # de-duplicate while preserving order
            seen = set()
            flattened = []
            for item in flattened_ke:
                if item and item not in seen:
                    seen.add(item)
                    flattened.append(item)
            flattened_ke = flattened
        elif isinstance(ke, (list, tuple)):
            flattened_ke = list(ke)
        else:
            flattened_ke = [str(ke)] if ke else []

        return {
            "id": None,
            "url": None,
            "title": data.get("title", title),
            "summary": data.get("summary", summary),
            "key_entities": flattened_ke,
            "sections": data.get("sections", sections),
            "questions": questions,
            "related_topics": related,
        }

    except Exception as e:
        # Surface a clearer error for debugging and logs
        raise RuntimeError(f"LLM generation failed: {e}")
