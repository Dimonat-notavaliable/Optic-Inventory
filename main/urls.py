from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('facilities/', views.facilities, name="facilities"),
    path('focls/', views.focls, name="focls"),
    path('hardware/', views.hardware, name="hardware"),
    path('users/', views.users, name="users")
]
