import json
from flask import url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Role, Operation, Year, Day, Account


class FlaskClientTestCase(TestCase):
    app_context = None

    @classmethod
    def create_app(cls):
        return create_app('testing')

    @classmethod
    def setUpClass(cls):
        cls.app = cls.create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.drop_all()
        db.create_all()
        Role.insert_role()
        User.insert_users()
        Account.insert_account()
        Year.insert_year()
        Day.insert_day()
        Operation.insert_operations()
        cls.client = cls.app.test_client(use_cookies=True)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_get_operations(self):
        response = self.client.get(url_for('api.get_operations'))
        # Get the JSON
        json_response = json.loads(response.get_data())
        self.assertTrue(len(json_response['operations']) > 0)
        first_operation = json_response['operations'][0]
        self.assertEqual(first_operation['descr'], 'operation 1')
        self.assertEqual(first_operation['frequency'], 1)
        self.assertEqual(first_operation['value'], 1)
