from django.urls import path

from . import views

urlpatterns = [
    path("facility/<int:pk>/", views.facility_scheme, name="facility_scheme"),
    path(
        "facility/<int:pk>/all/",
        views.get_facility_schemes,
        name="get_facility_schemes",
    ),
    path(
        "facility/<int:pk>/save/",
        views.save_facility_scheme,
        name="save_facility_scheme",
    ),
    path("muff/<int:pk>/", views.muff_scheme, name="muff_scheme"),
    path("muff/<int:pk>/save/", views.save_muff_scheme, name="save_muff_scheme"),
    path("muff/<int:pk>/all/", views.get_muff_schemes, name="get_muff_schemes"),
]
