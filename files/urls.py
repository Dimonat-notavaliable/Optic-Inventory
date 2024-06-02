from django.urls import path

from . import views

urlpatterns = [
    path('export/<str:extension>/hardware', views.export_hardware, name="export_hardware"),
    path('export/<str:extension>/hardware/<int:pk>', views.export_one_hardware, name="export_one_hardware"),

    path('export/<str:extension>/facilities', views.export_facilities, name="export_facilities"),
    path('export/<str:extension>/facilities/<int:pk>', views.export_facility, name="export_facility"),

    path('export/<str:extension>/muffs', views.export_muffs, name="export_muffs"),
    path('export/<str:extension>/muffs/<int:pk>', views.export_muff, name="export_muff"),

    path('export/<str:extension>/focls', views.export_focls, name="export_focls"),
    path('export/<str:extension>/focls/<int:pk>', views.export_focl, name="export_focl"),

    path('export/<str:extension>/crosses', views.export_crosses, name="export_crosses"),
    path('export/<str:extension>/crosses/<int:pk>', views.export_cross, name="export_cross"),

    path('import/hardware/', views.import_hardware, name="import_hardware"),
]
