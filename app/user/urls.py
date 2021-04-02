from django.urls import path

from user.routes.change_email import UpdateEmail
from user.routes.change_password import UpdatePassword
from .routes.users.detail import UserDetail
from .routes.users.list import UserList

urlpatterns = [
  path('', UserList.as_view()),
  path('<int:pk>', UserDetail.as_view()),
  path('email', UpdateEmail.as_view()),
  path('password', UpdatePassword.as_view()),
]
