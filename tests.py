#!notify/bin/python
import os
import unittest

from config import basedir
from app import app, db
import simplejson as json

USER_ID = 1
TEST_NOTIFICATION = dict(
    message='Hey there, checkout this cool new feature on the Balanced dashboard',
    uid=USER_ID
)


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['DATABASE_URL'] = 'mongodb://localhost/test'
        self.app = app.test_client()
        db['notifications'].remove()
        db['users'].remove()
        db['users'].insert([{ 'email': 'app@balancedpayments.com', '_id': USER_ID }, { 'email': 'tests@balancedpayments.com' }])

    def tearDown(self):
        db['notifications'].remove()
        db['users'].remove()

    def test_create_notification(self):
        TEST_NOTIFICATION['uid'] = USER_ID
        res = self.app.post('/notification', data=TEST_NOTIFICATION, headers={ 'x-balanced-admin': '1' })
        data = json.loads(res.data)
        assert data['data'] and len(data['data']) >= 1
        return data['data']

    def test_create_multi_notification(self):
        TEST_NOTIFICATION.pop('uid', None)
        res = self.app.post('/notification', data=TEST_NOTIFICATION, headers={ 'x-balanced-admin': '1' })
        data = json.loads(res.data)
        assert isinstance(data['data'], list) and len(data['data']) > 1

    def test_get_notifications(self):
        notification_id = self.test_create_notification()
        res = self.app.get('/notifications', headers={ 'x-balanced-user': USER_ID })
        assert TEST_NOTIFICATION.get('message') in res.data
        data = json.loads(res.data)
        assert notification_id == data['data'][0]['id']

    def test_delete_notifications(self):
        notification_id = self.test_create_notification()
        res = self.app.delete('/notification/' + notification_id, headers={ 'x-balanced-user': USER_ID })
        assert 'ok' in res.data

    def test_get_no_notifications(self):
        res = self.app.get(
            '/notifications', headers={ 'x-balanced-user': USER_ID })
        assert '[]' in res.data

    def test_get_users(self):
        res = self.app.get(
            '/users', headers={ 'x-balanced-admin': '1' })
        data = json.loads(res.data)
        assert isinstance(data['data'], list) and len(data['data']) > 1


if __name__ == '__main__':
    unittest.main()
