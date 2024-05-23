from django.urls import path

from . import views
from .decorators import writer_only

urlpatterns = [
    path('', views.index, name="home"),
    path('scheme', views.scheme, name="scheme"),

    path('centers/', views.communication_centers, name="centers"),

    path('facilities/', views.facilities, name="facilities"),
    path('facilities/map/', views.facilities_map, name="facilities_map"),
    path('facilities/new/', views.facility_create, name="facility_create"),
    path('facilities/<int:pk>/', views.facility, name="facility"),
    path('facilities/map/<int:pk>/', views.facility_map, name="facility_map"),
    path('facilities/delete/<int:pk>/', writer_only(views.FacilityDelete.as_view()), name="facility_delete"),
    path('facilities/update/<int:pk>/', writer_only(views.FacilityUpdate.as_view()), name="facility_update"),

    path('muffs/', views.muffs, name="muffs"),
    path('muffs/map', views.muffs_map, name="muffs_map"),
    path('muffs/new/', views.muff_create, name="muff_create"),
    path('muffs/<int:pk>/', views.muff, name="muff"),
    path('muffs/map/<int:pk>/', views.muff_map, name="muff_map"),
    path('muffs/delete/<int:pk>/', writer_only(views.MuffDelete.as_view()), name="muff_delete"),
    path('muffs/update/<int:pk>/', writer_only(views.MuffUpdate.as_view()), name="muff_update"),


    path('focls/', views.focls, name="focls"),
    path('focls/new/', views.focl_create, name="focl_create"),
    path('focls/<int:pk>/', views.focl, name="focl"),
    path('focls/delete/<int:pk>/', writer_only(views.FOCLDelete.as_view()), name="focl_delete"),
    path('focls/update/<int:pk>/', writer_only(views.FOCLUpdate.as_view()), name="focl_update"),

    path('ajax/load-centers/', views.load_centers, name='ajax_load_centers'),



    path('crosses/', views.crosses, name="crosses"),
    path('crosses/new/', views.cross_create, name="cross_create"),
    path('crosses/<int:pk>/', views.cross, name="cross"),
    path('crosses/delete/<int:pk>/', writer_only(views.CrossDelete.as_view()), name="cross_delete"),
    path('crosses/update/<int:pk>/', writer_only(views.CrossUpdate.as_view()), name="cross_update"),

    path('hardware/', views.many_hardware, name="many_hardware"),
    path('hardware/new/', views.hardware_create, name="hardware_create"),
    path('hardware/<int:pk>/', views.hardware, name="hardware"),
    path('hardware/delete/<int:pk>/', writer_only(views.HardwareDelete.as_view()), name="hardware_delete"),
    path('hardware/update/<int:pk>/', writer_only(views.HardwareUpdate.as_view()), name="hardware_update"),
    path('hardware/<int:hardware_id>/commutate/<int:port_id>', views.commutate_port, name="commutate_port"),
    path('ajax/load-port-commutations/<int:hardware_id>', views.load_port_commutations,
         name='ajax_load_port_commutations'),

    path('users/', views.users, name="users"),
    path('ajax/load-notifications/', views.load_notifications, name='ajax_load_notifications'),
    path('notifications/read/<int:pk>/', views.read_notification, name='read_notification'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name="notification_delete"),

]
