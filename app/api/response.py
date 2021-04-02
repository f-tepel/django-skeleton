from django.http import JsonResponse, HttpResponse


def transform_drf_response(res: HttpResponse, message: str = 'Success'):
  return JsonResponse({
    'status': res.status_code,
    'message': message,
    'data': dict(res.data) if res.data else {}
  },
    status=res.status_code
  )


def get_response(message: str = 'Success', status: int = 200, data: dict = {}) -> JsonResponse:
  return JsonResponse({
    'status': status,
    'message': message,
    'data': data
  },
    status=status
  )


SUCCESS_RESPONSE: JsonResponse = JsonResponse({
  'status': 200,
  'message': 'Success',
},
  status=200
)

DELETED_RESPONSE: JsonResponse = JsonResponse(data={
  'status': 204,
  'message': 'Success'
}, status=204)

INVALID_DATA_REPONSE: JsonResponse = JsonResponse({
  'status': 400,
  'message': 'Data is not valid',
},
  status=400
)


def SOMETHING_FAILED_REPONSE(error) -> JsonResponse:
  return JsonResponse({
    'status': 400,
    'detail': f'Something went wrong: {error}',
  },
    status=400
  )


AUTH_FAILED_RESPONSE = {
  'status': 401,
  'detail': 'Authentication failed',
}

FORBIDDEN_RESPONSE: JsonResponse = JsonResponse({
  'status': 403,
  'message': 'Forbidden. User is not allowed to perform this action',
},
  status=403
)

NOT_FOUND_RESPONSE: JsonResponse = JsonResponse({
  'status': 404,
  'message': 'Requested resource not found',
},
  status=404
)

METHOD_NOT_IMPLEMENTED_RESPONSE: JsonResponse = JsonResponse({
  'status': 404,
  'message': 'Requested method is not supported',
  'detail': 'Requested method is not supported',
},
  status=404
)

RESOURCE_EXISTS_RESPONSE: JsonResponse = JsonResponse({
  'status': 409,
  'message': 'Resource already exists',
},
  status=409
)
