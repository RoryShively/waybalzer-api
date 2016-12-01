from flask import Blueprint
from flask_restful import Resource, reqparse
from sqlalchemy.sql import func

from wayblazer.extensions import api

from wayblazer.blueprints.company.models import Company, Address
from wayblazer.blueprints.company.schemas import (
    company_schema, companies_schema, zipcode_schema, )


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


class CompaniesListAPI(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('state', type=str, location='args', required=False)
        parser.add_argument('employee_count', type=int, location='args', required=False)
        args = parser.parse_args()

        companies = Company.query.join(Address)

        if args.get('state'):
            companies = companies.filter(Address.state == args.get('state'))

        if args.get('employee_count'):
            companies = companies.outerjoin(Company.employees) \
                .group_by(Company) \
                .having(func.count_(Company.employees) == 3)

        companies = companies.all()

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

        return zipcode_schema.jsonify(addresses)


api.add_resource(CompaniesListAPI, '/api/company', endpoint='companies')
api.add_resource(CompanyAPI, '/api/company/<int:id>', endpoint='company')

api.add_resource(ZipcodeAPI, '/api/zipcode', endpoint='zipcodes')
