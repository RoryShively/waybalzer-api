from wayblazer.extensions import ma

from marshmallow import fields


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'route', 'city', 'state', 'zip', 'county', )


class CompanySchema(ma.Schema):
    addresses = fields.Nested(AddressSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'web', 'phone', 'addresses', )


class EmployeeSchema(ma.Schema):
    number = fields.Str(attribute='phone.number')
    company = fields.Nested(CompanySchema)

    class Meta:
        fields = ('id', 'first_name', 'last_name',
                  'email', 'number', 'company')


class PhoneSchema(ma.Schema):
    employees = fields.Nested(EmployeeSchema, many=True,
                              exclude=('number', 'company', ))

    class Meta:
        fields = ('id', 'number', 'employees', )


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

phone_schema = PhoneSchema(many=True)
