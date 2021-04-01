from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
  """
  Serializer for login user endpoint.
  """

  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True,)

  class Meta:
    model = User
    fields = ['email', 'password']
