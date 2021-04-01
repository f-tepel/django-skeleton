from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import mixins
from rest_framework import generics

from patient.models import PatientSerializer, Patient
from api.response import transform_drf_response


class PatientList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Patient.objects.all()
  serializer_class = PatientSerializer
  permission_classes = [IsAuthenticated, DjangoModelPermissions]

  def get_queryset(self, *args, **kwargs):
    return Patient.objects.all().filter(owner=self.request.user)

  def get(self, request, *args, **kwargs):
    return transform_drf_response(self.list(request, *args, **kwargs))

  def post(self, request, *args, **kwargs):
    return transform_drf_response(self.create(request, *args, **kwargs))
