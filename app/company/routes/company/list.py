from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import mixins
from rest_framework import generics

from company.models import Company
from .serializer import CompanySerializer
from api.response import transform_drf_response


class CompanyList(mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  permission_classes = [IsAuthenticated, DjangoModelPermissions]

  def post(self, request, *args, **kwargs):
    return transform_drf_response(self.create(request, *args, **kwargs))
