from app import db
from app.models import Account, Day, Operation, Year, User, Role


def seed():
    db.session.remove()
    db.drop_all()
    db.create_all()
    Role.insert_role()
    User.insert_users()
    Account.insert_account()
    Year.insert_year()
    Day.insert_day()
    Operation.insert_operations()