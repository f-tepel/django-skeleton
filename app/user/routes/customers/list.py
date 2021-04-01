from rest_framework import mixins, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.response import transform_drf_response
from api.permissions import Group, DjangoModelPermissionsWithRead
from user.models import User
from user.serializers import UserListSerializer


class CustomerList(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   LimitOffsetPagination):
  """
  Retrieve, update or delete a customer instance.
  """
  queryset = User.objects.all()
  serializer_class = UserListSerializer
  permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

  def get_queryset(self, *args, **kwargs):
    return User.objects.filter(company=self.request.user.company).filter(groups__name=Group.CUSTOMER)

  def get(self, request, *args, **kwargs):
    return transform_drf_response(self.list(request, *args, **kwargs))

  def post(self, request, *args, **kwargs):
    return transform_drf_response(self.create(request, *args, **kwargs))
