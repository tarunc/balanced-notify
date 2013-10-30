from datetime import timedelta
from functools import update_wrapper

from flask import make_response, request, current_app


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = True

            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            else:
                h['Access-Control-Allow-Headers'] = 'Authorization, \
                    Content-Type'

            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator


def register_api(view, endpoint, url, app=None, pk='id', pk_type='int'):
    app = app or current_app
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func,
                     methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    if not url:
        url = '/'
    _url = '{url}<{pk_type}:{pk}>'.format(url=url, pk_type=pk_type, pk=pk)
    app.add_url_rule(_url, view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
