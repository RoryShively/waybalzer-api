from lib.util_sqlalchemy import ResourceMixin
from wayblazer.extensions import db

from wayblazer.blueprints.company.states import STATES


class Company(ResourceMixin, db.Model):

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), index=True, nullable=False, server_default='')
    web = db.Column(db.String(1024), nullable=False, server_default='')
    phone = db.Column(db.String(24), nullable=False, server_default='')

    addresses = db.relationship('Address', backref='company',
                                lazy='joined')
    employees = db.relationship('Employee', backref='company',
                                lazy='joined')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Company, self).__init__(**kwargs)


class Address(ResourceMixin, db.Model):

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    route = db.Column(db.String(64), index=True, nullable=False, server_default='')
    city = db.Column(db.String(64), index=True, nullable=False, server_default='')
    county = db.Column(db.String(64), index=True, nullable=False, server_default='')
    state = db.Column(db.Enum(*STATES, name='states', native_enum=False),
                      index=True, nullable=False, server_default='')
    zip = db.Column(db.String(10), index=True, nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Address, self).__init__(**kwargs)
