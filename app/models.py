from app import app, db
from datetime import datetime

NotificationModel = db['notifications']
UserModel = db['users']

class Notification(object):
    @staticmethod
    def createModel(user_id, message):
        return {
            'message': message,
            'created_at': datetime.utcnow(),
            'uid': str(user_id)
        }

    @staticmethod
    def deleteNotification(user_id, notification_id):
        print NotificationModel.update({ '_id': notification_id, 'uid': user_id }, { '$set': { 'read': True } }, upsert=False, multi=False)
        print [doc for doc in NotificationModel.find({ 'uid': user_id })]

    @staticmethod
    def getForUser(user):
        return NotificationModel.find({ 'uid': user, '$or': [{ 'read': False }, { 'read': { '$exists': False } }] }, fields=['message', '_id'])

    @staticmethod
    def createNotifications(message, user_id):
        if user_id:
            notification = Notification.createModel(user_id, message)
        else:
            users = User.getUsers()
            notification = [Notification.createModel(user['_id'], message) for user in users]

        return NotificationModel.insert(notification)

class User(object):
    @staticmethod
    def getUsers():
        return UserModel.find(fields=['email', '_id'])
