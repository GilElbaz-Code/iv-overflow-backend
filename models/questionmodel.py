import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class QuestionModel(BaseModel):
    question_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    content: str
    date: datetime = datetime.now()
    tags: List[str]
    created_by: str
