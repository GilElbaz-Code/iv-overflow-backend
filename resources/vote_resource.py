from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request

from db import IVOverflowDB


class VoteResource(Resource):
    COLLECTION_NAME = 'answers'

    def __init__(self):
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
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
        return votes_sum

    @jwt_required()
    def post(self):
        data = request.json
        answer_id = data.get('answerId')
        direction = data.get('direction')

        if direction not in ['up', 'down']:
            return {'error': 'Invalid direction'}, 400

        answer = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                      field_name='answer_id',
                                      field_value=answer_id)

        if not answer:
            return {'error': 'Answer not found'}, 404

        if direction == 'up':
            answer['votes'] += 1
        else:
            answer['votes'] -= 1

        self.db.update_document(collection_name=self.COLLECTION_NAME,
                                field_name='answer_id',
                                field_value=answer_id,
                                update_data=answer)

        return {'message': 'Votes updated successfully'}
