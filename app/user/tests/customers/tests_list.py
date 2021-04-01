from django.test import TestCase
from rest_framework.test import APIClient

import test.test_utils as utils
from test.fixture import DBInitializer


class UserTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/customers/'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  # Test get in different roles
  def test_get_all_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)
    self.assertEquals(res.status_code, 403)

  def test_get_all_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)
    utils.get_detail_check(self, res)

  def test_get_all_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)
    utils.get_detail_check(self, res)

  # Test only customers from own company get returned
  def test_get_only_company_customers_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)

    utils.compare_list_length(self, res, 2)

  def test_get_only_company_customers_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(self.ROUTE)

    utils.compare_list_length(self, res, 2)

  def test_add_customer_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data={
      'email': self.db.CUSTOMER_EMAIL,
      'first_name': 'Max',
      'last_name': 'Musterman',
    }, content_type='application/json')

    utils.forbidden_check(self, res)
    self.assertEquals(res.status_code, 403)

  def test_add_customer_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data={
      'email': 'new@user.com',
      'first_name': 'Max',
      'last_name': 'Musterman',
    }, content_type='application/json')

    utils.created_check(self, res)
    self.assertEquals(res.status_code, 201)
