from app import db
from flask import url_for
from datetime import date
from app.exceptions import ValidationError


user_role_relationship_table = db.Table('user_role_relationship_table',
                                        db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), nullable=False),
                                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
                                        db.PrimaryKeyConstraint('role_id', 'user_id'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_role():
        name = 'admin'
        role = Role.query.filter_by(name=name).first()
        if role is None:
            role = Role(name=name)
            db.session.add(role)
            db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    roles = db.relationship('Role', secondary=user_role_relationship_table, backref='users')
    username = db.Column(db.String(64), unique=True, index=True)
    accounts = db.relationship('Account', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insert_users():
        username = 'guillaume'
        role_name = 'admin'
        user = User.query.filter_by(username=username).first()
        role = Role.query.filter_by(name=role_name).first()
        if user is None and role is not None:
            user = User(username=username)
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()


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
        current_year = date.today().year
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
        current_day = date.today()
        day = Day.query.filter_by(date=current_day).first()
        year = Year.query.filter_by(year=current_day.year).first()
        if day is None and year is not None:
            day = Day()
            day.date = current_day
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
        current = date.today()
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
        day = Day.query.filter_by(date=current).first()
        account = Account.query.filter_by(name='CELI').first()
        for o in ops:
            op = Operation.query.filter_by(descr=o['descr']).first()
            if op is None and account is not None:
                op = Operation(descr=o)
                op.descr = o['descr']
                op.date = current
                op.account_id = account.id
                op.day_id = day.id
                op.value = o['value']
                op.frequency = o['frequency']
                db.session.add(op)
        db.session.commit()

    def to_json(self):
        json_operation = {
            'id': self.id,
            'descr': self.descr,
            'date': self.date,
            'value': self.value,
            'frequency': self.frequency,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'account_id': url_for('api.get_account', id=self.account_id, _external=True)
        }
        return json_operation

    @staticmethod
    def from_json(json_obj):
        descr = json_obj.get('desc')
        date = json_obj.get('date')
        value = json_obj.get('value')
        frequency = json_obj.get('frequency')
        start_date = json_obj.get('start_date')
        end_date = json_obj.get('end_date')
        account_id = json_obj.get('account_id')
        if descr is None or descr == '':
            raise ValidationError('Wrong operation description')
        if date is None or date == '':
            raise ValidationError('Wrong operation date')
        if value is None or value == '':
            raise ValidationError('Wrong operation value')
        if frequency is None or frequency == '':
            raise ValidationError('Wrong operation frequency')
        if frequency > 1:
            if start_date is None or start_date == '':
                raise ValidationError('Wrong operation start date')
            if end_date is None or end_date == '':
                raise ValidationError('Wrong operation end date')
        if account_id is None or account_id == '':
            raise ValidationError('Wrong account id')
        return Operation(descr=descr, date=date, value=value, frequency=frequency,
                         start_date=start_date, end_date=end_date, account_id=account_id)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Account %r>' % self.name

    @staticmethod
    def insert_account():
        name = 'CELI'
        username = 'guillaume'
        user = User.query.filter_by(username=username).first()
        account = Account.query.filter_by(name=name).first()
        if account is None and user is not None:
            account = Account()
            account.name = name
            account.user_id = user.id
            db.session.add(account)
            db.session.commit()

    def to_json(self):
        json_account = {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }
        return json_account
