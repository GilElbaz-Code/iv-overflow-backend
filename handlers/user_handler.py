import hashlib
import jwt

from db import Database

from datetime import datetime, timedelta


class UserHandler:

    def __init__(self, db: Database, secret_key: str):
        self.db = db
        self.collection = self.db.get_db()['users']
        self.secret_key = secret_key

    def login(self, user_data: dict) -> dict:
        email = user_data.get('email')
        password = user_data.get('password')

        if email and password:
            user = self.collection.find_one({'email': email})
            if user and self._verify_password(plain_password=password, hashed_password=user['password']):
                token = self._generate_jwt_token(user_id=str(user['_id']))
                return {'token': token}
            else:
                return {'error': 'Invalid email or password'}
        else:
            return {'error': 'Email and password are required'}

    def get_user_info(self):
        raise NotImplementedError

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        hashed_input = hashlib.sha512(plain_password.encode('utf-8')).hexdigest()
        return hashed_input == hashed_password

    def _generate_jwt_token(self, user_id: str) -> str:
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        payload = {'user_id': user_id, 'exp': expiration_time}
        token = jwt.encode(payload=payload, key=self.secret_key, algorithm='HS256')
        return token
