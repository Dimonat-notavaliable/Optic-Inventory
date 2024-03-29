from django.urls import path
from .decorators import writer_only
from . import views

urlpatterns = [
    path('', views.index, name="home"),

    path('centers/', views.communication_centers, name="centers"),

    path('facilities/', views.facilities, name="facilities"),
    path('facilities/map/', views.facilities_map, name="facilities_map"),
    path('facilities/new/', views.facility_create, name="facility_create"),
    path('facilities/<int:pk>/', views.facility, name="facility"),
    path('facilities/map/<int:pk>/', views.facility_map, name="facility_map"),
    path('facilities/delete/<int:pk>/', writer_only(views.FacilityDelete.as_view()), name="facility_delete"),

    path('muffs/', views.muffs, name="muffs"),
    path('muffs/map', views.muffs_map, name="muffs_map"),
    path('muffs/new/', views.muff_create, name="muff_create"),

    path('focls/', views.focls, name="focls"),
    path('focls/new/', views.focl_create, name="focl_create"),
    path('ajax/load-centers/', views.load_centers, name='ajax_load_centers'),

    path('crosses/', views.crosses, name="crosses"),
    path('crosses/new/', views.cross_create, name="cross_create"),

    path('hardware/', views.many_hardware, name="many_hardware"),
    path('hardware/new/', views.hardware_create, name="hardware_create"),
    path('hardware/<int:pk>/', views.hardware, name="hardware"),
    path('hardware/delete/<int:pk>/', writer_only(views.HardwareDelete.as_view()), name="hardware_delete"),
    path('users/', views.users, name="users"),

]
