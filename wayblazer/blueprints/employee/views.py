from collections import OrderedDict

from flask import Blueprint
from flask_restful import Resource, reqparse
from sqlalchemy.sql import func

from lib.util_pagination import build_next_url, build_previous_url

from wayblazer.extensions import api, ma

from wayblazer.blueprints.company.models import Company, Address
from wayblazer.blueprints.employee.models import Employee, PersonalPhone
from wayblazer.blueprints.employee.schemas import (
    employee_schema, employees_schema, )

employee = Blueprint('employee', __name__, template_folder='templates')


# Who works for Rapid Trading Intl?
#   localhost:8000/api/employee?company=Rapid%20Trading%20Intl
#
# Do any employees have the same personal phone number? 504-845-1427
#   localhost:8000/api/employee?duplicate_number=true
#
# Bonus: Find all employees with a personal Gmail email address but exclude anyone from CA.
#   localhost:8000/api/employee?email_provider=gmail&exclude_state=CA
#


class EmployeesListAPI(Resource):
    def get(self):

        # TODO: limit url links to positive #'s
        # TODO: fix duplicate phone number problem

        parser = reqparse.RequestParser()
        parser.add_argument('company', type=str, location='args', required=False)
        parser.add_argument('duplicate_number', type=str, location='args', required=False)
        parser.add_argument('email_provider', type=str, location='args', required=False)
        parser.add_argument('exclude_state', type=str, location='args', required=False)
        parser.add_argument('limit', type=int, location='args', required=False)
        parser.add_argument('offset', type=int, location='args', required=False)
        args = parser.parse_args()

        employees = Employee.query.join(Company).join(Address)

        """ Refine query based on parameters passed in url. """
        # Filter based on employees company
        if args.get('company'):
            employees = employees.filter(Company.name == args.get('company'))

        # Filter based on which state to exclude in the query
        if args.get('exclude_state'):
            employees = employees.filter(Address.state != args.get('exclude_state'))

        # Filter based on email provider (i.e. `?email_provider=gmail` for all gmail accounts)
        if args.get('email_provider'):
            employees = employees.filter(Employee.email.like('%{}.com'.format(args.get('email_provider'))))

        # Paginate query based on offset and limit
        employees_query = employees.limit(args.get('limit', 10)) \
            .offset(args.get('offset', 0))

        # Get the number of entrees in query before pagination to get a running total
        employees_count = employees.count()

        # Dump results into the employees schema
        results = employees_schema.dump(employees_query)

        # if args.get('duplicate_number') == 'true':
        #     employees = [employee for employee in employees if len(employee.phone.employees) > 1]

        return OrderedDict({
            "previous": build_previous_url(self, args=args,
                                           limit=args.get('limit', 10),
                                           offset=args.get('offset', 0)),
            "next": build_next_url(self, args=args,
                                   limit=args.get('limit', 10),
                                   offset=args.get('offset', 0),
                                   count=employees_count),
            "pages": employees_count // args.get('limit', 10),
            "count": employees_count,
            "results": results.data
        })


class EmployeeAPI(Resource):
    pass


api.add_resource(EmployeesListAPI, '/api/employee', endpoint='employees')
api.add_resource(EmployeeAPI, '/api/employee/<int:id>', endpoint='employee')
