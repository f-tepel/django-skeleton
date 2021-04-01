from typing import List, Union

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsImportUser
from api.response import get_response, SOMETHING_FAILED_REPONSE
from company.models import Company
from user.models import User


class OwnerList(APIView):
  permission_classes = [IsAuthenticated, IsImportUser]

  def post(self, request) -> Union[Response, JsonResponse]:
    serializer = OwnerSerializer(data=request.data, many=True)
    if serializer.is_valid():
      users = self.transform_data_to_users(serializer.validated_data, request.user.company)
      errors, created_count, updated_count = self.save_users(users, request.user.company)

      return get_response(data={'created': created_count, 'updated': updated_count, 'errors': errors})
    else:
      return SOMETHING_FAILED_REPONSE(error=serializer.errors)

  def save_users(self, users: List[dict], company: Company) -> (List[str], int, int):
    errors = []
    created_count = 0
    updated_count = 0

    for user_data in users:
      try:
        user, created = User.objects.get_or_create(
          company=company,
          source_id=user_data['source_id'],
          defaults=user_data
        )

        if created:
          user.set_customer_group()
          user.save()
          created_count += 1
        else:
          User.objects.filter(pk=user.pk).update(**user_data)
          updated_count += 1
      except IntegrityError:
        errors.append(f"{user_data['email']} already exists")

    return errors, created_count, updated_count

  def transform_data_to_users(self, data: List[dict], company: Company) -> List[dict]:
    users = []
    for owner in data:
      user = self.owner_to_user(owner)
      user['company'] = company
      users.append(user)

    return users

  def owner_to_user(self, owner: dict) -> dict:
    return {
      'email': owner['EMAIL'],
      'source_id': owner['KNR'],
      'title': owner['TITEL'],
      'form_of_address': owner['ANR'],
      'first_name': owner['VNAME'],
      'last_name': owner['NAME'],
      'name_affix': owner['ZUSATZ'],
      'phone': self.get_phone_number(owner),
      'cellphone': owner['HANDY'],
      'fax': owner['FAX'],
      'birthday': owner['GEBDAT'],
      'agreed_DSGVO': owner['DSGVO'],
      'agreed_DSGVO_date': owner['DSGVODAT'],
      'transfer_data_colleague': owner['DAT_AN_KOL'],
      'transfer_data_lab': owner['DAT_AN_LAB'],
      'transfer_data_successor': owner['DAT_AN_NF'],
      'use_contact_details': owner['KONTAKT']
    }

  def get_phone_number(self, owner: dict) -> str:
    return owner['VORWAHL'] + owner['TEL']


class OwnerSerializer(serializers.Serializer):
  KNR = serializers.CharField()
  ANR = serializers.CharField()
  TITEL = serializers.CharField(allow_null=True)
  NAME = serializers.CharField()
  VNAME = serializers.CharField()
  ZUSATZ = serializers.CharField(allow_null=True)
  STR = serializers.CharField()
  PLZ = serializers.CharField()
  ORT = serializers.CharField()
  TEL = serializers.CharField(allow_null=True)
  FAX = serializers.CharField(allow_null=True)
  HANDY = serializers.CharField(allow_null=True)
  EMAIL = serializers.CharField()
  VORWAHL = serializers.CharField(allow_null=True)
  GEBDAT = serializers.DateField()
  DSGVO = serializers.BooleanField(allow_null=True)
  DSGVODAT = serializers.DateField(allow_null=True)
  DAT_AN_KOL = serializers.BooleanField(allow_null=True)
  DAT_AN_LAB = serializers.BooleanField(allow_null=True)
  DAT_AN_NF = serializers.BooleanField(allow_null=True)
  KONTAKT = serializers.BooleanField(allow_null=True)
