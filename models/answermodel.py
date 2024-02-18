from pydantic import BaseModel
from datetime import datetime


class AnswerModel(BaseModel):
    created_by: str
    content: str
    rating: int
    date: datetime
    question_id : str
