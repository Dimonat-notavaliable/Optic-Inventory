from django.urls import path

from . import views

urlpatterns = [
    path('export/<str:extension>/hardware', views.export_hardware, name="export_hardware"),
    path('export/<str:extension>/facility', views.export_facilities, name="export_facilities"),
    path('export/<str:extension>/muff', views.export_muffs, name="export_muffs"),
    path('export/<str:extension>/focl', views.export_focls, name="export_focls"),
    path('export/<str:extension>/cross', views.export_crosses, name="export_crosses"),
]
