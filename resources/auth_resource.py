import hashlib
from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask import current_app, request, make_response
from flask_restful import Resource
from db import IVOverflowDB


class AuthResource(Resource):
    """
    AuthResource handles user authentication and token generation in the IVOverflow API.

    Attributes:
        COLLECTION_NAME (str): The name of the collection in the database.
    """

    COLLECTION_NAME = 'users'

    def __init__(self):
        """
        Initializes the AuthResource with a database connection and key length configuration.
        """
        self.db = IVOverflowDB.get_db()
        self.key_length = current_app.config.get('KEY_LENGTH', 32)

    def post(self):
        """
        Handles POST requests for user authentication.

        Returns:
            make_response: A Flask response containing a JSON object with a token or an error message.
        """
        try:
            data = request.json
            email, password = data.get('email'), data.get('password')

            if email and password:
                user = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                            field_name="email",
                                            field_value=email)
                if user and self._verify_password(plain_password=password, hashed_password=user['password']):
                    identity = user.get('user_id')
                    expires_delta = timedelta(hours=1)
                    token = create_access_token(identity=identity, expires_delta=expires_delta)
                    return make_response({'token': token}, 201)
                else:
                    return make_response({'error': 'Invalid email or password'}, 401)
            else:
                return make_response({'error': 'Email and password are required'}, 400)

        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies the provided plain password against the hashed password.

        Args:
            plain_password (str): The plain password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        hashed_input = hashlib.sha512(plain_password.encode('utf-8')).hexdigest()
        return hashed_input == hashed_password
