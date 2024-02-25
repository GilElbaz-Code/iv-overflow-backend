# Import necessary modules from Flask and extensions
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Import the Config class from the config module
from config import Config

# Import resource classes from respective modules
from resources.answer_resource import AnswerResource
from resources.auth_resource import AuthResource
from resources.question_resource import QuestionResource
from resources.user_info_resource import UserInfoResource
from resources.vote_resource import VoteResource

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the entire application
CORS(app)

# Create an instance of Flask-RESTful API
api = Api(app)

# Configure Flask-JWT-Extended for JWT (JSON Web Token) support
jwt = JWTManager(app)

# Load configuration settings from the Config class
app.config.from_object(Config)

# Add resources and their corresponding endpoints to the API
api.add_resource(AuthResource, '/login')
api.add_resource(UserInfoResource, '/user-info')
api.add_resource(QuestionResource, '/questions')
api.add_resource(AnswerResource, '/answers')
api.add_resource(VoteResource, '/votes')

# Run the application if this script is executed
if __name__ == '__main__':
    app.run()
