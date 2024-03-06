from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('facilities/', views.facilities, name="facilities"),
    path('facilities/map/', views.facilities_map, name="facilities_map"),
    path('facilities/new/', views.facility_create, name="facility_create"),
    path('facilities/<int:pk>/', views.facility, name="facility"),
    path('facilities/map/<int:pk>/', views.facility_map, name="facility_map"),
    path('facilities/delete/<int:pk>/', login_required(views.FacilityDelete.as_view()), name="facility_delete"),
    path('focls/', views.focls, name="focls"),
    path('hardware/', views.hardware, name="hardware"),
    path('users/', views.users, name="users"),
]
