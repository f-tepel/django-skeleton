from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from api.response import transform_drf_response
from patient.models import PatientSerializer, Patient


class PatientDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  queryset = Patient.objects.all()
  serializer_class = PatientSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self, *args, **kwargs):
    return Patient.objects.all().filter(owner=self.request.user)

  def get(self, request, *args, **kwargs):
    return transform_drf_response(self.retrieve(request, *args, **kwargs))

  def put(self, request, *args, **kwargs):
    return transform_drf_response(self.update(request, *args, **kwargs))

  def delete(self, request, *args, **kwargs):
    return transform_drf_response(self.destroy(request, *args, **kwargs))
