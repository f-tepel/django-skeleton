from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoModelPermissions


class DjangoModelPermissionsWithRead(DjangoModelPermissions):
  perms_map = {
    'GET': ['%(app_label)s.view_%(model_name)s'],
    'OPTIONS': [],
    'HEAD': [],
    'POST': ['%(app_label)s.add_%(model_name)s'],
    'PUT': ['%(app_label)s.change_%(model_name)s'],
    'PATCH': ['%(app_label)s.change_%(model_name)s'],
    'DELETE': ['%(app_label)s.delete_%(model_name)s'],
  }


class IsCustomer(BasePermission):

  def has_permission(self, request, view) -> bool:
    user = request.user
    if user.groups.filter(name='customer').exists():
      return True
    else:
      return False


class IsUserOrBusiness(BasePermission):
  """
  Custom permission to only allow owners of an object to see and edit it.
  Admin users however have access to all.
  """

  def has_object_permission(self, request, view, obj):
    if request.user.is_business():
      return True

    return obj.id == request.user.id


class Group:
  BUSINESS = 'business_owner'
  STAFF = 'staff'
  CUSTOMER = 'customer'
