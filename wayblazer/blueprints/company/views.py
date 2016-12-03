from flask import Blueprint
from flask_restful import Resource, reqparse
from sqlalchemy.sql import func

from lib.util_pagination import paginated_results

from wayblazer.extensions import api

from wayblazer.blueprints.company.models import Company, Address
from wayblazer.blueprints.company.parsers import (
    get_company_list_parser, get_zipcode_list_parser,
)
from wayblazer.blueprints.company.schemas import (
    companies_schema, zipcode_schema,
)


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

        parser = get_company_list_parser()
        args = parser.parse_args()

        limit = args.get('limit') if args.get('limit') else 10
        offset = args.get('offset') if args.get('offset') else 0

        companies = Company.query.join(Address)

        if args.get('state'):
            companies = companies.filter(Address.state == args.get('state'))

        if args.get('employee_count'):
            companies = companies.outerjoin(Company.employees) \
                .group_by(Company) \
                .having(func.count_(Company.employees) == 3)

        companies_query = companies.limit(limit).offset(offset)

        companies_count = companies.count()

        results = companies_schema.dump(companies_query)

        return paginated_results(self,
                                 results=results.data,
                                 args=args,
                                 limit=limit,  # Returns None
                                 offset=offset,  # Returns None
                                 count=companies_count)


class CompanyAPI(Resource):
    pass


class ZipcodeAPI(Resource):

    def get(self):

        parser = get_company_list_parser()
        args = parser.parse_args()

        limit = args.get('limit') if args.get('limit') else 10
        offset = args.get('offset') if args.get('offset') else 0

        addresses = Address.query

        if args.get('state'):
            addresses = addresses.filter(Address.state == args.get('state'))

        addresses_query = addresses.limit(limit).offset(offset)

        addresses_count = addresses.count()

        results = zipcode_schema.dump(addresses_query)

        return paginated_results(self,
                                 results=results.data,
                                 args=args,
                                 limit=limit,  # Returns None
                                 offset=offset,  # Returns None
                                 count=addresses_count)


api.add_resource(CompaniesListAPI, '/api/company', endpoint='companies')
api.add_resource(CompanyAPI, '/api/company/<int:id>', endpoint='company')

api.add_resource(ZipcodeAPI, '/api/zipcode', endpoint='zipcodes')
