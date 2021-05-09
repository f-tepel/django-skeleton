from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from django_email_verification import send_email

from api.authentication import CsrfExemptSessionAuthentication
from user.models import User
from ..serializers.register_serializer import RegisterSerializer


class Register(generics.CreateAPIView):
  permission_classes = []
  authentication_classes = [CsrfExemptSessionAuthentication]
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  schema = AutoSchema(operation_id_base='RegisterUser')

  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    password = request.data.get('password')
    print('creating account for')
    print(email)
    print(password)

    try:
      user = User.objects.create_user(email=email, password=password)
      user.is_active = False
      password = User.objects.make_random_password()
      user.set_password(password)
      user.set_customer_group()
      send_email(user)

      data = {
        'status': 201,
        'message': 'User created',
        'data': {
          'id': user.id,
          'user_type': 'customer',
        },
      }

      return Response(data=data, status=201)
    except IntegrityError:
      return Response(data={
        'status': 400,
        'detail': 'User with this email already exists',
        'data': {},
      }, status=400)
