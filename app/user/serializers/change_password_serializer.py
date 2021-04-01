from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
  """
  Serializer for password change endpoint.
  """
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)

  @staticmethod
  def validate_new_password(value):
    validate_password(value)
    return value
