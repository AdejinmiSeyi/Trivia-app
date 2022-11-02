import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys
from sqlalchemy import asc, desc

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [questions.format() for questions in selection]
    current_question = questions[start:end]

    return current_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Allows '*' for origins
    # CORS(app)
    resources = ({r"*/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():

        category_list = Category.query.all()

        if len(category_list) == 0:
            abort(404)

        formatted_category = {
            category.id: category.type for category in category_list}

        #category.id: category.type

        return jsonify({
            'success': True,
            'category': formatted_category,
            'total_categories': len(category_list)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(desc(Question.id)).all()
        list_of_questions = paginate_questions(request, selection)

        if len(list_of_questions) == 0:
            abort(404)

        categories = Category.query.all()

        available_categories = {
            category.id: category.type for category in categories}

        for question in selection:
            category = Category.query.filter(
                Category.id == question.id).first()
        # formatted_categories = {category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': list_of_questions,
            'total_questions': len(selection),
            'categories': available_categories,
            'current_category': category.type

        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()
            question = Question.query.order_by(Question.id).all()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def search_and_create_new_questions():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', 1)
        difficulty = body.get('difficulty', 1)
        search_term = body.get('searchTerm', None)

        try:
            if search_term:

                if search_term == "":
                    selection = Question.query.order_by(Question.id).all()
                else:
                    selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike('%{}%'.format(search_term))).all()

                current_question = paginate_questions(request, selection)

                if search_term is None:
                    abort(404)

                return jsonify({
                    'success': True,
                    'questions': current_question,
                    'total_questions': len(selection)
                })

            else:
                if question == '' or answer == '' or category == '' or difficulty == '':
                    abort(422)

                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )
                question.insert()

                return jsonify({
                    'success': True,
                    'message': "New question was successfully created",
                })
        except Exception as e:

            question.rollback()
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:
            category = Category.query.filter(
                Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            selection = Question.query.filter(
                Question.category == category_id).all()
            questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": category.type
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quizzes():

        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']

            print(category_id)

            # if 'ALL' category is selected
            if category_id == 0:
                questions = Question.query.order_by(desc(Question.id)).all()

            # if a particular category is selected
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                                                  Question.category == category_id).all()

            # if len(questions) == 0:
            #     abort(404)

            question = None
            if (questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not found"
        }), 404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405,
        )

    return app

# Default port:
#     if __name__ == '__main__':
#         app.run(3000)

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 3000))
#     app.run(host='0.0.0.0', port=port)
