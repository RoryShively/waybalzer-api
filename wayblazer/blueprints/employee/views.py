from collections import deque

from flask import Blueprint
from flask_restful import Resource, reqparse
from flask_sqlalchemy import Pagination
from sqlalchemy.sql import func
from marshmallow import fields

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

        parser = reqparse.RequestParser()
        parser.add_argument('company', type=str, location='args', required=False)
        parser.add_argument('duplicate_number', type=str, location='args', required=False)
        parser.add_argument('email_provider', type=str, location='args', required=False)
        parser.add_argument('exclude_state', type=str, location='args', required=False)
        args = parser.parse_args()

        employees = Employee.query.join(Company).join(Address).join(PersonalPhone)

        if args.get('company'):
            employees = employees.filter(Company.name == args.get('company'))

        if args.get('exclude_state'):
            employees = employees.filter(Address.state != args.get('exclude_state'))

        # if args.get('duplicate_number') == 'true':
        #     employees = employees.having(func.count(PersonalPhone.employees) > 1)

        if args.get('email_provider'):
            employees = employees.filter(Employee.email.like('%{}.com'.format(args.get('email_provider'))))

        employees = employees.all()

        if args.get('duplicate_number') == 'true':
            employees = [employee for employee in employees if len(employee.phone.employees) > 1]

        return employees_schema.jsonify(employees)


class EmployeeAPI(Resource):
    pass

api.add_resource(EmployeesListAPI, '/api/employee', endpoint='employees')
api.add_resource(EmployeeAPI, '/api/employee/<int:id>', endpoint='employee')


