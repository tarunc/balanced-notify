from app import app, db
from bson.objectid import ObjectId
from datetime import datetime

NotificationModel = db['notifications']
UserModel = db['users']


class Notification(object):

    @staticmethod
    def create(user_id, message):
        return {
            'message': message,
            'created_at': datetime.utcnow(),
            'uid': str(user_id)
        }

    @staticmethod
    def delete_notification(user_id, notification_id):
        if not isinstance(notification_id, ObjectId):
            try:
                notification_id = ObjectId(notification_id)
            except:
                return dict(n=0)

        return (
            NotificationModel.update(
                {'_id': notification_id,
                 'uid': user_id},
                {'$set': {'read': True}},
                upsert=False,
                multi=False)
        )

    @staticmethod
    def get_for_user(user):
        return (
            NotificationModel.find(
                {'uid': user,
                 '$or': [{'read': False},
                         {'read': {'$exists': False}}]},
                fields=['message',
                        '_id'])
        )

    @staticmethod
    def create_notifications(message, user_id):
        if user_id:
            notification = Notification.create(user_id, message)
        else:
            users = User.get_users()
            notification = [Notification.create(
                user['_id'], message) for user in users]

        return NotificationModel.insert(notification)


class User(object):

    @staticmethod
    def get_users():
        return UserModel.find(fields=['email', '_id'])
