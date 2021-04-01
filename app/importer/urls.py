from django.urls import path

from importer.systems.MyANIWIN.owner import OwnerList

urlpatterns = [
    path('myaniwin/owners', OwnerList.as_view()),
]
