import json

import test.test_utils as utils
from django.test import TestCase
from rest_framework.test import APIClient
from test.fixture import DBInitializer


class UserDetailTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/users/'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  # Get user tests
  def test_get_user(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'{self.ROUTE}{self.db.staff_user.id}')
    utils.get_detail_check(self, res)

  def test_get_user_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'{self.ROUTE}{self.db.staff_user.id}')
    utils.forbidden_check(self, res)

  def test_get_user_unauthenticated(self):
    res = self.client.get(f'{self.ROUTE}{self.db.staff_user.id}')
    utils.unauthorized_check(self, res)

  # Update user tests
  def test_update_user(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(f'{self.ROUTE}{self.db.staff_user.id}', data={
      'email': self.db.STAFF_EMAIL,
      'first_name': 'Updated',
      'last_name': 'Name',
    }, content_type='application/json')

    utils.updated_check(self, res)

    body = json.loads(res.content)
    self.assertEquals(body.get('data').get('first_name'), 'Updated')
    self.assertEquals(body.get('data').get('last_name'), 'Name')

  def test_update_user_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(f'{self.ROUTE}{self.db.staff_user.id}', data={
      'email': 'some@email.com',
      'first_name': 'Updated',
      'last_name': 'Name',
    }, content_type='application/json')

    utils.forbidden_check(self, res)

  def test_update_user_unauthenticated(self):
    res = self.client.put(f'{self.ROUTE}{self.db.staff_user.id}', data={
      'email': self.db.STAFF_EMAIL,
      'first_name': 'Updated',
      'last_name': 'Name',
    }, content_type='application/json')

    utils.unauthorized_check(self, res)

  # Delete User tests
  def test_delete_unauthenticated(self):
    res = self.client.delete(f'{self.ROUTE}{self.db.staff_user.id}')

    utils.unauthorized_check(self, res)

  def test_delete(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.delete(f'{self.ROUTE}{self.db.staff_user.id}')

    utils.deleted_check(self, res)
