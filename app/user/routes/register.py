from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

import api.response as default_reponse


@csrf_exempt
def register_route(request: HttpRequest, *args, **kwargs):
  return default_reponse.METHOD_NOT_IMPLEMENTED_RESPONSE