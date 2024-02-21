import hashlib
import os
import random
import string
from datetime import datetime, timedelta

import jwt
from flask import request
from flask_restful import Resource
from db import IVOverflowDB


class AuthResource(Resource):
    COLLECTION_NAME = 'users'
    KEY_LENGTH = int(os.getenv(key="KEY_LENGTH", default=32))

    def __init__(self):
        self.db = IVOverflowDB.get_db()

    def post(self):
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')

            if email and password:
                user = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                            field_name="email",
                                            field_value=email)
                if user and self._verify_password(plain_password=password, hashed_password=user['password']):
                    token = self._generate_jwt_token(user_id=user.get('user_id'))
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

    def _generate_jwt_token(self, user_id: str) -> str:
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        payload = {'user_id': user_id, 'exp': expiration_time}
        token = jwt.encode(payload=payload, key=self._generate_jwt_key())
        return token

    def _generate_jwt_key(self):
        key = ''.join(random.choices(population=string.ascii_letters + string.digits, k=self.KEY_LENGTH))
        return key
