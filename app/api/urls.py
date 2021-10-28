from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
  path('api/admin/', admin.site.urls),
  path('api/users/', include('user.urls')),
  path('api/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
