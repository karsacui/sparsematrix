from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('output/', views.get_digits, name='get_digits'),
    path('', views.get_digits, name='get_digits'),
]