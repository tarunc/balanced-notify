import unittest

import simplejson as json
from jsonschema import validate

import notify
from notify.models import Notification, User


TEST_NOTIFICATION = dict(
    message='Checkout this cool new feature on the Balanced dashboard',
)

CREATE_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {"type": "string"}
    },
    "required": ["data"]
}

CREATE_MULTI_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["data"]
}

GET_NO_NOTIFICATIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "maxItems": 0
        }
    },
    "required": ["data"]
}

GET_NOTIFICATIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "id": {"type": "string"}
                },
                "required": ["id", "message"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["data"]
}

GET_USERS_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "id": {"type": "string"}
                },
                "required": ["id", "email"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["data"]
}


class TestCase(unittest.TestCase):

    def setUp(self):
        app = notify.make_app()
        self.app = app.test_client()
        for fixture in [
            {'email': 'app@balancedpayments.com'},
            {'email': 'tests@balancedpayments.com'}
        ]:
            User(**fixture).save()

    def tearDown(self):
        Notification.objects.delete()
        User.objects.delete()

    def assertStatus(self, response, status_code):
        """
        Helper method to check matching response status.

        :param response: Flask response
        :param status_code: response status code (e.g. 200)
        """
        self.assertEqual(response.status_code, status_code)

    def validateResponse(self, response, json_schema):
        """
        Helper method to parse a response as json and validate it given a
        json_schema

        :param response: Flask response
        :param json_schema: a json schema
        """

        data = json.loads(response.data)
        validate(data, json_schema)

        return data

    def test_create_notification(self):
        res = self.app.post(
            '/notifications',
            data=TEST_NOTIFICATION,
            headers={'x-balanced-admin': '1'})

        data = self.validateResponse(res, CREATE_SCHEMA)
        self.assertStatus(res, 201)

        return data['data']

    def test_create_notification_unauthorized(self):
        res = self.app.post(
            '/notifications',
            data=TEST_NOTIFICATION)

        self.assertStatus(res, 401)

    def test_create_notification_not_admin_authorized(self):
        res = self.app.post(
            '/notifications',
            data=TEST_NOTIFICATION,
            headers={'x-balanced-user': USER_ID})

        self.assertStatus(res, 401)

    def test_create_multi_notification(self):
        TEST_NOTIFICATION.pop('uid', None)
        res = self.app.post(
            '/notifications',
            data=TEST_NOTIFICATION,
            headers={'x-balanced-admin': '1'})
        data = self.validateResponse(res, GET_NOTIFICATIONS_SCHEMA)
        self.assertStatus(res, 201)

        return data['data']

    def test_get_notifications(self):
        notification_id = self.test_create_notification()
        res = self.app.get(
            '/notifications',
            headers={'x-balanced-user': USER_ID})

        data = self.validateResponse(res, GET_NOTIFICATIONS_SCHEMA)
        self.assertEqual(notification_id, data['data'][0]['id'])
        self.assertEqual(
            TEST_NOTIFICATION.get('message'),
            data['data'][0]['message'])

        self.assertStatus(res, 200)

    def test_get_notifications_unauthorized(self):
        notification_id = self.test_create_notification()
        res = self.app.get(
            '/notifications')

        self.assertStatus(res, 401)

    def test_delete_notifications(self):
        notification_id = self.test_create_notification()
        res = self.app.delete(
            '/notifications/' + notification_id,
            headers={'x-balanced-user': USER_ID})

        self.assertStatus(res, 204)
        self.test_get_no_notifications()

    def test_delete_notifications_twice(self):
        notification_id = self.test_create_notification()
        for expected_status_code in (204, 403):
            resp = self.app.delete(
                '/notifications/' + notification_id,
                headers={'x-balanced-user': USER_ID})

            self.assertStatus(resp, expected_status_code)

    def test_delete_notifications_unauthorized(self):
        notification_id = self.test_create_notification()
        res = self.app.delete(
            '/notifications/' + notification_id)

        self.assertStatus(res, 401)

    def test_delete_notifications_another_user(self):
        notification_id = self.test_create_notification()
        res = self.app.delete(
            '/notifications/' + notification_id,
            headers={'x-balanced-user': '5'})

        self.assertStatus(res, 403)

    def test_delete_notifications_random_id(self):
        res = self.app.delete(
            '/notifications/1dnnn',
            headers={'x-balanced-user': '5'})

        self.assertStatus(res, 403)

    def test_get_no_notifications(self):
        res = self.app.get(
            '/notifications', headers={'x-balanced-user': USER_ID})

        self.assertIn('[]', res.data)

        self.validateResponse(res, GET_NO_NOTIFICATIONS_SCHEMA)
        self.assertStatus(res, 200)

    def test_get_users(self):
        res = self.app.get(
            '/users', headers={'x-balanced-admin': '1'})

        data = json.loads(res.data)
        self.validateResponse(res, GET_USERS_SCHEMA)

        self.assertGreaterEqual(len(data['data']), 1)
        self.assertStatus(res, 200)

    def test_get_users_unauthorized(self):
        res = self.app.get(
            '/users')

        self.assertStatus(res, 401)

    def test_get_users_not_admin_authorized(self):
        res = self.app.get(
            '/users', headers={'x-balanced-user': '1'})

        self.assertStatus(res, 401)


if __name__ == '__main__':
    unittest.main()
