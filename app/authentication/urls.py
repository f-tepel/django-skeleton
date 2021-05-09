from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from django_email_verification import urls as email_urls

from authentication.routes import Login, Logout, Authenticate, Register

urlpatterns = [
  path('', Authenticate.as_view()),
  path('register', csrf_exempt(Register.as_view())),
  path('login', csrf_exempt(Login.as_view())),
  path('logout', Logout.as_view()),
  path('email', include(email_urls)),
]
