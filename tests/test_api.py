import flask.json as json
from datetime import date
from flask import url_for
from flask_testing import TestCase
from app import create_app, db, seed


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
        seed.seed()
        # db.drop_all()
        # db.create_all()
        # Role.insert_role()
        # User.insert_users()
        # Account.insert_account()
        # Year.insert_year()
        # Day.insert_day()
        # Operation.insert_operations()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_operations(self):
        response = self.client.get(url_for('api.get_operations'))
        # Get the JSON
        json_response = json.loads(response.get_data())
        self.assertTrue(len(json_response['operations']) > 0)
        first_operation = json_response['operations'][0]
        self.assertEqual(first_operation['descr'], 'operation 1')
        self.assertEqual(first_operation['frequency'], 1)
        self.assertEqual(first_operation['value'], 1)

    def test_post_new_operation(self):
        response = self.client.get(url_for('api.get_accounts'))
        json_account = json.loads(response.get_data())
        self.assertGreaterEqual(len(json_account['accounts']), 1, 'No account in the database')
        account_id = json_account['accounts'][0]['id']
        operation = {
            'descr': 'New operation',
            'date': date.today(),
            'value': 123,
            'frequency': 1,
            'start_date': '',
            'end_date': '',
            'account_id': account_id
        }
        response = self.client.post(url_for('api.new_operation'),
                                    headers=self.get_api_headers(),
                                    data=json.dumps(operation))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['descr'], operation['descr'])
