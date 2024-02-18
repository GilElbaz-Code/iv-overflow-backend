from db import Database
from models.answermodel import AnswerModel


class AnswerHandler:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.get_db()['answers']

    def get_question_answers(self, question_id: str, page: int, page_size: int) -> list:
        skip = (page - 1) * page_size
        projection = {'_id': 0, 'title': 1, 'content': 1, 'tags': 1, 'created_by': 1, 'date': 1, 'rating': 1}
        answers = list(self.collection.find({"question_id": question_id}, projection=projection).skip(skip=skip).limit(
            limit=page_size))
        return answers

    def create_answer(self, answer_data: dict):
        answer = AnswerModel.parse_obj(answer_data)
        self.collection.insert_one(answer)
