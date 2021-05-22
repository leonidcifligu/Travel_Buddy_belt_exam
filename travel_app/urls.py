from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('travels', views.travels),
    path('travels/add', views.addTravel),
    path('travels/create', views.createTravel),
    path('travels/<int:id>/join', views.join),
    path('travels/destination/<int:id>', views.destination),
]