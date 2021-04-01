from django.test import TestCase
from rest_framework.test import APIClient

import test.test_utils as utils
from test.fixture import DBInitializer
from user.models import User


class UserTestCase(TestCase):
  user: User
  client: APIClient

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_register(self):
    res = self.client.post('/api/users/register', data={
      'email': self.db.CUSTOMER_EMAIL,
      'password': self.db.PASSWORD
    }, content_type='application/json')

    utils.not_found_check(self, res)
