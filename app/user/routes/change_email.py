from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import ChangeEmailSerializer


class UpdateEmail(APIView):
  """
  An endpoint for changing email.
  """
  permission_classes = [IsAuthenticated]

  def get_object(self, queryset=None):
    return self.request.user

  def put(self, request, *args, **kwargs):
    self.object = self.get_object()
    serializer = ChangeEmailSerializer(data=request.data)

    if serializer.is_valid():
      self.object.email = serializer.data.get('email')
      self.object.save()

      return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
