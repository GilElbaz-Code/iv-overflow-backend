from typing import List
from datetime import datetime
from pydantic import BaseModel


class QuestionModel(BaseModel):
    question_id: str
    title: str
    content: str
    date: datetime = datetime.now()
    tags: List[str]
    full_name: str
