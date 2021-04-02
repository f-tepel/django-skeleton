from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
  path('api/', get_schema_view(
    title="My project API",
    description="API to for your super project.",
    version="0.1.0"
  ), name='openapi-schema'),
  path('api/admin/', admin.site.urls),
  path('api/users/', include('user.urls')),
  path('api/auth/', include('authentication.urls')),
]
