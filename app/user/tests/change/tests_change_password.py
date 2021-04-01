import json

from django.test import TestCase
from rest_framework.test import APIClient

from test.fixture import DBInitializer
import test.test_utils as utils


class ChangePasswordTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/users/password'
  NEW_PASSWORD: str = 'NEW_PASSWORD_1234'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_change_password(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data={
      'old_password': self.db.PASSWORD,
      'new_password': self.NEW_PASSWORD
    }, content_type='application/json')

    self.assertEqual(res.status_code, 204)

    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.NEW_PASSWORD)
    res = self.client.get('/api/users/auth')
    utils.get_detail_check(self, res)

  def test_old_password_does_not_work(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data={
      'old_password': self.db.PASSWORD,
      'new_password': self.NEW_PASSWORD
    }, content_type='application/json')
    self.assertEqual(res.status_code, 204)

    self.client.logout()
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get('/api/users/auth')
    utils.unauthorized_check(self, res)

  def test_change_password_unauthenticated(self):
    res = self.client.put(self.ROUTE, data={
      'old_password': self.db.PASSWORD,
      'new_password': self.NEW_PASSWORD
    }, content_type='application/json')

    self.assertEqual(res.status_code, 401)

    # Check that new password does not work
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.NEW_PASSWORD)
    res = self.client.get('/api/users/auth')
    utils.unauthorized_check(self, res)

    # Check if password remained the same
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get('/api/users/auth')
    utils.format_success_response_check(self, res)







