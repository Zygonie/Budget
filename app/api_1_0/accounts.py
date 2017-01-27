from app.models import Account
from . import api_blueprint as api
from flask import jsonify

@api.route('/accounts/')
def get_accounts():
    accounts = Account.query.all()
    return jsonify({ 'accounts': [account.to_json() for account in accounts] })

@api.route('/accounts/<int:id>')
def get_account(id):
    account = Account.query.get_or_404(id)
    return jsonify(account.to_json())