from django.urls import path
from . import views


urlpatterns = [
    path('packages/', views.PackageList.as_view()),
    path('packages/<slug:slug>/', views.PackageDetails.as_view(), name='details'),
]