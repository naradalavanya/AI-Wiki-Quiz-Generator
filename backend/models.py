from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class MCQ(BaseModel):
    question: str = Field(..., description="Clear, concise question")
    options: List[str] = Field(..., min_items=3, max_items=6)
    correct_answer: str = Field(..., description="Must exactly match one of the options exactly")
    explanation: Optional[str] = Field(None, description="Short explanation of the answer")
    difficulty: Optional[str] = Field("medium", description="easy, medium, or hard")  # ✅ Required by instructions

class QuizOutput(BaseModel):
    title: str
    summary: str
    sections: List[str] = Field(default_factory=list)  # ✅ Required
    key_entities: Dict[str, List[str]] = Field(default_factory=dict)  # ✅ Should be dict, not list
    related_topics: List[str] = Field(default_factory=list)
    questions: List[MCQ] = Field(..., min_items=5, max_items=20)
