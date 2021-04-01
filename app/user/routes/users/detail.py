from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsUserOrBusiness, Group
from api.response import transform_drf_response
from user.models import User
from user.serializers import UserDetailSerializer


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
  """
  Retrieve, update or delete a User instance.
  """
  queryset = User.objects.filter(groups__name__in=[Group.STAFF, Group.BUSINESS])
  serializer_class = UserDetailSerializer
  permission_classes = [IsAuthenticated, IsUserOrBusiness]

  def get_queryset(self, *args, **kwargs):
    return User.objects.filter(company=self.request.user.company).filter(groups__name__in=[Group.BUSINESS, Group.STAFF])

  def get(self, request, *args, **kwargs):
    return transform_drf_response(self.retrieve(request, *args, **kwargs))

  def put(self, request, *args, **kwargs):
    return transform_drf_response(self.update(request, *args, **kwargs))

  def delete(self, request, *args, **kwargs):
    return transform_drf_response(self.destroy(request, *args, **kwargs))
