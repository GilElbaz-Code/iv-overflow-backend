from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config import Config
from resources.answer_resource import AnswerResource
from resources.auth_resource import AuthResource
from resources.question_resource import QuestionResource

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(Config)

api.add_resource(AuthResource, '/login')
api.add_resource(QuestionResource, '/questions')
api.add_resource(AnswerResource, '/answers')

if __name__ == '__main__':
    app.run(debug=True)
