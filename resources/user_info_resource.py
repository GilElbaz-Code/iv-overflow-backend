from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from db import IVOverflowDB


class UserInfoResource(Resource):
    COLLECTION_NAME = 'users'

    def __init__(self):
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                    field_name='user_id',
                                    field_value=user_id)
        user_info = {
            'user_id': user_id,
            'email': user.get('email'),
            'full_name': user.get('full_name'),
        }
        return {'data': user_info}
