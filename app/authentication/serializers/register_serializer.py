from rest_framework import serializers
from django_email_verification import send_email

from user.models import User


class RegisterSerializer(serializers.Serializer):
  """
  Serializer for login user endpoint.
  """

  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True, )

  class Meta:
    model = User
    fields = ['email', 'password']

  def create(self, validated_data):
    user = User.objects.create(**validated_data)
    user.is_active = False
    password = User.objects.make_random_password()
    user.set_password(password)

    if 'customer' in self.context['request'].path:
      user.set_customer_group()
    else:
      user.set_staff_group()

    user.save()
    send_email(user)

    return user
