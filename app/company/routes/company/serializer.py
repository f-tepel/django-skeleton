from loguru import logger

from rest_framework import serializers

from company.models import Company, Whitelabel
from address.models import Address, AddressSerializer


class WhitelabelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Whitelabel
    fields = ['name', 'primary_color', 'logo_url']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
  address = AddressSerializer()
  whitelabel = WhitelabelSerializer()

  class Meta:
    model = Company
    fields = ['id', 'name', 'address', 'whitelabel']
    read_only_fields = ['id']

  def create(self, validated_data) -> Company:
    address_data = validated_data.pop('address')
    whitelabel_data = validated_data.pop('whitelabel')

    address = Address(**address_data)
    address.save()
    logger.debug(f'Saved address {address.id}')

    whitelabel = Whitelabel(**whitelabel_data)
    whitelabel.save()
    logger.debug(f'Saved whitelabel {whitelabel.id}')

    company = Company(name=validated_data['name'], address=address, whitelabel=whitelabel)
    company.save()
    logger.debug(f'Saved company {company.id}')

    return company

  def update(self, company: Company, validated_data: dict) -> Company:
    address_data = validated_data.pop('address')
    whitelabel_data = validated_data.pop('whitelabel')

    Address.objects.filter(pk=company.address.pk).update(**address_data)
    logger.debug(f'Updated address {company.address.id}')

    Whitelabel.objects.filter(pk=company.whitelabel.pk).update(**whitelabel_data)
    logger.debug(f'Updated whitelabel {company.whitelabel.id}')

    company.name = validated_data['name']
    company.save()
    logger.debug(f'Updated company {company.id}')

    return company
