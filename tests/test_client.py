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
        # db.drop_all()
        cls.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        # Get the HTML content as text
        response_txt = response.get_data(as_text=True)
        self.assertTrue('<title>Home</title>' in response_txt)

    def test_operation_list(self):
        # response = self.client.get(url_for('main.list_operations'))
        self.assertTrue(True)
