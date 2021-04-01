from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import generics

from api.permissions import DjangoModelPermissionsWithRead
from api.permissions import Group
from api.response import transform_drf_response
from user.models import User
from user.serializers import UserListSerializer


class UserList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin,
               LimitOffsetPagination):
  """
  Get all users that belong to a company or add a new user.
  """
  queryset = User.objects.all()
  serializer_class = UserListSerializer
  permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

  def get_queryset(self, *args, **kwargs):
    return User.objects.filter(company=self.request.user.company).filter(groups__name__in=[Group.BUSINESS, Group.STAFF])

  def get(self, request, *args, **kwargs):
    return transform_drf_response(self.list(request, *args, **kwargs))

  def post(self, request, *args, **kwargs):
    return transform_drf_response(self.create(request, *args, **kwargs))
