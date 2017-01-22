# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, Response, json
from app.models import Operation
from app.main import main_blueprint as main
from app import db

# Set the route and accepted methods
@main.route('/', methods=['GET'])
def index():
    """Renders the home page."""
    return render_template(
        'main/index.html',
        title='Main page'
    )

@main.route('/partials/<path:path>')
def render_partial(path):
    """Renders the partial view list of entries."""
    return render_template('partials/{}'.format(path))


@main.route('/operations', methods=['GET', 'POST'])
def list_operations():
    operations = Operation.query.all()
    if operations is None:
        return redirect(url_for('index'))
    return render_template('main/operation_list.html',
                           operations=operations)
