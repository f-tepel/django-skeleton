from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User


class ChangeEmailSerializer(serializers.Serializer):
  """
  Serializer for email change endpoint.
  """
  email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
