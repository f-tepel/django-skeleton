from django.contrib.auth import logout
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from api.serializer import EmptySerializer
from user.models import User


class Logout(generics.CreateAPIView):
  """
  An endpoint to log in a user.
  """
  permission_classes = [IsAuthenticated]
  queryset = User.objects.all()
  serializer_class = EmptySerializer
  schema = AutoSchema(operation_id_base='LogoutUser')

  def get(self, request):
    logout(request)

    return Response(data={
      'status': 200,
      'detail': 'User logged out successfully'
    })
