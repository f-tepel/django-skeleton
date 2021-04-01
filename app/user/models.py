from typing import NoReturn

from django.contrib.auth.models import Group, AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils.html import strip_tags
from loguru import logger
from phonenumber_field.modelfields import PhoneNumberField

import company.models as CompanyModel
from .exceptions import NoSupportedGroup
from .manager import UserManager
from .routes.path import UserType


class FormOfAddress(models.TextChoices):
  MALE = 'Male'
  FEMALE = 'Female'
  FAMILY = 'Family'
  COMPANY = 'Company'


class User(AbstractUser):
  username = None
  email = models.EmailField(unique=True)
  source_id = models.CharField(max_length=50, blank=True, null=True)
  company = models.ForeignKey(CompanyModel.Company, on_delete=models.SET_NULL, blank=True, null=True)
  title = models.CharField(max_length=50, blank=True, null=True)
  form_of_address = models.CharField(max_length=10, choices=FormOfAddress.choices, blank=True, null=True)
  # first_name on abstract user
  # last_name on abstract user
  name_affix = models.CharField(max_length=50, blank=True, null=True)
  phone = PhoneNumberField(blank=True, null=True)
  cellphone = PhoneNumberField(blank=True, null=True)
  fax = PhoneNumberField(blank=True, null=True)
  birthday = models.DateField(blank=True, null=True)
  agreed_DSGVO = models.BooleanField(default=False)
  agreed_DSGVO_date = models.DateField(blank=True, null=True)
  transfer_data_colleague = models.BooleanField(default=False)
  transfer_data_lab = models.BooleanField(default=False)
  transfer_data_successor = models.BooleanField(default=False)
  use_contact_details = models.BooleanField(default=False)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()

  def is_business(self) -> bool:
    return self.groups.filter(name='business_owner').exists() or self.groups.filter(name='staff').exists()

  def is_customer(self) -> bool:
    return self.groups.filter(name='customer').exists()

  def is_staff_member(self) -> bool:
    return self.groups.filter(name='staff').exists()

  def is_business_owner(self) -> bool:
    return self.groups.filter(name='business_owner').exists()

  def set_staff_group(self) -> NoReturn:
    g = Group.objects.get(name='staff')
    self.groups.add(g.id)

  def set_customer_group(self) -> NoReturn:
    g = Group.objects.get(name='customer')
    self.groups.add(g.id)

  def get_user_type(self) -> str:
    """Checks if a user is a customer or part of a business and returns the correct redirect URL.

    Args:
      user: The user that must be checked

    Returns:
      The URL where the user must be redirected to.

    Raises:
      NoSupportedGroup if the user is not part of the customer, staff or business group.
    """

    user_groups = self.groups.all()

    if Group.objects.get(name='customer') in user_groups:
      return UserType.CUSTOMER
    elif Group.objects.get(name='business_owner') in user_groups or Group.objects.get(name='staff') in user_groups:
      return UserType.BUSINESS
    elif Group.objects.get(name='import') in user_groups:
      return UserType.IMPORT
    else:
      msg = 'User cant authenticate because it has no supported group. Make sure it has group customer or business.'
      logger.warning(msg)
      raise NoSupportedGroup(msg)

  def send_initial_password_email(self, password: str) -> NoReturn:
    msg = f"""
      Herzlich Willkommen {self.first_name},
      <br><br>Sie können sich <a href="http://staging.services.ebrain-solutions.de/">hier</a> mit Ihrem Initial 
      Passwort einloggen. Bitte denken sie daran das Passwort sofort zu ändern.
      <br><br>Initial Passwort: {password}<br><br>Beste Grüße,<br>Ihr {self.company.whitelabel.name} Team!
    """

    send_mail(
      subject=f'Willkommen bei {self.company.whitelabel.name}',
      message=strip_tags(msg),
      from_email='services@ebrain-solutions.de',
      recipient_list=[self.email],
      html_message=msg,
      fail_silently=False,
    )


