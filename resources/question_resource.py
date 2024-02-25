import uuid
from flask import request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from db import IVOverflowDB
from models.question_model import QuestionModel


class QuestionResource(Resource):
    """
    QuestionResource handles CRUD operations for questions in the IVOverflow API.

    Attributes:
        COLLECTION_NAME (str): The name of the collection in the database.
    """

    COLLECTION_NAME = 'questions'

    def __init__(self):
        """
        Initializes the QuestionResource with a database connection.
        """
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        """
        Handles GET requests to retrieve either a single question or a list of questions.

        Returns:
            make_response: A Flask response containing a JSON object with a question or a list of questions.
        """
        try:
            question_id = request.args.get('questionId')
            if question_id:
                # Retrieve a single question by question_id
                question = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                                field_name='question_id',
                                                field_value=question_id)
                return make_response({'question': question}, 200)
            else:
                # Retrieve a list of questions with optional pagination
                page = int(request.args.get('page', default=1))
                page_size = int(request.args.get('page_size', default=10))
                skip = (page - 1) * page_size

                questions = self.db.get_documents(
                    collection_name=self.COLLECTION_NAME,
                    skip=skip,
                    limit=page_size)
                return make_response({'questions': questions}, 200)
        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)

    @jwt_required()
    def post(self):
        """
        Handles POST requests to submit a new question.

        Returns:
            make_response: A Flask response containing a JSON object with the result of the operation.
        """
        try:
            data = request.json
            title = data.get('title')
            content = data.get('content')
            tags = data.get('tags')
            full_name = data.get('fullName')

            # Create a QuestionModel instance
            question = QuestionModel(question_id=str(uuid.uuid4()),
                                     title=title,
                                     content=content,
                                     tags=tags,
                                     full_name=full_name)

            # Store the question in the database
            result = self.db.create_document(collection_name=self.COLLECTION_NAME, document_data=question.dict())

            return make_response({"result": result}, 201)

        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)
