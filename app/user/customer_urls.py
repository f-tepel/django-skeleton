from django.urls import path
from .routes.customers.list import CustomerList
from .routes.customers.detail import CustomerDetail

urlpatterns = [
    path('', CustomerList.as_view()),
    path('<int:pk>', CustomerDetail.as_view()),
]