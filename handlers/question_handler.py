from db import Database

from models.questionmodel import QuestionModel


class QuestionHandler:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db.get_db()['questions']

    def get_questions(self, page: int, page_size: int) -> list:
        skip = (page - 1) * page_size
        projection = {'_id': 0, 'title': 1, 'content': 1, 'tags': 1, 'created_by': 1, 'date': 1}
        questions = list(self.collection.find({}, projection=projection).skip(skip).limit(page_size))
        return questions

    def create_question(self, question_data: dict):
        question = QuestionModel.parse_obj(question_data)
        self.collection.insert_one(question.dict())

