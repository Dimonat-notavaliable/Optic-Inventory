from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ["email"]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return self.readonly_fields

    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "last_name", "first_name", "patronymic")},
        ),
        ("Права доступа", {"fields": ("is_active", "is_superuser", "is_writer")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = ("email", "last_name", "first_name")
    list_filter = (
        "is_active",
        "is_writer",
        "is_superuser",
    )
    search_fields = ("email",)
    ordering = ("id",)
    filter_horizontal = ()
