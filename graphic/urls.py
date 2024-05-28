from django.urls import path

from . import views

urlpatterns = [
    path('facility/<int:pk>/', views.facility_scheme, name="facility_scheme"),
    path('muff/<int:pk>/', views.muff_scheme, name="muff_scheme"),
]
