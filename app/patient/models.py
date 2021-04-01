from django.db import models
from rest_framework import serializers

from user.models import User


class Gender(models.TextChoices):
  MALE = 'MALE'
  FEMALE = 'FEMALE'


class Patient(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50, blank=True, null=True)
  age = models.IntegerField(blank=True, null=True)
  gender = models.CharField(choices=Gender.choices, max_length=50)
  species = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.name} - {self.species}"


class PatientSerializer(serializers.ModelSerializer):
  owner = serializers.SlugRelatedField(read_only=True, slug_field='id')

  class Meta:
    model = Patient
    fields = ['id', 'owner', 'name', 'age', 'gender', 'species']
    read_only_fields = ['id', 'owner']

  def get_user(self) -> User:
    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      user = request.user

    return user

  def create(self, validated_data):
    return Patient.objects.create(**validated_data, owner=self.get_user())
