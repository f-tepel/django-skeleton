from typing import NoReturn

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission, ContentType

from user.models import User


class DBInitializer:
  customer_user: User
  customer_user_2: User
  staff_user: User
  business_user: User
  import_user: User
  customer_user_b: User
  staff_user_b: User
  business_user_b: User
  import_user_b: User
  customer_group: Group
  staff_group: Group
  business_group: Group
  import_group: Group
  CUSTOMER_EMAIL: str = 'customer@test.com'
  CUSTOMER_EMAIL_2: str = 'customer2@test.com'
  CUSTOMER_EMAIL_B: str = 'customer@testb.com'
  STAFF_EMAIL: str = 'staff@test.com'
  STAFF_EMAIL_B: str = 'staff@testb.com'
  BUSINESS_EMAIL: str = 'business@test.com'
  BUSINESS_EMAIL_B: str = 'business@testb.com'
  IMPORT_EMAIL: str = 'import@test.com'
  PASSWORD: str = 'Start1234'

  def __init__(self):
    self._create_groups()
    # assign user permissions to objects
    self._add_permissions_on_user()

    self._create_customers()
    self._create_staff_members()
    self._create_business_owners()
    self._create_import_user()

  def _create_groups(self) -> NoReturn:
    self.customer_group = Group.objects.create(name='customer')
    self.staff_group = Group.objects.create(name='staff')
    self.business_group = Group.objects.create(name='business_owner')
    self.import_group = Group.objects.create(name='import')

  def _create_customers(self):
    self.customer_user = User.objects.create_user(self.CUSTOMER_EMAIL, password=self.PASSWORD)
    self.customer_user.groups.add(self.customer_group)
    self.customer_user.save()

    self.customer_user_2 = User.objects.create_user(self.CUSTOMER_EMAIL_2, password=self.PASSWORD)
    self.customer_user_2.groups.add(self.customer_group)
    self.customer_user_2.save()

    self.customer_user_b = User.objects.create_user(self.CUSTOMER_EMAIL_B, password=self.PASSWORD)
    self.customer_user_b.groups.add(self.customer_group)
    self.customer_user_b.save()

  def _create_staff_members(self):
    self.staff_user = User.objects.create_user(self.STAFF_EMAIL, password=self.PASSWORD)
    self.staff_user.groups.add(self.staff_group)
    self.staff_user.save()

    self.staff_user_b = User.objects.create_user(self.STAFF_EMAIL_B, password=self.PASSWORD)
    self.staff_user_b.groups.add(self.staff_group)
    self.staff_user_b.save()

  def _create_business_owners(self):
    self.business_user = User.objects.create_user(self.BUSINESS_EMAIL, password=self.PASSWORD)
    self.business_user.groups.add(self.business_group)
    self.business_user.save()

    self.business_user_b = User.objects.create_user(self.BUSINESS_EMAIL_B, password=self.PASSWORD)
    self.business_user_b.groups.add(self.business_group)
    self.business_user_b.save()

  def _create_import_user(self):
    self.import_user = User.objects.create_user(self.IMPORT_EMAIL, password=self.PASSWORD)
    self.import_user.groups.add(self.import_group)
    self.import_user.save()

  def _add_permissions_on_user(self):
    content_type = ContentType.objects.get_for_model(User)
    perms = Permission.objects.filter(content_type=content_type)
    for p in perms:
      self.staff_group.permissions.add(p)
      self.business_group.permissions.add(p)

      if 'delete' not in p.name:
        self.import_group.permissions.add(p)
