from pydantic import BaseModel
from datetime import datetime


class AnswerModel(BaseModel):
    answer_id: str
    question_id: str
    created_by: str
    content: str
    rating: int = 0
    date: datetime = datetime.now()
