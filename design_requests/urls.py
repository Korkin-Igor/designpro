from django.urls import path
from design_requests import views

urlpatterns = [
    path('', views.index, name='index'),
]