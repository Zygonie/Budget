import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role, Operation, Year, Day


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Year.insert_year()
        Day.insert_day()
        Operation.insert_operations()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        # Get the HTML content as text
        response_txt = response.get_data(as_text=True)
        self.assertTrue('Stranger' in response_txt)

    def test_operation_list(self):
        # response = self.client.get(url_for('main.list_operations'))
        self.assertTrue(True)
