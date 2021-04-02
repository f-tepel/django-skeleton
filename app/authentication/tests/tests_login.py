import json

import test.test_utils as utils
from django.test import TestCase
from rest_framework.test import APIClient
from test.fixture import DBInitializer

from user.models import User


class UserTestCase(TestCase):
  user: User
  client: APIClient
  ROUTE: str = '/api/auth/login'
  CONTENT_TYPE: str = 'application/json'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_login_customer(self):
    res = self.client.post(self.ROUTE, data={
      'email': self.db.CUSTOMER_EMAIL,
      'password': self.db.PASSWORD
    }, content_type=self.CONTENT_TYPE)

    body = json.loads(res.content)
    utils.get_detail_check(self, res)

    self.assertIsNotNone(body.get('data').get('id'))
    self.assertIsInstance(body.get('data').get('id'), int)

    self.assertIsNotNone(body.get('data').get('user_type'))
    self.assertEqual(body.get('data').get('user_type'), 'customer')

  def test_login_staff(self):
    res = self.client.post(self.ROUTE, data={
      'email': self.db.STAFF_EMAIL,
      'password': self.db.PASSWORD
    }, content_type=self.CONTENT_TYPE)

    body = json.loads(res.content)
    utils.get_detail_check(self, res)

    self.assertIsNotNone(body.get('data').get('id'))
    self.assertIsInstance(body.get('data').get('id'), int)

    self.assertIsNotNone(body.get('data').get('user_type'))
    self.assertEqual(body.get('data').get('user_type'), 'business')

  def test_login_business(self):
    res = self.client.post(self.ROUTE, data={
      'email': self.db.BUSINESS_EMAIL,
      'password': self.db.PASSWORD
    }, content_type=self.CONTENT_TYPE)

    body = json.loads(res.content)
    utils.get_detail_check(self, res)

    self.assertIsNotNone(body.get('data').get('id'))
    self.assertIsInstance(body.get('data').get('id'), int)

    self.assertIsNotNone(body.get('data').get('user_type'))
    self.assertEqual(body.get('data').get('user_type'), 'business')

  def test_not_implemented_routes(self):
    res = self.client.get(self.ROUTE)
    self.assertEquals(res.status_code, 405)

    res = self.client.put(self.ROUTE)
    self.assertEquals(res.status_code, 405)

    res = self.client.delete(self.ROUTE)
    self.assertEquals(res.status_code, 405)
