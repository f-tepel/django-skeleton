from rest_framework import serializers

from user.models import User


class UserListSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name']
    read_only_fields = ['id', 'email']

  def create(self, validated_data):
    user = User.objects.create(**validated_data)
    password = User.objects.make_random_password()
    user.set_password(password)

    if 'customer' in self.context['request'].path:
      user.set_customer_group()
    else:
      user.set_staff_group()

    user.save()
    user.send_initial_password_email(password)

    return user
