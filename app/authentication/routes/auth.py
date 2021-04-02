from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.response import AUTH_FAILED_RESPONSE
from api.serializer import EmptySerializer
from user.exceptions import NoSupportedGroup
from user.models import User


class Authenticate(generics.CreateAPIView):
  """
  An endpoint to log in a user.
  """
  permission_classes = [IsAuthenticated]
  queryset = User.objects.all()
  serializer_class = EmptySerializer

  def get(self, request):
    """
    An endpoint to log in a user.
    """
    try:
      user_type = request.user.get_user_type()

      return Response(data={
        'status': 200,
        'message': 'User authenticated',
        'data': {
          'id': request.user.id,
          'user_type': user_type,
        }
      }, status=200)
    except NoSupportedGroup:
      return Response(data=AUTH_FAILED_RESPONSE, status=401)
