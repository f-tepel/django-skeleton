from django.db import models
from rest_framework import serializers


class Address(models.Model):
  street = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  postal_code = models.CharField(max_length=50)
  country = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.street} - {self.city}"


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ['street', 'city', 'postal_code', 'country']

