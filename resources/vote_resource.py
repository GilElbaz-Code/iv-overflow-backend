from flask_jwt_extended import jwt_required
from flask_restful import Resource

from db import IVOverflowDB


class VoteResource(Resource):
    COLLECTION_NAME = 'answers'

    def __init__(self):
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        raise NotImplemented

    @jwt_required()
    def post(self):
        raise NotImplemented
