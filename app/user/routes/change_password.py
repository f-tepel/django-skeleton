from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import ChangePasswordSerializer


class UpdatePassword(APIView):
  """
  An endpoint for changing password.
  """
  permission_classes = [IsAuthenticated]

  def get_object(self, queryset=None):
    return self.request.user

  def put(self, request, *args, **kwargs):
    self.object = self.get_object()
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
      old_password = serializer.data.get("old_password")
      if not self.object.check_password(old_password):
        return Response({"old_password": ["Wrong password."]},
                        status=status.HTTP_400_BAD_REQUEST)

      self.object.set_password(serializer.data.get("new_password"))
      self.object.save()

      return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
