import os
from typing import Dict
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.models import QuizOutput

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-pro")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

# LLM client
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)

parser = JsonOutputParser(pydantic_object=QuizOutput)
format_instructions = parser.get_format_instructions()

SYSTEM_PROMPT = (
    "You are an expert educational content creator. Given a Wikipedia article's cleaned text, "
    "produce a concise summary and 5-10 multiple-choice questions (MCQs). Each MCQ must have 3-6 options "
    "and exactly one correct answer that matches one option verbatim. Keep wording unambiguous and "
    "explanations short. Also list key entities and related topics."
)

USER_PROMPT = (
    "Article Title: {title}\n\n"
    "Article Text (cleaned):\n{article_text}\n\n"
    "Return ONLY valid JSON following these rules:\n{format_instructions}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", USER_PROMPT),
])

# Chain = prompt → LLM → JSON parser
chain = prompt | llm | parser

def generate_quiz_payload(title: str, article_text: str) -> Dict:
    """Returns a dict validated by QuizOutput Pydantic schema."""
    try:
        result = chain.invoke({
            "title": title,
            "article_text": article_text,
            "format_instructions": format_instructions,
        })
        return result
    except Exception as e:
        # Common cause: configured MODEL_NAME not available for the API or
        # not supported by the selected API version. Surface a clearer
        # error with actionable next steps for the user.
        msg = (
            f"LLM generation failed: {e}\n\n"
            "Possible causes and fixes:\n"
            "- The configured MODEL_NAME (env var MODEL_NAME) is not available or not supported for your API version.\n"
            "  Check or change MODEL_NAME in backend/.env to a model your account supports.\n"
            "- Call ListModels (via your provider or cloud console) to see supported models and their compatible methods.\n"
            "- Ensure your API key has access to the requested model and the correct API/version is being used.\n\n"
            "Practical steps:\n"
            "1) Open backend/.env and set MODEL_NAME to a supported model (or remove it to use a default the provider lists).\n"
            "2) Use your provider's model-listing tool or console (for Google GenAI, check the Models page in Cloud Console or use the corresponding ListModels API).\n"
            "3) If you want, set MODEL_NAME to a known stable model for testing (example: 'gemini-1.0' or another model your account supports).\n\n"
            "Original exception: " + repr(e)
        )
        raise RuntimeError(msg)
