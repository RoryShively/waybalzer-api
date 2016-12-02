from lib.util_sqlalchemy import ResourceMixin
from wayblazer.extensions import db


class Employee(ResourceMixin, db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    number_id = db.Column(db.Integer, db.ForeignKey('personal_numbers.id'))

    first_name = db.Column(db.String(128), nullable=False, server_default='')
    last_name = db.Column(db.String(128), index=True,
                          nullable=False, server_default='')
    email = db.Column(db.String(128), index=True,
                      nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Employee, self).__init__(**kwargs)


class PersonalPhone(ResourceMixin, db.Model):
    __tablename__ = 'personal_numbers'

    id = db.Column(db.Integer, primary_key=True)

    employees = db.relationship('Employee', backref='phone',
                                lazy='joined')

    number = db.Column(db.String(24), nullable=False, server_default='')
