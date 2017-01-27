from app.models import Operation
from . import api_blueprint as api
from flask import jsonify

@api.route('/operations/')
def get_operations():
    operations = Operation.query.all()
    return jsonify({'operations': [op.to_json() for op in operations]})