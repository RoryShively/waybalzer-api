from flask import Blueprint
from flask_restful import Resource, reqparse
from sqlalchemy.sql import func
from marshmallow import fields

from wayblazer.extensions import api, ma

from wayblazer.blueprints.company.models import Company, Address


company = Blueprint('company', __name__, template_folder='templates')


# What companies are located in Texas?
#   localhost:8000/api/company?state=TX
#
# What companies have exactly 3 employees listed?
#   localhost:8000/api/company?employee_count=3
#
# What zip codes are within California?
#   localhost:8000/api/zipcode?state=CAs
#


class ZipcodeSchema(ma.Schema):
    class Meta:
        fields = ('zip', )


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'route', 'city', 'state', 'zip', 'county', )


class CompanySchema(ma.Schema):
    addresses = fields.Nested(AddressSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'web', 'phone', 'addresses', )

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

zipcode_schema = ZipcodeSchema(many=True)


class CompaniesListAPI(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('state', type=str, location='args', required=False)
        parser.add_argument('employee_count', type=int, location='args', required=False)
        args = parser.parse_args()

        companies = Company.query.join(Address)

        if args.get('state'):
            companies = companies.filter(Address.state == args.get('state'))

        # if args.get('employee_count'):
        #     companies = companies.having(func.count(Company.employees) == args.get('employee_count'))

        companies = companies.all()

        if args.get('employee_count'):
            companies = [project for project in companies if len(project.employees) == args.get('employee_count')]

        return companies_schema.jsonify(companies)


class CompanyAPI(Resource):
    pass


class ZipcodeAPI(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('state', type=str, location='args', required=False)
        args = parser.parse_args()

        addresses = Address.query

        if args.get('state'):
            addresses = addresses.filter(Address.state == args.get('state'))

        addresses = addresses.all()

        # addresses = set(addresses)

        return zipcode_schema.jsonify(addresses)


api.add_resource(CompaniesListAPI, '/api/company', endpoint='companies')
api.add_resource(CompanyAPI, '/api/company/<int:id>', endpoint='company')

api.add_resource(ZipcodeAPI, '/api/zipcode', endpoint='zipcodes')
