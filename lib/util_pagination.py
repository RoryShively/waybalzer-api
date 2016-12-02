import re

from wayblazer.extensions import api


def build_previous_url(resource, args, limit, offset):
    if offset - limit < 0:
        return None

    url = api.url_for(resource, _external=True)
    limit = limit
    offset = offset - limit

    params = []
    for arg in args:
        print(arg)
        if args.get(arg) and (arg not in ['limit', 'offset']):
            value = re.sub(' ', '+', str(args.get(arg)))
            params.append('{}={}'.format(arg, value))

    params.append('limit={}'.format(limit))
    params.append('offset={}'.format(offset))

    print(params)

    params = '&'.join(params)

    return '{}?{}'.format(url, params)


def build_next_url(resource, args, limit, offset, count):
    if offset + limit > count:
        return None

    url = api.url_for(resource, _external=True)
    limit = limit
    offset = offset + limit

    params = []
    for arg in args:
        print(arg)
        if args.get(arg) and (arg not in ['limit', 'offset']):
            value = re.sub(' ', '+', str(args.get(arg)))
            params.append('{}={}'.format(arg, value))

    params.append('limit={}'.format(limit))
    params.append('offset={}'.format(offset))

    print(params)

    params = '&'.join(params)

    return '{}?{}'.format(url, params)