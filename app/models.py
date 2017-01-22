from app import db
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(64), unique=True, index=True)
    accounts = db.relationship('Account', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, index=True)
    # days = db.relationship('Day', backref='year', order_by='day.date')
    initial_value = db.Column(db.Float)
    end_value = db.Column(db.Float)

    def __repr__(self):
        return '<Year %r>' % self.year

    @staticmethod
    def insert_year():
        current_year = datetime.now().year
        year = Year.query.filter_by(year=current_year).first()
        if year is None:
            year = Year(year=current_year)
            year.initial_value = 123
            db.session.add(year)
            db.session.commit()


class Day(db.Model):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'))
    date = db.Column(db.Date, unique=True, index=True)
    value = db.Column(db.Float)
    operations = db.relationship('Operation', backref='day')

    def __repr__(self):
        return '<Day %r>' % self.date

    @staticmethod
    def insert_day():
        current_day = datetime.now()
        day = Day.query.filter_by(date=current_day).first()
        year = Year.query.filter_by(year=current_day.year).first()
        if day is None and year is not None:
            day = Day()
            day.date = current_day.date()
            day.value = 20
            day.year_id = year.id
            db.session.add(day)
            db.session.commit()


class Operation(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'))
    descr = db.Column(db.String(64))
    date = db.Column(db.Date, index=True)
    value = db.Column(db.Float, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    frequency = db.Column(db.Integer, default=1)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)

    def __repr__(self):
        return '<Operation %r>' % self.descr

    @staticmethod
    def insert_operations():
        current = datetime.now()
        ops = [{
                    'descr': 'operation 1',
                    'value': 1,
                    'frequency': 1
                },
                {
                    'descr': 'operation 2',
                    'value': 2,
                    'frequency': 1
                },
                {
                    'descr': 'operation 3',
                    'value': 3,
                    'frequency': 2
                }
        ]
        day = Day.query.filter_by(date=current.date()).first()
        for o in ops:
            op = Operation.query.filter_by(descr=o['descr']).first()
            if op is None:
                op = Operation(descr=o)
                op.descr = o['descr']
                op.date = current
                op.day_id = day.id
                op.value = o['value']
                op.frequency = o['frequency']
                db.session.add(op)
        db.session.commit()


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Account %r>' % self.name
