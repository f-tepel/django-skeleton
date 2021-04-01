import json

from django.test import TestCase
from rest_framework.test import APIClient

import test.test_utils as utils
from test.fixture import DBInitializer


class PatientListTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/patients/'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_get_all(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)
    
    utils.get_list_check(self, res)

  def test_get_all_unauthenticated(self):
    res = self.client.get(self.ROUTE)
    
    utils.unauthorized_check(self, res)

  def test_add(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data={
      'name': 'Catinho',
      'age': 12,
      'gender': 'FEMALE',
      'species': 'Husky'
    }, content_type='application/json')

    utils.created_check(self, res)

    body = json.loads(res.content)
    user_id = body.get('data').get('id')

    res = self.client.get(f'{self.ROUTE}{user_id}')
    body = json.loads(res.content)
    self.assertEqual(body.get('data').get('name'), 'Catinho')

    utils.get_detail_check(self, res)

  def test_add_unauthenticated(self):
    res = self.client.post(self.ROUTE, data={
      'name': 'Catinho',
      'age': 12,
      'gender': 'FEMALE',
      'species': 'Husky'
    }, content_type='application/json')

    utils.unauthorized_check(self, res)
