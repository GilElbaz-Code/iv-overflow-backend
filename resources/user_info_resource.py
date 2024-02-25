from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from db import IVOverflowDB


class UserInfoResource(Resource):
    """
    UserInfoResource handles the retrieval of user information based on the authenticated user's token in the IVOverflow API.

    Attributes:
        COLLECTION_NAME (str): The name of the collection in the database.
    """

    COLLECTION_NAME = 'users'

    def __init__(self):
        """
        Initializes the UserInfoResource with a database connection.
        """
        self.db = IVOverflowDB.get_db()

    @jwt_required()
    def get(self):
        """
        Handles GET requests to retrieve user information.

        Returns:
            make_response: A Flask response containing a JSON object with user information.
        """
        try:
            # Get the user_id from the token
            user_id = get_jwt_identity()

            # Retrieve user information from the database
            user = self.db.get_document(collection_name=self.COLLECTION_NAME,
                                        field_name='user_id',
                                        field_value=user_id)

            # Create a dictionary with user information
            user_info = {
                'userId': user_id,
                'email': user.get('email'),
                'fullName': user.get('full_name'),
            }

            # Return the user information in a Flask response
            return make_response({'data': user_info}, 200)

        except Exception as e:
            error_message = str(e)
            return make_response({'error': error_message}, 500)
