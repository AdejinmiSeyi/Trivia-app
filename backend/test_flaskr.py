import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
# from settings import DB_NAME_TEST, DB_PASSWORD, DB_USER


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_path = "postgresql://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What is the largest mammal in the world?",
            "answer": "Blue Whale",
            "category": 1,
            "difficulty": 3
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # def test_get_questions_by_category(self):
    #     res = self.client().get('/categories/5/questions')
    #     data = json.loads(res.data)

    #     self.assertTrue(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["current_category"], "Entertainment")
    #     self.assertTrue(len(data["questions"]))

    # def test_get_categories(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["category"])

    # def test_404_categories_does_not_exist(self):
    #     res = self.client().get('/categories/10/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"],False)
    #     self.assertTrue(data["message"], "resource not found")

    # def test_to_verify_new_question_created(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(
    #         data['message'], 'New question was successfully created')

    # def test_405_sent_if_question_not_created(self):
    #     res = self.client().post('/questions/100', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "method not allowed")

    # def test_get_question_search_with_results(self):
    #     res = self.client().get('/questions', json={"searchTerm": "largest"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_questions'])

    # def test_422_sent_if_question_does_not_exist_before_delete(self):
    #     res = self.client().delete('/questions/25')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'unprocessable')

    # def test_that_questions_endpoint_exists(self):
    #     res = self.client().get('/questions')

    #     self.assertEqual(res.status_code, 200)

    # def test_that_categories_endpoint_exists(self):
    #     res = self.client().get('/categories')

    #     self.assertEqual(res.status_code, 200)

    def test_that_quizzes_endpoint_exists(self):
        res = self.client().post('/quizzes')

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
