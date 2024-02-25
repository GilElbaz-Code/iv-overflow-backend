from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request, make_response
from db import IVOverflowDB


class VoteResource(Resource):
    """
    VoteResource handles the retrieval and updating of votes for answers in the IVOverflow API.

    Attributes:
        COLLECTION_NAME (str): The name of the collection in the database.
    """

    COLLECTION_NAME = 'answers'

    def __init__(self):
        """
        Initializes the VoteResource with a database connection.
        """
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        """
        Handles GET requests to retrieve the sum of votes for answers to a specific question.

        Returns:
            make_response: A Flask response containing the sum of votes for answers and an HTTP status code.
        """
        try:
            data = request.args
            question_id = data.get('questionId')
            pipeline = [
                {
                    '$match': {'question_id': question_id}
                },
                {
                    '$group': {
                        '_id': None,
                        'votes_sum': {'$sum': '$votes'}
                    }
                }
            ]
            result = self.db.aggregate(collection_name=self.COLLECTION_NAME, pipeline=pipeline)
            votes_sum = next(result, {'votes_sum': 0}).get('votes_sum', 0)
            return votes_sum, 200

        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)

    @jwt_required()
    def post(self):
        """
        Handles POST requests to update votes for a specific answer.

        Returns:
            make_response: A Flask response containing a success message or an error message with an HTTP status code.
        """
        try:
            data = request.json
            answer_id = data.get('answerId')
            vote_type = data.get('voteType')

            if vote_type not in ['up', 'down']:
                return make_response({'error': 'Invalid direction'}, 400)

            # Retrieve the answer from the database
            answer = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                          field_name='answer_id',
                                          field_value=answer_id)

            if not answer:
                return make_response({'error': 'Answer not found'}, 404)

            # Update the votes based on the vote type
            if vote_type == 'up':
                answer['votes'] += 1
            else:
                answer['votes'] -= 1

            # Update the answer in the database
            self.db.update_document(collection_name=self.COLLECTION_NAME,
                                    field_name='answer_id',
                                    field_value=answer_id,
                                    update_data=answer)

            return make_response({'message': 'Votes updated successfully'})

        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)
