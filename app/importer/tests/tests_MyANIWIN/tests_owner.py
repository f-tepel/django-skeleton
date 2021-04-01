import json
import copy
from django.test import TestCase
from rest_framework.test import APIClient

import test.test_utils as utils
from test.fixture import DBInitializer


class ImportOwnerTestCase(TestCase):
  db: DBInitializer
  client: APIClient
  ROUTE: str = '/api/import/myaniwin/owners'
  JSON: dict = [
    {
      "KNR": "5029",
      "KGR": "Kleintierhalter",
      "ANR": "Frau",
      "TITEL": None,
      "NAME": "Musterfrau",
      "VNAME": "Siglinde",
      "ZUSATZ": None,
      "STR": "Straße 28",
      "NAT": None,
      "PLZ": "60320",
      "ORT": "Frankfurt",
      "TEL": "999999",
      "FAKL": 1,
      "FAKM": 1,
      "KUST": True,
      "MAHN": True,
      "ZTEXT": None,
      "IMPFERINN": True,
      "NEW": None,
      "FAX": None,
      "INSTITUT": None,
      "KONTO": None,
      "BLZ": None,
      "EINZUG": None,
      "PREIS": False,
      "TVN": None,
      "VKNR": None,
      "ENTFERNUNG": None,
      "EKP": False,
      "RBW": None,
      "BANR": "Sehr geehrte Frau Musterfrau,",
      "HANDY": None,
      "EMAIL": "test@email.de",
      "VORWAHL": "0123456",
      "VOLLNAME": "Musterfrau Siglinde",
      "FAKS": 1,
      "KREDIT": 0.0,
      "MID": None,
      "FREIFELD1": None,
      "FREIFELD2": None,
      "FREIFELD3": None,
      "FREIFELD4": None,
      "FREIFELD5": None,
      "PREISGRP": None,
      "LPREISGRP": None,
      "KOLLEGEN_I": 0,
      "GEWERBE": None,
      "GEBDAT": "1999-01-01",
      "SKONTO": 0.0,
      "SKONTOZEIT": 0.0,
      "ABZUG": None,
      "HOMEPAGE": None,
      "BETRIEBNR": None,
      "BFSCHECK": None,
      "BFSDATUM": None,
      "BFSBETRAG": None,
      "IBAN": None,
      "BIC": None,
      "DATSEPAM": None,
      "LETZEINZ": None,
      "MANDAT": 105029.0,
      "DATSEPAM2": None,
      "LETZEINZ2": None,
      "MANDAT2": 205029.0,
      "HIT_NUTZAR": None,
      "QSMELDEN": True,
      "HITMELDEN": True,
      "DEBITOR": None,
      "AGESMELD": None,
      "AGESTART": None,
      "AGESNUTZAR": None,
      "COLOREM": 0,
      "MAILZUSTIM": 2,
      "DSGVO": True,
      "DSGVODAT": "2018-07-02",
      "DAT_AN_KOL": True,
      "DAT_AN_LAB": True,
      "DAT_AN_NF": True,
      "KONTAKT": True
    }
  ]

  @classmethod
  def setUpTestData(cls):
    cls.db = DBInitializer()
    cls.client = APIClient()

  def tests_unauthorized(self):
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')
    
    utils.unauthorized_check(self, res)

  def tests_add_new_user(self):
    self.client.login(username=self.db.IMPORT_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')

    utils.import_format_check(self, res)

    # Check if new customer was actually added from POST request
    res = self.client.get('/api/customers/')
    utils.get_list_check(self, res)

    body = json.loads(res.content)
    user_created = False
    for customer in body.get('data').get('results'):
      if customer['email'] == self.JSON[0]['EMAIL']:
        user_created = True

    self.assertEqual(user_created, True)

  def test_update_user(self):
    self.client.login(username=self.db.IMPORT_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')
    utils.import_format_check(self, res)

    # update the just added user
    json_input = copy.deepcopy(self.JSON)
    json_input[0]['NAME'] = 'NewName'
    json_input[0]['EMAIL'] = 'some_other_import_email@test.com'
    res = self.client.post(self.ROUTE, data=json_input, content_type='application/json')
    utils.import_format_check(self, res)

    # Check if customer was actually updated from POST request and tests change email behaviour
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.get(f'/api/customers/')
    utils.get_list_check(self, res)

    body = json.loads(res.content)
    user_updated = False
    for customer in body.get('data').get('results'):
      if customer['last_name'] == json_input[0]['NAME'] \
        and customer['email'] == json_input[0]['EMAIL'] \
        and customer['source_id'] == json_input[0]['KNR']:

        user_updated = True

    self.assertEqual(user_updated, True)

  def tests_add_missing_field(self):
    self.client.login(username=self.db.IMPORT_EMAIL, password=self.db.PASSWORD)
    
    json_input = copy.deepcopy(self.JSON)
    del json_input[0]['KNR']
    res = self.client.post(self.ROUTE, data=json_input, content_type='application/json')

    utils.format_failed_response_check(self, res)

  def tests_add_as_business(self):
    self.client.login(username=self.db.BUSINESS_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')

    utils.format_failed_response_check(self, res)

  def tests_add_as_staff(self):
    self.client.login(username=self.db.STAFF_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')

    utils.format_failed_response_check(self, res)

  def tests_add_as_customer(self):
    self.client.login(username=self.db.CUSTOMER_EMAIL, password=self.db.PASSWORD)
    res = self.client.post(self.ROUTE, data=self.JSON, content_type='application/json')

    utils.format_failed_response_check(self, res)

