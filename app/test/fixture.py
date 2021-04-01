from typing import NoReturn

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission, ContentType

from company.models import Company, Whitelabel
from address.models import Address
from user.models import User
from patient.models import Patient


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
  address: Address
  company: Company
  company_b: Company
  whitelabel: Whitelabel
  patient: Patient
  patient_b: Patient
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
    self._add_permissions_on_company()
    self._add_permissions_on_user()
    self._add_permissions_on_patient()

    self.company = self._create_company(name='CompanyA')
    self.company_b = self._create_company(name='CompanyB')

    self._create_customers()
    self._create_staff_members()
    self._create_business_owners()
    self._create_patients()
    self._create_import_user()

  def _create_groups(self) -> NoReturn:
    self.customer_group = Group.objects.create(name='customer')
    self.staff_group = Group.objects.create(name='staff')
    self.business_group = Group.objects.create(name='business_owner')
    self.import_group = Group.objects.create(name='import')

  def _create_company(self, name: str) -> Company:
    self.whitelabel = Whitelabel(name=name, logo_url='https://google.com', primary_color='#37ab56')
    self.whitelabel.save()
    self.address = Address(street='Teststreet', city='Frankfurt', postal_code='62350', country='Germany')
    self.address.save()
    company = Company(name=name, whitelabel=self.whitelabel, address=self.address)
    company.save()

    return company

  def _create_customers(self):
    self.customer_user = User.objects.create_user(self.CUSTOMER_EMAIL, password=self.PASSWORD)
    self.customer_user.groups.add(self.customer_group)
    self.customer_user.company = self.company
    self.customer_user.save()

    self.customer_user_2 = User.objects.create_user(self.CUSTOMER_EMAIL_2, password=self.PASSWORD)
    self.customer_user_2.groups.add(self.customer_group)
    self.customer_user_2.company = self.company
    self.customer_user_2.save()

    self.customer_user_b = User.objects.create_user(self.CUSTOMER_EMAIL_B, password=self.PASSWORD)
    self.customer_user_b.groups.add(self.customer_group)
    self.customer_user_b.company = self.company_b
    self.customer_user_b.save()

  def _create_staff_members(self):
    self.staff_user = User.objects.create_user(self.STAFF_EMAIL, password=self.PASSWORD)
    self.staff_user.groups.add(self.staff_group)
    self.staff_user.company = self.company
    self.staff_user.save()

    self.staff_user_b = User.objects.create_user(self.STAFF_EMAIL_B, password=self.PASSWORD)
    self.staff_user_b.groups.add(self.staff_group)
    self.staff_user_b.company = self.company_b
    self.staff_user_b.save()

  def _create_business_owners(self):
    self.business_user = User.objects.create_user(self.BUSINESS_EMAIL, password=self.PASSWORD)
    self.business_user.groups.add(self.business_group)
    self.business_user.company = self.company
    self.business_user.save()

    self.business_user_b = User.objects.create_user(self.BUSINESS_EMAIL_B, password=self.PASSWORD)
    self.business_user_b.groups.add(self.business_group)
    self.business_user_b.company = self.company_b
    self.business_user_b.save()

  def _create_import_user(self):
    self.import_user = User.objects.create_user(self.IMPORT_EMAIL, password=self.PASSWORD)
    self.import_user.groups.add(self.import_group)
    self.import_user.company = self.company
    self.import_user.save()

  def _create_patients(self):
    self.patient = Patient.objects.create(owner=self.customer_user, name='Cat', age=12, gender='FEMALE', species='Husky')
    self.patient_b = Patient.objects.create(owner=self.customer_user_b, name='Cat B', age=12, gender='FEMALE', species='Husky')

  def _add_permissions_on_company(self):
    content_type = ContentType.objects.get_for_model(Company)
    perms = Permission.objects.filter(content_type=content_type)
    for p in perms:
      self.business_group.permissions.add(p)

  def _add_permissions_on_user(self):
    content_type = ContentType.objects.get_for_model(User)
    perms = Permission.objects.filter(content_type=content_type)
    for p in perms:
      self.staff_group.permissions.add(p)
      self.business_group.permissions.add(p)

      if 'delete' not in p.name:
         self.import_group.permissions.add(p)

  def _add_permissions_on_patient(self):
    content_type = ContentType.objects.get_for_model(Patient)
    perms = Permission.objects.filter(content_type=content_type)
    for p in perms:
      self.customer_group.permissions.add(p)
      self.staff_group.permissions.add(p)
      self.business_group.permissions.add(p)




