from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .routes.users.detail import UserDetail
from .routes.users.list import UserList
import user.routes as routes
from user.routes.change_email import UpdateEmail
from user.routes.change_password import UpdatePassword
from user.routes.login import LoginUser
from user.routes.auth import AuthenticateUser
from user.routes.logout import LogoutUser

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:pk>', UserDetail.as_view()),
    path('register', routes.register_route),
    path('login', csrf_exempt(LoginUser.as_view())),
    path('logout', LogoutUser.as_view()),
    path('auth', AuthenticateUser.as_view()),
    path('email', UpdateEmail.as_view()),
    path('password', UpdatePassword.as_view()),
]