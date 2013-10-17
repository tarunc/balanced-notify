from app import app, db
from app.crossdomain import crossdomain
from app.models import Notification, User
from flask import request
from bson import json_util
from bson.objectid import ObjectId
import simplejson as json

@app.route('/notifications', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def getNotifications():
    user = request.headers.get('x-balanced-user')
    email = request.headers.get('x-balanced-email')
    admin = request.headers.get('x-balanced-admin')

    if not user:
        return '', 401

    notification_cursor = Notification.getForUser(user)
    return json.dumps({ 'data': [{ 'message': doc['message'], 'id': str(doc['_id']) } for doc in notification_cursor] }, default=json_util.default)


@app.route('/notification', methods=['POST'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def createNotifications():
    admin = request.headers.get('x-balanced-admin')

    if not admin:
        return 'Authorization Required', 401

    if not request.form['message']:
        return 'Message required', 400

    message = str(request.form['message'])
    user_id = request.form.get('uid')

    notification_id = Notification.createNotifications(message, user_id)

    return json.dumps({ 'data': str(notification_id) if isinstance(notification_id, ObjectId) else [str(obj_id) for obj_id in notification_id] }, default=json_util.default)


@app.route('/notification/<string:notification_id>', methods=['DELETE'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def markNotificationsAsRead(notification_id):
    user = request.headers.get('x-balanced-user')

    if not user:
        return '', 401

    Notification.deleteNotification(user, notification_id)

    return 'ok'


@app.route('/users', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def getAllUsers():
    admin = request.headers.get('x-balanced-admin')

    if not admin:
        return 'Authorization Required', 401

    return json.dumps({ 'data': [{ 'id': str(doc['_id']), 'email': doc['email'] } for doc in User.getUsers()] }, default=json_util.default)

