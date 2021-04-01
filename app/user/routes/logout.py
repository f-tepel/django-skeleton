from django.contrib.auth import logout
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from user.models import User
from api.authentication import CsrfExemptSessionAuthentication
from api.serializer import EmptySerializer


class LogoutUser(generics.GenericAPIView,
                 mixins.ListModelMixin):
  """
  An endpoint to log in a user.
  """
  permission_classes = []
  authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
  queryset = User.objects.all()
  serializer_class = EmptySerializer

  def get(self, request, *args, **kwargs):
    logout(request)

    return Response(data={
      'status': 200,
      'detail': 'User logged out successfully'
    })
