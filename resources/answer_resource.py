import uuid
from flask import request, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from db import IVOverflowDB
from models.answer_model import AnswerModel


class AnswerResource(Resource):
    """
    AnswerResource handles CRUD operations for answers in the IVOverflow API.

    Attributes:
        COLLECTION_NAME (str): The name of the collection in the database.
    """

    COLLECTION_NAME = 'answers'

    def __init__(self):
        """
        Initializes the AnswerResource with a database connection.
        """
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        """
        Handles GET requests to retrieve answers for a specific question.

        Returns:
            make_response: A Flask response containing a JSON object with answers.
        """
        try:
            question_id = request.args.get('questionId')
            answers = self.db.get_documents(
                collection_name=self.COLLECTION_NAME,
                field_name='question_id',
                field_value=question_id,
                sort={'votes': -1}
            )
            return make_response({'answers': answers}, 200)
        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)

    @jwt_required()
    def post(self):
        """
        Handles POST requests to submit a new answer.

        Returns:
            make_response: A Flask response containing a JSON object with the result of the operation.
        """
        try:
            data = request.json
            question_id = data.get('questionId')
            full_name = data.get('fullName')
            content = data.get('content')

            # Create an AnswerModel instance
            answer = AnswerModel(answer_id=str(uuid.uuid4()),
                                 question_id=question_id,
                                 full_name=full_name,
                                 content=content)

            # Store the answer in the database
            result = self.db.create_document(collection_name=self.COLLECTION_NAME, document_data=answer.dict())

            # Prepare the response data
            response_data = {
                'result': result,
                'status': 'success',
                'message': 'Answer submitted successfully',
                'answer': answer.to_dict()
            }

            return make_response(response_data, 201)
        except Exception as e:
            print(e)  # Consider using logging instead of print in production
            error_message = str(e)
            return make_response({'error': error_message}, 500)
