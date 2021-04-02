from rest_framework import serializers

from user.models import User


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'updated_at', 'created_at']
    read_only_fields = ['id', 'email']
