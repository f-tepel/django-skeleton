import json

from django.http import HttpResponse
from django.test import TestCase


def get_detail_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  instance.assertEqual(res.status_code, 200)
  instance.assertEqual(body.get('status'), 200)
  format_success_response_check(instance, res)


def get_list_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  instance.assertEqual(res.status_code, 200)
  instance.assertEqual(body.get('status'), 200)
  instance.assertIsInstance(body.get('data'), dict)
  instance.assertIsInstance(body.get('data').get('results'), list)
  format_success_response_check(instance, res)


def import_format_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  format_success_response_check(instance, res)
  data = body.get('data')
  instance.assertIsInstance(data.get('created'), int)
  instance.assertIsInstance(data.get('updated'), int)
  instance.assertIsInstance(data.get('errors'), list)


def created_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  format_success_response_check(instance, res)
  instance.assertEqual(res.status_code, 201)
  instance.assertEqual(body.get('status'), 201)


def updated_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  format_success_response_check(instance, res)
  instance.assertEqual(res.status_code, 200)
  instance.assertEqual(body.get('status'), 200)


def deleted_check(instance: TestCase, res: HttpResponse):
  instance.assertEqual(res.status_code, 204)


def not_found_check(instance: TestCase, res: HttpResponse):
  format_failed_response_check(instance, res)
  instance.assertEqual(res.status_code, 404)


def unauthorized_check(instance: TestCase, res: HttpResponse):
  format_failed_response_check(instance, res)
  instance.assertEqual(res.status_code, 401)


def forbidden_check(instance: TestCase, res: HttpResponse):
  format_failed_response_check(instance, res)
  instance.assertEqual(res.status_code, 403)


def format_failed_response_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)
  failed_codes: [int] = [400, 401, 403, 404]

  instance.assertIn(res.status_code, failed_codes)
  instance.assertIsNotNone(body.get('detail'))


def format_success_response_check(instance: TestCase, res: HttpResponse):
  body = json.loads(res.content)

  instance.assertLess(res.status_code, 300)
  instance.assertLess(body.get('status'), 300)
  instance.assertIsNotNone(body.get('message'))
  instance.assertIsNotNone(body.get('data'))
  instance.assertIsInstance(body.get('data'), dict)


def compare_list_length(instance: TestCase, res: HttpResponse, expected_length: int):
  body = json.loads(res.content)
  data = body.get('data')

  instance.assertEqual(data.get('count'), expected_length)
