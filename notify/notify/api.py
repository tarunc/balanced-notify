from flask import request
from bson import json_util
from bson.objectid import ObjectId
import simplejson as json

from notify.notify.app.crossdomain import crossdomain
from notify.notify.app.models import Notification, User
import auth
from notify.notify import app


@app.route('/notifications', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.user()
def get_notifications():
    user = request.headers.get('x-balanced-user')
    notification_cursor = Notification.get_for_user(user)

    return (
        json.dumps({'data': [{'message': doc['message'], 'id': str(doc['_id'])}
                   for doc in notification_cursor]}, default=json_util.default)
    ), 200


@app.route('/notification', methods=['POST'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.admin()
def create_notifications():
    if not request.form['message']:
        return 'Message required', 400

    message = str(request.form['message'])
    user_id = request.form.get('uid')

    notification_id = Notification.create_notifications(message, user_id)

    return (
        json.dumps(
            {'data': str(notification_id) if isinstance(notification_id,
                                                        ObjectId) else [str(
                obj_id) for obj_id in notification_id]},
            default=json_util.default)
    ), 201


@app.route('/notification/<string:notification_id>', methods=['DELETE'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.user()
def mark_notification_as_read(notification_id):
    user = request.headers.get('x-balanced-user')
    res = Notification.delete_notification(user, notification_id)

    if res['n'] >= 1:
        return '', 204
    else:
        return 'Forbidden', 403


@app.route('/users', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.admin()
def get_all_users():
    return (
        json.dumps({'data': [{'id': str(doc['_id']), 'email': doc['email']}
                   for doc in User.get_users()]}, default=json_util.default)
    ), 200
