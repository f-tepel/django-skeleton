from rest_framework import serializers

from address.models import AddressSerializer

from user.models import User


class UserListSerializer(serializers.HyperlinkedModelSerializer):
  address = AddressSerializer(required=False, allow_null=True, many=True)
  company = serializers.SlugRelatedField(read_only=True, slug_field='id')

  class Meta:
    model = User
    fields = ['id', 'source_id', 'email', 'first_name', 'last_name', 'address', 'company']
    read_only_fields = ['id', 'email', 'company']

  def create(self, validated_data):
    req_user: User = self.context['request'].user
    user = User.objects.create(**validated_data)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.company = req_user.company

    if 'customer' in self.context['request'].path:
      user.set_customer_group()
    else:
      user.set_staff_group()

    user.save()
    user.send_initial_password_email(password)

    return user
