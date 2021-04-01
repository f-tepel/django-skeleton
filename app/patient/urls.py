from django.urls import path
from .routes import PatientList, PatientDetail

urlpatterns = [
    path('', PatientList.as_view()),
    path('<int:pk>', PatientDetail.as_view()),
]