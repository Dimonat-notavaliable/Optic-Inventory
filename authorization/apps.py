from django.apps import AppConfig
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authorization"


class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


class MyAdminConfig(AdminConfig):
    default_site = "authorization.apps.MyAdminSite"
