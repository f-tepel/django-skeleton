from django.test import TestCase
from rest_framework.test import APIClient

from test.fixture import DBInitializer
import test.test_utils as utils


class CompanyTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/company/'
  BODY: dict = {
    "name": "Test Bank",
    "address": {
      "street": "Testlebenstraße",
      "city": "FFM",
      "postal_code": "123564",
      "country": "Deutschland"
    },
    "whitelabel": {
      "name": "Tolle Praxis",
      "primary_color": "#425169",
      "logo_url": "google.com"
    }
  }
  CONTENT_TYPE: str = 'application/json'

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def test_get_company(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'{self.ROUTE}{self.db.company.id}')

    utils.get_detail_check(self, res)

  def test_get_company_unauthenticated(self):
    res = self.client.get(f'{self.ROUTE}{self.db.company.id}')

    utils.unauthorized_check(self, res)

  def test_add_company_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.forbidden_check(self, res)

  def test_add_company_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.forbidden_check(self, res)

  def test_add_company_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.created_check(self, res)

  def test_update_company_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.forbidden_check(self, res)

  def test_update_company_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(self.ROUTE, data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.forbidden_check(self, res)

  def test_update_company_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.put(f'{self.ROUTE}{self.db.company.id}', data=self.BODY, content_type=self.CONTENT_TYPE)

    utils.updated_check(self, res)
