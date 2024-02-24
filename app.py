from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager


from config import Config
from resources.answer_resource import AnswerResource
from resources.auth_resource import AuthResource
from resources.question_resource import QuestionResource
from resources.user_info_resource import UserInfoResource
from resources.vote_resource import VoteResource

app = Flask(__name__)

CORS(app)
api = Api(app)
jwt = JWTManager(app)
app.config.from_object(Config)

api.add_resource(AuthResource, '/login')
api.add_resource(UserInfoResource, '/user-info')
api.add_resource(QuestionResource, '/questions')
api.add_resource(AnswerResource, '/answers')
api.add_resource(VoteResource, '/votes')


if __name__ == '__main__':
    app.run(debug=True)
