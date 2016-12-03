from flask.ext.restful import reqparse


def get_company_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('state', type=str,
                        location='args', required=False)
    parser.add_argument('employee_count', type=int,
                        location='args', required=False)
    parser.add_argument('limit', type=int,
                        location='args', required=False)
    parser.add_argument('offset', type=int,
                        location='args', required=False)
    return parser


def get_zipcode_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('state', type=str,
                        location='args', required=False)
    parser.add_argument('limit', type=int,
                        location='args', required=False)
    parser.add_argument('offset', type=int,
                        location='args', required=False)
    return parser
