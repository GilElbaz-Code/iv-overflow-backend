from pydantic import BaseModel
from datetime import datetime


class AnswerModel(BaseModel):
    answer_id: str
    question_id: str
    full_name: str
    content: str
    votes: int = 0
    date: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {
            "answer_id": self.answer_id,
            "question_id": self.question_id,
            "full_name": self.full_name,
            "content": self.content,
            "votes": self.votes,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S") if self.date else None,
        }
