from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from loguru import logger

from .serializer import CompanySerializer
from api.response import transform_drf_response
from company.models import Company


class CompanyDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
  """
  Retrieve, update or delete a company instance.
  """

  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  permission_classes = [IsAuthenticated, DjangoModelPermissions]

  def get_queryset(self):
    company: Company = self.request.user.company
    try:
      return Company.objects.filter(id=company.id)
    except:
      logger.warning(f'User {self.request.user.id} has no company associated to it')
      return Company.objects.none()

  def get(self, request, *args, **kwargs):
    if request.user.company.id != kwargs.get('pk'):
      raise PermissionDenied('You do not have permission to view this information')

    return transform_drf_response(self.retrieve(request, *args, **kwargs))

  def put(self, request, *args, **kwargs):
    if request.user.company.id != kwargs.get('pk'):
      raise PermissionDenied('You do not have permission to update this information')

    return transform_drf_response(self.update(request, *args, **kwargs))
