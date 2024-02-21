import hashlib
from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask import current_app, request
from flask_restful import Resource

from db import IVOverflowDB


class AuthResource(Resource):
    COLLECTION_NAME = 'users'

    def __init__(self):
        self.db = IVOverflowDB.get_db()
        self.key_length = current_app.config.get('KEY_LENGTH', 32)

    def post(self):
        try:
            data = request.json
            email, password = data.get('email'), data.get('password')

            if email and password:
                user = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                            field_name="email",
                                            field_value=email)
                if user and self._verify_password(plain_password=password, hashed_password=user['password']):
                    expires_delta = timedelta(hours=1)
                    user_id = user.get('user_id')
                    token = create_access_token(identity=user_id, expires_delta=expires_delta)
                    return {'data': {'token': token}}, 201
                else:
                    return {'data': {'error': 'Invalid email or password'}}, 401
            else:
                return {'data': {'error': 'Email and password are required'}}, 400

        except Exception as e:
            error_message = str(e)
            return {'data': {'error': error_message}}, 500

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        hashed_input = hashlib.sha512(plain_password.encode('utf-8')).hexdigest()
        return hashed_input == hashed_password
