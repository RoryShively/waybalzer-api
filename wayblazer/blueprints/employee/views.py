from flask import Blueprint
from flask_restful import Resource
from sqlalchemy.sql import func

from lib.util_pagination import paginated_results

from wayblazer.extensions import api

from wayblazer.blueprints.company.models import Company, Address
from wayblazer.blueprints.employee.models import Employee, PersonalPhone
from wayblazer.blueprints.employee.parsers import (
    get_employees_list_parser, get_duplicate_number_list_parser,
)
from wayblazer.blueprints.employee.schemas import employees_schema, phone_schema

employee = Blueprint('employee', __name__, template_folder='templates')


class EmployeesListAPI(Resource):
    def get(self):

        parser = get_employees_list_parser()
        args = parser.parse_args()

        limit = args.get('limit') if args.get('limit') else 10
        offset = args.get('offset') if args.get('offset') else 0

        employees = Employee.query.join(Company).join(Address)

        """ Refine query based on parameters passed in url. """
        # Filter based on employees company
        if args.get('company'):
            employees = employees.filter(Company.name == args.get('company'))

        # Filter based on which state to exclude in the query
        if args.get('exclude_state'):
            employees = employees\
                .filter(Address.state != args.get('exclude_state'))

        # Filter based on email provider
        # (i.e. `?email_provider=gmail` for all gmail accounts)
        if args.get('email_provider'):
            employees = employees\
                .filter(Employee.email
                        .like('%{}.com'.format(args.get('email_provider'))))

        # Paginate query based on offset and limit
        employees_query = employees.limit(limit).offset(offset)

        # Get the number of entrees in query before pagination
        # to get a running total
        employees_count = employees.count()

        # Dump results into the employees schema
        results = employees_schema.dump(employees_query)

        return paginated_results(self,
                                 results=results.data,
                                 args=args,
                                 limit=limit,  # Returns None
                                 offset=offset,  # Returns None
                                 count=employees_count)


class EmployeeAPI(Resource):
    pass


class DuplicateNumberAPI(Resource):
    def get(self):

        parser = get_duplicate_number_list_parser()
        args = parser.parse_args()

        limit = args.get('limit') if args.get('limit') else 10
        offset = args.get('offset') if args.get('offset') else 0

        phones = PersonalPhone.query \
            .outerjoin(PersonalPhone.employees) \
            .group_by(PersonalPhone) \
            .having(func.count_(PersonalPhone.employees) > 1)

        phones_query = phones.limit(limit).offset(offset)

        phones_count = phones.count()

        results = phone_schema.dump(phones_query)

        return paginated_results(self,
                                 results=results.data,
                                 args=args,
                                 limit=limit,  # Returns None
                                 offset=offset,  # Returns None
                                 count=phones_count)


api.add_resource(EmployeesListAPI, '/api/employee', endpoint='employees')
api.add_resource(EmployeeAPI, '/api/employee/<int:id>', endpoint='employee')

api.add_resource(DuplicateNumberAPI, '/api/duplicate_numbers', endpoint='duplicate')
