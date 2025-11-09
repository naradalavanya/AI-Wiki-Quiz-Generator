from typing import List, Optional
from pydantic import BaseModel, Field

class MCQ(BaseModel):
    question: str = Field(..., description="Clear, concise question")
    options: List[str] = Field(..., min_items=3, max_items=6)
    correct_answer: str = Field(..., description="Must exactly match one option")
    explanation: Optional[str] = Field(None, description="Short explanation of answer")

class QuizOutput(BaseModel):
    title: str
    summary: str
    key_entities: List[str] = Field(default_factory=list)
    related_topics: List[str] = Field(default_factory=list)
    questions: List[MCQ] = Field(..., min_items=5, max_items=20)
