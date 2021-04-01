from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from ..exceptions import NoSupportedGroup
from loguru import logger

from user.models import User
from api.response import AUTH_FAILED_RESPONSE
from api.authentication import CsrfExemptSessionAuthentication
from api.serializer import EmptySerializer


class AuthenticateUser(generics.GenericAPIView,
                       mixins.ListModelMixin):
  """
  An endpoint to log in a user.
  """
  permission_classes = [IsAuthenticated]
  authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
  queryset = User.objects.all()
  serializer_class = EmptySerializer

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      logger.debug(f'Auth successful for user {request.user.id}')
      try:
        user_type = request.user.get_user_type()

        return Response(data={
          'status': 200,
          'message': 'User authenticated',
          'data': {
            'id': request.user.id,
            'user_type': user_type,
            'company': request.user.company.id
          }
        }, status=200)
      except NoSupportedGroup:
        return Response(data=AUTH_FAILED_RESPONSE, status=401)

    else:
      logger.debug("Auth failed")
      return Response(data=AUTH_FAILED_RESPONSE, status=401)
