from wayblazer.extensions import ma

from marshmallow import fields


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