import uuid

from flask import request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from db import IVOverflowDB
from models.answer_model import AnswerModel


class AnswerResource(Resource):
    COLLECTION_NAME = 'answers'

    def __init__(self):
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        try:
            question_id = request.args.get('questionId')
            answers = self.db.get_documents(collection_name=self.COLLECTION_NAME,
                                            field_name='question_id',
                                            field_value=question_id)
            return make_response({'answers': answers})
        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.json
            question_id = data.get('question_id')
            created_by = data.get('created_by')  # user_id
            content = data.get('content')

            answer = AnswerModel(answer_id=str(uuid.uuid4()),
                                 question_id=question_id,
                                 created_by=created_by,
                                 content=content)

            result = self.db.create_document(collection_name=self.COLLECTION_NAME, document_data=answer.dict())

            return {'result': result}, 201
        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500