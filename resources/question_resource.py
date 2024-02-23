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
            data = request.args
            question_id = data.get('question_id')
            if question_id:
                question = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                                field_name='question_id',
                                                field_value=question_id)
                return make_response({'question': question})
            else:
                # Retrieve a list of questions
                page = int(request.args.get('page', default=1))
                page_size = int(request.args.get('page_size', default=10))
                skip = (page - 1) * page_size

                questions = self.db.get_documents(
                    collection_name=self.COLLECTION_NAME,
                    skip=skip,
                    limit=page_size
                )
                return make_response({'questions': questions})
        except Exception as e:
            error_message = str(e)
            return {'data': {'error': error_message}}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.json
            title = data.get('title')
            content = data.get('content')
            tags = data.get('tags')
            full_name = data.get('fullName')

            question = QuestionModel(question_id=str(uuid.uuid4()),
                                     title=title,
                                     content=content,
                                     tags=tags,
                                     full_name=full_name)

            result = self.db.create_document(collection_name=self.COLLECTION_NAME, document_data=question.dict())

            return {"result": result}, 201

        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500
