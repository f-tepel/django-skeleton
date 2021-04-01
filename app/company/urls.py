from django.urls import path
from .routes.company.detail import CompanyDetail
from .routes.company.list import CompanyList


urlpatterns = [
  path('', CompanyList.as_view()),
  path('<int:pk>', CompanyDetail.as_view()),
]
