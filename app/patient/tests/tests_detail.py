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

  def test_get_format(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'{self.ROUTE}{self.db.patient.id}')

    utils.get_detail_check(self, res)

  def test_put_format(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(f'{self.ROUTE}{self.db.patient.id}', data={
      "name": "Doggo",
      "age": 10,
      "gender": "FEMALE",
      "species": "Husky"
    }, content_type='application/json')

    utils.updated_check(self, res)

  def test_delete_format(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.delete(f'{self.ROUTE}{self.db.patient.id}')

    utils.deleted_check(self, res)
