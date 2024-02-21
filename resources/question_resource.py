import uuid

from flask import request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db import IVOverflowDB
from models.question_model import QuestionModel


class QuestionResource(Resource):
    COLLECTION_NAME = 'questions'

    def __init__(self):
        self.db = IVOverflowDB.get_db()
    @jwt_required()
    def get(self):
        try:
            page = int(request.args.get('page', default=1))
            page_size = int(request.args.get('page_size', default=10))
            skip = (page - 1) * page_size

            questions = self.db.get_documents(collection_name=self.COLLECTION_NAME,
                                              projection={"_id": 0},
                                              skip=skip,
                                              limit=page_size)

            return make_response({'data':{'questions': questions}}, 200)
        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.json
            title = data.get('title')
            content = data.get('content')
            categories = data.get('categories')
            created_by = data.get('userId') # todo: find a way to get full name from user id

            question = QuestionModel(question_id=str(uuid.uuid4()),
                                     title=title,
                                     content=content,
                                     categories=categories,
                                     created_by=created_by)

            result = self.db.create_document(collection_name=self.COLLECTION_NAME, document_data=question.dict())

            return {"result": result}, 201

        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500
