import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel


class QuestionModel(BaseModel):
    question_id: str
    title: str
    content: str
    date: datetime = datetime.now()
    categories: List[str]
    created_by: str
