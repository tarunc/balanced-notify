#!notify/bin/python
import os
import unittest

from config import basedir
from app import app, db

TEST_NOTIFICATION = dict(
    message='Hey there, checkout this cool new feature on the Balanced dashboard',
    email='app@balancedpayments.com'
)


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_1_create_notification(self):
        res = self.app.post('/notification', data=TEST_NOTIFICATION)
        assert TEST_NOTIFICATION.get('message') in res.data

    def test_2_get_notifications(self):
        self.test_1_create_notification()
        res = self.app.get(
            '/notifications?email=' +
            TEST_NOTIFICATION.get(
                'email'))
        assert TEST_NOTIFICATION.get('message') in res.data

    def test_3_delete_notifications(self):
        self.test_1_create_notification()
        res = self.app.delete('/notification/1')
        assert 'ok' in res.data

    def test_4_get_no_notifications(self):
        res = self.app.get(
            '/notifications?email=' +
            TEST_NOTIFICATION.get(
                'email'))
        assert '[]' in res.data


if __name__ == '__main__':
    unittest.main()
