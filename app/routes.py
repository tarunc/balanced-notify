from app import app
from app.crossdomain import crossdomain
from app.models import Notification, User
import auth
from flask import request
from bson import json_util
from bson.objectid import ObjectId
import simplejson as json

@app.route('/notifications', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.user()
def getNotifications():
    user = request.headers.get('x-balanced-user')
    notification_cursor = Notification.getForUser(user)
    return json.dumps({ 'data': [{ 'message': doc['message'], 'id': str(doc['_id']) } for doc in notification_cursor] }, default=json_util.default)


@app.route('/notification', methods=['POST'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.admin()
def createNotifications():
    if not request.form['message']:
        return 'Message required', 400

    message = str(request.form['message'])
    user_id = request.form.get('uid')

    notification_id = Notification.createNotifications(message, user_id)

    return json.dumps({ 'data': str(notification_id) if isinstance(notification_id, ObjectId) else [str(obj_id) for obj_id in notification_id] }, default=json_util.default)


@app.route('/notification/<string:notification_id>', methods=['DELETE'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.user()
def markNotificationAsRead(notification_id):
    user = request.headers.get('x-balanced-user')
    Notification.deleteNotification(user, notification_id)
    return 'ok'


@app.route('/users', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
@auth.admin()
def getAllUsers():
    return json.dumps({ 'data': [{ 'id': str(doc['_id']), 'email': doc['email'] } for doc in User.getUsers()] }, default=json_util.default)

