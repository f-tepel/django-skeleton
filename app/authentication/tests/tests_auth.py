import json

import test.test_utils as utils
from django.test import TestCase
from rest_framework.test import APIClient
from test.fixture import DBInitializer

from user.models import User


class UserTestCase(TestCase):
  user: User
  client = APIClient()
  ROUTE: str = '/api/auth/'
  CONTENT_TYPE: str = 'application/json'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_auth(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)

    res = self.client.get(self.ROUTE, content_type=self.CONTENT_TYPE)

    body = json.loads(res.content)
    utils.get_detail_check(self, res)

    self.assertIsNotNone(body.get('data').get('id'))
    self.assertIsInstance(body.get('data').get('id'), int)

    self.assertIsNotNone(body.get('data').get('user_type'))
    self.assertEqual(body.get('data').get('user_type'), 'customer')

  def test_auth_not_logged_in(self):
    response = self.client.get(self.ROUTE, content_type=self.CONTENT_TYPE)
    self.assertEqual(response.status_code, 401)
