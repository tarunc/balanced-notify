from flask import request
from functools import update_wrapper


def user():
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            user = request.headers.get('x-balanced-user')

            if not user:
                return '', 401

            return f(*args, **kwargs)

        return update_wrapper(wrapped_function, f)

    return decorator


def admin():
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            admin = request.headers.get('x-balanced-admin')

            if not admin:
                return 'Authorization Required', 401

            return f(*args, **kwargs)

        return update_wrapper(wrapped_function, f)

    return decorator
