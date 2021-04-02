from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from api.authentication import CsrfExemptSessionAuthentication
from api.response import AUTH_FAILED_RESPONSE
from user.models import User
from ..serializers.login_serializer import LoginSerializer


class Login(generics.CreateAPIView):
  """
  An endpoint to login a user.
  """
  permission_classes = []
  authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
  serializer_class = LoginSerializer
  queryset = User.objects.all()
  schema = AutoSchema(operation_id_base='LoginUser', tags=['Auth'])

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)

    if user is not None:
      try:
        login(request, user)
        user_type = user.get_user_type()
        data = {
          'status': 200,
          'message': 'User authenticated',
          'data': {
            'id': user.id,
            'user_type': user_type,
          },
        }
        return Response(data=data, status=200)
      except Exception as e:
        return Response(data=AUTH_FAILED_RESPONSE, status=401)

    return Response(data=AUTH_FAILED_RESPONSE, status=401)
