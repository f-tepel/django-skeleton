from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from user.models import User
from ..serializers.register_serializer import RegisterSerializer


class Register(generics.CreateAPIView):
  permission_classes = []
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  schema = AutoSchema(operation_id_base='RegisterUser')

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
      user = User.objects.create_user(email=email, password=password)
      user_type = user.get_user_type()
      data = {
        'status': 201,
        'message': 'User created',
        'data': {
          'id': user.id,
          'user_type': user_type,
        },
      }

      return Response(data=data, status=201)
    except IntegrityError:
      return Response(data={
        'status': 400,
        'detail': 'User with this email already exists',
        'data': {},
      }, status=400)
