from flask.ext.restful import reqparse


def get_employees_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('company', type=str,
                        location='args', required=False)
    parser.add_argument('duplicate_number', type=str,
                        location='args', required=False)
    parser.add_argument('email_provider', type=str,
                        location='args', required=False)
    parser.add_argument('exclude_state', type=str,
                        location='args', required=False)
    parser.add_argument('limit', type=int,
                        location='args', required=False)
    parser.add_argument('offset', type=int,
                        location='args', required=False)
    return parser
