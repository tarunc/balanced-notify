from app import app, db
from app.crossdomain import crossdomain
from flask import request
from datetime import datetime
from bson import json_util
from bson.objectid import ObjectId
import simplejson as json

Notification = db['notifications']
User = db['users']

def createNotification(user_id, message):
    return {
        'message': message,
        'created_at': datetime.utcnow(),
        'uid': str(user_id)
    }

def deleteNotification(user_id, notification_id):
    Notification.update({ '_id': notification_id, 'uid': user_id }, { '$set': { 'read': True } }, upsert=False, multi=False)

def getUsers():
    return User.find(fields=['email', '_id'])

@app.route('/notifications', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def getNotifications():
    user = request.headers.get('x-balanced-user')
    email = request.headers.get('x-balanced-email')
    admin = request.headers.get('x-balanced-admin')

    print email, user, admin

    if not user:
        return '', 401

    notification_cursor = Notification.find({ 'uid': user, '$or': [{ 'read': False }, { 'read': { '$exists': False } }] }, fields=['message', '_id'])
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

    if user_id:
        notification = createNotification(user_id, message)
    else:
        users = getUsers()
        notification = [createNotification(user['_id'], message) for user in users]

    notification_id = Notification.insert(notification)

    return json.dumps({ 'data': str(notification_id) if isinstance(notification_id, ObjectId) else [str(obj_id) for obj_id in notification_id] }, default=json_util.default)


@app.route('/users', methods=['GET'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def getAllUsers():
    admin = request.headers.get('x-balanced-admin')

    if not admin:
        return 'Authorization Required', 401

    return json.dumps({ 'data': [{ 'id': str(doc['_id']), 'email': doc['email'] } for doc in getUsers()] }, default=json_util.default)


@app.route('/notification/<string:notification_id>', methods=['DELETE'])
@crossdomain(origin=app.config.get('CORS_DOMAIN'))
def markNotificationsAsRead(notification_id):
    user = request.headers.get('x-balanced-user')

    if not user:
        return '', 401

    deleteNotification(user, notification_id)

    return 'ok'

