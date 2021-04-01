import json

from django.test import TestCase
from rest_framework.test import APIClient

from test.fixture import DBInitializer
import test.test_utils as utils


class ChangeEmailTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/users/email'
  NEW_EMAIL: str = 'some_other_email@testa.com'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_change_email_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data={
      'email': self.NEW_EMAIL
    }, content_type='application/json')
    
    self.assertEqual(res.status_code, 204)

    res = self.client.get(f'/api/customers/{self.db.customer_user.id}')
    utils.get_detail_check(self, res)
    body = json.loads(res.content)
    self.assertEqual(body['data']['email'], self.NEW_EMAIL)

  def test_change_email_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data={
      'email': self.NEW_EMAIL
    }, content_type='application/json')

    self.assertEqual(res.status_code, 204)

    res = self.client.get(f'/api/users/{self.db.staff_user.id}')
    utils.get_detail_check(self, res)
    body = json.loads(res.content)
    self.assertEqual(body['data']['email'], self.NEW_EMAIL)

  def test_change_email_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data={
      'email': self.NEW_EMAIL
    }, content_type='application/json')

    self.assertEqual(res.status_code, 204)

    res = self.client.get(f'/api/users/{self.db.business_user.id}')
    utils.get_detail_check(self, res)
    body = json.loads(res.content)
    self.assertEqual(body['data']['email'], self.NEW_EMAIL)

  def test_change_email_unauthenticated(self):
    res = self.client.put(self.ROUTE, data={
      'email': self.NEW_EMAIL
    }, content_type='application/json')
    utils.unauthorized_check(self, res)

    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'/api/customers/{self.db.customer_user.id}')
    utils.get_detail_check(self, res)
    body = json.loads(res.content)
    self.assertEqual(body['data']['email'], self.db.CUSTOMER_EMAIL)

