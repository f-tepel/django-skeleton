from django.db import models
import address.models as AddressModels
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Whitelabel(models.Model):
  name = models.CharField(max_length=50)
  logo_url = models.CharField(max_length=100)
  primary_color = models.CharField(max_length=10)

  def __str__(self) -> str:
    return self.name


class Company(models.Model):
  name = models.CharField(max_length=50)
  address = models.OneToOneField(AddressModels.Address, on_delete=models.CASCADE)
  whitelabel = models.OneToOneField(Whitelabel, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self) -> str:
    return self.name


@receiver(post_delete, sender=Company)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.address:
      instance.address.delete()

    if instance.whitelabel:
      instance.whitelabel.delete()

