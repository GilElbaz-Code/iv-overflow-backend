from flask import Flask, request, jsonify
from flask_cors import CORS

from handlers.answer_handler import AnswerHandler
from handlers.question_handler import QuestionHandler
from handlers.user_handler import UserHandler
from db import Database
from config import Config

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

db = Database()

user_handler = UserHandler(db=db, secret_key=app.config['SECRET_KEY'])
question_handler = QuestionHandler(db=db)
answer_handler = AnswerHandler(db=db)


# User Handler

@app.route('/login', methods=["POST"])
def login():
    try:
        data = request.json
        result = user_handler.login(user_data=data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# TODO: Figure out user info logic
@app.route('/userInfo', methods=["GET"])
def get_user_info():
    try:
        data = request.json
        result = user_handler.get_user_info()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Question Handler
@app.route('/getQuestions', methods=["GET"])
def get_questions():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))

        questions_data = question_handler.get_questions(page=page, page_size=page_size)

        return jsonify({'questions': questions_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/createQuestion', methods=["POST"])
def create_question():
    try:
        question_data = request.json
        result = question_handler.create_question(question_data=question_data)
        return jsonify({'ok': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Answer Handler
@app.route('/getQuestionAnswer', methods=["GET"])
def get_question_answers():
    try:
        question_id = request.args.get('question_id')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))

        answers_data = answer_handler.get_question_answers(question_id=question_id, page=page, page_size=page_size)

        return jsonify({'answers': answers_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/createAnswer', methods=["POST"])
def create_answer():
    # TODO: need to pass question id to answer constructor
    try:
        question_data = request.json
        result = question_handler.create_question(question_data=question_data)
        return jsonify({'ok': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run()
