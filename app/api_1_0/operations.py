from app import db
from app.models import Operation
from . import api_blueprint as api
from flask import jsonify, request, url_for, g


@api.route('/operations/')
def get_operations():
    operations = Operation.query.all()
    return jsonify({'operations': [op.to_json() for op in operations]})


@api.route('/operations/<int:id>')
def get_operation(id):
    operation = Operation.query.get_or_404(id)
    return jsonify(operation.to_json())


@api.route('/operations/<int:id>', methods=['PUT'])
def edit_operation(id):
    operation = Operation.query.get_or_404(id)
    operation.body = request.json.get('body', operation.body)
    db.session.add(operation)
    return jsonify(operation.to_json())


@api.route('/operations/', methods=['POST'])
def new_operation():
    operation = Operation.from_json(request.json)
    db.session.add(operation)
    db.session.commit()
    return jsonify(operation.to_json()), 201
